class Taggable:
    def tag(self):
        raise NotImplementedError("Метод tag() должен быть переопределен")


class Book(Taggable):
    # Статический член для автоматического назначения кода книги
    __code_counter = 1

    def __init__(self, author, title):
        if not title:
            raise ValueError("Название книги не может быть пустым")

        self.__author = author
        self.__title = title
        self.__code = None  # Код будет назначен при добавлении в библиотеку

    def get_author(self):
        return self.__author

    def get_title(self):
        return self.__title

    def set_code(self, code):
        self.__code = code

    def get_code(self):
        return self.__code

    @staticmethod
    def get_next_code():
        next_code = Book.__code_counter
        Book.__code_counter += 1
        return next_code

    def __str__(self):
        # Формат: [код] И.Автор 'Название'
        author_parts = self.__author.split()
        author_initials = author_parts[0][0] + "."
        author_last_name = author_parts[-1]
        return f"[{self.__code}] {author_initials}{author_last_name} '{self.__title}'"

    def tag(self):
        # Разбиваем название на слова и возвращаем те, что начинаются с большой буквы
        words = self.__title.split()
        return [word for word in words if word and word[0].isupper()]


class Library:
    def __init__(self, number, address):
        self.__number = number
        self.__address = address
        self.__books = []

    def __iadd__(self, book):
        # Назначаем код книге и добавляем в библиотеку
        book.set_code(Book.get_next_code())
        self.__books.append(book)
        return self

    def __iter__(self):
        # Позволяет итерироваться по книгам в библиотеке
        return iter(self.__books)


lib = Library(1, '51 Some str., NY')
lib += Book('Leo Tolstoi', 'War and Peace')
lib += Book('Charles Dickens', 'David Copperfield')

for book in lib:
    print(book)
    print(book.tag())