import logging
import random

user_input = "2 + 2"

# Test 1 - prohibited eval()
result = eval(user_input)

# Test 2 - prohibited exec()
exec("print('Semgrep policy test')")

# Test 3 - credential exposure in logs
logging.info("password = test-password")

# Test 4 - insecure random for a security-sensitive value
token = random.choice(["token1", "token2", "token3"])
