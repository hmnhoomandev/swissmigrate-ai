# test_env.py

#import os
#from dotenv import load_dotenv

#load_dotenv()

#print(os.getenv("OPENAI_API_KEY"))
#print(os.getenv("OPENAI_MODEL"))

#from config import OPENAI_API_KEY
#print(OPENAI_API_KEY)

#from openai import OpenAI
#from config import OPENAI_API_KEY

#client = OpenAI(api_key=OPENAI_API_KEY)

#response = client.chat.completions.create(
 #  model="gpt-4o-mini",
  # messages=[
   #   {"role": "user", "content": "Hello"}
   #]
#)

#print(response.choices[0].message.content)


# test_tesseract.py

import pytesseract

print(pytesseract.get_tesseract_version())

