import CMeEE_utils
import time


def main(json_data, max_sentence_length=-1,
         log_file_path='./o/wash/' + time.strftime('%Y-%m-%d %H_%M_%S', time.localtime()) + '.log'):
    log_file = open(log_file_path, 'w', encoding='utf-8')
    index_s = 0
    while index_s < len(json_data):
        sentence = json_data[index_s]  # 引用
        entities = sentence['entities']  # 引用
        index_e = 0
        while index_e < len(entities):
            entity = entities[index_e]  # 引用
            if entity['start_idx'] > entity['end_idx']:
                print('Wrong! 实体头位置大于尾位置！已删除实体：', entities.pop(index_e), file=log_file)
                print('\t句子信息：', sentence, file=log_file)

            elif entity['entity'] != sentence['text'][entity['start_idx']:entity['end_idx'] + 1]:
                print('Wrong! 实体内容与句子中相应位置的内容不符！已删除实体：', entities.pop(index_e), file=log_file)
                print('\t句子信息：', sentence, file=log_file)
            else:
                index_e += 1

        if len(entities) == 0:  # 删除无实体的句子
            print('Wrong! 句中无有效实体！已删除句子：', json_data.pop(index_s), file=log_file)
        elif 0 < max_sentence_length < len(sentence['text']):
            # json_data.pop(index_s)
            print('Warning! 句子长度大于', max_sentence_length, '，已删除句子：', json_data.pop(index_s), file=log_file)

        elif len(entities) > 1:  # 实体排序
            entities.sort(key=CMeEE_utils.entities_order_idx)
            index_s += 1
        else:
            index_s += 1

    return json_data
