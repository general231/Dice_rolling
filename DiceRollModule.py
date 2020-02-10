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
        self.myMortalWoundModified = 100
        self.myMortalWoundUnmodified = 100
        self.myExplodingHitsModified = []
        self.myExplodingHitsUnmodified = []
        print("Success object created")

    def _doesItExplode(self, value):
        # This function handles cases where a success generates multiple successes, e.g. Death to the false emperor
        output = []
        if value + self.myDiceModifier >= self.myExplodingHitsModified[0]:
            output.append(self.myExplodingHitsModified[1])
        if value >= self.myExplodingHitsUnmodified[0]:
            output.append(self.myExplodingHitsUnmodified[1])
        return output

    def _diceToNum(self, value):
        # This converts dice rolls D6, 3D6 etc and gives a integer number out
        if 'D' in value:
            if len(value) == 2:
                tempDiceRoller = DiceRoller(int(value[1]))
                return tempDiceRoller()
            else:
                temp = 0
                tempDiceRoller = DiceRoller(int(value[2]))
                for i in range(0, int(value[0])):
                    temp += tempDiceRoller
                return temp
        else:
            return int(value)

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
            if self.myRerollType == 'hits':
                if newDiceRoll + self.myDiceModifier >= self.mySuccessRoll:
                    return newDiceRoll
            if self.myRerollType == 'failedhits' and value < self.mySuccessRoll:
                if newDiceRoll >= self.mySuccessRoll:
                    return newDiceRoll
            if self.myRerollType == 'ones' and value == 1:
                if newDiceRoll + self.myDiceModifier >= self.mySuccessRoll:
                    return newDiceRoll
            return None

    def _doISucceed(self, value):
        if value + self.myDiceModifier >= self.mySuccessRoll and value != 1:
            return True
        else:
            return False


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
        output += ['success']*self.doesItExplode(value)
        output += self._mortalWounds(value)
        if self._doISucceed(value):
            output.append('success')
        else:
            newDice = self._applyReRoll(value)
            if newDice is not None:
                output += self.__call__(newDice)
        return output

