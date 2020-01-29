import re
import pandas as pd
import numpy as np
import data_processing as data_pro
import utils 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import LabelEncoder
from ripser import Rips
from sklearn_tda.vector_methods import Landscape
import jieba.analyse
jieba.set_dictionary("jieba_dict/dict.txt.big")

# title -> word vector
def title_transform(df):
    use_list = []
    for title in df['title']:
        tags = jieba.analyse.extract_tags(title)
        result = ' '.join(tags)
        # print(result)
        use_list.append(result)
    docs = np.array(use_list)
    count = CountVectorizer()
    tfidf = TfidfTransformer()
    word_vector = tfidf.fit_transform(count.fit_transform(docs)).toarray()
    tmp_df = pd.DataFrame(count.fit_transform(docs).toarray()).iloc[-9643:]
    title_feats = word_vector[:,tmp_df.loc[:, tmp_df.any()].columns]
    return title_feats

#The way to fill the author_feats
def fill_way(name,name_dict):
    try:
        return list(name_dict[name].values())[0]
    except:
        return 0

def content_transform(df):
    use_list = []
    for content in df['content']:
        tags = jieba.analyse.extract_tags(content)
        result = ' '.join(tags)
        use_list.append(result)
    docs = np.array(use_list)
    count = CountVectorizer()
    tfidf = TfidfTransformer()
    word_vector = tfidf.fit_transform(count.fit_transform(docs)).toarray()
    tmp_df = pd.DataFrame(count.fit_transform(docs).toarray()).iloc[-9643:]
    content_feats = word_vector[:,tmp_df.loc[:, tmp_df.any()].columns]
    return content_feats

def content_topology(df):
    norm_list = []
    for content in df['content']:
        sentences = re.split('(。|！|\!|\.|？|\?)',content)     
        new_sents = []
        for i in range(int(len(sentences)/2)):
            sent = sentences[2*i] + sentences[2*i+1]
            new_sents.append(sent)
        use_list = []
        for sent in new_sents:
            tags = jieba.analyse.extract_tags(content)
            result = ' '.join(tags)
            use_list.append(result)
        docs = np.array(use_list)
        count = CountVectorizer()
        tfidf = TfidfTransformer()

        try:
            result = tfidf.fit_transform(count.fit_transform(docs)).toarray()
        except:
            norm_list.append(0)
            continue

        result = Rips().fit_transform(result)
        result[0] = np.delete(result[0],-1,0)
        result = np.concatenate((result[0], result[1]), axis=0)
        landscape_model = Landscape(num_landscapes=len(result))
        try:
            landscape = landscape_model.fit_transform([result])
        except:
            norm_list.append(0)
            continue
        length = int(len(landscape[0])/100)
        Y_values = [landscape[0][i:(i+1)*100] for i in range(length)]
        norm_list.append(utils.lambda_1_norm(Y_values,[result]))
    return norm_list

def main():
    #Load the data
    content_data =  data_pro.main()

    #title_feats
    title_feats = title_transform(content_data)

    #source_feats
    source_feats = pd.get_dummies(content_data['source']).values

    #reporter_feats
    reporter_feats = pd.get_dummies(content_data['reporter']).values

    #week_feats
    week_feats = pd.get_dummies(content_data['week']).values

    #topology_feat
    try:
        content_data['l1_norm'] = pd.read_csv('l1_norm.csv')['l1_norm'] 
    except:
        print('csv file not found recalculate')
        content_data['l1_norm'] = content_topology(content_data)
    
    train_data,_,_ = utils.split(content_data)
    sh_ratio_dict,total_count_dict = utils.compute_author(train_data)
    content_data['sh_ratio_range'] = content_data['author'].apply(lambda x: fill_way(x,sh_ratio_dict))
    content_data['total_count_range'] = content_data['author'].apply(lambda x:fill_way(x,total_count_dict))
    return title_feats,source_feats,reporter_feats,week_feats,content_data

if __name__ == '__main__':
    main()