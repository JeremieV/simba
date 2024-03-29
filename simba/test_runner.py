import simba.simba as simba
import simba.simplest_test_suite as st

## Running the Python tests ##

t = st.simple_tests
tests_done = 0
for i in range(len(t)):
    if (i % 2) == 0:
        res = simba.eval_str(t[i])
        # try:
        print(t[i], '=>', res)
        assert(res == t[i+1])
        # except:
        #     print(f"Error: {simba.print_sexp(t[i])} == {res} != {t[i+1]}")
        tests_done = tests_done + 1

print(f"{tests_done} tests successfully passed.")