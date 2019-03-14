from tkinter import *
import random
import math
import copy
from image_util import *
import time

from imageLoading import *
from playerClass import *
from handEvaluator import *
from winnerFinder import *
from gameflowMechanics import *
from AIClass import *
#Integrates visuals with game mechanics and gameflow. 
#Takes care of all visual aspects of the game
#implements AI Moves which require data

####################################
# init
####################################
class Button():
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.size = 75
        self.text = text

    def createButton(self, canvas, color):
        canvas.create_rectangle(self.x - self.size, self.y - self.size, self.x + self.size, self.y + self.size, fill = color)
        canvas.create_text(self.x, self.y, text = self.text, font = ('system', '15'), fill = "white")

    def withinBounds(self, event):
        if self.x - self.size < event.x < self.x + self.size and\
    self.y - self.size < event.y < self.y + self.size:
            return True
        else:
            return False 


def init(data): #Initalizes variables to setup game
    data.numOps = 2
    data.game = Poker(data.numOps)
    data.game.deck.shuffle()
    data.game.startGame()
    data.mode = "menu"
    data.playerPos = []
    data.numPlayers = len(data.game.players)
    data.callButton = Button(100, 500, "Call/Check")
    data.foldButton = Button(900, 100, "Fold")
    data.endTurnButton = Button(300, 500, "End Turn")
    data.raiseButton = Button(900, 500, "Raise")
    data.flopButton = Button(900, 100, "Flop")
    data.nextRoundButton = Button(data.width/2 - 350, data.height/2 + 200, "Next Round")
    data.timer = 0
    data.gameFlow = gameFlow(data.numPlayers, data.game.players, data.game)
    data.gameFlow.blinds(data.game.players)
    data.cardImages = makeImageDict("C:/Users/danie/Desktop/cards")
    data.currPlayerCards = imageLoader(data.game.playerHands[0], data)
    if data.numPlayers == 2:
        data.opponentCards1 = imageLoader(data.game.playerHands[1], data)
        data.op0Card1 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.opponentCards1[0])
        data.op0Card2 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.opponentCards1[1])
    else:
        data.opponentCards1 = imageLoader(data.game.playerHands[1], data)
        data.opponentCards2 = imageLoader(data.game.playerHands[2], data)
        data.opponentCards3 = imageLoader(data.game.playerHands[3], data)
        data.op0Card1 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.opponentCards1[0])
        data.op0Card2 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.opponentCards1[1])
        data.op1Card1 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.opponentCards2[0])
        data.op1Card2 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.opponentCards2[1])
        data.op2Card1 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.opponentCards3[0])
        data.op2Card2 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.opponentCards3[1])
    data.card1 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.currPlayerCards[0])
    data.card2 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.currPlayerCards[1])
    data.back = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + "back.gif")
    data.menuBackground = PhotoImage(file = "C:/Users/danie/Desktop/CS Term Project/Actual Code/" + "menuBackground.gif")
    data.rotatedBack = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + "rotatedBack.gif")
    data.flopImages = None
    data.startGameButton = Button(data.width/2, data.height/2, "Play some Poker")
    data.singleplayerButton = Button(data.width/2 - 100, data.height/2, "Singleplayer")
    data.numOp1Button = Button(data.width/2 - 200, data.height/2, "Duel an AI")
    data.numOp3Button = Button(data.width/2 + 200, data.height/2, "Fight 3 AIs")
    data.easyDiffButton = Button(data.width/2 - 300, data.height/2, "Easy Mode")
    data.mediumDiffButton = Button(data.width/2 , data.height/2, "Medium Mode")
    data.hardDiffButton = Button(data.width/2 + 300, data.height/2, "Hard Mode")
    data.gameBackground = PhotoImage(file = "C:/Users/danie/Desktop/CS Term Project/Actual Code/" + "gameBackground.gif")
    data.game.simulatedFlop()
    data.flopCards = imageLoader(data.game.simulatedFlopCards, data)
    data.flop1 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.flopCards[0])
    data.flop2 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.flopCards[1])
    data.flop3 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.flopCards[2])
    data.flop4 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.flopCards[3])
    data.flop5 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.flopCards[4])
    data.slider = 0
    data.theatreModeButton = Button(data.width/2 + 100, data.height/2, "Theatre Mode")
    data.curt1 = PhotoImage(file = "C:/Users/danie/Desktop/CS Term Project/Actual Code/" + "curt#1.gif")
    data.curt2 = PhotoImage(file = "C:/Users/danie/Desktop/CS Term Project/Actual Code/" + "curt#2.gif")

def call(data):
    data.gameFlow.move("check/call", data.gameFlow.currentPlayer, data.game.players)

def fold(data):
    data.gameFlow.move("fold", data.gameFlow.currentPlayer, data.game.players)

def endTurn(data):
    data.currentPlayer = (data.currentPlayer + 1) % data.numPlayers

def raiseCash(data):
    data.gameFlow.move("raise", data.gameFlow.currentPlayer, data.game.players)

def showFlop(data):
    data.game.flop()

