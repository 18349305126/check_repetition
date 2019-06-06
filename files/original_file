import requests;
from bs4 import  BeautifulSoup;
import jieba;
import os;
import re;
import time;
from gensim import corpora,models,similarities;
import random;
import sys;

def get_review_tag(src):
    review_response=requests.get(src);
    review_soup=BeautifulSoup(review_response.text);
    review_tag=review_soup.find('div',{'class':'review-content clearfix'});
    time.sleep(1);
    return review_tag;

def get_review_list(book_num):
    review_list = [];  # 书评列表，每一篇文章是一个元素
    start=0;
    while(True):
        book_reviews_response = requests.get("https://book.douban.com/subject/%d/reviews?start=%d"%(book_num,start));
        book_reviews_soup = BeautifulSoup(book_reviews_response.text);
        src_tags = book_reviews_soup.find_all('a', {
            'href': re.compile('^https://book.douban.com/review/\d*/$')});  # 获得所有长篇评论网页的网址
        time.sleep(2);
        if(len(src_tags)==0):
            break;
        for tag in src_tags:
            # print(tag.attrs['href']);
            text_tag = get_review_tag(tag.attrs['href']);
            p_tags = text_tag.find_all('p');
            text = "";
            if(len(p_tags)==0):
                text=text_tag.text;
                text = re.sub('[a-z]|[A-Z]', '', text);  # 清洗数据
            else:
                for p_tag in p_tags:
                    text = text + p_tag.text;
                    text = re.sub('[a-z]|[A-Z]', '', text);  # 清洗数据
            print(text);
            review_list.append(text);
        start=start+20;
    return review_list;

def train_model(texts_list,src):#使用jieba库和gensim生成model,texts_list为一个文本数组，元素为文本，src为model的路径。
    word_list = [];
    for doc in texts_list:#用jieba库做分词
        doc_list = [word for word in jieba.cut(doc)];
        word_list.append(doc_list);
    dictionary = corpora.Dictionary(word_list);
    corpus = [dictionary.doc2bow(doc) for doc in word_list];  # 建立语料库
    tfidf = models.TfidfModel(corpus);
    tfidf.save(src);

def get_word_list(texts_list):#切词
    word_list = [];
    for doc in texts_list:  # 用jieba库做分词
        doc_list = [word for word in jieba.cut(doc)];
        word_list.append(doc_list);
    return word_list;

def tfidf_model(corpus,text,dictionary):
    tfidf = models.TfidfModel(corpus);
    index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary.keys()));
    text_list = [word for word in jieba.cut(text)];
    text_vec = dictionary.doc2bow(text_list);
    sim = index[tfidf[text_vec]];
    sim = sorted(enumerate(sim), key=lambda item: -item[1]);
    return sim;

def lsi_model(corpus,text,dictionary):
    lsi_model = models.LsiModel(corpus, id2word=dictionary, num_topics=2);
    documents = lsi_model[corpus];
    text_list = [word for word in jieba.cut(text)];
    text_vec = dictionary.doc2bow(text_list);
    query_vec = lsi_model[text_vec];
    index = similarities.MatrixSimilarity(documents);
    sim = index[query_vec];
    sim = sorted(enumerate(sim), key=lambda item: -item[1]);
    return sim;


def main():
    file=open('test.txt','r');
    text=file.read();
    file.close();
    file=open('language_data.txt','r',encoding='utf-8');#要使用utf-8读取
    original_text_list=file.read().split('*$*');
    texts_list=get_review_list(26118072);
    texts_list.extend(original_text_list);

    word_list = get_word_list(texts_list);
    dictionary = corpora.Dictionary(word_list);
    corpus = [dictionary.doc2bow(doc) for doc in word_list];  # 建立语料库

    sim=tfidf_model(corpus,text,dictionary);
    # sim=tfidf_model(corpus,text,dictionary);

    for i in range(5):
        print(sim[i][1], ': ', texts_list[sim[i][0]]);
main();
