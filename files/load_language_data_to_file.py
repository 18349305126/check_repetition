import requests;
from bs4 import  BeautifulSoup;
import re;
import time;
import random;

def get_certain_web_texts(start_num,end_num):#数字从1000000到10220000
    web_text_list=[];
    while(start_num<end_num):
        rand_num=random.randint(2,1000);#平均步长为50，所以最终随机访问的页面为(end_num-start_num)/50
        response = requests.get("https://book.douban.com/review/%d/" % (start_num));
        soup = BeautifulSoup(response.text);

        tag = soup.find('div', {'class': 'review-content clearfix'});
        if(tag!=None):
            p_tags = tag.find_all('p');
            if (len(p_tags) == 0):
                text=tag.text;
                text=re.sub('[a-z]|[A-Z]|','',text);#清洗数据
                web_text_list.append(text);
                print(text);
            else:
                for p_tag in p_tags:
                    text = p_tag.text;
                    text = re.sub('[a-z]|[A-Z]', '',text);#清洗数据
                    web_text_list.append(text);

        start_num=start_num+rand_num;
        time.sleep(3);
    return web_text_list;

def load_all_web_text(start_num,end_num,src):#随机生成一些数字，对应随机的网页（因为网页数据太多，无法全部读完）
    while(start_num<end_num):
        text_small_list = get_certain_web_texts(start_num, start_num+10000);
        text = '*$*'.join(text_small_list);#'*$*‘作为分隔符
        print(text);
        file = open(src, 'a', encoding='utf-8');
        file.write(text);
        file.close();
        start_num=start_num+20000;
        print(start_num);#当程序意外停止时记录当前的数值，以便接下来继续
        time.sleep(5);

def main():
    load_all_web_text(1019231,10220000,'language_data.txt');

    # file=open('language_data.txt','r',encoding='utf-8');#要使用utf-8读取
    # text_list=file.read().split('*$*');
    # for text in text_list:
    #     print(text);
main();