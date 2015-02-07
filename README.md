QuickMaths.py
===========
QuickMaths.py is a mental arithmetic question generator and quizzer.

Why?
====
The Internet has been down for a week and I only have my mobile Internet.

Seriously?
----------
Why else would you write something like this?

Usage
=====

    ./quickmaths.py [[operation] [lowerbound] [upperbound]]

where operation is one of:

    sum - Addition questions
    dif - Subtraction questions
    pro - Multiplication questions
    div - Division questions

and lowerbound/upperbound define the minimum and maximum values of the
operands to each question, except for division where they define the
minimum and maximum values of the denominator and answer.

You can specify a single configuration like this:

    ./quickmaths.py pro 1 12

The above would generate multiplication questions only. You can
specify multiple different configurations like this:

    ./quickmaths.py pro 1 12 sum 20 50

The above would generate multiplication questions and addition questions.
Composite questions (one or both operands being a question in itself) are not
yet supported.

    exit

will leave the game, and

    skip

will let you skip the current question.

Example
=======

    > ./quickmaths.py pro 1 12 sum 1 10
    1) (5 + 4) > 9
    Correct, next!
    2) (10 + 9) > 19
    Correct, next!
    3) (9 + 3) > 12
    Correct, next!
    4) (1 + 9) > 10
    Correct, next!
    5) (4 * 12) > 48
    Correct, next!
    6) (5 + 6) > 11
    Correct, next!
    7) (9 + 6) > 15
    Correct, next!
    8) (4 * 9) > skip
    9) (2 * 5) > 10
    Correct, next!
    10) (4 + 3) > exit
    Out of 8 attempted answers, you got 8 (100.00%) right!
    On average, you took 1.7 seconds to answer a question correctly.