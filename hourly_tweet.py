import tweepy
from datetime import datetime, timezone
import launch
import requests
import os


'''
Configures Tweepy and returns an api object.

args:
    n/a

return:
    api - API object for tweepy
'''
def config():
    CKEY = ''
    CSEC = ''
    ATOK = ''
    ATSE = ''

    auth = tweepy.OAuthHandler(CKEY, CSEC)
    auth.set_access_token(ATOK, ATSE)
    api = tweepy.API(auth)

    return api

'''
Will post a tweet to the maintime line.

args:
    body - The body of the tweet to be published

return:
    n/a
'''
def post(body, img_url):
    api = config()
    filename = 'temp.jpg'
    request = requests.get(img_url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)

        api.update_with_media(filename, status=body)
        os.remove(filename)
    else:
        print("Unable to download image")
    print('Post made successfully!')


'''
Returns true if there is less than 1 hour until the next launch.

args:
    n/a

return:
    boolean - True if there is less than 1 hour until the next launch.
'''
def less_than_1_hour():
    l = launch.Launch()
    now = datetime.now(timezone.utc)
    launch_time = l.launch_dt_obj
    dif = (launch_time-now).total_seconds()
    hours = (dif//3600)
    if (hours != 0):
        print('%s Query successful, conditions not met. No post was made.'% (timestamp()))
        return False
    return True

'''
Converts the current time to UTC and then returns it as a string.

args:
    n/a

return:
    string - current time in UTC as a string
'''
def timestamp():
    return (str(datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")) + ':')

if __name__ == "__main__":
    if less_than_1_hour():
        l = launch.Launch()
        post(('\U0001F680 LAUNCH NOTICE! \U0001F680 We are currently tracking %s. This mission is scheduled to launch on %s. Be sure to follow along with us at https://www.nextlaunch.info/.' % (l.mission, l.launch_time_date)), l.img_url)
