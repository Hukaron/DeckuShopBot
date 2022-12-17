import sqlite3 as sq
from botCreate import bot
from keyboards import inline_keyboards as kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def sql_start():
    global base, cur
    base=sq.connect('database/DeckuShopDb.db')
    cur=base.cursor()
    if base:
        print("Database connected!")
        base.execute('Create table if not exists clothes(clothes_id integer primary key autoincrement, clothes_image text,\
             clothes_type text, clothes_brand text, clothes_model text, clothes_size numeric, clothes_price real, clothes_isordered integer default(0))')
        base.execute("create table if not exists orders(odr_id integer primary key autoincrement, user_id integer, odr_date text default(Data(\'now\')))")
        base.execute("create table if not exists shopping_cart( clothes_id integer primary key references clothes (clothes_id), user_id integer)")
        base.execute('create table if not exists cl_odr(cl_id integer references clothes (clothes_id), odr_id integer references orders (odr_id))')
        base.commit()


async def sql_add_clothes(state):
    async with state.proxy() as data:
        cur.execute('insert into clothes(clothes_image, clothes_type, clothes_brand, clothes_model, clothes_size, clothes_price) values(?,?,?,?,?,?)', tuple(data.values()))
        base.commit()

async def sql_add_to_shopping_cart(user_id, order):
    cur.execute('insert into shopping_cart (user_id, clothes_id) values(?,?)', [user_id, order])
    base.commit()

# Не работает!
async def sql_count_amount(values):
    #print("select count(*) from (select * from clothes where (clothes_type="+str(values[2])+" and clothes_brand=\'"+str(values[3])+"\' and clothes_model=\'"+str(values[4])+"\' and clothes_size="+str(values[5])+" and clothes_price="+str(values[6])+"))")
    return  cur.execute("select count(*) from (select * from clothes where (clothes_type='"+str(values[1])+"' and clothes_brand=\'"+str(values[2])+"\' and clothes_model=\'"+str(values[3])+"\' and clothes_size="+str(values[4])+" and clothes_price="+str(values[5])+"))").fetchone()[0]

async def sql_view_catalog(cl_type):
    return cur.execute("select distinct clothes_image, clothes_type, clothes_brand, clothes_model, clothes_size, clothes_price from clothes where (clothes_isordered=0 and clothes_type='"+cl_type+"')").fetchall()


async def sql_search_types():
    return cur.execute('select distinct clothes_type from clothes where clothes_isordered=0').fetchall()


async def sql_search_in_cart(user_id, clothes_id):
    return cur.execute('select * from shopping_cart where user_id='+str(user_id)+' and clothes_id='+str(clothes_id)).fetchall()


