from DiceRollModule import *
from math import floor


class DamageObject:
    def __init__(self, type, damage=1, ap=0):
        self.myType = type
        self.myDamage = damage
        self.myAp = ap


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
        self.myBaseAp = 0
        self.myRending = []
        self.myExplodingWoundsModifed = []
        self.myMortalWoundsModified = []
        print("Wounder created")

        def __generateDamageObject(self, type, bonusAp=0, bonusDamage=0):
            output = []
            if type == 'mortal':
                output += [DamageObject('mortal')]*bonusDamage
            else:
                output.append(DamageObject(type, self.myBaseDamage+bonusDamage, self.myBaseAp+bonusAp))
            return output

        def __call__(self, value, hitType):
            output = []
            if hitType == 'mortal':
                output.append(DamageObject('mortal'))
                return output
            #exploding wounds
            #exploding mortals


aDiceRoller = DiceRoller(6)

diceOut = aDiceRoller(10)

myHitter = Hitter(3)
myHitter.myDiceModifier = 0
myHitter.myExplodingHitsUnmodified = [6, 6, 6]
myHitter.myMortalWoundUnmodified = 5
myHitter.myRerollType = 'hits'
suc = 0
fai = 0
for j in diceOut:
    a = myHitter(j)
    if 'success' in a:
        suc += len(a)
    else:
        fai += 1

print("failures: " + str(fai) + " successes: " + str(suc) + " success rate: " + str(100 * suc / 200000) + "%")
woundTest = Wounder(1, 4, 2)
