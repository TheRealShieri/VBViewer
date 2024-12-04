# bot_logic.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from proxy_manager import ProxyManager

class BotLogic:
    def __init__(self, proxy_manager, driver_path):
        self.proxy_manager = proxy_manager
        self.driver_path = driver_path

    def start_browser_with_proxy(self, url):
        proxy = self.proxy_manager.get_random_proxy()
        
        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--mute-audio")
        if proxy:
            chrome_options.add_argument(f'--proxy-server={proxy}')
        
        driver = webdriver.Chrome(executable_path=self.driver_path, options=chrome_options)
        
        try:
            driver.get(url)
            # Let the page load for a while
            time.sleep(10)
        except Exception as e:
            print(f"Error: {e}")
            self.proxy_manager.remove_proxy(proxy)
        finally:
            driver.quit()
