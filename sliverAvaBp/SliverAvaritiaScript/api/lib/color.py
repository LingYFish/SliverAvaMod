class ColorGradientText:
    def __init__(self, text, color_list):
        self.text = unicode(text, 'utf-8').encode('utf-8')  # type: str
        self.color_list = color_list  # type: list

    def __color__(self):
        _text = ''
        for char in self.text.decode('utf-8'):
            if _text != ";":
                _text += '§' + str(self.color_list[0]) + char.encode('utf-8')
            else:
                _text += "\n"
            self.color_list.append(self.color_list.pop(0))
        return _text


    def __str__(self):
        return self.__color__()