def hardMove1(aiID, aiHand, playerList, gameFlow, data):
    playerID = aiID
    numTrials = 1000
    wins = 0
    for trial in range(numTrials):
        trialGame = Poker(len(playerList))
        index1 = trialGame.deck.deck.index(data.game.simulatedFlopCards[0])
        trialGame.deck.deck.pop(index1)
        index2 = trialGame.deck.deck.index(data.game.simulatedFlopCards[1])
        trialGame.deck.deck.pop(index2)
        index3 = trialGame.deck.deck.index(data.game.simulatedFlopCards[2])
        trialGame.deck.deck.pop(index3)
        trialGame.AIStartGame(aiHand, aiID)
        trialGame.deck.onBoard.append(data.game.simulatedFlopCards[0])
        trialGame.deck.onBoard.append(data.game.simulatedFlopCards[1])
        trialGame.deck.onBoard.append(data.game.simulatedFlopCards[2])
        trialGame.deck.burn(1)
        trialGame.deck.deal(1, True)
        trialGame.deck.burn(1)
        trialGame.deck.deal(1, True)
        result = bestInTable(trialGame.playerHands, trialGame.deck.onBoard)
        if result == "split":
            continue
        elif result[3] == playerID:
            wins += 1
    currentAI = data.game.AIList[aiID]
    if wins/numTrials < 0.4:
        if gameFlow.lastPlayerMove == "check/call":
            gameFlow.move("check/call", playerID, gameFlow.game.players)
        else:
            gameFlow.move("fold", playerID, gameFlow.game.players)
    elif 0.4 < wins/numTrials < 0.6:
        gameFlow.move("check/call", playerID, gameFlow.game.players)
    else:
        if gameFlow.numPlayers == 2 and currentAI.raised or gameFlow.numPlayers == 4 and currentAI.raised:
            gameFlow.move("check/call", playerID, gameFlow.game.players)
            currentAI.raised = False
        else:
            currentAI.raised = True
            gameFlow.move("raise", playerID, gameFlow.game.players)

def hardMove2(aiID, aiHand, playerList, gameFlow, data):
    playerID = aiID
    numTrials = 1000
    wins = 0
    for trial in range(numTrials):
        trialGame = Poker(len(playerList))
        index1 = trialGame.deck.deck.index(data.game.simulatedFlopCards[0])
        trialGame.deck.deck.pop(index1)
        index2 = trialGame.deck.deck.index(data.game.simulatedFlopCards[1])
        trialGame.deck.deck.pop(index2)
        index3 = trialGame.deck.deck.index(data.game.simulatedFlopCards[2])
        trialGame.deck.deck.pop(index3)
        index4 = trialGame.deck.deck.index(data.game.simulatedFlopCards[3])
        trialGame.deck.deck.pop(index4)
        trialGame.AIStartGame(aiHand, aiID)
        trialGame.deck.onBoard.append(data.game.simulatedFlopCards[0])
        trialGame.deck.onBoard.append(data.game.simulatedFlopCards[1])
        trialGame.deck.onBoard.append(data.game.simulatedFlopCards[2])
        trialGame.deck.onBoard.append(data.game.simulatedFlopCards[3])
        trialGame.deck.burn(1)
        trialGame.deck.deal(1, True)
        result = bestInTable(trialGame.playerHands, trialGame.deck.onBoard)
        if result == "split":
            continue
        elif result[3] == playerID:
            wins += 1
    currentAI = data.game.AIList[aiID]
    if wins/numTrials < 0.4:
        if gameFlow.lastPlayerMove == "check/call":
            gameFlow.move("check/call", playerID, gameFlow.game.players)
        else:
            gameFlow.move("fold", playerID, gameFlow.game.players)
    elif 0.4 < wins/numTrials < 0.6:
        gameFlow.move("check/call", playerID, gameFlow.game.players)
    else:
        if gameFlow.numPlayers == 2 and currentAI.raised or gameFlow.numPlayers == 4 and currentAI.raised:
            gameFlow.move("check/call", playerID, gameFlow.game.players)
            currentAI.raised = False
        else:
            currentAI.raised = True
            gameFlow.move("raise", playerID, gameFlow.game.players)

def hardMove3(aiID, aiHand, playerList, gameFlow, data):
    playerID = aiID
    numTrials = 1000
    wins = 0
    for trial in range(numTrials):
        trialGame = Poker(len(playerList))
        index1 = trialGame.deck.deck.index(data.game.simulatedFlopCards[0])
        trialGame.deck.deck.pop(index1)
        index2 = trialGame.deck.deck.index(data.game.simulatedFlopCards[1])
        trialGame.deck.deck.pop(index2)
        index3 = trialGame.deck.deck.index(data.game.simulatedFlopCards[2])
        trialGame.deck.deck.pop(index3)
        index4 = trialGame.deck.deck.index(data.game.simulatedFlopCards[3])
        trialGame.deck.deck.pop(index4)
        index5 = trialGame.deck.deck.index(data.game.simulatedFlopCards[4])
        trialGame.deck.deck.pop(index5)
        trialGame.AIStartGame(aiHand, aiID)
        trialGame.deck.onBoard.append(data.game.simulatedFlopCards[0])
        trialGame.deck.onBoard.append(data.game.simulatedFlopCards[1])
        trialGame.deck.onBoard.append(data.game.simulatedFlopCards[2])
        trialGame.deck.onBoard.append(data.game.simulatedFlopCards[3])
        trialGame.deck.onBoard.append(data.game.simulatedFlopCards[4])
        result = bestInTable(trialGame.playerHands, trialGame.deck.onBoard)
        if result == "split":
                continue
        elif result[3] == playerID:
            wins += 1
    currentAI = data.game.AIList[aiID]
    if wins/numTrials < 0.4:
        if gameFlow.lastPlayerMove == "check/call":
            gameFlow.move("check/call", playerID, gameFlow.game.players)
        else:
            gameFlow.move("fold", playerID, gameFlow.game.players)
    elif 0.4 < wins/numTrials < 0.6:
        gameFlow.move("check/call", playerID, gameFlow.game.players)
    else:
        if gameFlow.numPlayers == 2 and currentAI.raised or gameFlow.numPlayers == 4 and currentAI.raised:
            gameFlow.move("check/call", playerID, gameFlow.game.players)
            currentAI.raised = False
        else:
            currentAI.raised = True
            gameFlow.move("raise", playerID, gameFlow.game.players)
