# 10.  Разработайте программу, имитирующую работу транспортного агентства.
# Транспортное агентство имеет сеть филиалов в нескольких городах.
# Транспортировка грузов осуществляется между этими городами тремя видами транспорта:
# автомобильным, железнодорожным и воздушным. Любой вид транспортировки имеет стоимость
# единицы веса на единицу пути и скорость доставки. Воздушный транспорт можно
# использовать только между крупными городами, этот вид самый скоростной и самый дорогой.
# Железнодорожный транспорт можно использовать между крупными и средними городами,
# этот вид самый дешевый. Автомобильный транспорт можно использовать между любыми городами.
# Заказчики через случайные промежутки времени обращаются в один из филиалов транспортного
# агентства с заказом на перевозку определенной массы груза и возможным пожеланием о скорости/цене доставки.
# Транспортное агентство организует отправку грузов одним из видов транспорта с учетом пожеланий клиента.
#
# -Доход транспортного агентства, в том числе с разбивкой по видам транспорта и городам.
# -Среднее время доставки груза, в том числе с разбивкой по видам транспорта и городам.
# -Список исполняемых заказов с возможность сортировки по городам, видам транспорта, стоимости перевозки.
#
# from geopy import distance
#
#
# class City:
#     pass
#
# class Tranport:
#     def __init__(self, auto, avia,train, sity, distance):
#         self.auto = auto            # кол-во авто в городе
#         self.avia = avia            # кол-во самолетов в городе
#         self.train = train          # кол-во поездов в городе
#         self.sity = sity            # город
#         self.ditance = distance     # расстояние
#
#         if self.ditance > 300:
#             print(f'доставка ')
#
# class Minsk(City):
#     def garage(cls):
#         pass
#
#     @classmethod
#     def koordinat(cls):
#         dist = (53.9, 27.5667)
#         return dist
#
#
# class Vilnus(City):
#     @property
#     @classmethod
#     def koordinat(cls):
#         dist = (54.6892,25.2798)
#         return dist
#
# class Warsaw(City):
#     @property
#     @classmethod
#     def koordinat(cls):
#         dist = (52.2318, 21.0061)
#         return dist
#
#
# class Soligorsk(City):
#     @classmethod
#     def koordinat(cls):
#         dist = (52.7835, 27.5426)
#         return dist
#
# class Mogilev(City):
#     @classmethod
#     def koordinat(cls):
#         dist = (53.8942, 30.3303)
#         return dist
#
# class Brest(City):
#     @property
#     @classmethod
#     def koordinat(cls):
#         dist = (52.0966, 23.7040)
#         return dist
#
#
#
# class FinanceTA:
#     def distance_trevel(self, dest1: City, dest2: City):
#         dist = distance.geodesic(dest1, dest2).kilometers           # считает расстояние между городами
#         return dist
#
#     def cost(self,dest1,dest2,kg):
#         if self.distance_trevel(dest1,dest2)>=100 and kg <=20:
#             print(f'asd')
#
#
#
#
# TrancAg = FinanceTA()
# TrancAg.distance_trevel(Warsaw.koordinat, Vilnus.koordinat)


# class Calculator:
#
#     def init(self):
#         self._name = str()
#
#     @property
#     def name(self):
#         if Calculator.name().isalpha:
#             return self._name
#         else:
#             print('неправильно')
#
#     @classmethod
#     @name.setter
#     def name(self, name: str):
#         self._name = name
#
#
# a = Calculator()
# a.name = 234234
# print(a.name)


import sqlite3
import time

conn = sqlite3.connect('shop_box.db')
cursor = conn.cursor()
import datetime
from queiries import *
ConectionClass = Db_queiries()

# def tabl_purchases():
#     cursor.execute("""CREATE TABLE purchases (id INTEGER PRIMARY KEY AUTOINCREMENT, date_purchase TEXT, total_price REAL)""")
#     conn.commit()

class Goods:
    def __init__(self, name):
        self.name = name

    @classmethod
    def is_good(cls, name):
        good = cls(name)
        return good.good_select()


    def view_goods_in_shop(self):
        goods = ConectionClass.select_all_goods()
        for gd in goods:
            print(gd)


class Box:
    def add_goods(self, good, count):
        Db_queiries.insert_into_box(good, count)


    def del_goods(self, good):
        goods = cursor.execute("""
            SELECT goods.name, box.good_id FROM goods 
            INNER JOIN box USING (good_id)
            """)

        for gd in goods:
            if gd[0] == good:
                cursor.execute("""DELETE FROM box WHERE box.good_id == ?""", (gd[1],))
                conn.commit()
                break

    def resize_count_good(self, good, count):
        goods = cursor.execute("""
                    SELECT goods.name, box.good_id FROM goods 
                    INNER JOIN box USING (good_id)
                    """)

        for gd in goods:
            if gd[0] == good:
                cursor.execute("""UPDATE box SET count_good = ? 
                                    WHERE good_id = ?""", (count, gd[1],))
                conn.commit()
                break
        else:
            print('no goods')

    def watch_box(self):
        goods = Db_queiries.select_box()
        conn.commit()
        for pr in goods:
            print(f'{pr[0]}:{pr[1]}')

    def cost(self):
        good = cursor.execute("""SELECT sum(prime * count_good) AS 'сумма' FROM box
        INNER JOIN goods ON box.good_id = goods.good_id""")
        for pr in good:
            return pr[0]

    def del_all_in_box(self):
        cursor.execute("""DELETE FROM box""")
        conn.commit()


# class History_order:
#     @classmethod
#     def trig(cls, cost):
#         date = str(datetime.datetime.today())
#         date = date.split('.')[0]
#         print(date,cost)
#         cursor.execute("""
#                           CREATE TRIGGER IF NOT EXISTS history_of_ordery
#                           AFTER DELETE ON box
#                           WHEN (SELECT COUNT(*) FROM box) = 0
#                           BEGIN
#                           INSERT INTO purchases(date_purchase, total_price) VALUES (?,?);
#                           END
#
#         """,(date,cost))
#         conn.commit()

class Costumer:

    def __init__(self, name, age, money):
        self.name = name
        self.age = age
        self.money = money
        self.box = Box()

    def add_good(self, good, count):
        self.box.add_goods(good, count)

    def del_goods(self, good):
        self.box.del_goods(good)

    def change_goods(self, good, count):
        self.box.resize_count_good(good, count)

    def view_prod(self):
        self.box.watch_box()

    def cost_prod(self):
        self.box.cost()

    def total_price(self):
        if self.box.cost() <= self.money:
            price = self.box.cost()
            print(f'денег хватает, после покупки осталось {self.money - self.box.cost()}')
            History_order.trig(price)
            time.sleep(0.1)
            self.box.del_all_in_box()

def toolbar():
    while True:
        menu_variants()

        choose = input('введите пункт из меню: ')
        if choose == 'e':
            return
        elif choose == '1':
            shop.view_goods_in_shop()
        elif choose == '2':
            good = input('введите товар, который хотите положить в корзину')
            count = int(input('введите количество товара'))
            Vasia.add_good(good, count)
        elif choose == '3':
            Vasia.view_prod()



def menu_variants():
    print('1 - выбрать все продукты магазина')
    print('2 - купить продукт')
    print('3 - просмотреть корзину')
    print('e - выход')




Vasia = Costumer('Vasia', 45, 560)
# Vasia.get_good('milk',5)
# Vasia.total_price()
# box = Box()
# box.add_goods('egg',15)
shop = Goods(name= 'evroopt')
# shop.good_select()
toolbar()