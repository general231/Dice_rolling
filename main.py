import random as rand
from math import ceil

class DiceRoller:
    def __init__(self):
        print("Dice roller created")
    def __call__(self, diceToRoll):
        diceResults = []
        for i in range(0,diceToRoll):
            diceResults.append(ceil(6*rand.random()))
        return diceResults

class HitObject:
    def __init__(self,type = "success"):
        allowableTypes = ['success', 'fail', 'wound','mortal']
        if type in allowableTypes:
            self.type = type
        else:
            print("Invalid wound type: " + type)
            raise ValueError
    def getType(self):
        return self.type

class SuccessObject:
    def __init__(self, successRoll):
        self.SuccessRoll = successRoll
        self.hitModifer = 0
        self.reRollType = 'none'
    def addHitModifier(self, value):
        self.hitModifier = value
    def addReRoll(self, reRollType):
        allowableTypes = ['none','ones', 'failed hits', 'hits']
        if reRollType in allowableTypes:
            self.reRollType = reRollType
        else:
            print("Illegal re roll specified: " + reRollType + "accepted values are: " + allowableTypes)
    def __call__(self, value):
        if value >= self.SuccessRoll:
            return HitObject('success')
        else:
            return HitObject('fail')




aDiceRoller = DiceRoller()
aHitter = Hitter(3)
diceOut = aDiceRoller(20)
print(diceOut)

for i in diceOut:
    print(aHitter(i).type)