####################################
def updatePlayerCount(data, numPlayers):
    data.numOps = numPlayers
    data.game = Poker(data.numOps)
    data.game.deck.shuffle()
    data.game.startGame()
    data.mode = "menu"
    data.playerPos = []
    data.numPlayers = len(data.game.players)
    data.callButton = Button(100, 500, "Call/Check")
    data.foldButton = Button(900, 100, "Fold")
    data.endTurnButton = Button(300, 500, "End Turn")
    data.raiseButton = Button(900, 500, "Raise")
    data.flopButton = Button(900, 100, "Flop")
    data.nextRoundButton = Button(data.width/2 - 350, data.height/2 + 200, "Next Round")
    data.timer = 0
    data.gameFlow = gameFlow(data.numPlayers, data.game.players, data.game)
    data.gameFlow.blinds(data.game.players)
    data.cardImages = makeImageDict("C:/Users/danie/Desktop/cards")
    data.currPlayerCards = imageLoader(data.game.playerHands[0], data)
    if data.numPlayers == 2:
        data.opponentCards1 = imageLoader(data.game.playerHands[1], data)
        data.op0Card1 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.opponentCards1[0])
        data.op0Card2 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.opponentCards1[1])
    else:
        data.opponentCards1 = imageLoader(data.game.playerHands[1], data)
        data.opponentCards2 = imageLoader(data.game.playerHands[2], data)
        data.opponentCards3 = imageLoader(data.game.playerHands[3], data)
        data.op0Card1 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.opponentCards1[0])
        data.op0Card2 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.opponentCards1[1])
        data.op1Card1 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.opponentCards2[0])
        data.op1Card2 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.opponentCards2[1])
        data.op2Card1 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.opponentCards3[0])
        data.op2Card2 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.opponentCards3[1])
    data.card1 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.currPlayerCards[0])
    data.card2 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.currPlayerCards[1])
    data.back = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + "back.gif")
    data.menuBackground = PhotoImage(file = "C:/Users/danie/Desktop/CS Term Project/Actual Code/" + "menuBackground.gif")
    data.rotatedBack = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + "rotatedBack.gif")
    data.flopImages = None
    data.startGameButton = Button(data.width/2, data.height/2, "Play some Poker")
    data.singleplayerButton = Button(data.width/2 - 100, data.height/2, "Singleplayer")
    data.numOp1Button = Button(data.width/2 - 200, data.height/2, "Duel an AI")
    data.numOp3Button = Button(data.width/2 + 200, data.height/2, "Fight 3 AIs")
    data.easyDiffButton = Button(data.width/2 - 300, data.height/2, "Easy Mode")
    data.mediumDiffButton = Button(data.width/2 , data.height/2, "Medium Mode")
    data.hardDiffButton = Button(data.width/2 + 300, data.height/2, "Hard Mode")
    data.gameBackground = PhotoImage(file = "C:/Users/danie/Desktop/CS Term Project/Actual Code/" + "gameBackground.gif")
    data.game.simulatedFlop()
    data.flopCards = imageLoader(data.game.simulatedFlopCards, data)
    data.flop1 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.flopCards[0])
    data.flop2 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.flopCards[1])
    data.flop3 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.flopCards[2])
    data.flop4 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.flopCards[3])
    data.flop5 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.flopCards[4])
    data.slider = 0
    data.theatreModeButton = Button(data.width/2 + 100, data.height/2, "Theatre Mode")
    data.curt1 = PhotoImage(file = "C:/Users/danie/Desktop/CS Term Project/Actual Code/" + "curt#1.gif")
    data.curt2 = PhotoImage(file = "C:/Users/danie/Desktop/CS Term Project/Actual Code/" + "curt#2.gif")

def drawPlayer(canvas, data):
    if data.game.numPlayers == 2:
        for i in range(data.numPlayers):
            playerCoords = [] 
            x = 0
            y = 0
            if i == 0:
                y = data.height - 100
                x = data.width/2
            elif i == 1:
                y = 100
                x = data.width/2
            playerCoords.append(x)
            playerCoords.append(y)
            data.playerPos.append(playerCoords)
    else:
        for i in range(data.numPlayers):
            x = 0
            y = 0
            playerCoords = [] 
            if i % 2 != 0:
                y = data.height / 2
                if i == 1:
                    x = 100
                else:
                    x = data.width - 100
            else:
                x = data.width / 2
                if i == 0:
                    y = data.height - 100
                else:
                    y = 50
            playerCoords.append(x)
            playerCoords.append(y)
            data.playerPos.append(playerCoords)

