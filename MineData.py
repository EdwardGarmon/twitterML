import tweepy
import time
import json

config = json.load(open("./config.json"))

auth = tweepy.OAuthHandler(config["key"], config["secret"])
auth.set_access_token(config["access_token"], config["access_token_secret"])

api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

trainingJson = json.load(open("twitter_training.json"))

global users_gathered
users_gathered = 0

used_names = {}

def saveFriends(parent, username, max_depth):
    global users_gathered
    print(username, users_gathered)

    if users_gathered > max_depth:
        return

    try:
        data = {}

        user = api.get_user(username)
        activity = api.user_timeline(username)

        activities = []
        for tweet in activity:
            activities.append(tweet.text)
        data["bio"] = user.description
        data["activity"] = activities
        trainingJson["data"].append(data)

        users_gathered += 1
        used_names[username] = True

        with open('twitter_training.json', 'w') as outfile:
            json.dump(trainingJson, outfile)

        for f in user.friends():
            if f.screen_name != parent and f.screen_name not in used_names:
                saveFriends(username, f.screen_name, max_depth)

    except tweepy.error.TweepError:
        return



saveFriends("", "ChildrensPhila", 1000)

with open('twitter_training.json', 'w') as outfile:
    json.dump(trainingJson, outfile)
