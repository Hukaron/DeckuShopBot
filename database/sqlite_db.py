import sqlite3 as sq
from botCreate import bot
from keyboards import inline_keyboards as kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Create функции
def sql_start():
    global base, cur
    base=sq.connect('database/DeckuShopDb.db')
    cur=base.cursor()
    if base:
        print("Database connected!")
        base.execute('create table if not exists clothes(clothes_id integer primary key default rowid, clothes_image text,\
             clothes_type text, clothes_brand text, clothes_model text, clothes_size numeric, clothes_price real, clothes_isordered integer default(0))')
        base.execute("create table if not exists orders(odr_id integer primary key default rowid, user_id integer, odr_date datetime default ((DATE(\'now\'))) not null, odr_price real) ")
        base.execute("create table if not exists shopping_cart( clothes_id integer references clothes (clothes_id) , user_id integer)")
        base.execute('create table if not exists cl_odr(cl_id integer references clothes (clothes_id), odr_id integer references orders (odr_id))')
        base.commit()


# Select функции
# Подсчёт количества товара
async def sql_count_amount(values):
    return  cur.execute("select count(*) from (select * from clothes where (clothes_type='"+str(values[1])+"' and clothes_brand=\'"+str(values[2])+"\' and clothes_model=\'"+str(values[3])+"\' and clothes_price="+str(values[4])+" and clothes_isordered=0) )").fetchone()[0]

# Получение всех разделов
async def sql_search_types():
    return cur.execute('select distinct clothes_type from clothes where clothes_isordered=0').fetchall()

#Получение и вывод всех товаров в корзине пользователя
async def sql_view_cart(user_id):
    return cur.execute("select clothes_id from clothes where clothes_id in (select clothes_id from shopping_cart where user_id=\'"+str(user_id)+"')").fetchall()

async def sql_clothes_by_id(id):
    return cur.execute("select clothes_image, clothes_type, clothes_brand, clothes_model, clothes_size, clothes_price from clothes where clothes_id="+str(id)).fetchall()

async def sql_find_id_of_size(cl_type, cl_model, cl_size):
    return cur.execute("select clothes_id from clothes where clothes_type='"+str(cl_type)+"' and clothes_model='"+str(cl_model)+"' and clothes_size="+str(cl_size)+" and clothes_isordered=0 order by clothes_id desc limit 1").fetchall()

# Получение информации о всех товарах из раздела
async def sql_view_catalog(cl_type):
    return cur.execute("select distinct clothes_image, clothes_type, clothes_brand, clothes_model, clothes_price from clothes where (clothes_isordered=0 and clothes_type='"+cl_type+"')").fetchall()

async def sql_find_all_sizes(cl_type, cl_model):
    return cur.execute("select distinct clothes_size from clothes where clothes_type=\'"+str(cl_type)+"\' and clothes_model=\'"+str(cl_model)+"\'").fetchall()

# Поиск существующей фотографии
async def sql_find_photo(state):
    async with state.proxy() as data:
       return cur.execute("select distinct clothes_image from clothes where(clothes_type=\'"+tuple(data.values())[1]+"' and clothes_brand=\'"+tuple(data.values())[2]+"' and clothes_model=\'"+tuple(data.values())[3]+"' and clothes_price="+tuple(data.values())[5]+")").fetchall()

# Для добавления в корзину. Проверяем добавлял ли пользователь в корзину данный товар(неправильно работает с id. Пользователь не может добавить больше одной копии товара)
async def sql_search_in_cart(user_id, clothes_id):
    return cur.execute("select * from shopping_cart where user_id="+str(user_id)+" and clothes_id="+str(clothes_id)).fetchall()


async def sql_find_all_orders(user_id):
    return cur.execute('select odr_id, odr_date, odr_price from orders where user_id='+str(user_id)).fetchall()

async def sql_clothes_in_orders(order_id):
    return cur.execute("select clothes_image, clothes_type, clothes_brand, clothes_model, clothes_size, clothes_price from clothes where clothes_id in (select cl_id from cl_odr where odr_id="+str(order_id)+")").fetchall()




# Insert запросы

# Добавление одежды
async def sql_add_clothes(photo, state):
    async with state.proxy() as data:
        values=tuple(data.values())
        cur.execute('insert into clothes (clothes_image, clothes_type, clothes_brand, clothes_model, clothes_size, clothes_price) values(?,?,?,?,?,?)', [photo, str(values[1]), str(values[2]),str(values[3]),str(values[4]),str(values[5])] )
        base.commit()

# Добавление одежды в корзину
async def sql_add_to_shopping_cart(user_id, clothes_id):
    cur.execute('insert into shopping_cart (user_id, clothes_id) values(?,?)', [user_id, clothes_id])
    base.commit()

#Добавление из корзины в заказ
async def sql_add_to_order(user_id):
    cur.execute('insert into orders (user_id) values(?)', [str(user_id)] )
    base.commit()
    return cur.execute('select odr_id from orders order by odr_id desc limit 1').fetchall()

#Добавление цены в заказ
async def sql_add_price_for_order(price, order_id):
    cur.execute('update orders set odr_price='+str(price)+' where odr_id='+str(order_id))
    base.commit()

# Добавление в cl_odr товаров
async def sql_add_to_cl_odr( order_id, clothes_id):
    cur.execute('insert into cl_odr (cl_id, odr_id) values(?,?)', [str(clothes_id), str(order_id)])
    cur.execute('update clothes set clothes_isordered = 1 where clothes_id='+str(clothes_id))
    base.commit()

# Добавление в таблицу cl_odr

#Delete запросы

# Удаление из корзины товаров
async def sql_delete_from_cart(user_id, clothes_id):
    cur.execute("delete from shopping_cart where clothes_id="+str(clothes_id)+" and user_id="+str(user_id))
    base.commit()


# Select functions