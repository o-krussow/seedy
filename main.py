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
from dalle import make_image_from_headline
#from nanoGPT import get_headline

"""returns the headline given from nanoGPT as a string
@param prompt is a string representing the prompt to nanoGPT"""
def get_headline(prompt=""):
    #--- IMPLEMENT ME ---#
    #nanoGPT.get_headline()
    # return a default value because we don't have this implemented yet
    #prompt is just "starter prompt"
    return prompt+" nobody In Entire Dodgers Organization Has Heart To Tell Ohtani What Going On With Interpreter"

def get_paragraph(headline, no_api_call = False):
    #uses gpt.py
    return get_text_from_headline(headline, no_api_call)

"""returns the base64 encoded image string
@param headline is a string representing the headline of the article"""
def get_image(headline, no_api_call = False):
    #uses dalle.py

    # create the image and return the url
    return make_image_from_headline(headline, no_api_call)


def main():
    """test functionality of main.py by running main.py alone"""
    headline = get_headline()

    data = {
                'headline': headline,
                'text': get_text_from_headline(headline, True),
                'image': get_image(headline, True),
            }

    with open("data.json", 'w') as json_file:
        json.dump(data, json_file)

if __name__ == "__main__":
    main()
    
