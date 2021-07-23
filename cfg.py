# encoding:utf-8
from pathlib import Path
import multiprocessing
DATASET_DIR = Path("D:\WORKSPACE\CorpusProcess")
configs = {
    'wiki_ori_data_path': DATASET_DIR / 'zhwiki-2021714-pages-articles.xml.bz2',
    'wiki_tmp_txt_path': DATASET_DIR / 'wiki/wiki.cn.txt',
    'wiki_tmp_simple_path': DATASET_DIR / "wiki/wiki.cn.simple.txt",
    'wiki_tmp_sep_path': DATASET_DIR / 'wiki/wiki.cn.simple.separate.txt',
    'wiki_res_data_path': DATASET_DIR / 'wiki/wiki_final.txt',
    'wiki_w2c_model_path': '/home/stu/Documents/dataset/wiki/wiki.model'
}