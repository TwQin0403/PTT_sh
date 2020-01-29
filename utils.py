import pandas as pd
import numpy as np
import feature_engineer as feats
from sklearn_tda.preprocessing import DiagramScaler
from sklearn.preprocessing import MinMaxScaler

def compute_author(train_data):
    '''
    using the training data to compute the author's articles sh average and total count average.

    Return: dicts, the sh_ratio and total count quantile.
    '''
    tmp_df = train_data.groupby('author')[['sh_ratio','total_count']].mean()
    tmp_df['sh_ratio_range']= pd.qcut(tmp_df['sh_ratio'],q=5,labels=[0,1,2,3,4])
    tmp_df['total_count_range'] = pd.qcut(tmp_df['total_count'],q=5,labels=[0,1,2,3,4])
    sh_ratio_dict = tmp_df[['sh_ratio_range']].to_dict(orient='index')
    total_count_dict = tmp_df[['total_count_range']].to_dict(orient='index')
    return sh_ratio_dict,total_count_dict

def split(content_data):
    num_of_art = len(content_data)
    num_of_train = int(num_of_art * 0.6)
    num_of_validation = int(num_of_art * 0.2)
    num_of_test = num_of_art - num_of_train - num_of_validation
    train_data = content_data.iloc[-num_of_train:]
    validation_data = content_data.iloc[num_of_test:-num_of_train]
    test_data = content_data.iloc[:num_of_test]
    assert len(train_data) + len(validation_data) + len(test_data) == num_of_art
    return train_data,validation_data,test_data 

def compute_x(X):
    y = None
    sample_range=[np.nan, np.nan]
    pre = DiagramScaler(use=True, scalers=[([0], MinMaxScaler()), ([1], MinMaxScaler())]).fit(X,y)
    [mx,my],[Mx,My] = [pre.scalers[0][1].data_min_[0], pre.scalers[1][1].data_min_[0]], [pre.scalers[0][1].data_max_[0], pre.scalers[1][1].data_max_[0]]
    sample_range = np.where(np.isnan(np.array(sample_range)), np.array([mx, My]), np.array(sample_range))
    num_diag, Xfit = len(X), []
    x_values = np.linspace(sample_range[0], sample_range[1], 100)
    step_x = x_values[1] - x_values[0]
    return step_x

def lambda_1_norm(Y_values,X):
    step_x = compute_x(X)
    def L1_norm(y_values):
        return np.sum(np.absolute(y_values)*step_x)
    return sum([L1_norm(y_values) for y_values in Y_values])

def lambda_2_norm(Y_values,X):
    step_x = compute_x(X)
    def L2_norm(y_values):
        return np.sum(np.absolute(y_values)**2*step_x)
    return (sum([L2_norm(y_values) for y_values in Y_values]))**(1/2)

def merge_feats(data,source_feats,title_feats,reporter_feats,week_feats):
    author_feats = data[['sh_ratio_range','total_count_range','is_remark','l1_norm']].values
    source_feats = source_feats[data.index,:]
    title_feats = title_feats[data.index,:]
    reporter_feats =  reporter_feats[data.index,:]
    week_feats = week_feats[data.index,:]
    total_feats = np.append(title_feats,author_feats,axis=1)
    # total_feats = np.append(author_feats,source_feats,axis=1)
    total_feats = np.append(total_feats,source_feats,axis=1)
    total_feats = np.append(total_feats,reporter_feats,axis=1)
    total_feats = np.append(total_feats,week_feats,axis=1)
    return total_feats
