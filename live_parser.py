"""Run this script for realtime data parsing & processing
"""

import json
from time import sleep
from crawler import Crawler
from notificator import notify
from selenium.common.exceptions import NoSuchElementException

driver = Crawler("https://www.myscore.com.ua/basketball/").getDriver()

while True:

    # checking whether there are any games in progress

    in_track = False

    while not in_track:
        try:

            name = driver.find_element_by_xpath(
                "//div[@id='live-table']//div[@class='event']//div[@class='event__header top']//div[@class='event__titleBox']//span").text
            home = driver.find_element_by_xpath(
                "//div[@id='live-table']//div[@class='event']//div[@class='event__match event__match--live event__match--twoLine']//div[@class='event__participant event__participant--home']").text
            guest = driver.find_element_by_xpath(
                "//div[@id='live-table']//div[@class='event']//div[@class='event__match event__match--live event__match--twoLine']//div[@class='event__participant event__participant--away']").text

            p1_home = int(driver.find_element_by_xpath(
                "//div[@id='live-table']//div[@class='event']//div[@class='event__match event__match--live event__match--twoLine']//div[@class='event__part event__part--home event__part--1']").text)
            p1_gst = int(driver.find_element_by_xpath(
                "//div[@id='live-table']//div[@class='event']//div[@class='event__match event__match--live event__match--twoLine']//div[@class='event__part event__part--away event__part--1']").text)

            print ("LOG: There is a game in progress. ({}: {} - {})".format(name, home, guest))

            in_track = True

        except NoSuchElementException as e:
            print ("LOG: No games in progress")
            sleep(10)
            continue

    # checking whether the game is suitable for the strategy

    with open('data.json') as json_file:
        data = list(json.load(json_file))

    is_suitable = False

    for cf in data:
        if cf['home'] == home and cf['guest'] == guest:
            if cf['cf_home'] <= 1.3 or cf['cf_guest'] <= 1.3:
                is_suitable = True
                cf_home = cf['cf_home']
                cf_guest = cf['cf_guest']

    if not is_suitable:
        print ("LOG: The game is not suitable")
        sleep(10)
        continue

    # waiting for the second time

    time2 = False

    while not time2:

        print ('LOG: Waiting for the second time')

        p1_home = int(driver.find_element_by_xpath(
            "//div[@id='live-table']//div[@class='event']//div[@class='event__match event__match--live event__match--twoLine']//div[@class='event__part event__part--home event__part--1']").text)
        p1_gst = int(driver.find_element_by_xpath(
            "//div[@id='live-table']//div[@class='event']//div[@class='event__match event__match--live event__match--twoLine']//div[@class='event__part event__part--away event__part--1']").text)

        try:
            p2_home = int(driver.find_element_by_xpath(
                "//div[@id='live-table']//div[@class='event']//div[@class='event__match event__match--live event__match--twoLine']//div[@class='event__part event__part--home event__part--2']").text)
            p2_gst = int(driver.find_element_by_xpath(
                "//div[@id='live-table']//div[@class='event']//div[@class='event__match event__match--live event__match--twoLine']//div[@class='event__part event__part--away event__part--2']").text)

            time2 = True

        except NoSuchElementException:
            pass

# super complex strategy

    print ('LOG: Cheking...')

    if cf_home < cf_guest:
        if p1_gst - p1_home >= 5:
            notify(name, home, guest, 'П1')
            print ("LOG: " + home + ' is about to win!')
    elif cf_guest < cf_home:
        if p1_home - p1_gst >= 5:
            notify(name, home, guest, 'П2')
            print ("LOG: " + guest + ' is about to win!')

    sleep(2100)
