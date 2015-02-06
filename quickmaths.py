#!/usr/bin/python

########################################################################
#
#  QuickMaths.py, the rapid fire mental arithmetic quizzer
#
#  Copyright (C) 2015 Matthew Darby
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or (at
#  your option) any later version.
#
#  This program is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307,
#  USA.
#
########################################################################

import sys
from random import randint, choice
from math import sqrt
from time import time
## Formula stuff.

class Formula:
    """Base class for formulae"""
    def __init__(self):
        self.left = None
        self.right = None
        self.operation = None

    def value(self):
        return None

    def text(self):
        return ""

class NumberFormula(Formula):
    """Because we obviously need a wrapper around integers"""
    def __init__(self, value):
        super(NumberFormula, self).__init__()
        self.left = value

    def value(self):
        return self.left

    def text(self):
        return "{}".format(self.left)

class SumFormula(Formula):
    """One and one makes two, two and one makes three..."""
    def __init__(self, left, right):
        super(Formula, self).__init__()
        self.left = left
        self.right = right

    def value(self):
        return self.left.value() + self.right.value()

    def text(self):
        return "({} + {})".format(self.left.text(), self.right.text())

class DifferenceFormula(Formula):
    """We're not so different, you and I.'"""
    def __init__(self, left, right):
        super(Formula, self).__init__()
        self.left = left
        self.right = right

    def value(self):
        return self.left.value() - self.right.value()

    def text(self):
        return "({} - {})".format(self.left.text(), self.right.text())

class ProductFormula(Formula):
    """Go forth, and multiply!"""
    def __init__(self, left, right):
        super(Formula, self).__init__()
        self.left = left
        self.right = right

    def value(self):
        return self.left.value() * self.right.value()

    def text(self):
        return "({} * {})".format(self.left.text(), self.right.text())

class DivisionFormula(Formula):
    """Warning: Don't divide by zero!"""
    def __init__(self, left, right):
        super(Formula, self).__init__()
        self.left = left
        self.right = right

    def value(self):
        return self.left.value() // self.right.value()

    def text(self):
        return "({} / {})".format(self.left.text(), self.right.text())

## Quesiton stuff.

class Question:
    def __init__(self, formula):
        self.formula = formula

    def answer(self):
        return self.formula.value()

    def text(self):
        return self.formula.text()

class QuestionParameter:
    def __init__(self, formula, bottomValue, topValue):
        self.formula = formula
        self.bottomValue = bottomValue
        self.topValue = topValue

    def generateFormula(self):
        left = NumberFormula(randint(self.bottomValue, self.topValue))
        right = NumberFormula(randint(self.bottomValue, self.topValue))

        # Division is special, as we target a specific value instead
        if self.formula == DivisionFormula:
            target = randint(self.bottomValue, self.topValue)
            firstFactor = randint(2, int(sqrt(self.topValue)))
            secondFactor = randint(2, 8)
            left = NumberFormula(target * firstFactor * secondFactor)
            right = NumberFormula(firstFactor * secondFactor)

        aFormula = self.formula(left, right)
        return aFormula

class QuestionGenerator:
    def __init__(self, parameters):
        self.parameters = parameters

    def generate(self):
        """Pick a random parameter and generate a question"""
        aParameter = choice(self.parameters)
        aFormula = aParameter.generateFormula()
        aQuestion = Question(aFormula)
        return aQuestion

operationToFormula = {"sum": SumFormula,
                      "dif": DifferenceFormula,
                      "pro": ProductFormula,
                      "div": DivisionFormula}

def printUsage():
    progName = sys.argv[0]
    print("""Usage: {} - Print this usage information
       {} [operation] [lowRange] [highRange]""".format(progName, progName))

def checkArguments():
    aBottomValue = int(sys.argv[2])
    aTopValue = int(sys.argv[3])
    if aBottomValue >= aTopValue:
        print("The lower value of the range must be smaller than the higher value!")
        return False
    if sys.argv[1] not in operationToFormula.keys():
        print("Pick one of 'pro', 'dif', 'sum' or 'div'")
        return False
    return True

def beginGame():
    aFormulaClass = operationToFormula[sys.argv[1]]
    aBottomValue = int(sys.argv[2])
    aTopValue = int(sys.argv[3])
    aParameter = QuestionParameter(aFormulaClass, aBottomValue, aTopValue)
    aGenerator = QuestionGenerator([aParameter])
    myQuestion = aGenerator.generate()
    userString = ""
    totalAttempts = 0
    totalCorrect = 0
    averageTime = 0
    timeTaken = time()
    # This run loop is not my finest hour.
    while userString != "exit":
        print("{} > ".format(myQuestion.formula.text()), end='')

        userString = input()
        try:
            userAnswer = int(userString)
            if userAnswer == myQuestion.formula.value():
                print("Correct, next!")
                myQuestion = aGenerator.generate()
                timeTaken = time() - timeTaken
                averageTime = (averageTime * totalCorrect) + timeTaken
                totalCorrect += 1
                averageTime /= totalCorrect
                timeTaken = time()
            else:
                print("Incorrect, try again!")
            totalAttempts += 1

        except Exception as e:
            pass
    if totalAttempts == 0:
        pass
    else:
        print("Out of {} attempted answers, you got {}% right! On average, you took {} seconds to answer a question correctly.".format(totalAttempts,
                                                                                                                                       totalCorrect*100/totalAttempts,
                                                                                                                                       averageTime))


if __name__ == "__main__":
    if (len(sys.argv) == 1):
        printUsage()
    elif (len(sys.argv) == 4):
        if checkArguments():
            beginGame()
