import string


def entities_order_idx(e_info):
    return e_info['end_idx'], -e_info['start_idx']


def entities_order_id(e_info):
    return e_info['id']


def is_nested(e_info_1, e_info_2):
    if e_info_1['end_idx'] < e_info_2['start_idx'] or \
            e_info_2['end_idx'] < e_info_1['start_idx']:
        return False
    else:
        return True


def str_count(text):
    """找出字符串中的中英文、空格、数字、空格、标点符号个数"""
    count_zh = count_en = count_dg = count_sp = count_pu = 0

    for s in text:
        # 英文
        if s in string.ascii_letters:
            count_en += 1
        # 数字
        elif s.isdigit():
            count_dg += 1
        # 空格
        elif s.isspace():
            count_sp += 1
        # 中文
        elif s.isalpha():
            count_zh += 1
        # 特殊字符
        else:
            count_pu += 1
    en_per_len = count_en / len(text)
    return count_zh, count_en, count_dg, count_sp, count_pu, en_per_len
