
import random

#Deals with dictating which type of hand a player has
#Deals with equality checking if players have same hand type

################################################################################
class Card(): 
    numbers = {2:0, 3:1, 4:2, 5:3, 6:4, 7:5, 8:6, 9:7, 10:8, 11:9, 12:10, 13:11, 14:12}
    faceValues = {"J": 11, "Q": 12, "K": 13, "A": 14}
    suits = {"C": 0, "D": 1, "H": 2, "S": 3}
    cardWidth = 100
    cardHeight = 150
    
    def __init__(self, number, suit): #Initializes the Card class
        self.number = number
        self.suit = suit

    def __repr__(self):
        if self.number == 11:
            number = "J"
        elif self.number == 12:
            number = "Q"
        elif self.number == 13:
            number = "K"
        elif self.number == 14:
            number= "A"
        else:
            number = self.number
        return str(number) + self.suit
    def createCard(self):
        if self.number == 11:
            number = "J"
        elif self.number == 12:
            number = "Q"
        elif self.number == 13:
            number = "K"
        elif self.number == 14:
            number= "A"
        else:
            number = self.number
        return str(number) + self.suit

################################################################################
class Deck(): 
    def __init__(self): #Initializes the Deck class
        self.deck = []
        for suit in Card.suits: #Appends all possible 52 cards to Deck
            for number in Card.numbers:
                card = Card(number, suit).createCard()
                self.deck.append(card)
        self.onBoard = []

    def __repr__(self):
        return str(self.deck)

    def numCardsLeft(self):
        return len(self.deck)
    
    def shuffle(self): #Shuffles the deck randomly 
        random.shuffle(self.deck)

    def deal(self, numberOfCards, board = False):
        if len(self.deck) < numberOfCards:
            return False
        onBoard = []
        if board == True:
            for i in range(0, numberOfCards):
                onBoard.append(self.deck.pop(0))
            self.onBoard += onBoard
        else:
            for i in range(0, numberOfCards):
                onBoard.append(self.deck.pop(0))
            return onBoard
            

    def burn(self, numberOfCards):
        if len(self.deck) < numberOfCards:
            return None
        else: 
            for i in range(0, numberOfCards):
                self.deck.pop(i)

    def draw(self, canvas):
        pass

