import sqlite3

import datetime
conn = sqlite3.connect('shop_box.db')
cursor = conn.cursor()

class BdConnectionCM:
    def __init__(self, db_name):
        """Конструктор"""
        self.db_name = db_name

    def __enter__(self):
        """
        Открываем подключение с базой данных.
        """
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Закрываем подключение.
        """
        self.conn.close()
        if exc_val:
            raise




class Db_queiries:
    @classmethod
    def get_engine(cls):
        db = 'shop_box.db'
        with BdConnectionCM(db) as conn:
            cls.cursor = conn.cursor()

    @classmethod
    def select_all_goods(cls):            #проверка товара в магазине
        with BdConnectionCM('shop_box.db') as conn:
            cls.cursor = conn.cursor()
            goods = cursor.execute("SELECT * FROM goods")
            return goods

    @classmethod
    def select_good(cls, name):
        count = cursor.execute(""" 
                SELECT count(*) FROM box
                INNER JOIN goods ON box.good_id = goods.good_id
                WHERE goods.name == ?;  
        """, (name,))
        for i in count:
            return bool(i[0])



    @classmethod
    def select_box(cls):
        goods = cursor.execute(""" 
                SELECT name AS 'name', count_good AS 'количество' FROM box
                INNER JOIN goods ON box.good_id = goods.good_id 
        """)
        return goods

    @classmethod
    def insert_into_box(cls, good, count):
        all_goods = cls.select_all_goods()
        for gd in all_goods:
            if gd[1] == good:
                id_good = gd[0]

                cursor.execute("""INSERT INTO box (good_id, count_good) VALUES (?,?)
                """ , (id_good, count))
                conn.commit()

    @classmethod
    def delete_good_in_box(cls, good):
        cursor.execute("""DELETE FROM box
                                 INNER JOIN goods 
                                 ON box.good_id = goods.good_id
                                  WHERE goods.name == ?""", (good,))
        conn.commit()

    @classmethod
    def update_good_in_box(cls, good,count):
        cursor.execute("""UPDATE box SET count_good = ?
                                    INNER JOIN box USING (good_id)
                                    WHERE good.name = ?""", (count, good,))
        conn.commit()

    @classmethod
    def cost_goods(cls):
        total_price = cursor.execute("""SELECT sum(prime * count_good) AS 'сумма' FROM box
        INNER JOIN goods ON box.good_id = goods.good_id""")
        return total_price



    @classmethod
    def del_goods_in_box(cls):
        cursor.execute("""DELETE FROM box""")
        conn.commit()

# if __name__ == '__main__':
#     db = 'shop_box.db'




# for  i in Db_queiries.select_all_goods():
#     print(i)



