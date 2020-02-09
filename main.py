import random as rand
from math import ceil


# not working:
# attacks causing additional wounds

class DiceRoller:
    def __init__(self, maxValue):
        print("Dice roller created")
        self.myMaxValue = maxValue

    def __call__(self, diceToRoll = 1):
        if diceToRoll == 1:
            return ceil(self.myMaxValue * rand.random())
        dice_results = []
        for i in range(0, diceToRoll):
            dice_results.append(ceil(self.myMaxValue * rand.random()))
        return dice_results


hitTypes = ['hit', 'miss', 'wound', 'mortal']
hitTypesEnum = enumerate(hitTypes)
woundTypes = ['wound', 'fail', 'mortal']


class SuccessObject:
    def __init__(self, successRoll):
        self.__mySuccessRoll = successRoll
        self.myHitModifier = 0
        self.myRerollType = 'none'
        self.myDiceReRoller = DiceRoller(6)
        self.myAutoWoundModified = 100
        self.myAutoWoundUnmodified = 100
        self.myMortalWoundModified = 100
        self.myMortalWoundUnmodified = 100
        self.myExplodingHitsModified = []
        self.myExplodingHitsUnmodified = []
        self.myDestroyerMissile = False
        self.myAutoHit = False

    def __call__(self, value):
        unModifiedValue = value
        modifiedValue = value + self.myHitModifier
        output = []
        if self.myAutoHit == True:
            output.append('success')
            return output
        if modifiedValue >= self.__mySuccessRoll and value != 1:
            if modifiedValue >= self.myAutoWoundModified:
                output.append('wound')
                return output
            if unModifiedValue >= self.myAutoWoundUnmodified:
                output.append('wound')
            if modifiedValue >= self.myMortalWoundModified:
                output.append('mortal')
            if unModifiedValue >= self.myMortalWoundUnmodified:
                output.append('mortal')
            if self.myDestroyerMissile:  # Effects which do D3 mortal wounds on hit, e.g. tau destroyer missiles
                num_mortal_wounds = ceil(self.myDiceReRoller() / 2)  # convert from D6 to D3
                output += (['mortal'] * num_mortal_wounds)
            for i in self.myExplodingHitsModified:
                if modifiedValue >= i:
                    output.append('success')
            for i in self.myExplodingHitsUnmodified:
                if unModifiedValue >= i:
                    output.append('success')
            output.append('success')  # this is the success for passing the roll
        else:
            print(value)
            if self.myRerollType != 'none':
                # This is done so that you cant keep re rolling failed hits when the function calls itself
                newDiceRoll = self.myDiceReRoller()
                if (self.myRerollType == 'hits'):
                    if newDiceRoll + self.myHitModifier >= self.__mySuccessRoll:
                        output += self.__call__(newDiceRoll)
                if (self.myRerollType == 'failedhits'):
                    if newDiceRoll >= self.__mySuccessRoll:
                        output += self.__call__(newDiceRoll)
                if (self.myRerollType == 'ones' and value == 1):
                    if newDiceRoll + self.myHitModifier >= self.__mySuccessRoll:
                        output += self.__call__(newDiceRoll)
            else:
                output.append('fail')
        return output


aDiceRoller = DiceRoller(6)

diceOut = aDiceRoller(200000)
print(diceOut)
myHitter = SuccessObject(3)
#myHitter.myExplodingHitsUnmodified = [6, 6]
myHitter.myRerollType = 'hits'
suc = 0
fai = 0
for j in diceOut:
    if myHitter(j) == ['success']:
        suc += 1
    else:
        fai += 1

print("failures: " + str(fai) + " successes: " + str(suc) + " success rate: " + str(100*suc/200000) + "%")