################################################
#Menu Round Mode
################################################
def menuRedrawAll(canvas, data):
    canvas.create_image(data.width/2, data.height/2, image = data.menuBackground)
    data.startGameButton.createButton(canvas, "dark green")
    canvas.create_text(data.width/2, 50, text = "112 TEXAS HOLD'EM", font = ('ms serif', '40', "underline"), fill = "white")
    canvas.create_text(data.width/2, 550, text = "By Daniel Cohen", font = ('ms serif', '40'), fill = "white")

def menuMousePressed(event,data):
    if data.startGameButton.withinBounds(event):
        data.mode = "menu2"

################################################
#Menu2 Round Mode
################################################
def menu2RedrawAll(canvas, data):
    canvas.create_image(data.width/2, data.height/2, image = data.menuBackground)
    data.singleplayerButton.createButton(canvas, "deep sky blue")
    data.theatreModeButton.createButton(canvas, "violet")
    canvas.create_text(data.width/2, 70, text = "Choose A Mode", font = ('ms serif', '40', "underline"), fill = "white")

def menu2MousePressed(event,data):
    if data.singleplayerButton.withinBounds(event):
        data.mode = "choosePlayers"
    if data.theatreModeButton.withinBounds(event):
        data.mode = "choosePlayers"
        
        data.gameFlow.theatreMode = True

################################################
#Choose Players Round Mode
################################################
def choosePlayersRedrawAll(canvas, data):
    canvas.create_image(data.width/2, data.height/2, image = data.menuBackground)
    data.numOp1Button.createButton(canvas, "dark orange")
    data.numOp3Button.createButton(canvas, "dark orange")
    canvas.create_text(data.width/2, 70, text = "Choose your opponents", font = ('ms serif', '40', "underline"), fill = "white")

def choosePlayersMousePressed(event, data):
    if data.numOp1Button.withinBounds(event):
        if data.gameFlow.theatreMode != True:
            updatePlayerCount(data, 2)
            data.mode = "difficulty"
        else:
            updatePlayerCount(data, 2)
            data.gameFlow.theatreMode = True
            data.difficulty = "hard"
            data.game.AIList = [AI(i) for i in range(0, data.gameFlow.numPlayers)]
            data.mode = "theatre"

    elif data.numOp3Button.withinBounds(event):
        if data.gameFlow.theatreMode != True:
            updatePlayerCount(data, 4)
            data.mode = "difficulty"
        else:
            updatePlayerCount(data, 4)
            data.gameFlow.theatreMode = True
            data.difficulty = "hard"
            data.game.AIList = [AI(i) for i in range(0, data.gameFlow.numPlayers)]
            data.mode = "theatre"


################################################
#Choose Difficulty Mode
################################################
def difficultyRedrawAll(canvas, data):
    canvas.create_image(data.width/2, data.height/2, image = data.menuBackground)
    data.easyDiffButton.createButton(canvas, "chartreuse2")
    data.mediumDiffButton.createButton(canvas, "DarkOrange1")
    data.hardDiffButton.createButton(canvas, "firebrick3")
    canvas.create_text(data.width/2, 70, text = "Choose AI Difficulty", font = ('ms serif', '40', "underline"), fill = "white")
def difficultyMousePressed(event, data):
    if data.easyDiffButton.withinBounds(event):
        data.difficulty = "easy"
        data.mode = "Poker"
    elif data.mediumDiffButton.withinBounds(event):
        data.difficulty = "medium"
        data.mode = "Poker"
    elif data.hardDiffButton.withinBounds(event):
        data.difficulty = "hard"
        data.mode = "Poker"
def difficultyKeyPressed(event, data):
    pass


################################################
#Game Mode
################################################
def PokerMousePressed(event, data):
    if data.callButton.withinBounds(event):
        call(data)
    elif data.foldButton.withinBounds(event):
        fold(data)
    elif data.endTurnButton.withinBounds(event):
        endTurn(data)
    elif data.raiseButton.withinBounds(event):
        raiseCash(data)
    elif data.flopButton.withinBounds(event):
        showFlop(data)

def PokerKeyPressed(event, data):  
    if event.keysym == "Up":
        if data.gameFlow.tempBet < data.game.players[data.gameFlow.currentPlayer].money:
            data.gameFlow.tempBet += 10
    elif event.keysym == "Down":
        if data.gameFlow.tempBet >= data.gameFlow.defBet:
            data.gameFlow.tempBet -= 10

