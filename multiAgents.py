# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        # Successor game grid
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        # Successor coordinate
        newPos = successorGameState.getPacmanPosition()
        # Successor food grid
        newFood = successorGameState.getFood()
        # Successor remaining food list
        newFoodList = newFood.asList()
        # IDK
        newGhostStates = successorGameState.getGhostStates()
        # List with the number of moves that each ghost will remain scared
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #return successorGameState.getScore()
        dist = 99999
        
        if(len(newFood.asList())!=len(currentGameState.getFood().asList())):
            dist = 0
        else:
            for food in newFood.asList():
                if dist > util.manhattanDistance(food,newPos):
                    dist = util.manhattanDistance(food,newPos)
        
        for ghost in successorGameState.getGhostPositions():
            dist += 3**(2-util.manhattanDistance(ghost,newPos))
        
        return -dist
        

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        # Defineixo PACMAN amb el seu index
        PACMAN = 0;
        
        # Aquesta es la funcio que cridare quan toqui fer el max, es a dir, quan
        # li toqui al pacman.
        #       
        # Retorna una accio, si estem a depth=0 (primera crida).
        # Retorna el valor maxim dels successors altrament.
        def maxAgent(state,depth):
            
            # Si l'estat a evaluar es un estat final, retorno la puntuacio d'aquest.
            if state.isWin() or state.isLose():
                
                return state.getScore()
            
            # Guardo la llista de possibles accions a realitzar pel pacman.
            actions = state.getLegalActions(PACMAN)
            # Defineixo la puntuacio maxima com a -infinit.
            maxScore = float("-inf")
            # De moment, assumim que la millor accio es quedarse quiet.
            bestAction = Directions.STOP
            # Recorrem totes les possibles accions.
            for action in actions:
                
                # Ara hem de comprovar el valor de cada estat successor i actualitzarem
                # quan sigui major que el valor maxim actual, actualitzant tambe l'accio
                # per poderla retornar despres.
                if minAgent(state.generateSuccessor(PACMAN,action), depth, 1) > maxScore:
                    
                    maxScore = minAgent(state.generateSuccessor(PACMAN,action), depth, 1)
                    bestAction = action
                    
            # Explicat a sobre del def maxAgent().      
            if depth == 0: return bestAction
            else: return maxScore
        
        # Aquesta es la funcio que cridare quan toqui fer el min, es a dir, quan
        # li toqui a cadascun dels fantasmes.
        #       
        # Retorna el valor minim dels successors.
        def minAgent(state,depth,ghost):
            
            # Si l'estat a evaluar es un estat final, retorno la puntuacio d'aquest.
            if state.isWin() or state.isLose():
                
                return state.getScore()
            # Defineixo l'index del que sera el proper fantasma i...
            nextGhost = ghost + 1
            # ...si aquest es el mateix que el numero d'agents que tenim, voldra dir
            # que el seguent agent sera el pacman.
            if nextGhost == state.getNumAgents():
                nextGhost = PACMAN
            
            # Defineixo la llista de possibles accions a realitzar pel fantasma(actual).
            actions = state.getLegalActions(ghost)
            # Defineixo la puntuacio minima com a infinit.
            minScore = float("inf")
            # Defineixo una variable score que em servira per emmagatzemar valors per a
            # compararlos amb la puntuacio minima.
            score = minScore
            
            # Recorrem totes les possibles accions.
            for action in actions:
                
                # Si el seguent agent es pacman...
                if nextGhost == PACMAN:
                    # ...i estem a la profunditat escollida (en aquest cas sera self.depth-1
                    # ja que comencem a comptar per 0) o la profunditat escollida es 0, la 
                    # puntuacio sera la que s'evalua si el fantasma fa l'accio actual.
                    if depth == self.depth-1 or self.depth == 0:
                        score = self.evaluationFunction(state.generateSuccessor(ghost,action))
                    # Altrament, la puntuacio sera la que ens retorni el maxAgent() amb una
                    # profunditat mes.
                    else:
                        score = maxAgent(state.generateSuccessor(ghost,action),depth+1)
                # Si no, la puntuacio sera la que ens retorni el seguent minAgent().
                else:
                    score = minAgent(state.generateSuccessor(ghost,action),depth,nextGhost)
                # Actualitzem la puntuacio minima si aquesta es major que la puntuacio
                # actual.
                if score < minScore:
                    minScore = score
            return minScore
        # Retornem la crida a maxAgent(estat,0).
        # El 0 representa que estem a profunditat 0, es a dir, que es la primera iteracio de
        # la recursivitat (si es que n'hi ha).
        return maxAgent(gameState,0)
            
        
        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # Defineixo PACMAN amb el seu index
        PACMAN = 0;
        
        # Defineixo les alpha i beta inicials.
        ALPHA = float("-inf")
        BETA = float("inf")
        
        # Aquesta es la funcio que cridare quan toqui fer el max, es a dir, quan
        # li toqui al pacman.
        #       
        # Retorna una accio, si estem a depth=0 (primera crida).
        # Retorna el valor maxim dels successors altrament.
        def maxAgent(state,depth,alpha,beta):
            
            # Si l'estat a evaluar es un estat final, retorno la puntuacio d'aquest.
            if state.isWin() or state.isLose():
                
                return state.getScore()
            
            # Guardo la llista de possibles accions a realitzar pel pacman.
            actions = state.getLegalActions(PACMAN)
            # Defineixo la puntuacio maxima com a -infinit.
            maxScore = float("-inf")
            # De moment, assumim que la millor accio es quedarse quiet.
            bestAction = Directions.STOP
            # Recorrem totes les possibles accions.
            for action in actions:
                
                # Ara hem de comprovar el valor de cada estat successor i actualitzarem
                # quan sigui major que el valor maxim actual, actualitzant tambe l'accio
                # per poderla retornar despres.
                if minAgent(state.generateSuccessor(PACMAN,action), depth, 1,alpha,beta) > maxScore:
                    
                    maxScore = minAgent(state.generateSuccessor(PACMAN,action), depth, 1,alpha,beta)
                    bestAction = action
                
                # Si la puntuacio actual es major al factor beta que tenim, podem deixar d'explorar
                # estats successors.
                if maxScore > beta: break
            
                # Actualitzem el valor d'alpha.
                alpha = max(maxScore,alpha)
                    
            # Explicat a sobre del def maxAgent().      
            if depth == 0: return bestAction
            else: return maxScore
        
        # Aquesta es la funcio que cridare quan toqui fer el min, es a dir, quan
        # li toqui a cadascun dels fantasmes.
        #       
        # Retorna el valor minim dels successors.
        def minAgent(state,depth,ghost,alpha,beta):
            
            # Si l'estat a evaluar es un estat final, retorno la puntuacio d'aquest.
            if state.isWin() or state.isLose():
                
                return state.getScore()
            # Defineixo l'index del que sera el proper fantasma i...
            nextGhost = ghost + 1
            # ...si aquest es el mateix que el numero d'agents que tenim, voldra dir
            # que el seguent agent sera el pacman.
            if nextGhost == state.getNumAgents():
                nextGhost = PACMAN
            
            # Defineixo la llista de possibles accions a realitzar pel fantasma(actual).
            actions = state.getLegalActions(ghost)
            # Defineixo la puntuacio minima com a infinit.
            minScore = float("inf")
            # Defineixo una variable score que em servira per emmagatzemar valors per a
            # compararlos amb la puntuacio minima.
            score = minScore
            
            # Recorrem totes les possibles accions.
            for action in actions:
                
                # Si el seguent agent es pacman...
                if nextGhost == PACMAN:
                    # ...i estem a la profunditat escollida (en aquest cas sera self.depth-1
                    # ja que comencem a comptar per 0) o la profunditat escollida es 0, la 
                    # puntuacio sera la que s'evalua si el fantasma fa l'accio actual.
                    if depth == self.depth-1 or self.depth == 0:
                        score = self.evaluationFunction(state.generateSuccessor(ghost,action))
                    # Altrament, la puntuacio sera la que ens retorni el maxAgent() amb una
                    # profunditat mes.
                    else:
                        score = maxAgent(state.generateSuccessor(ghost,action),depth+1,alpha,beta)
                # Si no, la puntuacio sera la que ens retorni el seguent minAgent().
                else:
                    score = minAgent(state.generateSuccessor(ghost,action),depth,nextGhost,alpha,beta)
                # Actualitzem la puntuacio minima si aquesta es major que la puntuacio
                # actual.
                if score < minScore:
                    minScore = score
                    
                # Si la puntuacio actual es menor al factor alpha que tenim, podem deixar d'explorar
                # estats successors.
                if minScore < alpha: break
            
                # Actualitzem el valor de beta.
                beta = min(minScore,beta)
            return minScore
        # Retornem la crida a maxAgent(estat,0,alpha,beta).
        # El 0 representa que estem a profunditat 0, es a dir, que es la primera iteracio de
        # la recursivitat (si es que n'hi ha).
        # alpha es -infinit inicialment.
        # beta es infinit inicialment.
        return maxAgent(gameState,0,ALPHA,BETA)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        # Defineixo PACMAN amb el seu index
        PACMAN = 0;
        
        def maxAgent(state,depth):
            
            if state.isWin() or state.isLose():
                return state.getScore()
            
            actions = state.getLegalActions(PACMAN)
            
            maxValue = float("-inf")
            
            bestAction = None
            
            for action in actions:
                
                value = expAgent(state.generateSuccessor(PACMAN,action),1,depth)
                
                if value > maxValue:
                    
                    maxValue = value
                    bestAction = action
            
            if depth==0:
                return bestAction
            else:
                return maxValue
        
        def expAgent(state,ghost,depth):
            
            if state.isWin() or state.isLose():
                return state.getScore()
            
            actions = state.getLegalActions(ghost)
            
            value = 0
            prob = 1./float(len(actions))
            
            for action in actions:
                
                if ghost + 1 == state.getNumAgents(): # => PACMAN is the next to move
                    
                    if depth == self.depth-1:# or depth == 0:
                        value += self.evaluationFunction(state.generateSuccessor(ghost,action))*prob
                    
                    else:
                        value += maxAgent(state.generateSuccessor(ghost,action),depth+1)*prob
                
                else:
                    
                    value += expAgent(state.generateSuccessor(ghost,action),ghost+1,depth)*prob
            
            return value
        
        return maxAgent(gameState,0)
            
            
def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    VALOR_MENJAR = 10
    VALOR_FANTASMA_NORMAL = 10
    VALOR_FANTASMA_ESPANTAT = 100
    
    extremely_accurate_value = 0
    
    return extremely_accurate_value


# Abbreviation
better = betterEvaluationFunction

