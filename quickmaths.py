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
    """Base class for formulae. How are you so basic?"""
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
        if left.value() < right.value():
            self.right = left
            self.left = right
        else:
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
        self.left = NumberFormula(left.value() * right.value())
        self.right = NumberFormula(right.value())

    def value(self):
        return self.left.value() // self.right.value()

    def text(self):
        return "({} / {})".format(self.left.text(), self.right.text())

## Quesiton stuff.

class Question:
    """42. Sorry, that's not right."""
    def __init__(self, formula):
        self.formula = formula

    def answer(self):
        return self.formula.value()

    def text(self):
        return self.formula.text()

class QuestionParameter:
    """Within expected parameters."""
    def __init__(self, formula, bottomValue, topValue):
        self.formula = formula
        self.bottomValue = bottomValue
        self.topValue = topValue

    def generateFormula(self):
        left = NumberFormula(randint(self.bottomValue, self.topValue))
        right = NumberFormula(randint(self.bottomValue, self.topValue))
        aFormula = self.formula(left, right)
        return aFormula

class QuestionGenerator:
    """The enemy is in our base!"""
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

def getParameters():
    aTotalArguments = len(sys.argv) - 1

    if aTotalArguments % 3 != 0:
        print("Enter your desired question formats in the form [operation] \
[lowerbound] [upperbound]")
        return False

    aParameterSettings = sys.argv[1:]
    aParameterSettings.reverse()
    aParameters = []
    while aParameterSettings:
        aFormula = aParameterSettings.pop()
        aBottomValue = int(aParameterSettings.pop())
        aTopValue = int(aParameterSettings.pop())
        if aBottomValue >= aTopValue:
            print("The lower value of the range must be smaller than the higher \
value!")
            return False
        if aFormula not in operationToFormula.keys():
            print("Pick one of 'pro', 'dif', 'sum' or 'div'")
            return False
        aFormulaClass = operationToFormula[aFormula]
        aParameters.append(QuestionParameter(aFormulaClass,
                                             aBottomValue,
                                             aTopValue))
    return aParameters

def runGame(questionParameters):
    aFormulaClass = operationToFormula[sys.argv[1]]
    aBottomValue = int(sys.argv[2])
    aTopValue = int(sys.argv[3])
    aGenerator = QuestionGenerator(questionParameters)
    myQuestion = aGenerator.generate()
    userString = ""
    totalQuestions = 1
    totalAttempts = 0
    totalCorrect = 0
    averageTime = 0
    timeTaken = time()
    # This run loop is not my finest hour.
    while userString != "exit":
        # Print the current question number + text
        print("{}) {} > ".format(totalQuestions,
                                 myQuestion.formula.text()),
              end='')

        # Grab user input
        try:
            userString = input()
        except EOFError as e:
            # In case the user things 'EOF' is the way out
            print('')
            break

        # Allow user to skip questions
        if userString == "skip":
            myQuestion = aGenerator.generate()
            totalQuestions += 1
            timeTaken = time()

        # If the user provided an integer, parse it and check it
        try:
            userAnswer = int(userString)
            if userAnswer == myQuestion.formula.value():
                print("Correct, next!")
                myQuestion = aGenerator.generate()
                timeTaken = time() - timeTaken
                averageTime = (averageTime * totalCorrect) + timeTaken
                totalCorrect += 1
                totalQuestions += 1
                averageTime /= totalCorrect
                timeTaken = time()
            else:
                print("Incorrect, try again!")
            totalAttempts += 1
        except Exception as e:
            pass

    # Alas, the game is over.
    if totalCorrect != 0:
        print("Out of {} attempted answers, you got {} ({:.2%}) right! \
\nOn average, you took {:.2} seconds \
to answer a question correctly.".format(totalAttempts,
                                        totalCorrect,
                                        totalCorrect/totalAttempts,
                                        averageTime))


if __name__ == "__main__":
    if (len(sys.argv) == 1):
        printUsage()
    else:
        aParameters = getParameters();
        if aParameters:
            runGame(aParameters)