def PokerTimerFired(data):
    data.timer += 100
    for i in range(len(data.gameFlow.gameStatus)):
        status = data.gameFlow.gameStatus[i]
        player = data.game.players[i]
        if player.money == 0:
            if player.fold == True:
                status = 0
            else:
                status = 1
    if data.gameFlow.currentPlayer == 0 and data.gameFlow.theatreMode:
        if data.game.players[data.gameFlow.currentPlayer].fold == True:
            data.gameFlow.currentPlayer += 1
            data.gameFlow.currentPlayer %= data.gameFlow.numPlayers
        else:
            currentAIPlayer = data.game.AIList[data.gameFlow.currentPlayer]
            hand = data.game.playerHands[data.gameFlow.currentPlayer]
            if data.difficulty == "easy":
                if data.timer % 2000 == 0:
                    currentAIPlayer.easyDiff(hand, data.game.players, data.gameFlow)
            elif data.difficulty == "medium":
                if "Post-Flop" in data.gameFlow.gameStage:
                    if data.timer % 2000 == 0:
                        currentAIPlayer.AIMove(hand, data.game.players, data.gameFlow)
                else:
                    if data.timer % 2000 == 0:
                        currentAIPlayer.preFlopMove(hand, data.game.players, data.gameFlow)
                        currentAIPlayer.strength = 0
            elif data.difficulty == "hard":
                if "Post-Flop" in data.gameFlow.gameStage and data.gameFlow.count == 1:
                    if data.timer % 2000 == 0:
                        hardMove1(data.gameFlow.currentPlayer, hand, data.game.players, data.gameFlow, data)
                elif "Post-Flop 1" in data.gameFlow.gameStage and data.gameFlow.count == 2:
                    if data.timer % 2000 == 0:
                        hardMove2(data.gameFlow.currentPlayer, hand, data.game.players, data.gameFlow, data)
                elif "Post-Flop 2" in data.gameFlow.gameStage and data.gameFlow.count == 3:
                    if data.timer % 2000 == 0:
                        hardMove3(data.gameFlow.currentPlayer, hand, data.game.players, data.gameFlow, data)
                else:
                    if data.timer % 2000 == 0:
                        currentAIPlayer.preFlopMove(hand, data.game.players, data.gameFlow)
                        currentAIPlayer.strength = 0
    else:
        if data.gameFlow.currentPlayer != 0:
            if data.game.players[data.gameFlow.currentPlayer].fold == True:
                data.gameFlow.currentPlayer += 1
                data.gameFlow.currentPlayer %= data.gameFlow.numPlayers
            else:
                currentAIPlayer = data.game.AIList[data.gameFlow.currentPlayer]
                hand = data.game.playerHands[data.gameFlow.currentPlayer]
                if data.difficulty == "easy":
                    if data.timer % 2000 == 0:
                        currentAIPlayer.easyDiff(hand, data.game.players, data.gameFlow)
                elif data.difficulty == "medium":
                    if "Post-Flop" in data.gameFlow.gameStage:
                        if data.timer % 2000 == 0:
                            currentAIPlayer.AIMove(hand, data.game.players, data.gameFlow)
                    else:
                        if data.timer % 2000 == 0:
                            currentAIPlayer.preFlopMove(hand, data.game.players, data.gameFlow)
                            currentAIPlayer.strength = 0
                elif data.difficulty == "hard":
                    if "Post-Flop" in data.gameFlow.gameStage and data.gameFlow.count == 1:
                        if data.timer % 2000 == 0:
                            hardMove1(data.gameFlow.currentPlayer, hand, data.game.players, data.gameFlow, data)
                    elif "Post-Flop 1" in data.gameFlow.gameStage and data.gameFlow.count == 2:
                        if data.timer % 2000 == 0:
                            hardMove2(data.gameFlow.currentPlayer, hand, data.game.players, data.gameFlow, data)
                    elif "Post-Flop 2" in data.gameFlow.gameStage and data.gameFlow.count == 3:
                            if data.timer % 2000 == 0:
                                hardMove3(data.gameFlow.currentPlayer, hand, data.game.players, data.gameFlow, data)
                    else:
                            if data.timer % 2000 == 0:
                                currentAIPlayer.preFlopMove(hand, data.game.players, data.gameFlow)
                                currentAIPlayer.strength = 0

    if data.gameFlow.roundOver:
        data.mode = "endRound"