################################################################################
class Hand():
    scores = {"High Card": 1, "One Pair": 2, "Two Pair": 3, "3 Of A Kind": 4,
    "Straight": 5, "Flush": 6, "Full House": 7, "4 Of A Kind": 8,
    "Straight Flush": 9, "Royal Flush": 10}
    
    def __init__(self, currHand):
        self.currHand = currHand
        self.type = self.checkHand()

    def __repr__(self):
        return str(self.currHand)
        
    def checkHand(self):
        return self.isRoyalFlush()

    def isRoyalFlush(self):
        wantedSuit = self.currHand[0][-1]
        sortedHand = sorted(self.currHand)
        ranks = []
        for card in sortedHand:
            currSuit = card[-1]
            currRank = card[:-1]
            if currSuit != wantedSuit:
                return self.isStraightFlush()
            if currRank != str(10):
                ranks.append(currRank)
        if sorted(ranks) != sorted(["A", "K", "Q", "J"]):
            return self.isStraightFlush()
        else:
            if str(10) + wantedSuit in self.currHand:
                return (Hand.scores["Royal Flush"], "Royal Flush")


    def isStraightFlush(self):
        ranks = []
        for card in self.currHand:
            rank = card[:-1]
            if rank.isdigit():
                ranks.append(int(rank))
            else:
                ranks.append(Card.faceValues[rank])
        sortedHand = sorted(self.currHand)
        wantedSuit = sortedHand[0][-1]
        for i in range(len(ranks) - 1):
            currRank = ranks[i]
            nextRank = ranks[i + 1]
            currSuit = sortedHand[i][-1]
            if nextRank - currRank == 1 and currSuit == wantedSuit:
                continue
            else:
                return self.is4OfAKind()
        return (Hand.scores["Straight Flush"], "Straight Flush")


    def is4OfAKind(self):
        sortedHand = sorted(self.currHand)
        d = dict()
        for card in sortedHand:
            currRank = card[:-1]
            d[currRank] = d.get(currRank, 0) + 1
        for rank in d:
            if d[rank] == 4:
                return (Hand.scores["4 Of A Kind"], "4 Of A Kind")
        return self.isFullHouse()

    def isFullHouse(self):
        sortedHand = sorted(self.currHand)
        pair = False
        trio = False
        d = dict()
        for card in sortedHand:
            currRank = card[:-1]
            d[currRank] = d.get(currRank, 0) + 1
        for rank in d:
            if d[rank] == 3:
                trio = True
            if d[rank] == 2:
                pair = True
        if pair and trio:
            return (Hand.scores["Full House"], "Full House")
        else:
            return self.isFlush()

    def isFlush(self):
        wantedSuit = self.currHand[0][-1]
        for i in range(len(self.currHand)):
            currSuit = self.currHand[i][-1]
            if currSuit != wantedSuit:
                return self.isStraight()
        return (Hand.scores["Flush"], "Flush")

    def isStraight(self):
        ranks = []
        for card in self.currHand:
            rank = card[:-1]
            if rank.isdigit():
                ranks.append(int(rank))
            else:
                ranks.append(Card.faceValues[rank])
        for i in range(len(ranks) - 1):
            currRank = ranks[i]
            nextRank = ranks[i + 1]
            if nextRank - currRank != 1:
                return self.is3OfAKind()
        return (Hand.scores["Straight"], "Straight")

    def is3OfAKind(self):
        d = dict()
        for card in self.currHand:
            currRank = card[:-1]
            d[currRank] = d.get(currRank, 0) + 1
        for rank in d:
            if d[rank] == 3:
                return (Hand.scores["3 Of A Kind"], "3 Of A Kind")
        return self.isTwoPair()

    def isTwoPair(self):
        d = dict()
        for card in self.currHand:
            currRank = card[:-1]
            d[currRank] = d.get(currRank, 0) + 1
        if list(d.values()).count(2) == 2:
            return (Hand.scores["Two Pair"], "Two Pair")        
        return self.isOnePair()

    def isOnePair(self):
        d = dict()
        for card in self.currHand:
            currRank = card[:-1]
            d[currRank] = d.get(currRank, 0) + 1
        if list(d.values()).count(2) == 1:
            return (Hand.scores["One Pair"], "One Pair")
        return self.isHighCard()

    def isHighCard(self):
        return (Hand.scores["High Card"], "High Card")

    def handType(self):
        return self.type

    def intHand(self):
        final = []
        for card in self.currHand:
            rank = card[:-1]
            if rank in "23456789" or rank in "10":
                final.append(int(rank))
            else:
                if rank == "J":
                    final.append(Card.faceValues["J"])
                elif rank == "Q":
                    final.append(Card.faceValues["Q"])
                elif rank == "K":
                    final.append(Card.faceValues["K"])
                elif rank == "A":
                    final.append(Card.faceValues["A"])
        return final

################################################################################

