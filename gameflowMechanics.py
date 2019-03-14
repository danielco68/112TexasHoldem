from handEvaluator import *
from playerClass import *
from winnerFinder import *
import copy
import time
################################################################################

#Takes care of all gamflow mechanics of the poker game
#Including changing players, advancing turns and rounds

class gameFlow():
    def __init__(self, numPlayers, playersList, game):
        self.roundNum = 1
        self.numPlayers = numPlayers
        self.smallBlind = 0
        self.bigBlind = self.smallBlind + 1
        self.dealer = (self.smallBlind - 1) % self.numPlayers
        self.defBet = 20
        self.minimumBet = self.defBet
        self.currentPlayer = (self.bigBlind + 1) % self.numPlayers
        self.bigBlindVal = self.minimumBet
        self.smallBlindVal = self.bigBlindVal // 2
        self.betList = [0] * self.numPlayers
        self.round = 1
        self.gameOver = False
        self.curBet = self.minimumBet
        self.tempBet = self.minimumBet
        self.onBoard = []
        self.game = game
        self.pot = 0
        self.gameStage = ["Pre-Flop"]
        self.lastRound = False
        self.gameStatus = [2] * self.numPlayers
        self.roundWinner = None
        self.winnerHand = None
        self.winnerType = None
        self.roundOver = False
        self.lastPlayerMove = None
        self.messages = []
        self.winDueToFold = [False, "has won as everyone else folded"]
        self.count = 0
        self.checkAfterRaise = False
        self.checkAfterCheck = False
        self.theatreMode = False
        self.numMoves = 0
        #0 - Folded
        #1 - Check
        #2 - Raise/Recheck

    def updateStatus(self, playerList):
        status = copy.copy(self.gameStatus)
        money = []
        for i in range(len(playerList)):
            player = playerList[i]
            if player.money > 0 and player.fold == False and status[i] != 0:
                status[i] = True
            else:
                status[i] = False
            if player.money == 0:
                money.append(player.money)
        if money == [0] * self.numPlayers:
            self.gameStatus = [1] * self.numPlayers
            status = [True] * self.numPlayers
        return status



    def move(self, move, playerID, playersList):
        if self.currentPlayer == 0 and move == "raise":
            currentAI = self.game.AIList[(self.currentPlayer + 1) % self.numPlayers]
            currentAI.raised = False
        currPlayer = playersList[self.currentPlayer]
        if move == "fold":
            self.messages.append("Player " + str(playerID) + " has FOLDED")
            currPlayer.fold = True
            currPlayer.alreadyPlayed = True
            self.gameStatus[self.currentPlayer] = 0
            self.lastPlayerMove = "fold"
        elif move == "check/call":
            if self.lastPlayerMove == "check/call":
                self.checkAfterCheck = True
            if self.lastPlayerMove == "raise":
                self.checkAfterRaise = True
            self.messages.append("Player " + str(playerID) + " has CHECKED/CALLED")
            call = max(self.betList) - self.betList[playerID]
            if call > currPlayer.money:
                call = currPlayer.money
            currPlayer.money -= call
            self.betList[playerID] += call
            currPlayer.alreadyPlayed = True
            self.lastPlayerMove = "check/call"
            self.gameStatus[self.currentPlayer] = 1
        elif move == "raise":
            if self.lastPlayerMove == "raise":
                self.tempBet *= 2
                self.checkAfterRaise = False
            self.messages.append("Player " + str(playerID) + " RAISED")
            if currPlayer.money - self.tempBet < 0:
                self.tempBet = currPlayer.money
            self.minimumBet = self.tempBet
            currPlayer.money -= self.tempBet
            self.betList[playerID] += self.tempBet
            currPlayer.alreadyPlayed = True
            self.gameStatus[self.currentPlayer] = 2
            self.lastPlayerMove = "raise"
            for state in self.gameStatus:
                if state == 1:
                    state = 2
        self.advancePlayer(self.game.players)
        self.currentPlayer %= self.numPlayers

    def advancePlayer(self, playerList):
        status = self.updateStatus(playerList)
        self.currentPlayer += 1
        if status.count(True) == 1:
            self.roundWinner = status.index(True)
            self.winnerHand = self.game.playerHands[self.roundWinner]
            self.pot += sum(self.betList)
            self.winDueToFold[0] = True
            self.roundOver = True
        if 2 not in self.gameStatus:
            self.nextTurn(playerList)
    
        if self.gameStatus.count(1) == self.numPlayers - 1 - self.gameStatus.count(0) and self.checkAfterRaise == True:
            self.checkAfterRaise = False
            self.nextTurn(playerList)
        if self.gameStatus.count(1) == self.numPlayers - self.gameStatus.count(0):
            self.nextTurn(playerList)


    def nextRound(self, playerList):
        playerList[self.roundWinner].money += sum(self.betList)
        self.smallBlind = (self.smallBlind + 1) % self.numPlayers
        self.bigBlind = (self.bigBlind + 1) % self.numPlayers
        self.dealer = (self.dealer + 1) % self.numPlayers
        self.currentPlayer = self.smallBlind
        for player in playerList:
            player.fold = False
            player.hand = []
        self.pot = 0
        self.count = 0
        self.game.deck = Deck()
        self.game.deck.onBoard = []
        self.game.playerHands = []
        self.game.simulatedFlopCards = []
        self.game.deck.shuffle()
        self.game.startGame()
        self.winnerHand = None
        self.winnerType = None
        self.roundWinner = None
        self.gameStage = ["Pre-Flop"]
        self.betList = [0] * self.numPlayers
        self.blinds(playerList)
        self.gameStatus = [2] * self.numPlayers
        self.defBet = 20
        self.tempBet = self.defBet

        
    def nextTurn(self, playersList):
        status = self.updateStatus(playersList)
        if status.count(True) == 1:
            self.roundWinner = status.index(True)
            playersList[self.roundWinner].money += sum(self.betList)
            self.roundOver = True
        self.pot += sum(self.betList)
        self.betList = [0] * self.numPlayers
        self.lastPlayerMove = None
        self.tempBet = 20
        self.messages = []
        foldCount = 0
        final = []
        for player in self.game.players:
            player.alreadyPlayed == False
            if player.fold == True:
                final.append(0)
            else:
                final.append(2)
        if len(self.game.deck.onBoard) < 5:
            self.gameStatus = final
            if "Pre-Flop" in self.gameStage and self.count == 0:
                self.game.flop()
                self.gameStage.append("Post-Flop")
                self.count += 1
            elif "Post-Flop" in self.gameStage and self.count == 1:
                self.gameStage.append("Post-Flop 1")
                self.game.deck.burn(1)
                self.game.deck.deal(1, True)
                self.count += 1
            elif "Post-Flop 1" in self.gameStage and self.count == 2:
                self.gameStage.append("Post-Flop 2")
                self.game.deck.burn(1)
                self.game.deck.deal(1, True)
                self.count += 1
        else:
            stillPlaying = []
            for i in range(len(self.gameStatus)):
                status = self.gameStatus[i]
                if status != 0:
                    stillPlaying.append(self.game.playerHands[i])

            result = bestInTable(stillPlaying, self.game.deck.onBoard)
            if result == "split" and self.numPlayers == 2:
                self.roundWinner = [0, 1]
                playersList[self.roundWinner[0]].money += (sum(self.betList)//2)
                playersList[self.roundWinner[1]].money += (sum(self.betList)//2)
            else: 
                self.roundWinner = result[3]
                self.winnerType = result[1]
                self.winnerHand = result[0]
                playersList[self.roundWinner].money += sum(self.betList)
            self.roundOver = True
    


    def blinds(self, playersList):
        self.betList[self.bigBlind] += self.bigBlindVal
        playersList[self.bigBlind].money -= self.bigBlindVal
        self.betList[self.smallBlind] += self.smallBlindVal
        playersList[self.smallBlind].money -= self.smallBlindVal