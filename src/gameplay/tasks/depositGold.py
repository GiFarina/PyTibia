import numpy as np
from ..typings import taskType
from ..factories.makeSay import makeSayTask
from ..factories.makeSetNextWaypoint import makeSetNextWaypointTask
from .groupTaskExecutor import GroupTaskExecutor


# TODO: check if gold was deposited successfully
class DepositGoldTask(GroupTaskExecutor):
    def __init__(self):
        super().__init__()
        self.delayBeforeStart = 1
        self.delayAfterComplete = 1
        self.name = 'depositGold'
        self.tasks = self.makeTasks()

    def makeTasks(self):
        return np.array([
            makeSayTask('hi'),
            makeSayTask('deposit all'),
            makeSayTask('yes'),
            makeSetNextWaypointTask(),
        ], dtype=taskType)
