from DiceRollModule import *

def hitterTester(aHitter, input, expectedOutput, testName):
    print(testName)
    for i in range(0, 6):
        output = aHitter(input[i])
        if output != expectedOutput[i]:
            why = output
            fail = expectedOutput[i]
            raise Exception("failed " + testName)


#test hitter
testHitter = Hitter(3)
diceRolls = [1,2,3,4,5,6]
expectedOutput = [['fail'], ['fail'], ['success'], ['success'], ['success'], ['success']]
hitterTester(testHitter, diceRolls, expectedOutput, 'basic hitter test')

#test auto hit
testHitter = Hitter(3)
diceRolls = [1,2,3,4,5,6]
expectedOutput = [['success'], ['success'], ['success'], ['success'], ['success'], ['success']]
testHitter.myAutoSuccess = True
hitterTester(testHitter, diceRolls, expectedOutput, 'auto success test')

#test exploding 6s
testHitter = Hitter(3)
diceRolls = [1,2,3,4,5,6]
testHitter.myExplodingHits = [6,1]
expectedOutput = [['fail'], ['fail'], ['success'], ['success'], ['success'], ['success','success']]
hitterTester(testHitter, diceRolls, expectedOutput, 'exploding 6 hitter test')

#test exploding mortal wounds
testHitter = Hitter(3)
diceRolls = [1,2,3,4,5,6]
testHitter.myMortalWound = [6,1]
expectedOutput = [['fail'], ['fail'], ['success'], ['success'], ['success'], ['mortal','success']]
hitterTester(testHitter, diceRolls, expectedOutput, 'mortal wounds on 6 hitter test')

#test auto wounding
testHitter = Hitter(3)
diceRolls = [1,2,3,4,5,6]
testHitter.myAutoWound = 6
expectedOutput = [['fail'], ['fail'], ['success'], ['success'], ['success'], ['wound']]
hitterTester(testHitter, diceRolls, expectedOutput, 'auto wound on 6 hitter test')

#test positive hit modifiers
testHitter = Hitter(3)
diceRolls = [1,2,3,4,5,6]
testHitter.myDiceModifier = 1
expectedOutput = [['fail'], ['success'], ['success'], ['success'], ['success'], ['success']]
hitterTester(testHitter, diceRolls, expectedOutput, 'bonus to hit test')

testHitter = Hitter(3)
testHitter.myDiceModifier = -1
diceRolls = [1,2,3,4,5,6]
expectedOutput = [['fail'], ['fail'], ['fail'], ['success'], ['success'], ['success']]
hitterTester(testHitter, diceRolls, expectedOutput, 'negative to hit test')


