"""Run this script for realtime updating of coeficcients database
"""

import json
from time import sleep
from crawler import Crawler
from selenium.common.exceptions import NoSuchElementException

driver = Crawler("https://www.myscore.com.ua/basketball/").getDriver()

# choose the 'coefficient' tab

sleep(0.5)
button = driver.find_element_by_xpath("//div[@class='tabs']//ul//li[5]//a")
driver.execute_script("arguments[0].click();", button)

# updating loop

while True:

    try:

        # loading previous data

        with open('data.json') as json_file:
            data = list(json.load(json_file))

        # updating the data

        next_home = driver.find_element_by_xpath(
            "//div[@id='live-table']//div[@class='event__participant event__participant--home']").text
        next_guest = driver.find_element_by_xpath(
            "//div[@id='live-table']//div[@class='event__participant event__participant--away']").text
        cf_home = driver.find_element_by_xpath(
            "//div[@class='odds__odd icon icon--arrow kx o_1 null null   ']//span").text
        cf_guest = driver.find_element_by_xpath(
                "//div[@class='odds__odd icon icon--arrow kx o_2 last null null   ']//span").text

        new_data = {'home': next_home, 'guest': next_guest, 'cf_home': cf_home, 'cf_guest': cf_guest}

        if new_data not in data:
            data.append(new_data)
            print ("PREPARSER_LOG: New data has been added to the preparsing database")
            with open('data.json', 'w') as outfile:
                json.dump(data, outfile)

    except NoSuchElementException:
        pass
