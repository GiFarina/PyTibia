from time import sleep
from src.features.hud.slot import getSlotPos
from src.features.inventory.config import itemsImagesHashes
from src.features.inventory.core import backpacksBarsImages
from src.utils.core import hashit, locate
from src.utils.mouse import mouseDrag
from .baseTask import BaseTask


class DropEachFlaskTask(BaseTask):
    def __init__(self, backpack):
        super().__init__()
        self.delayOfTimeout = 1
        self.name = 'dropEachFlask'
        self.terminable = False
        self.value = backpack
        self.slotIndex = 0

    def do(self, context):
        (item, position) = self.getSlot(context, self.slotIndex)
        if item is None:
            self.slotIndex += 1
            return context
        if item == 'empty slot':
            self.terminable = True
            return context
        slotPosX, slotPosY = getSlotPos((7, 5), context['hud']['coordinate'])
        mouseDrag(position[0], position[1], slotPosX, slotPosY)
        sleep(1)
        return context
    
    def getSlot(self, context, slotIndex):
        backpackBarPosition = locate(context['screenshot'], backpacksBarsImages[self.value], confidence=0.8)
        if backpackBarPosition is None:
            return (None, (0, 0))
        slotXIndex = slotIndex % 4
        slotYIndex = slotIndex // 4
        containerPositionX, containerPositionY = backpackBarPosition[1] + 18, backpackBarPosition[0] + 10
        y0 = containerPositionX + slotYIndex * 32 + slotYIndex * 5
        y1 = y0 + 21 
        x0 = containerPositionY + slotXIndex * 32 + slotXIndex * 5
        x1 = x0 + 32
        firstSlotImage = context['screenshot'][y0:y1, x0:x1]
        firstSlotImageHash = hashit(firstSlotImage)
        item = itemsImagesHashes.get(firstSlotImageHash, None)
        return (item, (x0 + 16, y0 + 16))
