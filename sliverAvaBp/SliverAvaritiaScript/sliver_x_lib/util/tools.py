import re
import random
def extract_numbers(s):
    """
    :sort的时候使用 自动获取格子内容
    """
    numbers = [int(num) for num in re.findall(r'\d+', s)]
    if numbers:
        return (numbers, s)
    else:
        return (float('inf'), s)
    
def random_pos(center_pos, r):
    """
    随机获取一点坐标。
    """
    if not center_pos:
        return
    ran_x = random.randint(-r, r)
    ran_z = random.randint(-r, r)
    x = center_pos[0] + ran_x
    z = center_pos[2] + ran_z
    ran_y = random.randint(-r, r)
    y = center_pos[1] + ran_y
    return x, y, z