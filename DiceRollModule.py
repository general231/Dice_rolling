import random as rand
from math import ceil
from math import floor


# not working:
# attacks causing additional wounds

class DiceRoller:
    def __init__(self, maxValue):
        self.myMaxValue = maxValue

    def __call__(self, diceToRoll=1):
        if diceToRoll == 1:
            return ceil(self.myMaxValue * rand.random())
        dice_results = []
        for i in range(0, diceToRoll):
            dice_results.append(ceil(self.myMaxValue * rand.random()))
        return dice_results


class DamageObject:
    def __init__(self, type, damage=1, ap=0):
        self.myType = type
        self.myDamage = damage
        self.myAp = ap


class SuccessObject:
    def __init__(self, successRoll):
        self.mySuccessRoll = successRoll
        self.myDiceModifier = 0
        self.myRerollType = 'none'
        print("Success object created")

    def _doesItExplode(self, diceValue, diceRequirment, isModified, bonusValue):
        # This function is a generic function to be called when a bonus occurs on a specific value, e.g. exploding 6s
       if isModified:
           diceValue = diceValue - self.myDiceModifier
       if diceValue >= diceRequirment:
           return bonusValue
       return 0

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

    def _applyReRoll(self, value):
        if self.myRerollType != 'none':
            # This is done so that you cant keep re rolling failed hits when the function calls itself
            tempDiceRoller = DiceRoller(6)
            newDiceRoll = tempDiceRoller()
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
        if value + self.myDiceModifier >= self.mySuccessRoll and not value <= 1:
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
        self.myAutoWound = 100
        self.myAutoWoundIsModified = False
        self.myMortalWound = []
        self.myMortalWoundIsModified = False
        self.myExplodingHits = []
        self.myExplodingHitsIsModified = False

    def __call__(self, value):
        # this function returns an array of strings, possible results are 'fail', 'success', 'mortal or 'wound' depending
        # on the dice roll, an array is returned because you can generate more hits then dice in
        modifiedValue = value + self.myDiceModifier
        output = []
        if self.myAutoSuccess:
            output.append('success')
            return output
        if modifiedValue >= self.myAutoWoundModified:
            output.append('wound')
            return output
        if len(self.myExplodingHits) != 0:
            output += ['success']*self._doesItExplode(value, self.myExplodingHits[0],
                                                        self.myExplodingHitsIsModified, self.myExplodingHits[1])
        if len(self.myMortalWound) != 0:
            output += ['success'] * self._doesItExplode(value, self.myMortalWound[0],
                                                        self.myExplodingHitsIsModified, self.myMortalWound[1])
        if self._doISucceed(value):
            output.append('success')
        else:
            newDice = self._applyReRoll(value)
            if newDice is not None:
                output += self.__call__(newDice)
            else:
                output.append('fail')
        return output


class Wounder(SuccessObject):
    def __init__(self, strength, toughness, baseDamage, baseAp):
        if strength == toughness:
            successRoll = 4
        elif floor(strength / 2) >= toughness:
            successRoll = 2
        elif strength > toughness:
            successRoll = 3
        elif floor(toughness / 2) >= strength:
            successRoll = 6
        else:
            successRoll = 5
        super().__init__(successRoll)
        self.myStrength = strength
        self.myToughness = toughness
        self.myBaseDamage = baseDamage
        self.myBaseAp = baseAp
        self.myExplodingWounds = []
        self.myExplodingWoundsIsModified = False
        self.myRending = []
        self.myRendingIsModified = False
        self.myExplodingDamage = []
        self.myExplodingDamageIsModified = False
        self.myMortalWounds = []
        self.myMortalWoundsIsModified = False
        print("Wounder created")

    def __generateDamageObject(self, type, bonusDamage=0, bonusAp=0):
        output = []
        if type == 'mortal':
            output += [DamageObject('mortal')]*bonusDamage
        else:
            output.append(DamageObject(type, self.myBaseDamage+bonusDamage, self.myBaseAp+bonusAp))
        return output

    def __call__(self, diceValue, hitType):
        output = []
        if hitType == 'mortal':
            output += self.__generateDamageObject('mortal')
            return output
        if hitType == 'wound':
            output += self.__generateDamageObject('normal')
            return output
        if len(self.myRending) != 0:
            output += self.__generateDamageObject('normal', self.myBaseDamage, self._doesItExplode(diceValue,
                                                       self.myRending[0], self.myRendingIsModified, self.myRending[1]))
            return output
        if len(self.myExplodingDamage) != 0:
            bonusDamage = self._diceToNum(self._doesItExplode(diceValue, self.myExplodingDamage[0],
                                                       self.myExplodingDamageIsModified, self.myExplodingDamage[1]))
            output += self.__generateDamageObject('normal', self.myBaseDamage + bonusDamage)
            return output
        if len(self.myMortalWounds) != 0:
            numMortalWounds = self._diceToNum(self._doesItExplode(diceValue, self.myMortalWounds[0],
                                                       self.myMortalWoundsIsModified, self.myMortalWounds[1]))
            output += self.__generateDamageObject('mortal', numMortalWounds)
        if len(self.myExplodingWounds) != 0:
            output +=  self.__generateDamageObject('normal') * self._doesItExplode(diceValue, self.myExplodingWounds[0],
                                                        self.myExplodingWoundsIsModified, self.myExplodingWounds[1])
        if self._doISucceed(diceValue):
            output += self.__generateDamageObject('normal')
        else:
            newDice = self._applyReRoll(diceValue)
            if newDice is not None:
                output += self.__call__(newDice)
        return output