def PokerRedrawAll(canvas, data): 
    canvas.create_image(data.width/2, data.height/2, image = data.gameBackground)
    drawPlayer(canvas, data)
    if "Post-Flop" in data.gameFlow.gameStage:
        canvas.create_image(350, data.height/2, image = data.flop1)
        canvas.create_image(430, data.height/2, image = data.flop2)
        canvas.create_image(510, data.height/2, image = data.flop3)
    if "Post-Flop 1" in data.gameFlow.gameStage:
        canvas.create_image(590, data.height/2, image = data.flop4)
    if "Post-Flop 2" in data.gameFlow.gameStage:
        canvas.create_image(670, data.height/2, image = data.flop5)
    if data.mode != "theatre":
        data.callButton.createButton(canvas, "dark green")
        data.foldButton.createButton(canvas, "firebrick4")
        data.raiseButton.createButton(canvas, "DarkSlateGray4")
    else:
        canvas.create_image(60, data.height/2, image = data.curt1)
        canvas.create_image(940, data.height/2, image = data.curt2)
    for player in data.playerPos:
        x = player[0]
        y = player[1]
        size = 50
        canvas.create_rectangle(x - size, y - size, x + size, y + size)
    if data.mode != "theatre":
        canvas.create_text(65, 50, text = "Pot: $" + str(data.gameFlow.pot), font = ('system', '20', "underline"), fill = "white")
    else:
        canvas.create_text(200, 70, text = "Pot: $" + str(data.gameFlow.pot), font = ('system', '20', "underline"), fill = "white")
    if data.mode != "theatre":
        if data.gameFlow.lastPlayerMove == "raise":
            canvas.create_text(900, 520, text = "Raise by " + str(data.gameFlow.tempBet * 2), font = ('system', '10'), fill = "white")
        else:
            canvas.create_text(900, 520, text = "Raise by " + str(data.gameFlow.tempBet), font = ('system', '10'), fill = "white")
    for player in range(len(data.game.players)):
        cards = data.game.playerHands[player]
        playerX = data.playerPos[player][0]
        playerY = data.playerPos[player][1] 
        if player == 0:
            canvas.create_image(playerX - 100, playerY, image = data.card1)
            canvas.create_image(playerX + 100, playerY, image = data.card2)
        else:
            if data.mode != "theatre":
                if player == 1 and data.gameFlow.numPlayers == 2:
                    canvas.create_image(playerX - 100, playerY, image = data.back)
                    canvas.create_image(playerX + 100, playerY, image = data.back)
                elif player == 1 and data.gameFlow.numPlayers != 2:
                    canvas.create_image(playerX + 100, playerY - 50, image = data.rotatedBack)
                    canvas.create_image(playerX + 100, playerY + 50, image = data.rotatedBack)
                elif player == 2 and data.gameFlow.numPlayers != 2:
                    canvas.create_image(playerX - 100, playerY, image = data.back)
                    canvas.create_image(playerX + 100, playerY, image = data.back)
                elif player == 3 and data.gameFlow.numPlayers != 2:
                    canvas.create_image(playerX - 100, playerY - 50, image = data.rotatedBack)
                    canvas.create_image(playerX - 100, playerY + 50, image = data.rotatedBack)
            else:
                if player == 1 and data.gameFlow.numPlayers != 2:
                    canvas.create_image(playerX - 40, playerY + 130, image = data.op0Card1)
                    canvas.create_image(playerX + 40, playerY + 130, image = data.op0Card2)
                elif player == 1 and data.gameFlow.numPlayers == 2:
                    canvas.create_image(playerX - 100, playerY, image = data.op0Card1)
                    canvas.create_image(playerX + 100, playerY, image = data.op0Card1)
                elif player == 2:
                    canvas.create_image(playerX - 100, playerY, image = data.op1Card1)
                    canvas.create_image(playerX + 100, playerY, image = data.op1Card2)
                elif player == 3:
                    canvas.create_image(playerX - 40, playerY + 130, image = data.op2Card1)
                    canvas.create_image(playerX + 40, playerY + 130, image = data.op2Card2)

        money = data.game.players[player].money
        moneyOnBoard = data.gameFlow.betList[player]
        canvas.create_text(playerX, playerY + 20, text = "Money: $" + str(money),  font = ("system", "10"), fill = "white")
        canvas.create_text(playerX, playerY - 20, text = "On board: $" +str(moneyOnBoard), font = ("system", "10"), fill = "white")
        if player == data.gameFlow.dealer:
            offsetDealer = 0
            if (player == data.gameFlow.bigBlind and player == data.gameFlow.dealer) or\
            (player == data.gameFlow.smallBlind and player == data.gameFlow.dealer):
                offsetDealer = 40
            if data.gameFlow.numPlayers == 2:
                if data.gameFlow.dealer == 0:
                    dealerX = playerX - offsetDealer
                    dealerY = playerY - 100
                else:
                    dealerX = playerX - offsetDealer
                    dealerY = playerY + 100
            else:
                if data.gameFlow.dealer == 0:
                    dealerX = playerX - offsetDealer
                    dealerY = playerY - 100
                elif data.gameFlow.dealer == 1:
                    dealerX = playerX + 185
                    dealeyY = playerY - offsetDealer
                elif data.gameFlow.dealer == 2:
                    dealerX = playerX - offsetDealer
                    dealerY = playerY + 100
                elif data.gameFlow.dealer == 3:
                    dealerX = playerX - 185
                    dealerY = playerY - offsetDealer
            canvas.create_oval(dealerX - 30, dealerY - 30, dealerX + 30, dealerY + 30, fill = "white")
            canvas.create_text(dealerX, dealerY, text = "DEALER")
        if player == data.gameFlow.currentPlayer:
            if data.gameFlow.numPlayers == 2:
                canvas.create_text(playerX - 230, playerY, text = "Current Player", font = ("system", "9", "underline"), fill = "white")
            else:
                canvas.create_text(playerX, playerY + 60, text = "Current Player", font = ("system", "9", "underline"), fill = "white")
        if data.game.players[player].fold:
            canvas.create_text(playerX, playerY - 40, text = "FOLDED", font = ("system", "9", "underline"), fill = "white")
        if player == data.gameFlow.smallBlind:
            smallBlindX = 0
            smallBlindY = 0
            offsetSmall = 0
            if player == data.gameFlow.smallBlind and player == data.gameFlow.dealer:
                offsetSmall = 40
            if data.gameFlow.numPlayers == 2:
                if data.gameFlow.smallBlind == 0:
                    smallBlindX = playerX + offsetSmall
                    smallBlindY = playerY - 100
                else:
                    smallBlindX = playerX + offsetSmall
                    smallBlindY = playerY + 100
            else:
                if data.gameFlow.smallBlind == 0:
                    smallBlindX = playerX + offsetSmall
                    smallBlindY = playerY - 100
                elif data.gameFlow.smallBlind == 1:
                    smallBlindX = playerX + 185
                    smallBlindY = playerY + offsetSmall
                elif data.gameFlow.smallBlind == 2:
                    smallBlindX = playerX + offsetSmall
                    smallBlindY = playerY + 100
                elif data.gameFlow.smallBlind == 3:
                    smallBlindX = playerX - 185
                    smallBlindY = playerY + offsetSmall

            canvas.create_oval(smallBlindX - 30, smallBlindY - 30, smallBlindX + 30, smallBlindY + 30, fill = "yellow")
            canvas.create_text(smallBlindX, smallBlindY, text = "SMALL B")
        if player == data.gameFlow.bigBlind:
            offsetBig = 0
            if player == data.gameFlow.bigBlind and player == data.gameFlow.dealer:
                offsetBig = 40
            if data.gameFlow.numPlayers == 2:
                if data.gameFlow.bigBlind == 0:
                    bigBlindX = playerX + offsetBig
                    bigBlindY = playerY - 100
                else:
                    bigBlindX = playerX + offsetBig
                    bigBlindY = playerY + 100
            else:
                if data.gameFlow.bigBlind == 1:
                    bigBlindX = playerX + 185
                    bigBlindY = playerY + offsetBig
                elif data.gameFlow.bigBlind == 2:
                    bigBlindX = playerX + offsetBig
                    bigBlindY = playerY + 100
                elif data.gameFlow.bigBlind == 3:
                    bigBlindX = playerX - 185
                    bigBlindY = playerY + offsetBig
            canvas.create_oval(bigBlindX - 30, bigBlindY - 30, bigBlindX + 30, bigBlindY + 30, fill = "blue")
            canvas.create_text(bigBlindX, bigBlindY, text = "BIG BLIND", fill = "white")
        for message in data.gameFlow.messages:
            messageList = list(message)
            if player == 0 and messageList[7] == "0":
                canvas.create_text(playerX, playerY - 60 , text = message, font = ("system", "6"), fill = "white")
            elif player == 1 and data.gameFlow.numPlayers == 2 and messageList[7] == "1":
                canvas.create_text(playerX, playerY + 60 , text = message, font = ("system", "6"), fill = "white")
            elif player == 1 and data.gameFlow.numPlayers == 4 and messageList[7] == "1":
                canvas.create_text(playerX, playerY + 110, text = message, font = ("system", "6"), fill = "white")
            elif player == 2 and messageList[7] == "2":
                canvas.create_text(playerX, playerY + 60 , text = message, font = ("system", "6"), fill = "white")
            elif player == 3 and messageList[7] == "3":
                canvas.create_text(playerX, playerY + 110, text = message, font = ("system", "6"), fill = "white")
    if data.timer % 4000 == 0:
        data.gameFlow.messages = []

