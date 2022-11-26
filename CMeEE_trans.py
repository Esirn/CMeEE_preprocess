import json
import CMeEE_utils


def jf2jd(file_path_r):
    with open(file_path_r, 'r', encoding='utf8') as fp:
        json_data = json.load(fp)
    return json_data


def jd2jf(json_data, file_path_w):
    with open(file_path_w, 'w', encoding='utf8') as fp:
        json.dump(json_data, fp, indent=2, ensure_ascii=False)


def jd2bf(json_data, file_path_w):
    with open(file_path_w, mode='w', encoding='utf-8') as file_obj:
        for sentence in json_data:
            entities = sentence['entities']  # 引用
            entity_idx = 0
            entities.sort(key=CMeEE_utils.entities_order_idx)
            while entity_idx + 1 < len(entities):
                if entities[entity_idx]['end_idx'] < entities[entity_idx + 1]['start_idx']:
                    entity_idx = entity_idx + 1
                else:
                    del entities[entity_idx]
                    entity_idx = 0

            entity_idx = 0
            for char_index in range(len(sentence['text'])):
                label = ''  # 本行应该可删
                if entity_idx < len(entities):
                    entity = entities[entity_idx]  # 引用
                    if entity['start_idx'] <= char_index <= entity['end_idx']:
                        if entity['start_idx'] == entity['end_idx']:
                            label = 'S-' + entity['type']
                            entity_idx = entity_idx + 1
                        elif char_index == entity['start_idx']:
                            label = 'B-' + entity['type']
                        elif char_index == entity['end_idx']:
                            label = 'E-' + entity['type']
                            entity_idx = entity_idx + 1
                        else:
                            label = 'M-' + entity['type']
                    else:
                        label = 'O'
                elif entity_idx == len(entities):
                    label = 'O'

                file_obj.write(sentence['text'][char_index] + ' ' + label + '\n')
            file_obj.write('\n')


def bf2jd(file_path_r):
    with open(file_path_r, encoding='utf-8') as file_obj:
        lines = file_obj.readlines()

    json_data = []
    text = ''
    entities = []

    line_idx = 0
    flag = ''
    entity_dict = {}
    for line in lines:
        if line != '\n':
            text += line[0]
            if line[2] == 'O':
                if flag not in ['', 'O', 'S', 'E']:
                    print('Wrong! flag: ', flag, '\n\t', line)
                    # 若 B/M 接 O，则将实体缓存清空
                    entity_dict.clear()

            elif line[2] == 'B':
                if flag not in ['', 'O', 'S', 'E']:
                    print('Wrong! flag: ', flag, '\n\t', line)
                    # 若 B/M 接 B，则将旧实体清零，start_idx更新
                entity_dict['start_idx'] = line_idx
                entity_dict['entity'] = line[0]
            elif line[2] == 'M':
                if flag not in ['B', 'M']:
                    print('Wrong! flag: ', flag, '\n\t', line)
                    # 若 E/S/O 接 M，则应该无实体缓存可清，将其视为O，什么都不做
                else:
                    entity_dict['entity'] += line[0]
            elif line[2] == 'E':
                if flag not in ['B', 'M']:
                    print('Wrong! flag: ', flag, '\n\t', line)
                    # 若 E/S/O 接 E，则将其视为O，什么都不做
                else:
                    entity_dict['entity'] += line[0]
                    entity_dict['type'] = line[4:-1]
                    entity_dict['end_idx'] = line_idx
                    if entity_dict.__contains__('start_idx'):
                        entities.append(entity_dict.copy())
                        # entities.append(copy.copy(entity_dict))
                    entity_dict.clear()
            elif line[2] == 'S':
                if flag not in ['', 'O', 'S', 'E']:
                    print('Wrong! flag: ', flag, '\n\t', line)
                    # 若 B/M 接 S，则忽视旧信息，只看当前S
                entity_dict = {
                    'start_idx': line_idx,
                    'end_idx': line_idx,
                    'type': line[4:-1],
                    'entity': line[0]}
                entities.append(entity_dict.copy()) # 要拷贝，否则是引用
                entity_dict.clear()
            line_idx += 1
            flag = line[2]
        else:
            sentence = {
                'text': text,
                'entities': entities
            }
            json_data.append(sentence)
            line_idx = 0
            text = ''
            entities = []
            flag = ''
            entity_dict.clear()
    return json_data


def jf2bf(file_path_r, file_path_w):
    json_data = jf2jd(file_path_r)
    jd2bf(json_data, file_path_w)


def bf2jf(file_path_r, file_path_w):
    json_data = bf2jd(file_path_r)
    jd2jf(json_data, file_path_w)
