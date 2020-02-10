from DiceRollModule import *





aDiceRoller = DiceRoller(6)

diceOut = aDiceRoller(200000)

myHitter = Hitter(3)
myHitter.myDiceModifier = -1
#myHitter.myExplodingHits = [6]
#myHitter.myMortalWoundUnmodified = 5
myHitter.myRerollType = 'ones'
suc = 0
fai = 0
for j in diceOut:
    a = myHitter(j)
    print(a)
    if 'success' in a:
        suc += len(a)
    else:
        fai += 1

print("failures: " + str(fai) + " successes: " + str(suc) + " success rate: " + str(100 * suc / 200000) + "%")