################################################
#Theatre Mode Player Select
################################################


################################################
#Next Round Mode
################################################
def endRoundRedrawAll(canvas, data):
    canvas.create_image(data.width/2, data.height/2, image = data.gameBackground)
    canvas.create_text(data.width/2, data.height/2 - 65, text = "On the Table:", font = ("system", "6"), fill = "white")
    if "Post-Flop" in data.gameFlow.gameStage:
        canvas.create_image(350, data.height/2, image = data.flop1)
        canvas.create_image(430, data.height/2, image = data.flop2)
        canvas.create_image(510, data.height/2, image = data.flop3)
    if "Post-Flop 1" in data.gameFlow.gameStage:
        canvas.create_image(590, data.height/2, image = data.flop4)
    if "Post-Flop 2" in data.gameFlow.gameStage:
        canvas.create_image(670, data.height/2, image = data.flop5)
    for player in range(len(data.game.players)):
        cards = data.game.playerHands[player]
        playerX = data.playerPos[player][0]
        playerY = data.playerPos[player][1] 
        if player == 0:
            canvas.create_text(playerX, playerY - 70, text = "Player 0 Hand", font = ("system", "6"), fill = "white")
            canvas.create_image(playerX - 50, playerY, image = data.card1)
            canvas.create_image(playerX + 50, playerY, image = data.card2)
        else:
            if data.gameFlow.numPlayers == 2:
                canvas.create_text(playerX, playerY + 70, text = "Player 1 Hand", font = ("system", "6"), fill = "white")
                canvas.create_image(playerX - 50, playerY, image = data.op0Card1)
                canvas.create_image(playerX + 50, playerY, image = data.op0Card2)
            else:
                canvas.create_text(playerX, playerY + 70, text = "Player " + str(player) + " Hand", font = ("system", "6"), fill = "white")
                if player == 1:
                    canvas.create_image(playerX - 50, playerY, image = data.op0Card1)
                    canvas.create_image(playerX + 50, playerY, image = data.op0Card2)
                elif player == 2:
                    canvas.create_image(playerX - 50, playerY, image = data.op1Card1)
                    canvas.create_image(playerX + 50, playerY, image = data.op1Card2)
                elif player == 3:
                    canvas.create_image(playerX - 50, playerY, image = data.op2Card1)
                    canvas.create_image(playerX + 50, playerY, image = data.op2Card2)
    if data.gameFlow.winDueToFold[0]:
        data.nextRoundButton.createButton(canvas, "violet red")
        canvas.create_text(data.width/2, data.height/2 + 80, text = "Player " + str(data.gameFlow.roundWinner) + " " + data.gameFlow.winDueToFold[1], font = ("system", "6"), fill = "white")
        canvas.create_text(data.width/2, data.height/2 + 100, text =  "Player " + str(data.gameFlow.roundWinner) + " won $" + str(data.gameFlow.pot), font = ("system", "6"), fill = "white")
    else:
        if type(data.gameFlow.roundWinner) == list:
            canvas.create_text(data.width/2, data.height/2 + 100, text = "Both players have exactly equal hands: Pot is split", font = ("system", "6"), fill = "white")
            canvas.create_text(data.width/2, data.height/2 + 120, text =  "Each player won $" + str(data.gameFlow.pot//2), font = ("system", "6"), fill = "white")
        else:
            canvas.create_text(data.width/2 + 200, data.height/2 + 100, text = "Player " + str(data.gameFlow.roundWinner) + " has won", font = ("system", "6"), fill = "white")
            canvas.create_text(data.width/2 + 200, data.height/2 + 200, text = "Had " + str(data.gameFlow.winnerHand), font = ("system", "6"), fill = "white")
            canvas.create_text(data.width/2 + 200, data.height/2 + 220, text = "Won with " + str(data.gameFlow.winnerType) + " hand", font = ("system", "6"), fill = "white")
            canvas.create_text(data.width/2 + 200, data.height/2 + 240, text =  "Player won $" + str(data.gameFlow.pot), font = ("system", "6"), fill = "white")
        data.nextRoundButton.createButton(canvas, "violet red")

def endRoundMousePressed(event, data):
    if data.nextRoundButton.withinBounds(event):
        data.gameFlow.roundOver = False
        data.gameFlow.winDueToFold[0] = False
        data.gameFlow.nextRound(data.game.players)
        data.currPlayerCards = imageLoader(data.game.playerHands[0], data)
        data.card1 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.currPlayerCards[0])
        data.card2 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.currPlayerCards[1])
        if data.numPlayers == 2:
            data.opponentCards1 = imageLoader(data.game.playerHands[1], data)
            data.op0Card1 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.opponentCards1[0])
            data.op0Card2 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.opponentCards1[1])
        else:
            data.opponentCards1 = imageLoader(data.game.playerHands[1], data)
            data.opponentCards2 = imageLoader(data.game.playerHands[2], data)
            data.opponentCards3 = imageLoader(data.game.playerHands[3], data)
            data.op0Card1 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.opponentCards1[0])
            data.op0Card2 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.opponentCards1[1])
            data.op1Card1 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.opponentCards2[0])
            data.op1Card2 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.opponentCards2[1])
            data.op2Card1 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.opponentCards3[0])
            data.op2Card2 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.opponentCards3[1])
        data.back = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + "back.gif")
        data.game.simulatedFlop()
        data.flopCards = imageLoader(data.game.simulatedFlopCards, data)
        data.flop1 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.flopCards[0])
        data.flop2 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.flopCards[1])
        data.flop3 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.flopCards[2])
        data.flop4 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.flopCards[3])
        data.flop5 = PhotoImage(file = "C:/Users/danie/Desktop/cards/" + data.flopCards[4])
        if data.gameFlow.theatreMode:
            data.mode = "theatre"
        else:
            data.mode = "Poker"

