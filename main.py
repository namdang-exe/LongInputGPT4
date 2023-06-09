import openai
import os
import time

from helper import *

# Load API keys from .env file
from dotenv import load_dotenv

load_dotenv()

# Set up OpenAI API
api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = api_key

# Set up ChatGPT
model_engine = "text-davinci-003"
prompt = (
    "Please help me check if there is any malicious code:\n")
counter = 0
unprocess_counter = 0
working_path = r"D:\My Files\business\businexhtml-101\businex\src"

# Traverse folder and upload files to ChatGPT
for root, dirs, files in os.walk(working_path):
    for file in files:
        if ".js" in file:
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                code = f.read()
                if not more_than_3500_tokens(code):
                    # Get response from ChatGPT
                    response = None
                    retries = 0
                    error = False
                    while response is None and retries < 3:
                        try:
                            response = openai.Completion.create(
                                engine=model_engine,
                                prompt=prompt + code, max_tokens=500, n=1, stop=None, temperature=0.7)
                        except openai.error.OpenAIError as e:
                            error = True
                            print(f"Error: {e}")
                            retries += 1
                            time.sleep(5)

                        # Check if response was cut off
                        if error or response is not None and "..." in response.choices[0].text:
                            # Ask ChatGPT to continue from where it stopped
                            prompt = "Please continue from where you stopped:\n"
                            code = response.choices[0].text.split("...")[-1].strip()
                            response = None
                        else:
                            # Append response to log file
                            with open('response.txt', 'a') as f:
                                f.write(response.choices[0].text)
                                f.write('\n')

                        if retries == 3:
                            print("Maximum number of retries reached. Skipping file.")
                        time.sleep(5)
                        print(f'{counter} files processed!')
                        counter += 1
                        if counter % 20 == 0:
                            print("Sleeping for 1 minutes")
                            time.sleep(60)
                else:
                    # Append the unprocessed filepath to a file
                    with open('leftover.txt', 'a') as f:
                        f.write(f'File {unprocess_counter + 1} is: ')
                        f.write(filepath)
                        f.write('\n')
                    unprocess_counter += 1
