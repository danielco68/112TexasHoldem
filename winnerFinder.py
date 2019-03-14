from handEvaluator import *
import itertools

#Finds best possible hand for any given player
#Finds best player hand on the poker table
#Takes care of who wins the poker game
################################################################################    
def findBestHand(tableAndHand):
    combs = itertools.combinations(tableAndHand, 5) 
    allHands = []
    bestHand = None
    maxScore = -1
    for comb in combs:
        allHands.append(list(comb))
    for hand in allHands:
        currHand = Hand(hand)
        handScore = currHand.checkHand()[0]
        if handScore > maxScore:
            maxScore = handScore
            bestHand = currHand
    winScore = bestHand.checkHand()[0]
    winHand = bestHand
    return (winScore, winHand)

################################################################################
def bestInTable(players, table):
    bestPlayerHand = None
    maxHandScore = -1
    bestPlayer = None
    bestPlayerType = None
    equal = []
    for player in players:
        total = player + table
        currBestHand = findBestHand(total)
        if currBestHand[0] > maxHandScore:
            bestPlayerHand = currBestHand[1]
            maxHandScore = currBestHand[0]
            bestPlayer = player
            bestPlayerType = bestPlayerHand.checkHand()[1]
        elif currBestHand[0] == maxHandScore:
            hand1 = currBestHand[1]
            hand2 = bestPlayerHand
            bestOfTwo = equalityChecker(hand1, hand2)
            if bestOfTwo == "split":
                return "split"
            else:
                bestPlayerHand = bestOfTwo
                maxHandScore = bestPlayerHand.checkHand()[0]
                bestPlayer = player
                bestPlayerType = bestPlayerHand.checkHand()[1]
    playerID = players.index(bestPlayer)
    return (bestPlayerHand, bestPlayerType, maxHandScore, playerID)