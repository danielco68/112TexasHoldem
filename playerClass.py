
#Initiates Player class to create a player who can take part in a poker game

################################################################################
class Player():
    def __init__(self, playerID):
        self.playerID = playerID
        self.hand = []
        self.money = 2000
        self.fold = False
        self.smallBlind = False
        self.bigBlind = False
        self.alreadyPlayed = False

    def showHand(self):
        return self.hand

    def lost(self):
        if self.money <= 0:



            self.fold = True