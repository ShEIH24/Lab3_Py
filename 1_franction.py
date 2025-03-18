# Класс для предоставления дробей
class Franction:
    def __init__(self, num, den):
        self.__num = num
        self.__den = den
        self.reduce()

    def __str__(self):
        return "%d/%d" % (self.__num, self.__den)

    def reduce(self):
        g = Franction.gcd(self.__num, self.__den)
        self.__num //= g
        self.__den //= g

    # Метод для унарного минуса
    def __neg__(self):
        return Franction(-self.__num, self.__den)

    # Метод для оператора ~
    def __invert__(self):
        return Franction(self.__den, self.__num)

    # Метод для возведения в степень
    def __pow__(self, power, modulo=None):
        return Franction(self.__num ** power, self.__den ** power)

    # Метод для преобразования в float
    def __float__(self):
        return self.__num / self.__den

    # Метод для преобразования в int
    def __int__(self):
        return self.__num // self.__den

    @staticmethod
    def gcd(n ,m):
        if m == 0:
            return n
        else:
            return Franction.gcd(m, n % m)

frac = Franction(15, 4)
print(-frac)
print(~frac)
print(frac ** 2)
print(float(frac))
print(int(frac))
