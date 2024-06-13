import os

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
    # 확장자 설정
    file_extension = original_img_src.rsplit('.', 1)[-1].split('/', 1)[0].split('?', 1)[0]
    if file_extension == 'com':
        file_extension = 'png'
    if file_extension == 'net':
        file_extension = 'png'
    filename = 'images\\' + f'{query}_{i + 1}.{file_extension}'
    return filename
