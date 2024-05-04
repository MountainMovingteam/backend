import datetime

begin_day = datetime.datetime.strptime("2024-2-26", "%Y-%m-%d")


def get_week_num():
    now = datetime.datetime.now()
    day_diff = (now - begin_day).days
    return (day_diff // 7) + 1


def get_week_day():
    now = datetime.datetime.now()
    return now.weekday()


def trans_index(time_index):
    # 相对-> 绝对
    flag = time_index > 28  # 0-学院路 1-沙河
    if time_index > 28:
        index1 = time_index - 28
    else:
        index1 = time_index
    index2 = index1 + 4 * get_week_day()
    new_week_num = get_week_num() + index2 // 29
    if index2 > 28:
        new_time_index = index2 - 28 + flag * 28
    else:
        new_time_index = index2 + flag * 28

    return new_week_num, new_time_index




if __name__ == '__main__':
    get_week_num()
    get_week_day()
