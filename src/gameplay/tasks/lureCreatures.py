import numpy as np
import pyautogui
from src.features.hud.creatures import getCreaturesGraph
from features.hud.typings import creatureType
from src.features.radar.types import coordinateType
from src.utils.coordinate import getDirectionBetweenCoordinates
from ..factories.makeSetNextWaypoint import makeSetNextWaypointTask
from ..factories.makeSingleWalkPress import makeSingleWalkPress
from ..factories.makeWalk import makeWalkTask
from ..typings import taskType
from ..waypoint import generateFloorWalkpoints
from .groupTaskExecutor import GroupTaskExecutor


class LureCreaturesTask(GroupTaskExecutor):
    def __init__(self, value):
        super().__init__()
        self.name = 'lureCreatures'
        self.state = 'init'
        self.value = value
        self.tasks = np.array([], dtype=taskType)
    
    def getCreaturesByInverseHudDirection(self, direction, creatures):
        inveserCreatures = []
        if direction == 'up':
            for creature in creatures:
                if creature['slot'][1] > 5:
                    inveserCreatures.append(creature)
        elif direction == 'down':
            for creature in creatures:
                if creature['slot'][1] < 5:
                    inveserCreatures.append(creature)
        elif direction == 'left':
            for creature in creatures:
                if creature['slot'][0] > 7:
                    inveserCreatures.append(creature)
        elif direction == 'right':
            for creature in creatures:
                if creature['slot'][0] < 7:
                    inveserCreatures.append(creature)
        return np.array(inveserCreatures, dtype=creatureType)

    def ping(self, context):
        # (X) gerar caminho para o lure point
        # recalcular apenas se aparecer novos monstros na tela
        nonWalkableCoordinates = context['cavebot']['holesOrStairs'].copy()
        for monster in context['monsters']:
            monsterCoordinateTuple = (monster['coordinate'][0], monster['coordinate'][1], monster['coordinate'][2])
            coordinatesToAppend = np.array([monsterCoordinateTuple], dtype=coordinateType)
            nonWalkableCoordinates = np.append(nonWalkableCoordinates, coordinatesToAppend)
        walkpoints = generateFloorWalkpoints(
            context['radar']['coordinate'], self.value, nonWalkableCoordinates=nonWalkableCoordinates)
        self.currentTaskIndex = 0
        tasks = np.array([], dtype=taskType)
        for walkpoint in walkpoints:
            walkpointTask = makeWalkTask(context, walkpoint)
            taskToAppend = np.array([walkpointTask], dtype=taskType)
            tasks = np.append(tasks, [taskToAppend])
        tasksToAppend = np.array([], dtype=taskType)
        if len(walkpoints) > 0:
            # (x) decidir intenção de caminho, se é para esquerda, ou direita. Saber sempre quem está atrás de mim
            direction = getDirectionBetweenCoordinates(context['radar']['coordinate'], walkpoints[0])
            hasHudCreatures = len(context['monsters']) > 0
            if hasHudCreatures:
                # (x) obter os monstros targetaveis
                targetableCreatures = getCreaturesGraph(context['monsters'], context['radar']['coordinate'])
                # (x) pegar monstros que estão na posição oposta do char
                inverseCreatures = self.getCreaturesByInverseHudDirection(direction, targetableCreatures)
                if len(inverseCreatures) > 0:
                    if direction == 'up':
                        creaturesY = inverseCreatures['slot'][:, 1]
                        creatureYSlots = creaturesY[creaturesY > 8]
                        if len(creatureYSlots[creatureYSlots > 8]) > 0:
                            self.currentTaskIndex = 0
                            self.tasks = np.array([], dtype=taskType)
                        else:
                            self.currentTaskIndex = 0
                            tasks = np.array([], dtype=taskType)
                            walkpointTask1 = makeWalkTask(context, walkpoints[0])
                            taskToAppend = np.array([walkpointTask1], dtype=taskType)
                            tasks = np.append(tasks, [taskToAppend])
                            self.tasks = tasks
                    elif direction == 'down':
                        creaturesY = inverseCreatures['slot'][:, 1]
                        if len(creaturesY[creaturesY < 2]) > 0:
                            self.currentTaskIndex = 0
                            self.tasks = np.array([], dtype=taskType)
                        else:
                            self.currentTaskIndex = 0
                            tasks = np.array([], dtype=taskType)
                            walkpointTask1 = makeWalkTask(context, walkpoints[0])
                            taskToAppend = np.array([walkpointTask1], dtype=taskType)
                            tasks = np.append(tasks, [taskToAppend])
                            self.tasks = tasks
                    elif direction == 'left':
                        creaturesX = inverseCreatures['slot'][:, 0]
                        if len(creaturesX[creaturesX > 12]) > 0:
                            self.currentTaskIndex = 0
                            self.tasks = np.array([], dtype=taskType)
                        else:
                            self.currentTaskIndex = 0
                            tasks = np.array([], dtype=taskType)
                            walkpointTask1 = makeWalkTask(context, walkpoints[0])
                            taskToAppend = np.array([walkpointTask1], dtype=taskType)
                            tasks = np.append(tasks, [taskToAppend])
                            self.tasks = tasks
                    elif direction == 'right':
                        creaturesX = inverseCreatures['slot'][:, 0]
                        if len(creaturesX[creaturesX < 2]) > 0:
                            self.currentTaskIndex = 0
                            self.tasks = np.array([], dtype=taskType)
                        else:
                            self.currentTaskIndex = 0
                            tasks = np.array([], dtype=taskType)
                            walkpointTask1 = makeWalkTask(context, walkpoints[0])
                            taskToAppend = np.array([walkpointTask1], dtype=taskType)
                            tasks = np.append(tasks, [taskToAppend])
                            self.tasks = tasks
                    hasKeyPressed = context['lastPressedKey'] is not None
                    if hasKeyPressed:
                        pyautogui.keyUp(context['lastPressedKey'])
                        context['lastPressedKey'] = None
                    return context
                else:
                    self.tasks = np.append(tasks, [tasksToAppend])  
            else:
                self.tasks = np.append(tasks, [tasksToAppend])     
        # CRIATURAS:
        # a distancia para o ultimo bicho é sempre 12
        # a distancia de sempre é sempre no maximo 11
        # (x) ao atingir 11, release no teclado para nao correr
        # desviar sempre que o parametro minimo nao atingiu
        # obter as criaturas targetaveis
        # eliminar as criaturas que atacam de longe
        # ignorar criaturas que fogem
        # se automaticamente levar trap, destruir task e gerar task de atacar target
        # limite minimo de criaturas parametrizado
        # espera o de mais longe
        
        # BOX:
        # calcular ponto medio quando achar box fora do lure point
        # se chegar o numero ideal de box, esperar fechar box e atacar
        # se nao tiver bicho vindo da direita, fazer box com os da esquerda
        # posso chegar em algum ponto na esquerda e ainda nao ter dado respawn, entao matar os bicho que lurou da direita
        
        # FIM:
        # como terminar o waypoint...
        return context
    
    def did(self, _):
        return False
