from CMeEE_trans import *
from CMeEE_reshape import *
import CMeEE_stats
import CMeEE_wash
import os

os.makedirs('./o/reshape', exist_ok=True)
os.makedirs('./o/stats', exist_ok=True)
os.makedirs('./o/wash', exist_ok=True)
os.makedirs('./o/trans', exist_ok=True)

if __name__ == '__main__':
    tasks = {
        '1': '离线训练：将在线train-dev重新分配为离线train-dev-test',
        '2': '预测：将在线test.json转为test.CMeEE.bmes',
        '3': '在线提交：将预测test.CMeEE.out.bmes转为test.CMeEE.out.json'
    }

    task = 1

    if task == 1:
        print('【合并】 train集与dev集 并写入文件...')
        json_data_all = merge('i/CMeEE_train.json', 'i/CMeEE_dev.json')
        jd2jf(json_data_all, 'o/reshape/CMeEE_all.json')
        print('Done.')

        print('【清洗】 合并后的数据 并写入文件...')
        json_data_all_washed = CMeEE_wash.main(json_data_all)
        jd2jf(json_data_all_washed, 'o/wash/CMeEE_all_washed.json')
        print('Done.')

        print('【统计】 清洗后的数据 并写入文件...')
        CMeEE_stats.main(
            json_data_all_washed,
            '清洗后（不洗长句子）',
            'o/stats/CMeEE_all_washed_sentence.csv',
            'o/stats/CMeEE_all_washed_entities.csv',
            'o/stats/CMeEE_sum.csv')
        print('Done.')

        print('【划分并转化】 清洗后的数据 并写入文件...')
        json_train, json_dev, json_test = split(json_data_all, 7, 2, 1)
        jd2bf(json_train, 'o/trans/train.char.bmes')
        jd2bf(json_dev, 'o/trans/dev.char.bmes')
        jd2bf(json_test, 'o/trans/test.char.bmes')
        print('Done.')

    elif task == 2:
        jf2bf('i/CMeEE_test.json', 'o/trans/test.CMeEE.bmes')
        json_test = bf2jd('o/trans/test.CMeEE.bmes')
        CMeEE_stats.main(
            json_test,
            'test.bmes 预测前',
            'o/stats/test_1_sentence.csv',
            'o/stats/test_1_entities.csv',
            'o/stats/test_sum.csv')

    elif task == 3:
        json_output = bf2jd('o/CMeEE_out.bmes')
        jd2jf(json_output, 'o/CMeEE-test.json')
        CMeEE_stats.main(
            json_output,
            'test.bmes 预测后',
            'o/stats/test_2_sentence.csv',
            'o/stats/test_2_entities.csv',
            'o/stats/test_sum.csv')
