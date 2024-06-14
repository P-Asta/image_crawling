import os
import time
import random
import urllib.request
import requests
import certifi
from functools import wraps
from urllib.error import URLError, HTTPError
from ssl import SSLError

def ssl_setting(original_img_src):
    requests.get(original_img_src, verify=certifi.where())

def retry(ExceptionToCheck, tries=4, delay=2+random.random(), backoff=2, logger=None):
    """Retry calling the decorated function using an exponential backoff.

    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    :param ExceptionToCheck: the exception to check. may be a tuple of
        exceptions to check
    :type ExceptionToCheck: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    :param logger: logger to use. If None, print
    :type logger: logging.Logger instance
    """
    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck as e:
                    msg = f"{str(e)}, Retrying in {mdelay} seconds..."
                    print(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)
        return f_retry # true decorator
    return deco_retry

def create_save_folder(query):
    if not os.path.exists('images'):
        os.makedirs('images')
    if not os.path.exists(query):
        os.makedirs(f'images\{query}', exist_ok=True)
        print(f"'{query}' 폴더 생성 완료...")

def image_limit_check(i, num_images, images):
    if i >= num_images or i >= len(images):
        return True

def file_extention_f(original_img_src, query, i):
    # 확장자 설정&파읽경로 설정
    file_extension = original_img_src.rsplit('.', 1)[-1].split('/', 1)[0].split('?', 1)[0]
    if file_extension == 'com':
        file_extension = 'png'
    if file_extension == 'net':
        file_extension = 'png'
    filename = f'images\{query}\{query}_{i + 1}.{file_extension}'
    return filename

@retry((TimeoutError, URLError, HTTPError, SSLError), tries=3, delay=2+random.random(), backoff=2)
def image_download(original_img_src, filename, query, i, num_images):
    ssl_setting(original_img_src)
    urllib.request.urlretrieve(original_img_src, filename)
    print(f"{query} : {i + 1}/{num_images} 이미지 다운로드 완료...")
