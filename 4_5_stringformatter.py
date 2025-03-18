import wx

class StringFormatter:
    def __init__(self, delimiter = ' '):
        """Инициализация с делителем"""
        self.delimiter = delimiter

    def delete_words(self, string, n):
        """Удаление всех слов из строки, длина которых меньше n"""
        words = string.split(self.delimiter)
        filtered_words = [word for word in words if len(word) >= n]
        return self.delimiter.join(filtered_words)

    @staticmethod
    def replace_digits(string):
        """Замена всех цифр на *"""
        result = ''
        for char in string:
            if char.isdigit():
                result += '*'
            else:
                result += char
        return result

    @staticmethod
    def insert_spaces(string):
        """Вставка по одному пробелу между всеми символами"""
        result = ' '.join(string)
        return result

    def sort_by_size(self, string):
        """Сортировка слов по размеру"""
        words = string.split(self.delimiter)
        sorted_words = sorted(words, key = len)
        return self.delimiter.join(sorted_words)

    def sort_lexicographically(self, string):
        """Сортировка слов в лексикографическом порядке"""
        words = string.split(self.delimiter)
        sorted_words = sorted(words)
        return self.delimiter.join(sorted_words)

class StringFormatterDemo(wx.Frame):
    """Графическое приложение"""
    def __init__(self, parent, title):
        super(StringFormatterDemo, self).__init__(parent, title = title, size = (400, 400))

        self.formatter = StringFormatter()
        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        """Инициализация интерфейса"""
        panel = wx.Panel(self)

        self.create_components(panel)
        self.layout_components()

    def create_components(self, panel):
        """Создание компонентов интерфейса"""
        wx.StaticText(panel, label = 'Строка', pos = (10, 20))
        self.input_text = wx.TextCtrl(panel, pos = (100, 15), size = (280, -1))

        self.check_delete = wx.CheckBox(panel, label = 'Удалить слова размером меньше', pos = (10, 50))
        self.check_delete.SetValue(True)

        self.min_length = wx.SpinCtrl(panel, min = 1, max = 100, initial = 5, pos = (250, 50), size = (40, -1))
        wx.StaticText(panel, label = 'букв', pos = (300, 50))

        self.check_replace = wx.CheckBox(panel, label = 'Заменить все цифры на "*"', pos = (10, 80))
        self.check_replace.SetValue(True)

        self.check_spaces = wx.CheckBox(panel, label = 'Вставить по пробелу между символами', pos = (10, 110))
        self.check_spaces.SetValue(True)

        self.check_sort = wx.CheckBox(panel, label = 'Сортировать слова в строке', pos = (10, 140))
        self.check_sort.SetValue(True)

        """Методы сортировки"""
        self.radio_size = wx.RadioButton(panel, label = 'По размеру', pos = (40, 170), style = wx.RB_GROUP)
        self.radio_lex = wx.RadioButton(panel, label = 'Лексикографически', pos = (40, 200))
        self.radio_lex.SetValue(True)

        """Кнопка форматирования"""
        self.format_button = wx.Button(panel, label = 'Форматировать', pos = (150, 230))
        self.format_button.Bind(wx.EVT_BUTTON, self.on_format)

        """Поле результата"""
        wx.StaticText(panel, label = 'Результат:', pos = (10, 270))
        self.output_text = wx.TextCtrl(panel, pos = (100, 265), size = (280, -1), style = wx.TE_READONLY)

    def layout_components(self):
        """Размещение компонентов"""
        pass

    def on_format(self, event):
        """Обработчик нажатия на кнопку"""
        input_string = self.input_text.GetValue()
        result = input_string

        """Удаление слов меньше заданной длины"""
        if self.check_delete.GetValue():
            min_len = self.min_length.GetValue()
            result = self.formatter.delete_words(result, min_len)

        """Замена цифр на символ *"""
        if self.check_replace.GetValue():
            result = self.formatter.replace_digits(result)

        """Сортировка слов"""
        if self.check_sort.GetValue():
            if self.radio_size.GetValue():
                result = self.formatter.replace_digits(result)
            else:
                result = self.formatter.sort_lexicographically(result)

        """Вставка пробелов между символами"""
        if self.check_spaces.GetValue():
            result = self.formatter.insert_spaces(result)

        """Результат"""
        self.output_text.SetValue(result)

def main():
    app = wx.App()
    StringFormatterDemo(None, title='StringFormatter Demo')
    app.MainLoop()

if __name__ == '__main__':
    main()