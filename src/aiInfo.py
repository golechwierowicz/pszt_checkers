from controller import AIRandom
from controllerSimpleEvolution1 import AISimpleEvolution1
from controllerEvolution2 import AIEvolution2
from controllerEvolutionProp import AIEvolutionProp
from controllerTestingHybrid import AITestingHybrid
from minimax import MiniMax

try:
    from controllerNNetwork import AINNetwork
    NNETWORK_ENABLED = True
except:
    NNETWORK_ENABLED = False

AI_NAMES = {
    AIRandom: ('AIRandom', 'random', '0'),
    AISimpleEvolution1: ('AISimpleEvolution1', 'simple', '1', 'evolution1'),
    AIEvolution2: ('AIEvolution2', '2', 'evolution2'),
    AIEvolutionProp: ('AIEvolutionProp', '4', 'evolutionProp'),
    MiniMax: ('MiniMax', 'minmax'),
    AITestingHybrid: ('AITestingHybrid', 'hybrid'),
}
if NNETWORK_ENABLED:
    AI_NAMES[AINNetwork] = ('AINNetwork', '3', 'nnetwork')

AI_CLASSES = {name.lower(): aiClass for aiClass, names in AI_NAMES.items()
              for name in names}


def initAI(aiTypeName, inputFile=None, mustLoad=False):
    '''
    :return: Controller object
    :rtype: Object
    '''
    def initLoad(aiClass):
        ai = aiClass()
        if mustLoad:
            assert inputFile != None
        if not hasattr(aiClass, 'deserialize'):
            return ai
        if inputFile != None:
            print('from file:', inputFile, end='')
            ai.deserialize(inputFile)
        else:
            print('with initial data', end='')
        return ai

    aiTypeName = aiTypeName.lower()

    print('initAI: ', end='')
    aiClass = AI_CLASSES[aiTypeName]
    print(AI_NAMES[aiClass][0], '', end='')
    ret = initLoad(aiClass)

    print()
    return ret


def getAIName(aiObject):
    return AI_NAMES[type(aiObject)][0]
