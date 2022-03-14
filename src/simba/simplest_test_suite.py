#! python3
"""
This is the only Python test file. For testing the really basic features. 
All the other tests will be written in Simba.
"""

simple_tests = [
    # literals
    "()", None,
    # "(a: 1, b: 2)", None,
    "nil", None,
    "true", True,
    "false", False,
    "\"Some string\"", "Some string",
    "", None,
    "0", 0,
    "1", 1,
    "-3", -3,
    "1.2000000000000008376", 1.2000000000000008, # Python rounding up floats

    # arithmetic
    "(+ 123 321)", 444,
    "(* 123 321)", 39483,
    "(- 123 321)", -198,
    "(- 3)", -3,
    "(- -3)", 3,
    "(- 23 4 34 5)", -20,
    "(+ 123 (- 45) 653 3 (* 543663 736623))", 400474670783,
    "(+ (- 53763 367354 (* 536 73823 929) (+ 373 3880 3)) 9 0)", -36760037750,

    # special forms
    "(if true 1 0)", 1,
    "(if false 1 0)", 0,
    "(def a 3)", None,
    "(do 1 2 3)", 3,
    "(do (def a 5) a)", 5, # asserts that the intermediate exprs are evaluated

    "(def a 5) (let [b (+ a 2)] (let [a 1] b))", 7,

    # closures
    """
    (def a 5)
    (def f (fn [] (+ a 5)))
    (def a 10)
    (f)
    """, 15,
    """
    (def a 5)
    (def f (fn [] (+ a 5)))
    (def a 10)
    (let [a 20]
        (f))
    """, 15,

    # interop
]
