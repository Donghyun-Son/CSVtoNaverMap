import pyperclip
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Crawler:
    def __init__(self, args):
        self.driver = webdriver.Chrome()
        self.login_id = args.login_id
        self.login_pw = args.login_pw
        self.favorite = args.favorite
        self.city = args.city
        self.driver.implicitly_wait(1)
        self.wait = WebDriverWait(self.driver, 1)

    def wait_element(self, search_by, element):
        try:
            result = self.wait.until(EC.presence_of_element_located((search_by, element)))
        except TimeoutException:
            print(f"Timeout: {element} is not found")
            return None
        return result

    def wait_and_click(self, search_by, element):
        try:
            element = self.wait.until(EC.element_to_be_clickable((search_by, element)))
            element.click()
        except TimeoutException:
            print(f"Timeout: {element} is not clickable")
            return None
        return element

    def get_naver_map(self):
        self.driver.get("https://map.naver.com")

    def login(self):
        login_button = self.wait_element(By.CSS_SELECTOR, "#gnb_login_button")
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

        login_id_text = self.wait_and_click(By.CSS_SELECTOR, "#id")
        pyperclip.copy(self.login_id)
        login_id_text.send_keys(Keys.CONTROL + "v")

        login_pw_text = self.wait_and_click(By.CSS_SELECTOR, "#pw")
        pyperclip.copy(self.login_pw)
        login_pw_text.send_keys(Keys.CONTROL + "v")

        # login button
        self.wait_and_click(By.CSS_SELECTOR, "#log\\.login")

        self.check_captcha()
        if "deviceConfirm" in self.driver.current_url:
            self.check_new_device()

    def go_to_map_home(self):
        # map_home_button
        self.wait_and_click(By.XPATH, "//*[@id='header']/nav/ul/li[1]/a")

    def check_new_device(self):
        # not_enroll_button
        self.wait_and_click(By.CSS_SELECTOR, "#new\\.dontsave")

    def search_address(self, address):
        search_text = self.wait_element(By.XPATH, "//*[@class='input_search']")
        if search_text.get_attribute("value") != "":
            # clear_button
            self.wait_and_click(By.CLASS_NAME, "btn_clear")
        search_text.send_keys(address)
        search_text.send_keys(Keys.ENTER)

        search_list = self.wait_element(By.XPATH, "//*[@class='sc-48msce bcmMFw']")
        if search_list is None:
            return True

        try:
            search_address_list = search_list.find_elements(
                By.XPATH,
                "//*[@class='sc-j1m19h fFQjPA sc-98ivrk eYoqTc sc-lr1nk3 cdpDce']",
            )
        except NoSuchElementException:
            print("주소 검색 결과가 존재하지 않습니다.")
            print("장소 검색을 확인합니다.")

        if len(search_address_list) > 0:
            for result in search_address_list:
                if self.city in result.text:
                    result.click()
                    break
            else:
                print(f"{self.city}의 지역이 검색되지 않았습니다.")
                print("첫번째 검색 결과를 선택합니다.")
                search_address_list[0].click()
            return True

        try:
            search_place_list = search_list.find_elements(
                By.XPATH,
                "//div[contains(@class, 'qbGlu')]//a[contains(@class, 'P7gyV') and not(ancestor::div/a[contains(@class, 'gU6bV mdfXq')])]",
            )
        except NoSuchElementException:
            print("장소 검색 결과가 존재하지 않습니다.")
            print(f"{address}의 검색 결과를 찾지 못했습니다.")
            return False

        if search_place_list is not None and len(search_place_list) > 0:
            print("장소 검색 결과를 찾았습니다.")
            print("첫번째 검색 결과를 선택합니다.")
            search_place_list[0].click()

        return True

    def check_no_result(self):
        if self.wait_element(By.XPATH, "//*[@class='FYvSc']") is not None:
            print("검색 결과가 존재하지 않습니다.")
            return True
        return False

    def add_address_to_favorite(self):
        add_favorite_button = self.wait_element(By.CLASS_NAME, "btn.btn_favorite")
        if add_favorite_button is None:
            print("즐겨찾기 추가 버튼을 찾지 못했습니다.")
            return
        if add_favorite_button.get_attribute("aria-pressed") == "true":
            print("이미 즐겨찾기에 추가된 주소입니다.")
            return
        add_favorite_button.click()

        check_button = self.wait_and_click(
            By.XPATH,
            f"//li[contains(@class, 'swt-save-group-item') and .//strong[contains(@class, 'swt-save-group-name') and text()='{self.favorite}']]//span[contains(@class, 'swt-save-group-check-area')]",
        )
        if check_button is None:
            print(f"{self.favorite}가 즐겨찾기 목록에 없습니다.")
            raise ValueError

        # save_favorite_button
        self.wait_and_click(By.CLASS_NAME, "swt-save-btn")

    def input_to_naver_map(self, locations):
        self.get_naver_map()
        self.login()
        for location in locations:
            result = self.search_address(location)
            if result:
                self.add_address_to_favorite()