def endRoundTimerFired(data):
    pass
        
####################################
# mode dispatcher
####################################

#Chooses mode base on what data.mode is set to
def mousePressed(event, data):
    if (data.mode == "Poker"): PokerMousePressed(event, data)
    elif data.mode == "difficulty": difficultyMousePressed(event, data)
    elif (data.mode == "endRound"):   endRoundMousePressed(event, data)
    elif (data.mode == "menu"): menuMousePressed(event, data)
    elif data.mode == "menu2": menu2MousePressed(event, data)
    elif data.mode == "choosePlayers": choosePlayersMousePressed(event, data)
    elif data.mode == "theatre" : PokerMousePressed(event, data)
    
def keyPressed(event, data):
    if (data.mode == "Poker"): PokerKeyPressed(event, data)
    elif (data.mode == "menu"):   menuKeyPressed(event, data)
    elif (data.mode == "GameOver"):       GameOverKeyPressed(event, data)
    elif data.mode == "difficulty": difficultyKeyPressed(event, data)


def timerFired(data):
    if (data.mode == "Poker"): PokerTimerFired(data)
    elif (data.mode == "endRound"):   endRoundTimerFired(data)
    elif data.mode == "theatre" :   PokerTimerFired(data)

def redrawAll(canvas, data):
    if (data.mode == "Poker"): PokerRedrawAll(canvas, data)
    elif (data.mode == "menu"):   menuRedrawAll(canvas, data)
    elif data.mode == "difficulty": difficultyRedrawAll(canvas, data)
    elif (data.mode == "endRound"):  endRoundRedrawAll(canvas, data)
    elif data.mode == "menu2": menu2RedrawAll(canvas, data)
    elif data.mode == "choosePlayers": choosePlayersRedrawAll(canvas, data)
    elif data.mode == "theatre" : PokerRedrawAll(canvas, data)
    
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.geometry("1000x600+0+0")
    root.mainloop()  # blocks until window is closed

run(1000, 600)