from genericpath import exists
import numpy as np
import os,sys
from cfg import configs
from logginger import init_logger
import utils
import time
from PIL import Image
class DataReader:

    def __init__(self,inputFileName,logger,savePath="./stat/") -> None:
        self.inputFileName = inputFileName

        self.word2id = dict()
        self.id2word = dict()
        self.sentences_count = 0
        self.word_frequency = dict()
        self.logger = logger
        self.savePath = savePath
        self.imgSavePath = savePath+"img/"
        

        pass
    def buildDictionary(self):
        
        if os.path.exists(self.savePath+"word2id.pkl"):
            self.logger.info("词表已存在，无需创建")
            return
        with open(self.inputFileName,'r',encoding='utf-8') as f:
            lines = f.readlines()
        
        self.logger.info("开始创建词表")
        count = 0
        for i, line in enumerate(lines):
            words = line.split()
            # print(line)
            # print(words)
            for w in words:

                if w not in self.word2id.keys():
                    self.word2id[w] = count
                    self.word_frequency[w] = 0
                    count += 1
                else:
                    self.word_frequency[w] += 1
            if i % 4000 == 0:
                self.logger.info('目前已处理 %d 条句子，词表大小：%d，词频表大小：%d'% (i,len(self.word2id),len(self.word_frequency)) )
                
            # break
        
        self.logger.info("最终的词表大小：%d，词频表大小：%d"%(len(self.word2id),len(self.word_frequency)))

        self.logger.info("开始保存词表、词频表数据")
        utils.pkl_dump(self.word_frequency,self.savePath+"word_freq.pkl")
        utils.pkl_dump(self.word2id,self.savePath+"word2id.pkl")
        self.logger.info("保存词表完成")
        
    def buildVocabulary(self):
        word2id = utils.pkl_load(self.savePath+"word2id.pkl")
        word2freqs =utils.pkl_load(self.savePath+"word_freq.pkl")


        word2freqs = {k:v  for k,v in word2freqs.items() if v > 99}

        keys = word2freqs.keys()
        word2id_compress = {k:word2id[k] for k in keys}
        char_set = list()
        for i,(word,v) in enumerate(word2id_compress.items()):
            for w in word:
                # print(w,end="")
                char_set.append(w)
                # break
            # print()
            # if i ==10:
            #     break
        print(len(char_set))
        single_char_set = list(set(char_set))
        # 论文中是5030个字
        print('总字数',len(char_set),'',len(single_char_set))
        char2ix = dict()
        for i,ch in enumerate(single_char_set):
            # print(i,ch)
            char2ix[ch] = i+1 # 空一个0

            
        #     print(k,v)
            # if i ==10:
                # break
        # print(char2ix)
        utils.pkl_dump(word2id_compress,self.savePath+"word2id_compress.pkl")
        utils.pkl_dump(char2ix,self.savePath+"char2ix.pkl")

        
        vocabulary_path = self.savePath +"vocabulary.txt"
        with open(vocabulary_path,"w",encoding='utf-8') as f:
            f.write("%d %d\n" % (len(word2freqs),sum(word2freqs.values())))
        
            for char, char_freq in word2freqs.items():
                e = '%s %s\n' % (char,str(char_freq))
                f.write(e)

        print(len(word2freqs),len(word2id),sum(word2freqs.values()))
    def buildCharImage(self):
        '''
        根据字典构建字典图片
        '''
        self.logger.info("开始请求图片数据")
        char2ix = utils.pkl_load(self.savePath+"char2ix.pkl")
        exists_ch = os.listdir(self.imgSavePath)
        exists_ch = [int(ch_jpg.split(".")[0])  for ch_jpg in exists_ch]

    
        for count,(ch,ch_id) in enumerate(char2ix.items()):
            if ch_id in exists_ch:
                continue
            imgData = utils.getImgData(ch)
            print(ch,ch_id)
            
            if type(imgData) == bytes:
                with open(self.imgSavePath+"{}.jpg".format(ch_id),'wb') as f:
                    f.write(imgData)
                    time.sleep(1) # 暂停0.5 s
                if count % 20 == 0:
                    self.logger.info("{}: {} 写入成功".format(count,ch)) 
            elif type(imgData) == int:
                self.logger.info("{}:{} 写入失败，状态码：{}".format(count,ch,imgData))
            elif type(imgData) == str:
                self.logger.info("{}:{} 写入失败，异常信息：{}".format(count,ch,imgData))
        self.logger.info("所有数据处理完毕")


    def buildImage2numpy(self):
        '''
        处理思路：
        从char字典中获取的字的id然后来顺序读取,
        
        这里需要注意，索引id 0 是用于补全的，这里取均值
        '''
        self.logger.info("开始构建图像矩阵")
        char2ix = utils.pkl_load(self.savePath+"char2ix.pkl")

        img_list = list()
        values = list(char2ix.values())
        # print(values == sorted(values))
        # 如果是升序
        if values == sorted(values):
        
            for idx,(ch,ch_id) in enumerate(char2ix.items()):
                imgPath = os.path.join("D:\WORKSPACE\CorpusProcess\stat\img_black_ground","{}.jpg".format(ch_id))
                # imgPath = os.path.join("D:\WORKSPACE\CorpusProcess\stat\img","{}.jpg".format(ch_id))
                imgArray = utils.image2numpy(imgPath)

                # print(imgPath)
                # print(imgArray.shape)
                img_list.append(imgArray)
                
                # break

        np_img_list =np.array(img_list) # [5240,40,40]
        # print(np_img_list.shape,np_img_list.dtype)
        np_img_mean = np_img_list.mean(0) # [40,40]
        img_mean = Image.fromarray(np_img_mean)
        img_mean.convert("RGB").save("fuck.jpg")
        # print(np_img_mean.shape)

        # sys.exit(0)
        if len(char2ix) == np_img_list.shape[0]:
            self.logger.info("数据读取完毕，保存图片：%d 个" %(len(char2ix)) )            
            np_mean_img_list = np_img_list - np_img_mean
            np_mean_img_list = np.insert(np_mean_img_list,0,np_img_mean,0) # 插入元素
            np_img_list = np.insert(np_img_list,0,np_img_mean,0) # 插入元素

            print(np_img_list.shape,np_mean_img_list.shape)
            # utils.pkl_dump(np_mean_img_list,self.savePath+"char_img_mean.pkl")
            # utils.pkl_dump(np_img_list,self.savePath+"char_img.pkl")
            utils.pkl_dump(np_mean_img_list,self.savePath+"char_img_mean_bg.pkl")
            utils.pkl_dump(np_img_list,self.savePath+"char_img_bg.pkl")
        else:
            self.logger.info("字典数量：%d，图片数量：%d" % (len(char2ix),np_img_list.shape[0]))
        


        # imgs = os.listdir(self.imgSavePath)
        # imgs = [os.path.join(self.imgSavePath,img) for img in imgs]
        
        # for i,img in enumerate(imgs):

            # img_array = utils.image2numpy(img)
            # print(img,img_array.shape,type(img_array))
            # if i == 10:
                # break





def stat_char():
    '''
    统计字符数量
    '''
    with open(configs['wiki_res_data_path'],'r',encoding='utf-8') as f:
        lines = f.readlines()

    print(lines[0].split("\n"))

if __name__ == "__main__":
    # stat_char()
    logger = init_logger(log_name='wikiStatic',log_dir='log')
    dr = DataReader(configs['wiki_res_data_path'],logger)
    # dr.buildDictionary() # step 1
    # dr.buildVocabulary() # step 2
    # dr.buildCharImage() # step 3
    dr.buildImage2numpy() # step 4

