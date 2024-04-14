"""
gpt.py
Usage: 
    from gpt import get_text_from_headline
    body_text = get_text_from_headline(headline)
    
    !! IF you want to run a test (no api call so it's free):

    body_text = get_text_from_headline('', no_api_call = True)

    ^ this will return some sample body about the Dodgers interpreter ^
"""
import os
from openai import OpenAI

# !!! MUST DO !!! 
# 'export OPENAI_API_KEY='<my api key from discord>'
# on whatever machine is running this code

"""
@param: 
headline: string representing a headline that we generate
no_api_call: default False, set to True if you want to use a default value (for testing)
"""
def get_text_from_headline(headline, no_api_call = False):
    # if we don't want to make a call to the api
    if no_api_call:
        # return a default value
        return "LOS ANGELES—Admitting that they were all just too embarrassed to come out and say it, sources confirmed Wednesday that nobody in the entire Dodgers organization has the heart to tell Shohei Ohtani what’s going on with his interpreter. “It’s gotten to the point where we all just kind of look at each other and hope someone else will deal with it,” said manager Dave Roberts, adding that Ohtani has been showing up to games and press conferences with a man who is clearly not his interpreter but instead just someone he met on the street. “We know it’s not our place to tell him, but it’s getting more and more awkward every day. We’re all just hoping he figures it out on his own.”"
    else:
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        chat = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": f"One paragraph The Onion article body text only from headline {headline}. Make sure it's funny!"
                    }
                ],
                max_tokens=250,
                temperature=.7,
                n=1,
                stop=None,
                model="gpt-3.5-turbo"
               )
        return chat.choices[0].message.content.strip()

# run test script
if __name__ == "__main__":
    print(get_text_from_headline("", True))

