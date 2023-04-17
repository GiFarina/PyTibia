from src.features.hud.creatures import getClosestCreature, hasTargetToCreature
from .tasks.groupOfAttackClosestCreature import GroupOfAttackClosestCreatureTasks
from .tasks.groupOfFollowTargetCreature import GroupOfFollowTargetCreatureTasks


def resolveCavebotTasks(context):
    if context['cavebot']['isAttackingSomeCreature']:
        hasNoTargetCreature = context['cavebot']['targetCreature'] == None
        if hasNoTargetCreature:
            return None
        hasNoTargetToTargetCreature = hasTargetToCreature(
            context['monsters'], context['cavebot']['targetCreature'], context['radar']['coordinate']) == False
        if hasNoTargetToTargetCreature:
            context['cavebot']['closestCreature'] = getClosestCreature(context['monsters'], context['radar']['coordinate'])
            hasNoClosestCreature = context['cavebot']['closestCreature'] == None
            if hasNoClosestCreature:
                return None
            return GroupOfAttackClosestCreatureTasks(context)
        # TODO: recalculate route if something cross walkpoints
        return GroupOfFollowTargetCreatureTasks(context)
    context['cavebot']['closestCreature'] = getClosestCreature(context['monsters'], context['radar']['coordinate'])
    hasNoClosestCreature = context['cavebot']['closestCreature'] == None
    if hasNoClosestCreature:
        return None
    return GroupOfAttackClosestCreatureTasks(context)


def shouldAskForCavebotTasks(context):
    if context['way'] != 'cavebot':
        return False
    if context['currentTask'] is None:
        return True
    return (context['currentTask'].name not in ['groupOfLootCorpse', 'groupOfRefillChecker', 'groupOfSingleWalk', 'useRopeWaypoint', 'useShovelWaypoint'])

