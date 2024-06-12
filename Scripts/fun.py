import urllib.request
import ssl
import os
from selenium import webdriver
from selenium.webdriver.common.by import By

scroll_pause_time = 1.7

def create_save_folder(query):
    if not os.path.exists(query):
        os.makedirs(query)
        print(f"'{query}' 폴더 생성 완료...")

def image_limit_check(i, num_images, images):
    if i >= num_images or i >= len(images):
        return True

def image_download(query, i, num_images, original_img_src):
    # HTTP 헤더 설정
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')]
    urllib.request.install_opener(opener)

    # 확장자 설정
    file_extension = original_img_src.rsplit('.', 1)[-1].split('/', 1)[0].split('?', 1)[0]
    if file_extension == 'com':
        file_extension = 'png'
    if file_extension == 'net':
        file_extension = 'png'
    filename = f'{query}_{i + 1}.{file_extension}'

    # 이미지 다운로드
    save_path = os.path.join(query, filename)
    urllib.request.urlretrieve(original_img_src, save_path)
    print(f"{query} : {i + 1}/{num_images} 이미지 다운로드 완료...")

def ssl_error_handler(query, i, num_images, original_ssl_context):
    try:
        print("ssl 오류 발생\n다시 시도합니다.")
        ssl._create_default_https_context = ssl._create_unverified_context
        # 큰 이미지 URL 가져오기
        driver = webdriver.Chrome()
        original_img_element = driver.find_element(By.XPATH, "/html/body/div[6]/div/div/div/div/div/div/c-wiz/div/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]/a/img[1]")
        original_img_src = original_img_element.get_attribute('src')

        if original_img_src and "http" in original_img_src:
            image_download(original_img_src, query, i, num_images)
    
    except Exception as e:
        print(f"{i+1}번째 이미지 처리 중 오류 발생: {e}")

    finally:
        ssl._create_default_https_context = original_ssl_context