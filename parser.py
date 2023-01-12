import asyncio
import os
import zipfile

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from fake_useragent import UserAgent
from selenium import webdriver
from multiprocessing import Pool
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

load_dotenv()

PROXY_HOST = os.getenv('PROXY_HOST')  # rotating proxy or host
PROXY_PORT = os.getenv('PROXY_PORT')
PROXY_USER = os.getenv('PROXY_LOGIN')
PROXY_PASS = os.getenv('PROXY_PASSWORD')

manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)


def get_chromedriver(use_proxy=False, user_agent=None, headless=False, driver_path_name='chromedriver'):
    path = os.path.dirname(os.path.abspath(__file__))
    chrome_options = webdriver.ChromeOptions()
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)
    # if headless:
    #     chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(
        os.path.join(path, driver_path_name),
        chrome_options=chrome_options)
    return driver, chrome_options


class Parser:
    def __init__(self):
        self.user_agent = UserAgent()
        self.driver, self.options = get_chromedriver(use_proxy=True)
        self.driver2, self.options2 = get_chromedriver(use_proxy=True, driver_path_name='other/chromedriver')

        self.data1 = {"url": 'https://lucky-jet-b.1play.one/?exitUrl=null&language=ru&b=demo',
                      'driver': self.driver,
                      'proccess': 'LUCKY JET:',
                      "selenium_class": 'sc-iTFTee',
                      'soup_tag': 'div',
                      'soup_class': "sc-bYMpWt"
                      }
        self.data2 = {"url": 'https://demo.spribe.io/launch/aviator?currency=USD&lang=ru',
                      'driver': self.driver2,
                      'proccess': 'AVIATOR:',
                      "selenium_class": 'payouts-block',
                      'soup_tag': 'app-payout-item',
                      'soup_class': "payout ng-star-inserted"
                      }

    async def get_content(self, **kwargs):

        self.options = '--disable-blink-features=AutomationControlled'
        driver = kwargs.get('driver')

        driver.get(kwargs.get('url'))
        await asyncio.sleep(5)

        last_index: str = ''

        while True:
            driver.find_elements(By.CLASS_NAME, kwargs.get('selenium_class'))
            await asyncio.sleep(2)

            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            result = soup.find_all(kwargs.get('soup_tag'), class_=kwargs.get('soup_class'))

            first = result[0]
            current_index = first.text

            if current_index != last_index:
                last_index = current_index
                print(f'{kwargs.get("proccess")} index: {last_index}')
            else:
                continue

    # async def get_content_aviator(self):
    #     self.options.add_argument('--disable-blink-features=AutomationControlled')
    #     self.driver.get(self.URL2)
    #     await asyncio.sleep(5)
    #
    #     last_index: str = ''
    #     while True:
    #         self.driver.find_elements(By.CLASS_NAME, )
    #         await asyncio.sleep(2)
    #
    #         html = self.driver.page_source
    #         soup = BeautifulSoup(html, 'lxml')
    #         result = soup.find_all('app-payout-item', class_=)
    #
    #         first = result[0]
    #         current_index = first.get_text(strip=True)
    #
    #         if current_index != last_index:
    #             last_index = current_index
    #             print(f'aviator index: {last_index}')
    #
    #         else:
    #             continue

    async def run(self):

        try:

            await asyncio.gather(self.get_content(**self.data1), self.get_content(**self.data2))

            # await self.get_content(**data)
            # await self.get_content_luckyjet()
            print('----------')
        except Exception as e:
            print(e)
        finally:
            self.driver.close()
            self.driver.quit()


if __name__ == '__main__':
    asyncio.run(Parser().run())
