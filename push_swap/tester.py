import subprocess
import unittest
import random
from itertools import permutations

PUSH_SWAP_PATH = "../../push_swap"
CHECKER_PATH = "../../checker_linux"
RED = "\033[31m"
GREEN = "\033[32m"
END_COLOR = "\033[0m"

def check_result(func):
    def wrapper(*args, **kwarg):
        result = exec_checker(*args)
        print(*args)
        if (result == "OK"):
            print(GREEN + result + END_COLOR)
        else:
            print(RED + result + END_COLOR)
        print()
        return func(*args, **kwarg)
    return wrapper

def exec_exe(*args, path=PUSH_SWAP_PATH):
    call_args = []
    call_args.append(path)
    call_args.extend(args)
    call_result = subprocess.run(call_args, capture_output=True, text=True)
    call_stdout = call_result.stdout.splitlines(True)
    call_stderr = call_result.stderr
    if call_stdout == '':
        call_stdout = None
    if call_stderr == '':
        call_stderr = None
    result = {
        "stdout": call_stdout,
        "stderr": call_stderr,
	}
    return result

def exec_checker(*args):
    push_swap = subprocess.Popen([PUSH_SWAP_PATH, *args], stdout=subprocess.PIPE)
    checker = subprocess.Popen(
        [CHECKER_PATH, *args],
        stdin=push_swap.stdout,
        text=True,
        stdout=subprocess.PIPE,
        )
    byte_string = checker.stdout.read().encode(encoding="ascii")
    checker_result = byte_string.decode("ascii").strip()
    push_swap.kill()
    checker.kill()
    return checker_result

def num_to_string(iterable: list):
    strings = []
    for item in iterable:
        strings.append(str(item))
    return strings

class TestFirstArg(unittest.TestCase):
    
    def test_single_string(self):
        self.assertEqual('Error\n', exec_exe("a").get("stderr"))
    
    def test_single_num(self):
        self.assertIsNone(exec_exe("1").get("stderr"))
        
    def test_single_empty(self):
        self.assertIsNone(exec_exe("").get("stderr"))
    
    def test_single_big(self):
        self.assertEqual('Error\n', exec_exe("11111111111").get("stderr"))
    
    def test_single_min(self):
        self.assertEqual('Error\n', exec_exe("-").get("stderr"))
    
    def test_single_plus(self):
        self.assertEqual('Error\n', exec_exe("+").get("stderr"))
    
    def test_single_zero(self):
        self.assertIsNone(exec_exe("0").get("stderr"))
    
    def test_single_min_zero(self):
        self.assertEqual("Error\n", exec_exe("-0").get("stderr"))
    
    def test_single_plus_zero(self):
        self.assertEqual('Error\n', exec_exe("+0").get("stderr"))
    
    def test_single_plus_zero_space(self):
        self.assertEqual('Error\n', exec_exe("+ 0").get("stderr"))
 
class TestMixedArgs(unittest.TestCase):
    
    def test_invalid_mixed(self):
        mixed_tests = [
            ["-0", "0"],
            ["11111111111111", "1"],
            ["30000000000"],
            ["5", "2", "-0"],
            ["5", "1", "3", "5"],
            ["5", "1", "-0", "5"],
            ["5", "-0", "4", "5"],
            ["1", "-31", "2147483648"],
            ["2147483647", "2147483648"],
            ["3", "@", "5"],
            ["-5+3", "2"],
            ["-5-3", "2"],
            ["@$!$%!%", "dog"],
            ["0", "0"],
            ["----------"],
            ["1351", "------", "5"],
            ["--1"],
		]
        for test in mixed_tests:
            joined = " ".join(test)
            self.assertEqual("Error\n", exec_exe(*test).get("stderr"))
            self.assertEqual("Error\n", exec_exe(joined).get("stderr"))
            self.assertEqual(1,
                             exec_exe(*test).
                             get("stderr").
                             count("Error\n")
                             )
            
    def	test_valid_mixed(self):
        mixed_tests = [
            ["-5", "5"],
            ["0", "-1"],
            ["2147483647", "-2147483648"],
		]
        for test in mixed_tests:
            self.assertIsNone(exec_exe(*test).get("stderr"))

class TestNumbers(unittest.TestCase):
    
    def test_three(self):
        perms = permutations(range(1, 4), 3)
        for perm in perms:
            result = exec_exe(*num_to_string(perm)).get("stdout")
            self.assertTrue(result == None or len(result) <= 3)
    
    def test_five(self):
        perms = permutations(range(1, 6), 5)
        for perm in perms:
            result = exec_exe(*num_to_string(perm)).get("stdout")
            self.assertTrue(result == None or len(result) <= 12)
            
    def test_hundred(self):
        tests = []
        for _ in range(100):
            tests.append(random.sample(range(-10000, 10000), 100))
        for test in tests:
            result = exec_exe(*num_to_string(test)).get("stdout")
            self.assertTrue(result == None or len(result) <= 700)
    
    def test_five_hundred(self):
        tests = []
        for _ in range(100):
            tests.append(random.sample(range(-10000, 10000), 500))
        for test in tests:
            result = exec_exe(*num_to_string(test)).get("stdout")
            self.assertTrue(result == None or len(result) <= 5500)

if __name__ == '__main__':
    unittest.main()
