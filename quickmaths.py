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
        return self.left.value() / self.right.value()

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
        aFormula = self.formula(left ,right)
        return aFormula

class QuestionGenerator:
    def __init__(self, parameters):
        self.parameters = parameters

    def generate(self):
        """Pick a random parameter and generate a question from it"""
        aParameter = choice(self.parameters)
        aFormula = aParameter.generateFormula()
        aQuestion = Question(aFormula)
        return aQuestion

if __name__ == "__main__":
    aParameter = QuestionParameter(SumFormula, 5, 10)
    aGenerator = QuestionGenerator([aParameter])
    myQuestion = aGenerator.generate()
    print(myQuestion.formula.text() + " = " + str(myQuestion.formula.value()))
