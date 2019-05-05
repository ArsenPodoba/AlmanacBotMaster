from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Crawler:
    """Use this class to get data from certain url
    """

    def __init__(self, url):

        self.chromedriver = "/home/alex/code/hackathon/chromedriver"
        self.options = Options()
        self.options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(executable_path=self.chromedriver,
                                       chrome_options=self.options)
        self.url = url

        self.driver.get(url)

    def getDriver(self):

        return self.driver
