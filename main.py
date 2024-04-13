"""
main.py
Interfaces with sd.py, gpt.py, and nanoGPT.
TODO:
    implement sd.py (CHASE)
        - either using a local stable diffusion build or
          the OPENAI_API_KEY that I have. See * for details

    finish nanoGPT (CHASE & DAVID [eventually])
        - whatever chase needs to do to get WORKING, not PERFECT headlines
        - I'll include sample calls, you all change it to what it needs to be

    finish website (DAVID [first priority])
        - finish up the HTML for the website

    link python backend to js frontend (OWEN)
        - I have, honestly, no idea what this looks like. 
        - this file will output everything to article.json
        - I believe in you :)

    *: run 'export OPENAI_API_KEY='<my api key from discord>'
       on whatever machine is running this code in order for the API calls to work.
"""
import json
import base64

from gpt import get_text_from_headline

#--- IMPLEMENT ME ---#
from sd import make_image_from_headline
#from nanoGPT import get_headline

def get_headline(prompt=""):
    #--- IMPLEMENT ME ---#
    #nanoGPT.get_headline()
    # return a default value because we don't have this implemented yet
    return prompt+" nobody In Entire Dodgers Organization Has Heart To Tell Ohtani What Going On With Interpreter"

def get_paragraph():
    return "FILLER PARAGRAPH"

def get_image():
    return "PRETEND THIS IS BASE64"

def main():
    # get the headline
    headline = get_headline()

    # create the image
    image_file_name = "image.jpg"
    #--- IMPLEMENT ME ---#
    make_image_from_headline(headline, image_file_name)

    with open(image_file_name, "rb") as image_file:
        image_data = image_file.read()

    encoded_image = base64.b64encode(image_data).decode("utf-8")

    data = {
                'headline': headline,
                # eventually, get rid of the True parameter to run the API call
                'text': get_text_from_headline(headline, True),
                'image': encoded_image
            }

    with open("data.json", 'w') as json_file:
        json.dump(data, json_file)

if __name__ == "__main__":
    main()
    

