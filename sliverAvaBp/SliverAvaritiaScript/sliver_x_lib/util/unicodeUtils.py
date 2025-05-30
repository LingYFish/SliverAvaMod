
def UnicodeConvert(input):
    """
    辅助函数 -- 把unicode编码的字符串、字典或列表转换成utf8编码
    """
    if isinstance(input, dict):
        return {UnicodeConvert(key): UnicodeConvert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [UnicodeConvert(element) for element in input]
    elif isinstance(input, tuple):
        tmp = [UnicodeConvert(element) for element in input]
        return tuple(tmp)
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    return input