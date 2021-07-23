import thulac	
import requests
import os
import utils
from PIL import Image
def test1():
    thu1 = thulac.thulac( seg_only=True)  #默认模式
    text = thu1.cut("我爱北京天安门",text=True)  #进行一句话分词
    print(text,text.split())


def test2():
    '''
    vcwe使用第一字体转换器进行转换，使用 
    楷书字体转换器在线转换生成，正楷字体
    '''
    

    url = "http://www.diyiziti.com"

    payload={'FontInfoId': '361',
    'FontSize': '24',
    'FontColor': '#FFFFFF',
    'ImageWidth': '40',
    'ImageHeight': '40',
    'ImageBgColor': '#000000',
    'Content': '倾',
    'ActionCategory': '2'}
    files=[

    ]
    proxy = {'http':'http://'+get_random_proxy()}

    headers = {}

    chars = ['淇','镇','药','倾']
    print("----")
    for ch in chars:
        payload['Content'] = ch
        try:
            response = requests.request("POST", url, headers=headers,data=payload, files=files)
            
            print(response.status_code)
            print(type(response.content))
            if type(response.content) == bytes:
                print("fuck yo")
            with open("./{}.jpg".format(ch),'wb') as f:
                f.write(response.content)
        except Exception as e:
            print(e)
            NETWORK_STATUS = False  # 请求超时改变状态

            if NETWORK_STATUS == False:
                '''请求超时'''
                for i in range(1, 10):
                    print('请求超时，第%s次重复请求' % i)
                    proxy = {'http': 'http://' + get_random_proxy()}
                    response = requests.request("POST", url, headers=headers, proxies = proxy,data=payload, files=files)
                    if response.status_code == 200:
                        break


def get_random_proxy():
    proxypool_url = 'http://127.0.0.1:5555/random'
    """
    get random proxy from proxypool
    :return: proxy
    """
    return requests.get(proxypool_url).text.strip()#输出的是字符串

def test3():
    '''
    读取图像矩阵，然后转为图片测试
    '''
    char2ix = utils.pkl_load("./stat/char2ix.pkl")

    np_img = utils.pkl_load("./stat/char_img.pkl")
    np_img_mean = utils.pkl_load("./stat/char_img_mean.pkl")
    print(np_img.dtype)

  
    print(np_img_mean.dtype)
    for idx, (ch,ch_id) in enumerate(char2ix.items()):
        # break
        # print(ch_id)
        img = np_img[ch_id-1]
        img_mean = np_img_mean[ch_id-1]

        img = Image.fromarray(img)
        img_mean = Image.fromarray(img_mean)
        img.convert("RGB").save("./test/{}.jpg".format(ch_id))
        img_mean.convert("RGB").save("./test/{}_mean.jpg".format(ch_id))
        # print(img)
        if idx == 5:
            break

if __name__ == "__main__":
    test3()
    # test2()
    # try:

    #     1 / 0
    # except Exception as e:
    #     print(str(e))
    #     print(type(str(e)))
    # imags = os.listdir("./stat/img")
    # imags = [int(ch_jpg.split(".")[0])  for ch_jpg in imags]
    # print(imags)
    # a = 0
    # if type(a) == int:
        # print("---")
    