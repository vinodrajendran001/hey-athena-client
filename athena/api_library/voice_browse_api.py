"""
Tools to automate browsing (requires Firefox)
"""
try:
    from urllib.parse import quote_plus  # Python 3
except ImportError:
    from urllib import quote_plus        # Python 2

import os
import traceback

from sys import platform as _platform
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from athena.classes.api import Api
from athena import settings

GOOGLE_URL = 'https://www.google.com/search?gs_ivs=1&q='

OS_KEY = Keys.CONTROL
if _platform == "darwin":
    OS_KEY = Keys.COMMAND
NW_TAB = OS_KEY+'n'
CL_TAB = OS_KEY+'w'
SW_TAB = OS_KEY+Keys.TAB


class VoiceBrowseApi(Api):

    def __init__(self):
        self.key = 'voice_browse_api'
        self.driver = None

    def open(self, url=None, new_tab=False):
        if not self.driver:
            try:
                # print(settings.CHROME_DRIVER)
                # print(os.path.isfile(settings.CHROME_DRIVER))
                if not os.path.isfile(settings.CHROME_DRIVER):
                    raise Exception
                self.driver = webdriver.Chrome(settings.CHROME_DRIVER)
            except:
                print(traceback.format_exc())
                self.driver = webdriver.Firefox()
        else:
            if new_tab:
                print('\n~ Opening new tab...')
                self.driver.find_element_by_tag_name('body').send_keys(NW_TAB)
        if url:
            if not url[0:4] == 'http':
                url = 'https://'+url.replace(' ', '')
            self.driver.get(url)

    def close(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

    def close_tab(self):
        if self.driver:
            self.driver.find_element_by_tag_name('body').send_keys(CL_TAB)
            try:
                self.driver.current_url()
            except:
                self.driver = None
                print('\n~ Browser closed.')

    def switch_tab(self):
        if self.driver:
            self.driver.find_element_by_tag_name('body').send_keys(SW_TAB)

    def maximize(self):
        if self.driver:
            self.driver.maximize_window()

    def search(self, q):
        print('\n~ Answering with Google...\n')
        self.open(GOOGLE_URL+quote_plus(q), new_tab=False)

    def clear(self):
        if self.driver:
            self.driver.switch_to_active_element().clear()

    def type(self, text):
        if self.driver:
            self.driver.switch_to_active_element().send_keys(text+Keys.RETURN)

    def click(self):
        if self.driver:
            self.driver.switch_to_active_element().click()
