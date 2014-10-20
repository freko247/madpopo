# -*- coding: utf-8 -*-
from random import randrange
import re
import urllib2

import BeautifulSoup

import db
from models import Status
from tweets import updateStatus


def main():
    base_url = 'http://knowyourmeme.com'
    myurl = "http://knowyourmeme.com/memes/people/gordon-ramsay/photos"
    links = []
    for link in re.findall(
            '''href=["'](.[^"']+)["']''', urllib2.urlopen(myurl).read(), re.I):
        if re.match('/photos/[0-9]', link):
            links.append(link)
    db.init_db()
    filtered_links = []
    for link in links:
        if not db.session.query(Status).filter(Status.text.like(link)).first():
            filtered_links.append(link)
    meme_link = filtered_links[randrange(len(filtered_links))]
    soup = BeautifulSoup.BeautifulSoup(urllib2.urlopen(base_url+meme_link))
    image_element = soup.findAll('img', {'class': 'centered_photo'})
    image_link = None
    for item in str(image_element)[6:-4].split():
        if item.startswith('src'):
            image_link = item[4:].strip('"')
    updateStatus('The @gordonramsay of today: ' + image_link, geo=True)

if __name__ == '__main__':
    main()
