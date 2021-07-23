import pickle as pkl
import os
import requests
from PIL import Image
import numpy as np

def pkl_load(f_path):
    with open(f_path,'rb') as f:
        return pkl.load(f)
def pkl_dump(data,f_path):
    pkl.dump(data,open(f_path,'wb'))

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def getImgData(ch):
    '''
    #FFFFFF 为白色
    #000000 为黑色
    '''
    url = "http://www.diyiziti.com"
    payload={
        'FontInfoId': '361',
    'FontSize': '24',
    'FontColor': '#000000', 
    'ImageWidth': '40',
    'ImageHeight': '40',
    'ImageBgColor': '#FFFFFF',
    'Content': '倾',
    'ActionCategory': '2'
    }
    headers = {
        'Referer': 'http://www.diyiziti.com/kaishu',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 Edg/91.0.864.71'

    }
    files=[

    ]
    payload["Content"] = ch
    requests.DEFAULT_RETRIES = 5
    try:
        response = requests.request("POST", url, headers=headers, data=payload, files=files,timeout=10)

        if response.status_code == 200:
            return response.content
        else:
            return response.status_code
    except Exception as e:
        return str(e)


def image2numpy(image_path,mode="F"):
    '''
    F 格式
    '''
    # imgs = os.listdir(image_dir)
    # imgs = [os.path.join(image_dir,img) for img in imgs]


    img = Image.open(image_path)
    chang_type_img = img.convert(mode)
    np_chang_type_img = np.array(chang_type_img)

    # print(np_chang_type_img.shape)

    # img2 = Image.fromarray(np_chang_type_img)
    # img2.convert("RGB").save("fuck.jpg")
    # print(np_rgb_img)
    return np_chang_type_img
    

if __name__ == "__main__":
    image2numpy("D:\WORKSPACE\CorpusProcess\stat\img_black_ground")