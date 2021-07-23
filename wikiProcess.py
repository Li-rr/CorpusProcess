import os
import utils
import zhconv
import jieba
import thulac
import re
import logging
from gensim.corpora import WikiCorpus
from logginger import init_logger
class WiKiPreprocessor:
    def __init__(self,config,logger):

        self.logger = logger
        self.ori_path = config['wiki_ori_data_path'] # 0. 原始文件
        self.tmp_text_path = config['wiki_tmp_txt_path'] # 1. xml转为txt
        self.tmp_simple_path = config['wiki_tmp_simple_path'] # 2. 繁体转为简体
        self.tmp_sep_path = config['wiki_tmp_sep_path'] # 3. 分词
        self.res_path = config['wiki_res_data_path'] # 4. 去除非中文词，得到最终结果

    def first_xml2txt(self):
        '''将维基百科数据从xml转为txt'''
        self.logger.info("开始读取维基语料")
        input_file = WikiCorpus(fname=self.ori_path,lemmatize=False,dictionary={})
        self.logger.info("维基语料读取完成")
        print(self.ori_path)
        tmp_dir = os.path.split(self.tmp_text_path)
        print(tmp_dir)
        utils.ensure_dir(tmp_dir[0])
        print(input_file)
        self.logger.info("xml2txt 开始转换")
        count = 0
        with open(self.tmp_text_path,'w',encoding='utf-8') as f:
            for text in input_file.get_texts():
                f.write(''.join(text)+"\n")
                count += 1
                if count % 10000 == 0:
                    self.logger.info('目前已处理%d条数据' % count)
            self.logger.info("xml2txt 转换结束")

    def second_tradition2simple(self):
        input_file = open(self.tmp_text_path, 'r', encoding='utf-8')
        output_file = open(self.tmp_simple_path, 'w', encoding='utf-8')

        self.logger.info('开始读入繁体文件...')
        lines = input_file.readlines()
        self.logger.info("读入繁体文件结束！")

        self.logger.info("开始转换为简体..")
        count = 0

        for line in lines:
            output_file.write(zhconv.convert(line, 'zh-hans'))
            count += 1
            if count % 10000 == 0:
                self.logger.info('目前已转换%d条数据' % count)
        input_file.close()
        output_file.close()
        self.logger.info('简繁转换执行结束！')
    def third_separate(self):
        input_file = open(self.tmp_simple_path, 'r', encoding='utf-8')
        output_file = open(self.tmp_sep_path, 'w', encoding='utf-8')
        self.logger.info('开始读入数据文件...')
        lines = input_file.readlines()
        self.logger.info('读入数据文件结束！')

        self.logger.info('分词程序执行开始...')

        thu1 = thulac.thulac( seg_only=True)  #默认模式
        text = thu1.cut("我爱北京天安门",text=True)  #进行一句话分词
        count = 0
        for line in lines:
            # 使用jieba 分词
            # jieba分词的结果是一个list，需要拼接，但是jieba把空格回车都当成一个字符处理
            # output_file.write(' '.join(jieba.cut(line.split('\n')[0].replace(' ', ''))) + '\n')

            # 在VCWE中使用的thulac分词
            
            # print(line)
            # temp = line.split("\n")
            # print(temp)
            try:
                text = thu1.cut(line.split('\n')[0].replace(' ', ''),text=True)
                output_file.write(text+"\n")
            except Exception as e:
                print("异常信息:",e)
                print("count",count)
                print("-------------------------->")
                print(line)
                print("=====================>")
                temp = line.split("\n")
                print(temp)

                break
            count += 1
            if count % 10000 == 0:
                print('目前已分词%d条数据' % count)
        output_file.close()
        input_file.close()
        self.logger.info('分词程序执行结束！')

    def four_remove(self):
        input_file = open(self.tmp_sep_path, 'r', encoding='utf-8')
        output_file = open(self.res_path, 'w', encoding='utf-8')

        self.logger.info('开始读入数据文件...')
        lines = input_file.readlines()
        self.logger.info('读入数据文件结束！')

        self.logger.info('分词程序执行开始...')
        count = 0
        cn_reg = '^[\u4e00-\u9fa5]+$'
        for line in lines:
            line_list = line.split('\n')[0].split(' ')
            line_list_new = []
            for word in line_list:
                if re.search(cn_reg, word):
                    line_list_new.append(word)
            # self.logger.info(line_list_new)
            output_file.write(' '.join(line_list_new) + '\n')
            count += 1
            if count % 10000 == 0:
                self.logger.info('目前已分词%d条数据' % count)
        input_file.close()
        output_file.close()
        self.logger.info('分词程序执行结束！')

if __name__ == '__main__':
    logger = init_logger(log_name='readZhWIKI',log_dir='log')
    from cfg import configs
    data_process = WiKiPreprocessor(config=configs,logger=logger)
    # data_process.first_xml2txt()
    # data_process.second_tradition2simple()
    data_process.third_separate()
    data_process.four_remove()