def equalityChecker(hand1, hand2):
    if hand1.checkHand()[1] == "Royal Flush":
        return "split"
    if hand1.checkHand()[1] == "Straight Flush":
        int1 = sorted(hand1.intHand())
        int2 = sorted(hand2.intHand())
        while len(int1) > 0:
            if int1[-1] > int2[-1]:
                return hand1
            elif int1[-1] == int2[-1]:
                if len(int1) == 1:
                    return "split"
                int1.pop()
                int2.pop()
            else: 
                return hand2
    elif hand1.checkHand()[1] == "Flush":
        int1 = sorted(hand1.intHand())
        int2 = sorted(hand2.intHand())
        while len(int1) > 0:
            if int1[-1] > int2[-1]:
                return hand1
            elif int1[-1] == int2[-1]:
                if len(int1) == 1:
                    return "split"
                int1.pop()
                int2.pop()
            else: 
                return hand2
    elif hand1.checkHand()[1] == "4 Of A Kind":
        int1 = hand1.intHand()
        int2 = hand2.intHand()
        quad1 = 0
        quad2 = 0
        for num in int1:
            if int1.count(num) == 4:
                quad1 = num
                int1.remove(num)
                int1.remove(num)
                int1.remove(num)
                int1.remove(num)
        for num in int2:
            if int2.count(num) == 4:
                quad2 = num
                int2.remove(num)
                int2.remove(num)
                int2.remove(num)
                int2.remove(num)
        if quad1 > quad2:
            return hand1
        elif quad1 == quad2:
            if int1[0] > int2[0]:
                return hand1
            elif int1[0] == int2[0]:
                return "split"
            else:
                return hand2
        else:
            return hand2

    elif hand1.checkHand()[1] == "Full House":
        int1 = hand1.intHand()
        pair1 = 0
        triple1 = 0
        pair2 = 0
        triple2 = 0
        int2 = hand2.intHand()
        for rank in int1:
            if int1.count(rank) == 3:
                triple1 = rank
            if int1.count(rank) == 2:
                pair1 = rank
        for rank in int2:
            if int2.count(rank) == 3:
                triple2 = rank
            if int2.count(rank) == 2:
                pair2 = rank
        if triple1 > triple2:
            return hand1
        elif triple1 == triple2:
            if pair1 > pair2:
                return hand1
            if pair1 == pair2:
                return "split"
            else:
                return hand2
        else:
            return hand2
    elif hand1.checkHand()[1] == "Straight":
        int1 = sorted(hand1.intHand())
        int2 = sorted(hand2.intHand())
        while len(int1) > 0:
            if int1[-1] > int2[-1]:
                return hand1
            elif int1[-1] == int2[-1]:
                if len(int1) == 1:
                    return "split"
                int1.pop()
                int2.pop()
            else: 
                return hand2
    elif hand1.checkHand()[1] == "3 Of A Kind":
        int1 = sorted(hand1.intHand())
        int2 = sorted(hand2.intHand())
        triple1 = 0
        triple2 = 0
        for num in int1:
            if int1.count(num) == 3:
                triple1 = num
                int1.remove(num)
                int1.remove(num)
                int1.remove(num)
        for num in int2:
            if int2.count(num) == 3:
                triple2 = num
                int2.remove(num)
                int2.remove(num)
                int2.remove(num)
        if triple1 > triple2:
            return hand1
        elif triple1 == triple2:
            while len(int1) > 0:
                if int1[-1] > int2[-1]:
                    return hand1
                elif int1[-1] == int2[-1]:
                    if len(int1) == 1:
                        return "split"
                    int1.pop()
                    int2.pop()
                else: 
                    return hand2
        else:
            return hand2

    elif hand1.checkHand()[1] == "Two Pair":
        int1 = hand1.intHand()
        int2 = hand2.intHand()
        player1Pairs = []
        player2Pairs = []
        for num in int1:
            if int1.count(num) == 2:
                player1Pairs.append(num)
                int1.remove(num)
                int1.remove(num)
        for num in int2:
            if int2.count(num) == 2:
                player2Pairs.append(num)
                int2.remove(num)
                int2.remove(num)
        player1Pairs.sort()
        player2Pairs.sort()
        if player1Pairs[1] > player2Pairs[1]:
            return hand1
        elif player1Pairs[1] == player2Pairs[1]:
            if player1Pairs[0] > player2Pairs[0]:
                return hand1
            elif player1Pairs[0] == player2Pairs[0]:
                if int1[0] > int2[0]:
                    return hand1
                elif int1[0] == int2[0]:
                    return "split"
                else:
                    return hand2
            else:
                return hand2
        else:
            return hand2
                
    elif hand1.checkHand()[1] == "One Pair":
        int1 = sorted(hand1.intHand())
        int2 = sorted(hand2.intHand())
        for i in int1:
            if int1.count(i) == 2:
                pair1 = i
                break
        for j in int2:
            if int2.count(j) == 2:
                pair2 = j
                break
        if pair1 > pair2:
            return hand1
        elif pair1 == pair2:
            int1.remove(pair1)
            int1.remove(pair1)
            int2.remove(pair2)
            int2.remove(pair2)
            while len(int1) > 0:
                if int1[-1] > int2[-1]:
                    return hand1
                elif int1[-1] == int2[-1]:
                    if len(int1) == 1:
                        return "split"
                    int1.pop()
                    int2.pop()
                else: 
                    return hand2
        else:
            return hand2
    elif hand1.checkHand()[1] == "High Card":
        int1 = sorted(hand1.intHand())
        int2 = sorted(hand2.intHand())
        while len(int1) > 0:
            if int1[-1] > int2[-1]:
                return hand1
            elif int1[-1] == int2[-1]:
                if len(int1) == 1:
                    return "split"
                int1.pop()
                int2.pop()
            else: 
                return hand2