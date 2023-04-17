import pyautogui
from src.utils.core import locate
from .baseTask import BaseTask


class ScrollToItemTask(BaseTask):
    def __init__(self, containerImage, itemImage):
        super().__init__()
        self.name = 'scrollToItem'
        self.terminable = False
        self.value = (containerImage, itemImage)
        self.itemPosition = None

    def shouldIgnore(self, context):
        itemPosition = self.getItemPosition(context['screenshot'])
        isItemVisible = itemPosition is not None
        return isItemVisible

    def do(self, context):
        containerPosition = locate(context['screenshot'], self.value[0], confidence=0.8)
        x = containerPosition[0] + 10
        y = containerPosition[1] + 15
        pyautogui.moveTo(x, y)
        pyautogui.scroll(-10)
        return context
    
    def ping(self, context):
        itemPosition = self.getItemPosition(context['screenshot'])
        isItemVisible = itemPosition is not None
        if isItemVisible:
            self.terminable = True
        return context

    def getItemPosition(self, screenshot):
        return locate(screenshot, self.value[1], confidence=0.8)
