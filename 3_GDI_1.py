import re
import os
import wx
import datetime


class LogSearchFrame(wx.Frame):
    def __init__(self, parent, title):
        super(LogSearchFrame, self).__init__(parent, title=title, size=(800, 600))

        self.log_file = "script18.log"
        self.current_file = ""
        self.search_results = []

        # Проверка наличия файла лога
        if not os.path.exists(self.log_file):
            dlg = wx.MessageDialog(self, "Файл лога не найден. Файл будет создан автоматически",
                                   "Информация", wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

            # Создаем пустой файл лога
            with open(self.log_file, 'w', encoding='utf-8'):
                pass

        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        # Создаем панель
        panel = wx.Panel(self)

        # Создаем строку меню
        menubar = wx.MenuBar()

        # Меню "Файл"
        fileMenu = wx.Menu()
        openItem = fileMenu.Append(wx.ID_OPEN, "Открыть...", "Открыть файл для поиска")
        menubar.Append(fileMenu, "Файл")

        # Меню "Лог"
        logMenu = wx.Menu()
        exportItem = logMenu.Append(wx.ID_SAVE, "Экспорт...", "Экспортировать результаты в файл")
        addToLogItem = logMenu.Append(wx.ID_ANY, "Добавить в лог", "Добавить результаты в лог")
        viewLogItem = logMenu.Append(wx.ID_ANY, "Просмотр", "Просмотреть содержимое лога")
        menubar.Append(logMenu, "Лог")

        self.SetMenuBar(menubar)

        # Привязываем события к пунктам меню
        self.Bind(wx.EVT_MENU, self.OnOpen, openItem)
        self.Bind(wx.EVT_MENU, self.OnExport, exportItem)
        self.Bind(wx.EVT_MENU, self.OnAddToLog, addToLogItem)
        self.Bind(wx.EVT_MENU, self.OnViewLog, viewLogItem)

        # Создаем список для результатов поиска
        self.resultsList = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.resultsList.InsertColumn(0, "Дата и время", width=200)
        self.resultsList.InsertColumn(1, "Файл", width=200)
        self.resultsList.InsertColumn(2, "Результаты", width=400)

        # Создаем сайзер для размещения элементов
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.resultsList, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        panel.SetSizer(vbox)

        # Создаем статусную строку
        self.statusbar = self.CreateStatusBar(2)
        self.statusbar.SetStatusWidths([-3, -2])  # 60% и 40% ширины окна
        self.statusbar.SetStatusText("", 0)
        self.statusbar.SetStatusText("", 1)

    def OnOpen(self, e):
        """Открывает файл и выполняет поиск по шаблону"""
        wildcard = "Текстовые файлы (*.txt)|*.txt|Все файлы (*.*)|*.*"
        dlg = wx.FileDialog(self, "Выберите файл", wildcard=wildcard, style=wx.FD_OPEN)

        if dlg.ShowModal() == wx.ID_OK:
            self.current_file = dlg.GetPath()
            file_size = os.path.getsize(self.current_file)

            # Устанавливаем статус
            self.statusbar.SetStatusText(f"Обработан файл {self.current_file}", 0)
            self.statusbar.SetStatusText(f"{self.format_size(file_size)} байт", 1)

            # Выполняем поиск и добавляем результаты в список
            self.search_in_file(self.current_file)

        dlg.Destroy()

    def search_in_file(self, file_path):
        """Выполняет поиск по шаблону в файле и добавляет результаты в список"""
        pattern = r'\(\d{3}\)(?:\d{7}|\d{3}-\d{2}-\d{2})'
        results = []
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    for match in re.finditer(pattern, line):
                        result = f"Строка {line_num}, позиция {match.start() + 1} : найдено '{match.group()}'"
                        results.append(result)

            if results:
                # Добавляем результаты в список
                file_name = os.path.basename(file_path)
                for result in results:
                    # Добавляем в хранилище результатов
                    self.search_results.append((timestamp, file_name, result))
                    # Добавляем в отображение
                    index = self.resultsList.InsertItem(self.resultsList.GetItemCount(), timestamp)
                    self.resultsList.SetItem(index, 1, file_name)
                    self.resultsList.SetItem(index, 2, result)

        except Exception as e:
            wx.MessageBox(f"Ошибка при обработке файла: {e}", "Ошибка", wx.OK | wx.ICON_ERROR)

    def OnExport(self, e):
        """Экспортирует результаты поиска в выбранный пользователем файл"""
        if not self.search_results:
            wx.MessageBox("Нет данных для экспорта", "Информация", wx.OK | wx.ICON_INFORMATION)
            return

        wildcard = "Текстовые файлы (*.txt)|*.txt|Все файлы (*.*)|*.*"
        dlg = wx.FileDialog(self, "Сохранить результаты", wildcard=wildcard, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if dlg.ShowModal() == wx.ID_OK:
            file_path = dlg.GetPath()

            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    for timestamp, file_name, result in self.search_results:
                        f.write(f"{timestamp} | {file_name} | {result}\n")

                wx.MessageBox(f"Результаты успешно экспортированы в файл {file_path}",
                              "Успех", wx.OK | wx.ICON_INFORMATION)

            except Exception as e:
                wx.MessageBox(f"Ошибка при экспорте: {e}", "Ошибка", wx.OK | wx.ICON_ERROR)

        dlg.Destroy()

    def OnAddToLog(self, e):
        """Добавляет результаты поиска в файл лога"""
        if not self.search_results:
            wx.MessageBox("Нет данных для добавления в лог", "Информация", wx.OK | wx.ICON_INFORMATION)
            return

        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                for timestamp, file_name, result in self.search_results:
                    f.write(f"{timestamp} | {file_name} | {result}\n")

            wx.MessageBox(f"Результаты успешно добавлены в лог", "Успех", wx.OK | wx.ICON_INFORMATION)

        except Exception as e:
            wx.MessageBox(f"Ошибка при добавлении в лог: {e}", "Ошибка", wx.OK | wx.ICON_ERROR)

    def OnViewLog(self, e):
        """Отображает содержимое файла лога"""
        if self.search_results:
            dlg = wx.MessageDialog(self,
                                   "Вы действительно хотите открыть лог? Данные последних поисков будут потеряны!",
                                   "Подтверждение",
                                   wx.YES_NO | wx.ICON_QUESTION)

            if dlg.ShowModal() != wx.ID_YES:
                dlg.Destroy()
                return

            dlg.Destroy()

        # Очистка текущего списка результатов
        self.resultsList.DeleteAllItems()
        self.search_results = []

        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split(" | ", 2)
                    if len(parts) == 3:
                        timestamp, file_name, result = parts

                        # Добавляем в хранилище результатов
                        self.search_results.append((timestamp, file_name, result))

                        # Добавляем в отображение
                        index = self.resultsList.InsertItem(self.resultsList.GetItemCount(), timestamp)
                        self.resultsList.SetItem(index, 1, file_name)
                        self.resultsList.SetItem(index, 2, result)

            # Обновляем статусную строку
            self.statusbar.SetStatusText("Открыт лог", 0)
            self.statusbar.SetStatusText("", 1)

        except Exception as e:
            wx.MessageBox(f"Ошибка при чтении лога: {e}", "Ошибка", wx.OK | wx.ICON_ERROR)

    def format_size(self, size):
        """Форматирует размер файла, добавляя пробелы между разрядами"""
        return f"{size:,}".replace(',', ' ')


def main():
    app = wx.App()
    LogSearchFrame(None, title='Поиск по шаблону')
    app.MainLoop()


if __name__ == '__main__':
    main()