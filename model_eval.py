import utils
import feature_engineer as feats
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

title_feats,source_feats,reporter_feats,week_feats,content_data = feats.main()
train_data,validation_data,test_data = utils.split(content_data)
train_feats = utils.merge_feats(train_data,source_feats,title_feats,reporter_feats,week_feats)
val_feats = utils.merge_feats(validation_data,source_feats,title_feats,reporter_feats,week_feats)
test_feats = utils.merge_feats(test_data,source_feats,title_feats,reporter_feats,week_feats)
train_labels = train_data['sh_count'].values
val_labels = validation_data['sh_count'].values
test_labels = test_data['sh_count'].values

def baseline(train_data,validation_data,test_data):
    benchmark_answer_val = np.array([train_data['sh_count'].mean()] * len(validation_data))
    benchmark_answer_test = np.array([train_data['sh_count'].mean()] * len(test_data))
    score_val = mean_absolute_error(validation_data['sh_count'].values,benchmark_answer_val)
    score_test = mean_absolute_error(test_data['sh_count'].values,benchmark_answer_test)
    print('val_score = {}'.format(score_val))
    print('test_score = {}'.format(score_test))


def rf(train_feats,val_feats,test_feats,train_labels,val_labels,test_labels):
    reg = RandomForestRegressor(random_state=0)
    reg.fit(train_feats,train_labels)
    val_prediction= reg.predict(val_feats)
    test_prediction = reg.predict(test_feats)
    score_val = mean_absolute_error(val_labels,val_prediction)
    score_test = mean_absolute_error(test_labels,test_prediction)
    print('val_score = {}'.format(score_val))
    print('test_score = {}'.format(score_test))


if __name__ == '__main__':
    baseline(train_data,validation_data,test_data)
    rf(train_feats,val_feats,test_feats,train_labels,val_labels,test_labels)