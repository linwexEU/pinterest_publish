import undetected_chromedriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.ui import WebDriverWait 
import os 
import time 
from pinterest.xpaths import Xpaths
import pickle 
import random


COOKIES_PATH = "pinterest/cookies"


def get_random_ua(): 
    with open("pinterest/user_agent.txt") as file: 
        ua = [item.strip() for item in file.readlines()]
        return random.choice(ua)


class PinterestPublisher: 
    def __init__(self):
        options = undetected_chromedriver.ChromeOptions() 
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")  
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--window-size=1920,1080")
        options.add_argument(f"--user-agent={get_random_ua()}") 
        self.browser = undetected_chromedriver.Chrome(options=options) 

    def wait_for_element(self, element): 
        while True:
            try:
                WebDriverWait(self.browser, 60).until(
                    EC.visibility_of(self.browser.find_element(element[0], element[1]))
                )
                break 
            except: 
                continue
            
    def login(self, email, password):
        if os.path.exists(f"{COOKIES_PATH}/{email}_cookies"): 
            self.browser.get("https://www.pinterest.com/")
            for cookie in pickle.load(open(f"{COOKIES_PATH}/{email}_cookies", "rb")): 
                self.browser.add_cookie(cookie) 
            time.sleep(1) 
            self.browser.refresh()
            self.wait_for_element((By.XPATH, "//div[@class='Eqh fZz fev zI7 iyn Hsu']"))
            print("[INFO] Авторизация прошла успешно")
        else: 
            self.browser.get("https://www.pinterest.com/")
            self.wait_for_element((By.CSS_SELECTOR, ".RCK.Hsu.USg.adn.CCY.NTm.KhY.S9z.Vxj.aZc.Zr3.hA-.Il7.hNT.BG7.hDj._O1.KS5.mQ8.Tbt.L4E"))

            login_button = self.browser.find_element(By.CSS_SELECTOR, Xpaths.LOGIN_BUTTON)
            login_button.click() 
            WebDriverWait(self.browser, 60).until(
                EC.element_to_be_clickable((By.XPATH, Xpaths.LOGIN_FORM))
            )
            
            email_form = self.browser.find_element(By.XPATH, Xpaths.EMAIL_FORM)
            if email_form:
                email_form.send_keys(email)
                time.sleep(0.5) 

            password_form = self.browser.find_element(By.XPATH, Xpaths.PASSWORD_FORM)
            if password_form:
                password_form.send_keys(password)
                time.sleep(0.5) 

            log = self.browser.find_element(By.CSS_SELECTOR, Xpaths.LOG_BUTTON)
            log.click()
            self.wait_for_element((By.XPATH, "//div[@class='Eqh fZz fev zI7 iyn Hsu']"))

            pickle.dump(self.browser.get_cookies(), open(f"{COOKIES_PATH}/{email}_cookies", "wb"))
            print("[INFO] Авторизация прошла успешно")

    def upload(self, video, name=None, description=None, link=None): 
        self.browser.get("https://www.pinterest.com/pin-creation-tool/") 
        self.wait_for_element((By.CSS_SELECTOR, ".OVX.XiG.zI7.iyn.Hsu"))

        file = self.browser.find_element(By.XPATH, Xpaths.FILE)
        if file: 
            file.send_keys(video)
            self.wait_for_element((By.CSS_SELECTOR, "button div.tBJ.dyH.iFc.sAJ.B1n.tg7.H2s"))
        
        name_of_pin = self.browser.find_element(By.XPATH, Xpaths.NAME)
        if name_of_pin: 
            if name:
                name_of_pin.send_keys(name)
                time.sleep(0.5) 

        description_of_pin = self.browser.find_element(By.XPATH, Xpaths.DESCRIPTION)
        if description_of_pin: 
            if description:
                description_of_pin.send_keys(description) 
                time.sleep(0.5) 

        link_of_pin = self.browser.find_elements(By.XPATH, Xpaths.LINK)[1] 
        if link_of_pin: 
            if link: 
                link_of_pin.send_keys(link)
                time.sleep(0.5) 

        publish = self.browser.find_element(By.CSS_SELECTOR, Xpaths.PUBLISH_BUTTON)
        if publish: 
            publish.click() 
            self.wait_for_element((By.CSS_SELECTOR, "span.tBJ.dyH.iFc.sAJ.B1n.zDA.IZT.swG.CKL")) 
        print("[INFO] Пост опубилкован")

    def close_browser(self):
        self.browser.close() 
        self.browser.quit() 



if __name__ == "__main__": 
    pp = PinterestPublisher() 
    pp.login("linwexunstop@gmail.com", "Ivansaha1805")
    pp.upload("Test + Selenium + Python")
    pp.close() 





