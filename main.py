import random as rand
from math import ceil


# not working:
# attacks causing additional wounds

class DiceRoller:
    def __init__(self, maxValue):
        print("Dice roller created")
        self.myMaxValue = maxValue

    def __call__(self, diceToRoll=1):
        if diceToRoll == 1:
            return ceil(self.myMaxValue * rand.random())
        dice_results = []
        for i in range(0, diceToRoll):
            dice_results.append(ceil(self.myMaxValue * rand.random()))
        return dice_results


class SuccessObject:
    def __init__(self, successRoll):
        self.mySuccessRoll = successRoll
        self.myDiceModifier = 0
        self.myRerollType = 'none'
        self.myDiceReRoller = DiceRoller(6)
        self.myMortalWoundModified = 100
        self.myMortalWoundUnmodified = 100
        self.myExplodingHitsModified = []
        self.myExplodingHitsUnmodified = []
        print("Success object created")

    def _explodingDice(self, value):
        # This function handles cases where a success generates multiple successes, e.g. Death to the false emperor
        output = []
        for i in self.myExplodingHitsModified:  # A for loop is used because you can stack these modifiers
            if value + self.myDiceModifier >= i:
                output.append('success')
        for i in self.myExplodingHitsUnmodified:
            if value >= i:
                output.append('success')
        return output

    def _mortalWounds(self, value):
        # this function handles cases where a certain value generates additional hits in addition to its normal result
        output = []
        if value + self.myDiceModifier >= self.myMortalWoundModified:
            output.append('mortal')
        if value >= self.myMortalWoundUnmodified:
            output.append('mortal')
        return output

    def _applyReRoll(self, value):
        if self.myRerollType != 'none':
            # This is done so that you cant keep re rolling failed hits when the function calls itself
            newDiceRoll = self.myDiceReRoller()
            if (self.myRerollType == 'hits'):
                if newDiceRoll + self.myDiceModifier >= self.mySuccessRoll:
                    return newDiceRoll
            if (self.myRerollType == 'failedhits' and value < self.mySuccessRoll):
                if newDiceRoll >= self.mySuccessRoll:
                    return newDiceRoll
            if (self.myRerollType == 'ones' and value == 1):
                if newDiceRoll + self.myDiceModifier >= self.mySuccessRoll:
                    return newDiceRoll
    def _doISucceed(self, value):
        if value + self.myDiceModifier >= self.mySuccessRoll and value != 1:
            return ['success']
        else:
            return ['fail']


class Hitter(SuccessObject):
    def __init__(self, successRoll):
        super().__init__(successRoll)
        self.myAutoWoundModified = 100
        self.myAutoWoundUnmodified = 100
        self.myDestroyerMissile = False
        self.myAutoSuccess = False
        self.myAutoWoundModified = 100
        self.myAutoWoundUnmodified = 100

    def __call__(self, value):
        modifiedValue = value + self.myDiceModifier
        output = []
        if self.myAutoSuccess:
            output.append('success')
            return output
        if modifiedValue >= self.myAutoWoundModified:
            output.append('wound')
            return output
        output += self._explodingDice(value)
        output += self._mortalWounds(value)
        output += self._doISucceed(value)
        if output
        return output


aDiceRoller = DiceRoller(6)

diceOut = aDiceRoller(200000)
print(diceOut)
myHitter = Hitter(3)
myHitter.myExplodingHitsUnmodified = [6, 6]
#myHitter.myRerollType = 'hits'
suc = 0
fai = 0
for j in diceOut:
    a = myHitter(j)
    if 'success' in a:
        suc += len(a)
    else:
        fai += 1

print("failures: " + str(fai) + " successes: " + str(suc) + " success rate: " + str(100 * suc / 200000) + "%")
