"""
Оказалось что логины созданные ранее @givinschool.org теперь при входе в Zoom требуют либо
1) Подключиться к аккаунту
либо
2) Поменять почту - надо первое выбирать и это только один раз.
"""
import csv
import traceback
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


def connect_zoom_login(login, password):
    try:
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument("--headless")
        browser = webdriver.Chrome(r'c:\MyGit\GivinToolsPython\chromedriver.exe', options=chromeOptions)
        # browser = webdriver.Chrome(r'/usr/local/bin/chromedriver', options=chromeOptions)
        # browser = webdriver.Chrome(r'chromedriver.exe')
        # browser = webdriver.Chrome(r'c:\Windows\System32\chromedriver.exe')
        # browser = webdriver.Chrome(r'c:\Users\MinistrBob\.wdm\drivers\chromedriver\79.0.3945.36\win32\chromedriver.exe')
        browser.get(r"https://www.zoom.us/signin")
        input_login = browser.find_element_by_css_selector("#email")
        input_login.send_keys(login)
        input_password = browser.find_element_by_css_selector("#password")
        input_password.send_keys(password)
        button = browser.find_element_by_css_selector("a.btn.btn-primary.submit.signin.user")
        button.click()
        time.sleep(4)
        try:
            error_text = 'error_txt'
            error_label = browser.find_element_by_css_selector("#error_msg")
            error_text = error_label.text
            print(f"{login},{password},{type},{error_text}")
        except NoSuchElementException:
            checkbox1 = browser.find_element_by_css_selector("#choose-option1")
            checkbox1.click()
            button = browser.find_element_by_css_selector("#btn-continue")
            browser.execute_script("return arguments[0].scrollIntoView(true);", button)
            button.click()
            print(f"{login},{password}")
    except:  # noqa: E722
        print(traceback.format_exc())
    finally:
        # закрываем браузер даже в случае ошибки
        browser.quit()


if __name__ == '__main__':
    file = r'd:\YandexDisk\TEMP\GS\3.txt'
    # file = r'd:\!SAVE\GS\test.csv'
    with open(file, newline='') as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        for row in reader:
            # print(row)
            connect_zoom_login(row[0], row[1])
