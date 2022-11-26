from CMeEE_utils import *
import csv
import time
import os


def main(json_data, info, file_path_w_s, file_path_w_e, file_path_w_sum):
    sum_info = {
        'info': info,
        's_num': 0,
        'e_num': 0,
        'group_num': 0,
        'time': ''
    }

    with open(file_path_w_s, 'w', newline='', encoding='utf-8') as csvfile_s:
        with open(file_path_w_e, 'w', newline='', encoding='utf-8') as csvfile_e:
            writer_s = csv.DictWriter(csvfile_s, fieldnames=[
                'id', 'len', 'text', 'num_of_entities',
                'count_zh', 'count_en', 'count_dg', 'count_sp', 'count_pu', 'en_per_len'])
            writer_s.writeheader()
            writer_e = csv.DictWriter(csvfile_e, fieldnames=[
                'id', 'len', 'text', 'from_sentence', 'start_idx', 'end_idx', 'type', 'group_id'])
            writer_e.writeheader()

            for sentence in json_data:
                count_str = str_count(sentence['text'])
                s_info = {'id': sum_info['s_num'], 'len': len(sentence['text']), 'text': sentence['text'],
                          'num_of_entities': len(sentence['entities']), 'count_zh': count_str[0],
                          'count_en': count_str[1], 'count_dg': count_str[2], 'count_sp': count_str[3],
                          'count_pu': count_str[4], 'en_per_len': count_str[5]}
                writer_s.writerow(s_info)

                sum_info['s_num'] += 1

                e_infos = []
                for entity in sentence['entities']:
                    e_info = {
                        'id': sum_info['e_num'],
                        'len': len(entity['entity']),
                        'text': entity['entity'],
                        'from_sentence': s_info['id'],
                        'start_idx': entity['start_idx'],
                        'end_idx': entity['end_idx'],
                        'type': entity['type'],
                        'group_id': -1
                    }
                    e_infos.append(e_info)
                    sum_info['e_num'] += 1

                e_infos.sort(key=entities_order_idx)

                groups = []
                e_infos_bak = []

                while len(e_infos) > 0:  # 判断嵌套并分配group_id, 0为非嵌套实体，嵌套组id从1开始

                    flag = False  # 是否已检测e_infos[0]的嵌套情况
                    if e_infos[0]['start_idx'] > e_infos[0]['end_idx']:
                        # print('Wrong! 实体头位置大于尾位置！已按非嵌套实体处理！info：', info)
                        # print('\t句子信息', sentence)
                        e_infos[0]['group_id'] = 0
                        e_infos_bak.append(e_infos.pop(0))
                        continue

                    for group in groups:  # 与已有group实体嵌套，加入该组
                        for e_info_2 in group:
                            if is_nested(e_infos[0], e_info_2):
                                e_infos[0]['group_id'] = e_info_2['group_id']
                                group.append(e_infos.pop(0))
                                flag = True
                                break
                        if flag:
                            break
                    if flag:
                        continue

                    if len(e_infos) == 1:  # 只剩一个未检测实体，且该实体没有与老组嵌套，则为非嵌套实体
                        e_infos[0]['group_id'] = 0
                        # e_infos_bak.append(e_infos.pop(0))  # 省略pop、flag、continue
                        break

                    for entity_idx in range(1, len(e_infos)):  # 与未检测实体嵌套，新建group
                        if is_nested(e_infos[0], e_infos[entity_idx]):
                            sum_info['group_num'] += 1
                            e_infos[0]['group_id'] = sum_info['group_num']
                            e_infos[entity_idx]['group_id'] = sum_info['group_num']
                            group = [e_infos.pop(entity_idx), e_infos.pop(0)]
                            groups.append(group)
                            flag = True
                            break
                    if flag:
                        continue
                    else:  # 无嵌套，group_id置零，暂时提到外面，避免多余检测
                        e_infos[0]['group_id'] = 0
                        e_infos_bak.append(e_infos.pop(0))
                        continue
                for group in groups:
                    e_infos.extend(group)
                    if len(group) > 1:
                        i = 0
                        while i < len(group):
                            if group[i]['type'] == 'sym':
                                del group[i]
                            else:
                                i += 1
                        if len(group) > 1:
                            group.sort(key=entities_order_idx)
                            j = 0
                            while j < len(group) - 1:
                                if is_nested(group[j], group[j + 1]):
                                    print('Warning! 出现除sym之外的嵌套实体：', group[j])
                                j += 1
                e_infos.extend(e_infos_bak)

                e_infos.sort(key=entities_order_id)
                writer_e.writerows(e_infos)

    flag_exist = False
    if os.path.exists(file_path_w_sum):
        flag_exist = True
    with open(file_path_w_sum, 'a', newline='', encoding='utf-8') as csvfile_sum:
        writer_sum = csv.DictWriter(csvfile_sum, fieldnames=[
            'info', 's_num', 'e_num', 'group_num', 'time'])
        if not flag_exist:
            writer_sum.writeheader()
        sum_info['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

        writer_sum.writerow(sum_info)
