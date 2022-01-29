import xmltodict
import os
from discord_webhook import DiscordWebhook
from flask import Flask, request
from xml.parsers.expat import ExpatError
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
hookUrl=os.environ.get('HOOK_URL')

app = Flask(__name__)

@app.route("/feed", methods=["GET", "POST"])
def feed():

    challenge = request.args.get("hub.challenge")
    if challenge:
        return challenge

    try:
        xml_dict = xmltodict.parse(request.data)
        video_url = xml_dict["feed"]["entry"]["link"]["@href"]
        channel_name=xml_dict["feed"]["entry"]["author"]["name"]
        print("New video URL: {}".format(video_url))
        message = video_url
        webhook = DiscordWebhook(url=hookUrl, content=message, username=channel_name)
        response = webhook.execute()

    except (ExpatError, LookupError):
        return "", 403

    return "", 204

if __name__ == "__main__":
    app.run()