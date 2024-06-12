import time
import ssl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from Scripts.fun import create_save_folder, image_download, ssl_error_handler, image_limit_check

original_ssl_context = ssl._create_default_https_context

while True:

    pause = 0.7
    # 검색어 입력
    query = input("검색어 입력: ")
    scroll_pause_time = 1.5

    create_save_folder(query)

    # 이미지 개수 입력
    num_images = int(input("수집할 이미지 개수 입력: "))

    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://www.google.com/preferences?hl=ko&prev=https://www.google.com/search?q%3D%25E3%2585%2587%26sca_esv%3Dcde25c42fe00d5a3%26sca_upv%3D1#tabVal=1")
    time.sleep(pause)

    s1 = driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(2) > div.iORcjf > div:nth-child(2) > div:nth-child(2) > div.HrFxGf > div > div > div > div").click()
    time.sleep(pause)

    s1 = driver.find_element(By.CSS_SELECTOR, "body > div.iORcjf > div:nth-child(2) > div > div:nth-child(2) > div > div:nth-child(2) > div > div:nth-child(2) > div.HrqWPb > div").click()
    time.sleep(pause)

    s1 = driver.find_element(By.CSS_SELECTOR, "#lb > div > div.mcPPZ.nP0TDe.xg7rAe.ivkdbf > span > div > g-text-field > div.WO1lOd > div.FFTibe > input")
    s1.click()
    time.sleep(pause)
    s1.send_keys("미국")

    s1 = driver.find_element(By.CSS_SELECTOR, "#lb > div > div.mcPPZ.nP0TDe.xg7rAe.ivkdbf > span > div > g-menu > g-menu-item:nth-child(53) > div").click()
    time.sleep(pause)

    s1 = driver.find_element(By.CSS_SELECTOR, "#lb > div > div.mcPPZ.nP0TDe.xg7rAe.ivkdbf > span > div > div.JhVSze > span:nth-child(2)").click()
    time.sleep(pause)

    driver.get("https://www.google.com/preferences?hl=ko&prev=https://www.google.com/search%3Fq%3D%25E3%2585%2587%26sca_esv%3Dcde25c42fe00d5a3%26sca_upv%3D1")
    s2 = driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(2) > div.iORcjf > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div > div > div > div").click()
    time.sleep(pause)

    s2 = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/g-radio-button-group/div[3]/div[3]").click()
    time.sleep(pause)

    driver.get("https://www.google.com/imghp")

    # 검색어 입력 및 검색 수행
    search_bar = driver.find_element(By.NAME, "q")
    search_bar.send_keys(query)
    search_bar.submit()
    time.sleep(pause)

    def scroll_and_load():
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                try:
                    load_more_button = driver.find_element(By.CSS_SELECTOR, ".mye4qd")
                    load_more_button.click()
                except:
                    break
            last_height = new_height

    scroll_and_load()
    driver.execute_script("window.scrollTo(0, 0)")
    time.sleep(pause)

    # 이미지 요소 탐색
    images = driver.find_elements(By.CSS_SELECTOR, ".YQ4gaf")
    print(f"총 {len(images)}개의 이미지를 찾았습니다.")

    # 이미지 다운로드
    for i in range(0, num_images):
        if image_limit_check(i, num_images, images):
            break

        try:
            img_element = driver.find_elements(By.CSS_SELECTOR, ".mNsIhb")[i]
            driver.execute_script("arguments[0].click();", img_element)
            time.sleep(pause)
            image_download(query, i, num_images, images[i].get_attribute('src'))

        except ssl.SSLError as e:
            ssl_error_handler(query, i, num_images, original_ssl_context)

        except Exception as e:
            print(f"{i+1}번째 이미지 처리 중 오류 발생: {e}")

    driver.quit()
    print("작업 완료 'exit' 입력시 종료 아니면 다시 반복합니다.")
    wa = input()
    if wa == 'exit':
        print("종료중...")
        break