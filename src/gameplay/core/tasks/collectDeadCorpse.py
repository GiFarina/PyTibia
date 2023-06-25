import numpy as np
from src.gameplay.typings import Context
import src.gameplay.utils as gameplayUtils
from src.repositories.gameWindow.slot import rightClickSlot
from src.repositories.gameWindow.typings import Creature
from src.utils.keyboard import keyDown, keyUp
from ...typings import Context
from .common.base import BaseTask


# TODO: check if something was looted or exactly count was looted
class CollectDeadCorpseTask(BaseTask):
    def __init__(self, creature: Creature):
        super().__init__()
        self.name = 'collectDeadCorpse'
        self.delayBeforeStart = 0.85
        self.creature = creature

    # TODO: add unit tests
    def do(self, context: Context) -> Context:
        keyDown('shift')
        rightClickSlot([6, 4], context['gameWindow']['coordinate'])
        rightClickSlot([7, 4], context['gameWindow']['coordinate'])
        rightClickSlot([8, 4], context['gameWindow']['coordinate'])
        rightClickSlot([6, 5], context['gameWindow']['coordinate'])
        rightClickSlot([7, 5], context['gameWindow']['coordinate'])
        rightClickSlot([8, 5], context['gameWindow']['coordinate'])
        rightClickSlot([6, 6], context['gameWindow']['coordinate'])
        rightClickSlot([7, 6], context['gameWindow']['coordinate'])
        rightClickSlot([8, 6], context['gameWindow']['coordinate'])
        keyUp('shift')
        return context

        # TODO: add unit tests
    def onComplete(self, context: Context) -> Context:
        creatureToLoot = context['loot']['corpsesToLoot'][0]
        indexesToDelete = []
        for index, corpseToLoot in enumerate(context['loot']['corpsesToLoot']):
            if gameplayUtils.coordinatesAreEqual(creatureToLoot['coordinate'], corpseToLoot['coordinate']):
                indexesToDelete.append(index)
        context['loot']['corpsesToLoot'] = np.delete(context['loot']['corpsesToLoot'], indexesToDelete)
        return context
