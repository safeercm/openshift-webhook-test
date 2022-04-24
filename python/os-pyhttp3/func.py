from parliament import Context
import os
import requests

def sendToTelegram(message,chat_id,bot_token):
    url="https://api.telegram.org/bot" + bot_token + "/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "MarkdownV2"
        }
    try:
        response = requests.post(url,data)
        if response.status_code == 200:
            return True,"success"
        else:
            print(response)
            return False, response.reason
    except Exception as e:
        print(e)
        return False, e

def main(context: Context):
    """
    Function template
    The context parameter contains the Flask request object and any
    CloudEvent received with the request.
    """
    chat_id=os.environ['CHAT_ID']
    bot_token=os.environ['BOT_TOKEN']
    if context['request'].method == "GET":
        return { "message": "Webhook is up" }, 200
    elif context['request'].method == "POST":
        data = context['request'].json
        repo_fullname = data['repository']['full_name']
        url = data['repository']['html_url']
        pusher = data['pusher']['name']
        head_commit_msg = data['head_commit']['message']
        msg = "Git push to [" + repo_fullname + "](" + url + ")\nBy [" + pusher + "(https://github.com/" + pusher + ")\nLast commit message: " + head_commit_msg
        print(msg)
        msg_status,msg_err = sendToTelegram(msg, chat_id,bot_token)
        if msg_status == True:
            return { "message": context['request'].json }, 200
        else:
            return { "message": "Failed to process the payload" + str(msg_err) + msg}, 500
    else:
        return { "message": "Method not allowed" }, 405
