from ge import chromosome_to_floats, floats_to_chromosome


def test_chromosome_encoding():
    tests = [
        ((1.99, 1.04, 0.25), (2.00, 1.05, 0.26)),
        ((2.00, 1.05, 0.26), None),
        ((12.34, 5.67, 1.89), None),
        ((12.341234567, 5.671234567, 1.8911234567), (12.34, 5.67, 1.89)),
        ((18.00, 9.42, 2.37), None),
        ((18.01, 9.43, 2.38), (18.00, 9.42, 2.37)),
    ]

    for test, expected in tests:
        Kp, Ti, Td = test
        c = floats_to_chromosome(Kp, Ti, Td)

        result = chromosome_to_floats(c)
        if not expected:
            expected = test

        if result != expected:
            raise AssertionError(f"{result} != {expected}")


tests_functions = (
    test_chromosome_encoding,
)

if __name__ == '__main__':
    for function in tests_functions:
        function()
        print(f"{function.__name__}: OK")
