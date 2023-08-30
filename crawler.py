import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyperclip


class Crawler:
    def __init__(self, args):
        self.driver = webdriver.Chrome()
        self.login_id = args.login_id
        self.login_pw = args.login_pwl
        self.favorite_list_name = args.favorite_list_name
        self.driver.implicitly_wait(1)

    def wait_until(self, search_by, element):
        try:
            result = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((search_by, element)))
        except TimeoutException:
            result = False
        if result:
            result_element = self.driver.find_element(search_by, element)
            return result_element
        else:
            return None

    def get_naver_map(self):
        self.driver.get("https://map.naver.com")

    def login(self):
        login_button = self.wait_until(By.CSS_SELECTOR, "#gnb_login_button")
        login_button.click()

        if "nid.naver.com" in self.driver.current_url:
            self.naver_login()
        else:
            print("Already logged in")
            self.go_to_map_home()

    def check_captcha(self):
        try:
            self.driver.find_element(By.CSS_SELECTOR, "#frmNIDLogin > ul > li > div > div.captcha_wrap")
            print("Captcha found")
            print("Please login manually")
            input("Press Enter to continue...")
        except NoSuchElementException:
            pass

    def naver_login(self):
        self.check_captcha()
        login_id_text = self.wait_until(By.CSS_SELECTOR, "#id")
        login_pw_text = self.wait_until(By.CSS_SELECTOR, "#pw")

        login_id_text.click()
        pyperclip.copy(self.login_id)
        login_id_text.send_keys(Keys.CONTROL + "v")

        login_pw_text.click()
        pyperclip.copy(self.login_pw)
        login_pw_text.send_keys(Keys.CONTROL + "v")

        login_button = self.wait_until(By.CSS_SELECTOR, "#log\\.login")
        login_button.click()
        self.check_captcha()
        if "deviceConfirm" in self.driver.current_url:
            self.check_new_device()

    def go_to_map_home(self):
        map_home_button = self.wait_until(
            By.CSS_SELECTOR, "#header > nav > ul > li.sc-13bg05j.ggZDYI > a > span.navbar_text"
        )
        map_home_button.click()

    def check_new_device(self):
        enroll_button = self.wait_until(By.CSS_SELECTOR, "#new\\.save")
        enroll_button.click()

    def search_address(self, address):
        input_box = self.wait_until(By.CSS_SELECTOR, "#section_content > div > div.sc-iwm9f4.jCPpmH > div > div > div")
        search_text = input_box.find_element(By.CLASS_NAME, "input_search")
        if search_text.get_attribute("value") != "":
            clear_button = self.wait_until(By.CLASS_NAME, "btn_clear")
            clear_button.click()
        search_text.send_keys(address)
        search_text.send_keys(Keys.ENTER)

        try:
            search_result_list = self.driver.find_element(
                By.CSS_SELECTOR,
                "#section_content > div.sc-fjy3z9.dAwFnA > div.sc-1wsjitl.dunggE > div > div > div > div.sc-1o6q4iu.eKnNkA > ul",
            )
        except NoSuchElementException:
            return

        search_result_list = search_result_list.find_elements(By.TAG_NAME, "li")
        # TODO : 범용 코드로 수정
        if len(search_result_list) > 0:
            for result in search_result_list:
                if "서울특별시" in result.text:
                    result.click()
                    break
            else:
                print("서울특별시의 지역이 검색되지 않았습니다.")
                print("첫번째 검색 결과를 선택합니다.")
                search_result_list[0].click()

    def add_address_to_favorite(self, address):
        add_favorite_button = self.wait_until(By.CLASS_NAME, "btn.btn_favorite")
        if add_favorite_button is None:
            print(f"{address}의 검색 결과를 찾지 못했습니다.")
            return
        elif add_favorite_button.get_attribute("aria-pressed") == "true":
            print("이미 즐겨찾기에 추가된 주소입니다.")
            return
        time.sleep(0.25)
        add_favorite_button.click()
        time.sleep(1)

        save_group_list = self.driver.find_elements(By.CLASS_NAME, "swt-save-group-item")
        for save_group_item in save_group_list:
            if save_group_item.find_element(By.CLASS_NAME, "swt-save-group-name").text == self.favorite_list_name:
                check_button = save_group_item.find_element(By.CLASS_NAME, "swt-save-group-check-area")
                check_button.click()
                break
        else:
            print(f"{self.favorite_list_name}가 목록에 없습니다.")
            raise ValueError
        save_favorite_button = self.wait_until(By.CLASS_NAME, "swt-save-btn")
        save_favorite_button.click()

    def input_to_naver_map(self, locations):
        self.get_naver_map()
        self.login()
        for location in locations:
            self.search_address(location)
            self.add_address_to_favorite(location)
