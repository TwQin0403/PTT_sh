import requests
from bs4 import BeautifulSoup as bs4
import logging
import json
import time
# import pdb

class PTTData():

    def __init__(self):
        self.url = 'https://www.ptt.cc/bbs/Gossiping/index37133.html'
        self.articles_list = []

    def Connect(self):
        self.r = requests.session()
        payload = { 
                    'from':'/bbs/Gossiping/index.html',
                    'yes':'yes'

                    }
        self.r.post("https://www.ptt.cc/ask/over18?from=%2Fbbs%2FGossiping%2Findex.html",payload)
        page = self.r.get(self.url)
        soup = bs4(page.text,'lxml')
        articles = soup.select('div.title a') 
        self.Articles(articles)
        paging = soup.select("div.btn-group-paging a")
        self.url = 'https://www.ptt.cc' + paging[1]['href']

    def Articles(self,articles):
        for article in articles:
            if not article.text.split(' ')[0] == '[新聞]':
                continue
            print(article.text,article['href'])
            article_page = self.r.get('http://www.ptt.cc'+article['href'])
            article_soup = bs4(article_page.text,'lxml')
            
            try:
                author = article_soup.find_all('div',{'class':'article-metaline'})[0].text
                time = article_soup.find_all('div',{'class':'article-metaline'})[2].text.replace('時間','')
            except IndexError as e:
                print(article['href'])
                print(e)
                continue
            content = article_soup.find('div',{'id':"main-content",'class':"bbs-screen bbs-content"})
            main_content = content.find_all(text = True , recursive = False)
            main_content = ''.join(main_content)
            push_content = content.find_all('div',{'class',"push"})
            push_content = [push.text for push in push_content]
            positive_push = []
            negative_push = []
            neutral_push = [] 
            for push in push_content:
                attitude = push.split(' ')[0]
                if attitude == '噓':
                    negative_push.append(push)
                elif attitude == '推':
                    positive_push.append(push)
                else:
                    neutral_push.append(push)
            
            result_dict = {
                    'title':article.text,
                    'author':author,
                    'time':time,
                    'main_content':main_content,
                    'positive_push':positive_push,
                    'negative_push':negative_push,
                    'neutral_push':neutral_push,
                    }
            self.articles_list.append(result_dict) 

    def GetPTTData(self,pages = 1000):
        for page in range(pages):
            self.Connect()
        return self.articles_list

if __name__ == '__main__':
    Data = PTTData()
    articles = Data.GetPTTData()
    with open('test.txt','w') as file:
        json.dump(articles, file)