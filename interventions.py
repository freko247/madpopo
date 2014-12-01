# -*- coding: utf-8 -*-
'''
    Generic framework for interventions

    Each bot tweets two original tweets about #hashtag
    Each bot retweets 10 first tweets about #hashtag
    Each bot retweets 50 tweets about #hashtag that do not originate from other
    bots
    Each bot favorites all tweets about #hashtag.

    Intervention schedule:
    Friday 14: #getyourflushot (did you get your flu-shot, I got mine!). link
    to this
    http://blogs.scientificamerican.com/symbiartic/2014/11/05/get-your-flu-shot
    or similar.
    Monday 17: #highfiveastranger Example“I high-fived a stranger today and it
    was awesome!” http://tech.mn/files/2012/06/High-Five.png
    Wednesday 19: #somethinggood. your bot just donated to #unicef to stop
    ebola. encourage others to help. Example tweet: "I just donated to support
    #unicef help kids in need. Why don't you spend $5 #somethinggood
    http://www.unicefusa.org"
    Friday 21: Missing
    Monday 24: Missing
    Wednesday 26: #turkeyface (Add someone’s (friend/celebrity) face to a
    turkey, see below)
    Thursday 27: #SFThanks (Thanksgiving). You’re thankful for living in
    San Fran
    Friday 28: #HowManyPushups. Example: “I just did 14 push ups! how many can
    you do?”
    Monday 1: Missing (maybe something christmas-related)

'''

from random import randrange
from time import sleep
from urllib2 import urlopen
import datetime

from log import logger
from tweets import updateStatus

INTERVENTION_SCHEDULE = [
    (datetime.date(2014, 11, 13),
     "I don't regret moving to SF #satisfied with life",
     'http://www.worldportsource.com/images/ports/USA/CA/SF_Market_Street.ss.jpg'
     ),
    (datetime.date(2014, 11, 14),
     'Just read earlier, http://www.cdc.gov/features/flu/, #getyourflushot',
     None),
    (datetime.date(2014, 11, 14),
     'Just got my shot, you go get it too! #getyourflushot',
     None),
    (datetime.date(2014, 11, 17),
     'Just read about #highfiveastranger, gonna try it out', None),
    (datetime.date(2014, 11, 17),
     'I did it, felt great! #highfiveastranger',
     None),
    (datetime.date(2014, 11, 19),
     'Stop the virus. #BandAid30 #somethinggood #unicef https://www.youtube.com/watch?v=-w7jyVHocTk',
     None),
    (datetime.date(2014, 11, 19),
     'You can also do #somethinggood, just gave donated to #unicef', None),
    (datetime.date(2014, 11, 21), '#HowManyPushups can I do? Let me try...', None),
    (datetime.date(2014, 11, 21), '31, a bit disappointing, can you beat me? #HowManyPushups', None),
    (datetime.date(2014, 11, 24),
     'Heard rumors about something weird going on in Golden gate park #GoldenGateAliens, did you see anything?',
     None),
    (datetime.date(2014, 11, 24),
     'Daleks in SF! #GoldenGateAliens #DrWho #Daleks', None),
    (datetime.date(2014, 11, 28),
     "I don't understand the thing with black friday, explain please! #blackfridaystories",
     None),
    (datetime.date(2014, 11, 28),
     "Black Friday isn't even in Friday anymore... http://www.sfgate.com/business/article/The-three-myths-of-Black-Friday-5920316.php",
     None),
    (datetime.date(2014, 12, 1), 'Are the rumours true is he here? #BanksySF', None),
    (datetime.date(2014, 12, 1), "Please someone, where's did you see his artwork? #BanksySF", None),
]


def main():
    logger.info('Started Intervention script')
    try:
        for date, tweet, media_url in INTERVENTION_SCHEDULE:
            if date == datetime.datetime.now().date():
                sleep_time = randrange(15)
                logger.info('Sleeping %s minutes before tweeting' % sleep_time)
                sleep(sleep_time * 60)
                if date == datetime.datetime.now().date():
                    params = {
                        'status': tweet,
                        'location': 'home'
                    }
                    if media_url:
                        image = urlopen(media_url)
                        params['media[]'] = image.read()
                    updateStatus(params)
    except Exception, err:
        logger.error('%s: %s' % (Exception, err))
    logger.info('Intervention script done')


if __name__ == '__main__':
    main()
