import pandas as pd
import re

source_dict = {
'新唐人':1,
'大紀元':2,
'聯合報':2,
'聯合':2,
'中央社':3,
'中央通訊社':4,
'中央廣播電台':5,
'Rti中央廣播電臺':5,
'rti':5,
'rti2':5,
'中廣':5,
"CNA":5,
'cna':5,
'中廣新聞網':5,
'TVBS新聞':6,
'TVBS':6,
'中廣新聞網':5,
'cdns':7,
'鏡周刊':8,
'sina':9,
'台視':10,
'中時電子報':11,
'中時':11,
'中時電子時報':11,
'ChinaTimes':11,
'中國時報':11,
'三立':12,
'3立':12,
'setn':12,
'三立新聞網':12,
'SETN三立新聞網':12,
'自由時報':13,
'自由電子報':13,
'ltn':13,
'LTN':13,
'民視新聞':14,
'民視':14,
'ETtoday':15,
'ETTODAY':15,
'東森 ETtoday':15,
'新聞雲':15,
'東森ETtoday':15,
'東森':15,
'東森新聞':15,
'EBC':15,
'ET':15,
'ETtoday新聞雲':15,
'Ettoday':15,
'ettoday':15,
'Etoday':15,
'ettdoay':15,
'ettdoay2':15,
'Et':15,
'yahoo':16,
'YAHOO奇摩':16,
'Yahoo':16,
'蕃薯藤新聞':17,
'udn':2,
'聯合新聞網':2,
'UDN':2,
'蘋果日報':18,
'apple':18,
'蘋果即時':18,
'蘋果':18,
'今日新聞':19,
':今日':19,
'NOWnews':19,
'nownews':19,
'NOWNEWS':19,
'鉅亨網':20,
'東森財經新聞':21,
'經濟日報':22,
'工商':23,
'工商時報':23,
'財訊':24,
'CTWANT':26,
'ithome':27,
'ITHOME':27,
'TechNews':28,
'商周':29,
'華視':30,
'公視新聞網':31,
'公視':31,
'公共電視':31,
'上報':32,
'upmedia':33,
'新頭殼newtalk':33,
'新頭殼':33,
'NEW頭殼':33,
'Newtalk':33,
'newtalk':33,
'newtalk2':33,
'NEWTALK':33,
'風傳媒':34,
'台灣醒報':35,
'芋傳媒':36,
'BBC':37,
'BBC中文網':37,
'英國衛報':38,
'英國金融時報':39,
'金融時報':40,
'日本経済新聞':41,
'読売新聞':42,
'朝日新聞':43,
'NHK':44,
'読売新聞':45,
'美國之音':46,
'世界日報':47,
'Fox news':48,
'外電':49,
':東亞日報':50,
}

def main():
    content_data = pd.read_csv('crawlar/pttData.csv')

    def count_push(txt):
        try:
            sh_list = txt.split('\t')
            return len(sh_list)-1
        except:
            return 0
    def select_source(text):
        for key in source_dict.keys():       
            try:
                re.findall(key,text)[0]
                return source_dict[key]
            except:
                continue 
    

    def select_reporter(text):
        try:
            result = re.findall('記者署名(.+?)3.',text)[0].replace('編譯','').replace(' ','').replace('報導','').replace(':','').replace('記者','').replace('〔','').replace('：','').replace('經濟日報','').split('／')[0][:3]
            if type(result) == str:
                return result
        except:
            return 

    def select_content(text):
        try:
            return re.findall('4.完整新聞內文:(.+)5',text)[0]
        except:
            return text
        
    def select_remark(text):
        try:
            result = re.findall('備註:(.+)',text)[0]
            if result == '--':
                return 0
            elif result.split(' ')[0] =='-----Sent':
                return 0
            else:
                return 1
        except:
            return 0
    
    content_data['sh_count'] = content_data['negative_push'].apply(count_push)
    content_data['push_count'] = content_data['positive_push'].apply(count_push)
    content_data['neutral_count'] = content_data['neutral_push'].apply(count_push)
    content_data['total_count'] = content_data['push_count'] + content_data['neutral_count'] + content_data['sh_count']
    content_data['sh_ratio'] = content_data['sh_count']/content_data['total_count']
    content_data['title'] = content_data['title'].apply(lambda x: ''.join(x.split(' ')[1:]))
    content_data['author'] = content_data['author'].apply(lambda x: x.split(' ')[0][2:])
    content_data['main_content'] = content_data['main_content'].apply(lambda x: x.replace('\t',''))
    content_data['source'] = content_data['main_content'].apply(select_source).fillna(0)
    content_data['reporter'] = content_data['main_content'].apply(select_reporter).fillna('無')
    content_data['content'] = content_data['main_content'].apply(select_content)
    content_data['is_remark'] = content_data['main_content'].apply(select_remark)
    content_data['time'] = content_data['time'].apply(lambda x:pd.to_datetime(x.split(' ')[0]))
    return content_data