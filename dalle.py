"""
dalle.py
Usage:
    from sd import make_image_from_headline
    make_image_from_headline("Sample Headline", "image.jpg")
"""
import os
from openai import OpenAI

# !!! MUST DO !!! 
# 'export OPENAI_API_KEY='<my api key from discord>'
# on whatever machine is running this code

"""
Creates the image associated with the headline and saves it to img.jpg
@param: 
headline: string representing a headline that we generate
"""
def make_image_from_headline(headline, no_api_call=False):
    if no_api_call:
        return "https://oaidalleapiprodscus.blob.core.windows.net/private/org-52ATyuOngjXAchaYE38n3Mtv/user-Ci6Pc5yVbUAlV7aqY1Avf8hK/img-9FFzbdKSJ5TAPDEiFGfLWqCA.png?st=2024-04-13T20%3A19%3A55Z&se=2024-04-13T22%3A19%3A55Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-04-13T12%3A09%3A09Z&ske=2024-04-14T12%3A09%3A09Z&sks=b&skv=2021-08-06&sig=6Htp3CqrjKz54j1cmu1be6f26hlkCjvKgBZjyYAx45o%3D"

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.images.generate(
            model="dall-e-3",
            prompt=headline,
            size="1024x1024",
            quality="standard",
            n=1,
           )
    return response.data[0].url

# run test script
if __name__ == "__main__":
    print(get_image_from_headline("A photograph of a white Siamese cat.", False))

