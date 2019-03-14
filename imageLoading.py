import os

#Takes care of managing the poker cards into a dictionary 
#for ease of access when creating images

################################################################################
def makeImageDict(path):
    d = dict()
    numbers = {2:0, 3:1, 4:2, 5:3, 6:4, 7:5, 8:6, 9:7, 10:8, 11:9, 12:10, 13:11, 14:12}
    for suit in ["d", "c", "s", "h"]:
        d[suit] = dict()
        for num in numbers:
            if num == 11:
                num = "j"
            elif num == 12:
                num = "q"
            elif num == 13:
                num = "k"
            elif num == 14:
                num = "a"
            d[suit][num] = None
    for image in os.listdir(path):
        if image == "back.gif" or image == "back2x.gif" or image == "black_joker.gif" or\
        image == "red_joker.gif" or image == "imagesTest.py" or image == "rotatedBack.gif":
            continue
        listImg = image.split("_")
        suit = listImg[2][0]
        if listImg[0][0].isdigit():
            if listImg[0] == "10":
                num = 10
            else:
                num = int(listImg[0][0])
        else:
            num = listImg[0][0]
        d[suit][num] = image
    return d


def imageLoader(hand, data):
    final = []
    for card in hand:
        num = 0
        suit = card[-1].lower()
        if card[:-1].isdigit():
            num = int(card[:-1])
        else:
            num = card[:-1].lower() 
        image = data.cardImages[suit][num]
        final.append(image)
    return final