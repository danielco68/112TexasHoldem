import math
from gameflowMechanics import *
from winnerFinder import *
from playerClass import *
from handEvaluator import *
#Includes AI Class to intiaite AI players
#Takes care of AI some moves
#Includes Poker Class to initiate a game of Poker
#These must be together as they are reliant on eachother



class Poker():
    def __init__(self, numPlayers = 2):
        self.numPlayers = numPlayers
        self.deck = Deck()
        self.deck.shuffle()
        self.call = 20
        self.players = [Player(i) for i in range(numPlayers)]
        self.playerHands = []
        self.AIList = [None] + [AI(i) for i in range(1, numPlayers)]
        self.simulatedFlopCards = []

    def shuffle(self):
        self.deck.shuffle()

    def flop(self):
        self.deck.burn(1)
        self.deck.onBoard.extend(self.deck.deal(3))

    def simulatedFlop(self):
        self.simulatedFlopCards.append(self.deck.deck[1])
        self.simulatedFlopCards.append(self.deck.deck[2])
        self.simulatedFlopCards.append(self.deck.deck[3])
        self.simulatedFlopCards.append(self.deck.deck[5])
        self.simulatedFlopCards.append(self.deck.deck[7])

    def theatreModeStart(self):
        self.AIList = [AI(i) for i in range(0, numPlayers)]



    def getOneCard(self):
        self.deck.burn(1)
        self.deck.onBoard.extend(self.deck.deal(1))
        

    def startGame(self):
        numberOfCards = 2
        self.deck.burn(1)
        for player in self.players:
            currHand = []
            for i in range(0, numberOfCards):
                currHand.append(self.deck.deal(1).pop())
            player.hand = currHand
            self.playerHands.append(currHand)

    def AIStartGame(self, aiHand, aiID):
        numberOfCards = 2
        self.deck.burn(1)
        for player in self.players:
            if self.players.index(player) == aiID:
                player.hand = aiHand
                self.playerHands.append(aiHand)
            else:
                currHand = []
                for i in range(0, numberOfCards):
                    currHand.append(self.deck.deal(1).pop())
                player.hand = currHand
                self.playerHands.append(currHand)
################################################################################

def isOnePairAI(self):
        d = dict()
        for card in self.currHand:
            currRank = card[:-1]
            d[currRank] = d.get(currRank, 0) + 1
        if list(d.values()).count(2) == 1:
            return True
        else:
            return False

def isFlushAI(self):
        wantedSuit = self.currHand[0][-1]
        for i in range(len(self.currHand)):
            currSuit = self.currHand[i][-1]
            if currSuit != wantedSuit:
                return False
        return True

################################################################################
class AI():
    def __init__(self, playerID):
        self.playerID = playerID
        self.strength = 0
        self.possibleMoves = ["fold", "call", "raise"]
        self.raised = False
        self.numRaises = 0

    def handStrength(self, hand): #Chen Hand Strength Algorithm 
        ranks = []
        for card in hand:
            rank = card[:-1]
            suit = card[-1]
            if rank == "A":
                rank = 10
            elif rank == "K":
                rank = 8
            elif rank == "Q":
                rank = 7
            elif rank == "J":
                rank = 6
            else:
                rank = int(rank)
                rank /= 2
            ranks.append(rank)
        maxRank = max(ranks)
        self.strength += maxRank
        if isOnePairAI(Hand(hand)):
            if hand[0][0].isdigit():
                if int(hand[0][0]) >= 5:
                    self.strength *= 2
                else:
                    self.strength += 5
            else:
                self.strength *= 2
        if isFlushAI(Hand(hand)):
            self.strength += 2
        diff = sorted(ranks)[1] - sorted(ranks)[0]
        if diff  == 1 or diff == 0:
            if 7 not in ranks and 8 not in ranks and 10 not in ranks:
                self.strength += 1
        if diff == 1:
            self.strength -= diff
        elif diff == 2:
            self.strength -= diff
        elif diff == 3:
            self.strength -= 4
        elif diff >= 4:
            self.strength -= 5
        if self.strength - math.floor(self.strength) < 0.5: #taken from https://stackoverflow.com/questions/33019698/how-to-properly-round-up-half-float-numbers-in-python 
            return math.floor(self.strength)
        return math.ceil(self.strength)

    def easyDiff(self, aiHand, playerList, gameFlow):
        checkMove = 60
        raiseMove = 35
        foldMove = 5
        moveList = ["check/call"] * checkMove + ["raise"] * raiseMove + ["fold"] * foldMove
        randMove = random.choice(moveList)
        gameFlow.move(randMove, self.playerID, gameFlow.game.players)

    def preFlopMove(self, aiHand, playerList, gameFlow):
        self.handStrength(aiHand)
        if self.strength >= 9:
            if gameFlow.numPlayers == 2 and self.raised or gameFlow.numPlayers == 4 and self.raised:
                gameFlow.move("check/call", self.playerID, gameFlow.game.players)
                self.raised = False
            else:
                self.raised = True
                gameFlow.move("raise", self.playerID, gameFlow.game.players)
        elif 5 <= self.strength <= 8:
            gameFlow.move("check/call", self.playerID, gameFlow.game.players)
        else:
            if gameFlow.lastPlayerMove == "check/call":
                gameFlow.move("check/call", self.playerID, gameFlow.game.players)
            else:
                gameFlow.move("fold", self.playerID, gameFlow.game.players)

    def AIMove(self, aiHand, playerList, gameFlow):
        numTrials = 1000
        wins = 0
        for trial in range(numTrials):
            trialGame = Poker(len(playerList))
            trialGame.AIStartGame(aiHand, self.playerID)
            trialGame.flop()
            trialGame.deck.burn(1)
            trialGame.deck.deal(1, True)
            trialGame.deck.burn(1)
            trialGame.deck.deal(1, True)
            result = bestInTable(trialGame.playerHands, trialGame.deck.onBoard)
            if result == "split":
                continue
            elif result[3] == self.playerID:
                wins += 1
        if wins/numTrials < 0.4:
            if gameFlow.lastPlayerMove == "check/call":
                gameFlow.move("check/call", self.playerID, gameFlow.game.players)
            else:
                gameFlow.move("fold", self.playerID, gameFlow.game.players)
        elif 0.4 < wins/numTrials < 0.6:
            gameFlow.move("check/call", self.playerID, gameFlow.game.players)
        else:
            if gameFlow.numPlayers == 2 and self.raised or gameFlow.numPlayers == 4 and self.raised:
                gameFlow.move("check/call", self.playerID, gameFlow.game.players)
                self.raised = False
            else:
                self.raised = True
                gameFlow.move("raise", self.playerID, gameFlow.game.players)
################################################################################