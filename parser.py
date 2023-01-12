import asyncio
import os
import zipfile

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By

from config import PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS

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
        self.driver, self.options = get_chromedriver(use_proxy=True, user_agent=self.user_agent.random)

        self.data = {"url": 'https://lucky-jet-b.1play.one/?exitUrl=null&language=ru&b=demo',
                     "selenium_class": 'sc-iTFTee',
                     'soup_tag': 'div',
                     'soup_class': "sc-bYMpWt"
                     }

    async def get_content(self, **kwargs):

        self.options = '--disable-blink-features=AutomationControlled'

        self.driver.get(kwargs.get('url'))
        await asyncio.sleep(5)

        last_index: str = ''

        while True:
            self.driver.find_elements(By.CLASS_NAME, kwargs.get('selenium_class'))
            await asyncio.sleep(2)

            html: str = self.driver.page_source
            soup: BeautifulSoup = BeautifulSoup(html, 'lxml')
            result: list = soup.find_all(kwargs.get('soup_tag'), class_=kwargs.get('soup_class'))

            first = result[0]
            current_index: str = first.text

            if current_index != last_index:
                last_index = current_index
                print(last_index)
                # TODO здесь запись в бд функция
            else:
                continue

    async def run(self):

        try:
            # await asyncio.gather(self.get_content(**self.data1), self.get_content(**self.data2))
            await self.get_content(**self.data)
        except Exception as e:
            print(e)
        finally:
            self.driver.close()
            self.driver.quit()


if __name__ == '__main__':
    asyncio.run(Parser().run())
