import cv2
import mss
import numpy as np
from typing import Callable, Union
import xxhash
from src.shared.typings import BBox, GrayImage


latestScreenshot = None


# TODO: add unit tests
def cacheObjectPosition(func: Callable) -> Callable:
    lastX = None
    lastY = None
    lastW = None
    lastH = None
    lastImgHash = None
    def inner(screenshot):
        nonlocal lastX, lastY, lastW, lastH, lastImgHash
        if lastX != None and lastY != None and lastW != None and lastH != None:
            if hashit(screenshot[lastY:lastY + lastH, lastX:lastX + lastW]) == lastImgHash:
                return (lastX, lastY, lastW, lastH)
        res = func(screenshot)
        if res is None:
            return None
        lastX = res[0]
        lastY = res[1]
        lastW = res[2]
        lastH = res[3]
        lastImgHash = hashit(screenshot[lastY:lastY + lastH, lastX:lastX + lastW])
        return res
    return inner


# TODO: add unit tests
def hashit(arr: np.ndarray) -> int:
    return xxhash.xxh64(np.ascontiguousarray(arr), seed=20220605).intdigest()


# TODO: add unit tests
def hashitHex(arr: np.ndarray) -> str:
    return xxhash.xxh64(np.ascontiguousarray(arr), seed=20220605).hexdigest()


# TODO: add unit tests
def locate(compareImage: GrayImage, img: GrayImage, confidence: float=0.85) -> Union[BBox, None]:
    cv2.imwrite('compareImage.png', compareImage)
    cv2.imwrite('img.png', img)
    match = cv2.matchTemplate(compareImage, img, cv2.TM_CCOEFF_NORMED)
    res = cv2.minMaxLoc(match)
    if res[1] <= confidence:
        return None
    return res[3][0], res[3][1], len(img[0]), len(img)


# TODO: add unit tests
def locateMultiple(compareImg: GrayImage, img: GrayImage, confidence: float=0.85) -> Union[BBox, None]:
    match = cv2.matchTemplate(compareImg, img, cv2.TM_CCOEFF_NORMED)
    loc = np.where(match >= confidence)
    resultList = []
    for pt in zip(*loc[::-1]):
        resultList.append((pt[0], pt[1], len(compareImg[0]), len(compareImg)))
    return resultList


# TODO: add unit tests
def getScreenshot() -> GrayImage:
    global latestScreenshot
    img = np.array(mss.mss().grab(mss.mss().monitors[1]))
    screenshot = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)[
                        ..., np.newaxis
                    ]
    if screenshot is None:
        return latestScreenshot
    latestScreenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2GRAY)
    return latestScreenshot
