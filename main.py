import twint
import schedule
import time
from datetime import datetime, timedelta
import csv
import os
import http.client, urllib

outputFileName = "output.csv"
lastParsedTweetTimeFileName = 'last_timestamp.txt'
timeFormat = '%Y-%m-%d %H:%M:%S'

# you can change the name of each "job" after "def" if you'd like.
def readLastTweetTime():
    currentTime = datetime.now().strftime(timeFormat)
    if os.path.exists(lastParsedTweetTimeFileName):
        with open(lastParsedTweetTimeFileName) as timeFile:
            timeStr = timeFile.readline().strip()
            if len(timeStr) <= 0:
                writeLastTweetTime(currentTime)
                exit()
            else:
                return timeStr
    else:
        writeLastTweetTime(currentTime)
        exit()

def writeLastTweetTime(time):
    timeFile = open(lastParsedTweetTimeFileName, "w")
    timeFile.write(time)
    timeFile.close()

def sendToPushover(token, userKey, localTimeZone, data):
    import pytz

    localTimeZone = pytz.timezone(localTimeZone)
    timeString = "{date} {time}".format(date = data['date'], time = data['time'])
    localizedTime = datetime.strptime(timeString, timeFormat).astimezone(localTimeZone).isoformat(' ', 'minutes')
    message = "Time:{datetime} \n\nTweet: {tweet} \n\nLink: {link}".format(datetime = localizedTime, tweet = data['tweet'], link = data['link'])
    
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
        "token": token,
        "user": userKey,
        "message": message,
    }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()

def jobone():
    pushoverToken = os.getenv('PUSHOVER_TOKEN')
    pushoverUserKey = os.getenv('PUSHOVER_USER_KEY')
    if (pushoverToken is None) or (pushoverUserKey is None):
        print("Pushover Token or User Key is missing")
        exit()
    twitterUsername = os.getenv('TWITTER_USERNAME')
    if (twitterUsername is None):
        print("TWITTER_USERNAME env variable is missing")
        exit()
    localTimeZone = os.getenv('TIMEZONE')
    if (localTimeZone is None):
        localTimeZone = 'US/Pacific'

    if os.path.exists(outputFileName):
        os.remove(outputFileName)
    lastTweetTime = readLastTweetTime()
    # Add one second so we don't keep getting the last tweet we already processed
    lastTweetTime = (datetime.strptime(lastTweetTime, timeFormat) + timedelta(seconds=1)).strftime(timeFormat)
    
    print ("Fetching Tweets")    
    c = twint.Config()
	# choose username (optional)
    c.Username = twitterUsername
    # choose beginning time (narrow results)
    c.Since = lastTweetTime
    # set limit on total tweets
    c.Limit = 100
    # no idea, but makes the csv format properly
    c.Store_csv = True
    # format of the csv
    c.Custom["tweet"] = ["id", "date", "time", "tweet", "link"]
    # change the name of the csv file
    c.Output = outputFileName
    twint.run.Search(c)

    if os.path.exists(outputFileName):
        with open(outputFileName, newline='') as csvfile:
            rows = csv.DictReader(csvfile, delimiter=',', quotechar='|')
            for index, data in enumerate(rows):
                if (index == 0):
                    writeLastTweetTime("{date} {time}".format(date = data["date"], time = data["time"]))
                
                sendToPushover(pushoverToken, pushoverUserKey, localTimeZone, data)

# run once when you start the program

jobone()

schedule.every(5).minutes.do(jobone)

while True:
  schedule.run_pending()
  time.sleep(1)