import json
from sklearn.model_selection import train_test_split


def merge(file_path_r1, file_path_r2):
    """将两个json文件读到同一个json数据

    :param file_path_r1: json文件1的路径
    :param file_path_r2: json文件2的路径
    :return: 合并后的json数据
    """
    with open(file_path_r1, 'r', encoding='utf8') as fp:
        json_data = json.load(fp)
    with open(file_path_r2, 'r', encoding='utf8') as fp:
        json_data_2 = json.load(fp)

    json_data.extend(json_data_2)

    return json_data


def split(json_data, size_train, size_dev, size_test):
    """将一个json数据按比例分为三部分json数据

    :param json_data: 合并的json数据
    :param size_train: 训练集占比
    :param size_dev: 验证集占比
    :param size_test: 测试集占比
    :return: 训练集、验证集、测试集的json数据
    """
    json_train, json_dt = train_test_split(json_data, random_state=10, train_size=size_train / (size_train + size_dev + size_test))
    json_dev, json_test = train_test_split(json_dt, random_state=10, train_size=size_dev / (size_dev + size_test))
    return json_train, json_dev, json_test
