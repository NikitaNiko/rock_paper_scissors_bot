import sqlite3
from bot_start import bot
from bot_keyboards.builder import build_kb

db = sqlite3.connect('server.db')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT,
            ready INT,
            find INT,
            enemy_id BIGINT,
            round INT,
            win_rounds INT,
            item TEXT
            )""")

db.commit()


#При запуске поиска в БД добавляется пользователь, либо флаг поиска сменяется на 1
async def add_user(user_id, search):
    sql.execute(f"SELECT user_id FROM users WHERE user_id = {user_id}")
    if sql.fetchone() is None:
        sql.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)", (user_id, 0, search, None, 1, 0, "nothing"))
    else:
        sql.execute(f"UPDATE users SET find = 1 WHERE user_id = {user_id}")
    
    db.commit()


# При остановке поиска флаг поиска сменяется на 0
async def stop_search(us_id):
    sql.execute(f"UPDATE users SET find = 0 WHERE user_id = {us_id}")
    db.commit()
    

# При нахождении противника флаги поиска сменяются на 3, а enemy_id на айди игроков
async def finding(us_id):
    v = sql.execute(f"SELECT user_id FROM users WHERE find = 1 AND user_id != {us_id}")
    for val in v:
        if val[0] != "":
            sql.execute(f"UPDATE users SET find = 3 WHERE user_id = {us_id}")
            sql.execute(f"UPDATE users SET enemy_id = {val[0]} WHERE user_id = {us_id}")
            
            sql.execute(f"UPDATE users SET find = 3 WHERE user_id = {val[0]}")
            sql.execute(f"UPDATE users SET enemy_id = {us_id} WHERE user_id = {val[0]}")
            db.commit()

            await bot.send_message(chat_id=us_id, text="Противник найден!", reply_markup=build_kb(["🗿", "✂", "📃"]))
            await bot.send_message(chat_id=val[0], text="Противник найден!", reply_markup=build_kb(["🗿", "✂", "📃"]))

            await bot.send_message(chat_id=us_id, text="Раунд 1!", reply_markup=build_kb(["🗿", "✂", "📃"]))
            await bot.send_message(chat_id=val[0], text="Раунд 1!", reply_markup=build_kb(["🗿", "✂", "📃"]))



# Возвращает флаг поиска заданного user_id
async def ret_find(user_id):
    v = sql.execute(f"SELECT find FROM users WHERE user_id = {user_id}")
    for val in v:
        return val[0]


# 🗿 ✂ 📃
# Установка флага готовности на 1, помещение предмета в item, попытка разыграть партию
async def playing_game(user_id, item):
    sql.execute(f"UPDATE users SET ready = 1 WHERE user_id = {user_id}")
    sql.execute(f"UPDATE users SET item = '{item}' WHERE user_id = {user_id}")
    db.commit()

    v = sql.execute(f"SELECT enemy_id, round, win_rounds FROM users WHERE user_id = {user_id}")
    for val in v:
        enemy_id = val[0]
        round_num_me = val[1]
        rounds_win_me = val[2]


    v = sql.execute(f"SELECT ready, item, round, win_rounds FROM users WHERE user_id = {enemy_id}")
    for val in v:
        f = val[0]
        item_enemy = val[1]
        round_num_enemy = val[2]
        rounds_win_enemy = val[3]

    if (f == 1):
        if (item == "камень"):
            if (item_enemy == "ножницы"):
                await bot.send_message(chat_id=user_id, text="Противник выбросил ножницы, раунд за вами", reply_markup=build_kb(["🗿", "✂", "📃"]))
                await bot.send_message(chat_id=enemy_id, text="Противник выбросил камень, раунд за ним", reply_markup=build_kb(["🗿", "✂", "📃"]))
                sql.execute(f"UPDATE users SET win_rounds = {rounds_win_me + 1}, round = {round_num_me + 1} WHERE user_id = {user_id}")
                sql.execute(f"UPDATE users SET round = {round_num_enemy + 1} WHERE user_id = {enemy_id}")

            elif (item_enemy == "бумага"):
                await bot.send_message(chat_id=user_id, text="Противник выбросил бумагу, раунд за противником", reply_markup=build_kb(["🗿", "✂", "📃"]))
                await bot.send_message(chat_id=enemy_id, text="Противник выбросил камень, раунд за вами!", reply_markup=build_kb(["🗿", "✂", "📃"]))
                sql.execute(f"UPDATE users SET round = {round_num_me + 1} WHERE user_id = {user_id}")
                sql.execute(f"UPDATE users SET win_rounds = {rounds_win_enemy + 1}, round = {round_num_enemy + 1} WHERE user_id = {enemy_id}")

            else:
                await bot.send_message(chat_id=user_id, text="Ничья, еще один раунд", reply_markup=build_kb(["🗿", "✂", "📃"]))
                await bot.send_message(chat_id=enemy_id, text="Ничья, еще один раунд", reply_markup=build_kb(["🗿", "✂", "📃"]))
                sql.execute(f"UPDATE users SET round = {round_num_me + 1} WHERE user_id = {user_id}")
                sql.execute(f"UPDATE users SET round = {round_num_enemy + 1} WHERE user_id = {enemy_id}")

        if (item == "ножницы"):
            if (item_enemy == "бумага"):
                await bot.send_message(chat_id=user_id, text="Противник выбросил бумагу, раунд за вами", reply_markup=build_kb(["🗿", "✂", "📃"]))
                await bot.send_message(chat_id=enemy_id, text="Противник выбросил ножницы, раунд за ним", reply_markup=build_kb(["🗿", "✂", "📃"]))
                sql.execute(f"UPDATE users SET win_rounds = {rounds_win_me + 1}, round = {round_num_me + 1} WHERE user_id = {user_id}")
                sql.execute(f"UPDATE users SET round = {round_num_enemy + 1} WHERE user_id = {enemy_id}")

            elif (item_enemy == "камень"):
                await bot.send_message(chat_id=user_id, text="Противник выбросил камень, раунд за противником", reply_markup=build_kb(["🗿", "✂", "📃"]))
                await bot.send_message(chat_id=enemy_id, text="Противник выбросил ножницы, раунд за вами!", reply_markup=build_kb(["🗿", "✂", "📃"]))
                sql.execute(f"UPDATE users SET round = {round_num_me + 1} WHERE user_id = {user_id}")
                sql.execute(f"UPDATE users SET win_rounds = {rounds_win_enemy + 1}, round = {round_num_enemy + 1} WHERE user_id = {enemy_id}")

            else:
                await bot.send_message(chat_id=user_id, text="Ничья, еще один раунд", reply_markup=build_kb(["🗿", "✂", "📃"]))
                await bot.send_message(chat_id=enemy_id, text="Ничья, еще один раунд", reply_markup=build_kb(["🗿", "✂", "📃"]))
                sql.execute(f"UPDATE users SET round = {round_num_me + 1} WHERE user_id = {user_id}")
                sql.execute(f"UPDATE users SET round = {round_num_enemy + 1} WHERE user_id = {enemy_id}")
        
        if (item == "бумага"):
            if (item_enemy == "камень"):
                await bot.send_message(chat_id=user_id, text="Противник выбросил камень, раунд за вами", reply_markup=build_kb(["🗿", "✂", "📃"]))
                await bot.send_message(chat_id=enemy_id, text="Противник выбросил бумагу, раунд за ним", reply_markup=build_kb(["🗿", "✂", "📃"]))
                sql.execute(f"UPDATE users SET win_rounds = {rounds_win_me + 1}, round = {round_num_me + 1} WHERE user_id = {user_id}")
                sql.execute(f"UPDATE users SET round = {round_num_enemy + 1} WHERE user_id = {enemy_id}")

            elif (item_enemy == "ножницы"):
                await bot.send_message(chat_id=user_id, text="Противник выбросил ножницы, раунд за противником", reply_markup=build_kb(["🗿", "✂", "📃"]))
                await bot.send_message(chat_id=enemy_id, text="Противник выбросил бумагу, раунд за вами", reply_markup=build_kb(["🗿", "✂", "📃"]))
                sql.execute(f"UPDATE users SET round = {round_num_me + 1} WHERE user_id = {user_id}")
                sql.execute(f"UPDATE users SET win_rounds = {rounds_win_enemy + 1}, round = {round_num_enemy + 1} WHERE user_id = {enemy_id}")

            else:
                await bot.send_message(chat_id=user_id, text="Ничья, еще один раунд", reply_markup=build_kb(["🗿", "✂", "📃"]))
                await bot.send_message(chat_id=enemy_id, text="Ничья, еще один раунд", reply_markup=build_kb(["🗿", "✂", "📃"]))
                sql.execute(f"UPDATE users SET round = {round_num_me + 1} WHERE user_id = {user_id}")
                sql.execute(f"UPDATE users SET round = {round_num_enemy + 1} WHERE user_id = {enemy_id}")

        sql.execute(f"UPDATE users SET ready = 0 WHERE user_id = {user_id}")
        sql.execute(f"UPDATE users SET ready = 0 WHERE user_id = {enemy_id}")
        db.commit()

        # Проверка на последний раунд
        v = sql.execute(f"SELECT win_rounds, round FROM users WHERE user_id = {enemy_id}")
        for val in v:
            rounds_win_enemy = val[0]
            rounds_enemy = val[1]

        v = sql.execute(f"SELECT win_rounds, round FROM users WHERE user_id = {user_id}")
        for val in v:
            rounds_win_me = val[0]
            rounds_me = val[1]

        if (rounds_win_me == 2 or rounds_win_enemy == 2):

            if (rounds_win_me == 2):
                await bot.send_message(chat_id=user_id, text="Вы выйграли!!!", reply_markup=build_kb('Завершить'))
                await bot.send_message(chat_id=enemy_id, text="Вы проиграли :(", reply_markup=build_kb('Завершить'))
            else:
                await bot.send_message(chat_id=user_id, text="Вы проиграли :(", reply_markup=build_kb('Завершить'))
                await bot.send_message(chat_id=enemy_id, text="Вы выйграли!!!", reply_markup=build_kb('Завершить'))

            sql.execute(f"UPDATE users SET round = 0, win_rounds = 0, find = 4 WHERE user_id = {user_id}")
            sql.execute(f"UPDATE users SET round = 0, win_rounds = 0, find = 4 WHERE user_id = {enemy_id}")
            db.commit()
        
        else:

            await bot.send_message(chat_id=user_id, text=f"Раунд {rounds_me}")
            await bot.send_message(chat_id=user_id, text=f"Выйграно раундов {rounds_win_me}/2")
            await bot.send_message(chat_id=enemy_id, text=f"Раунд {rounds_enemy}")
            await bot.send_message(chat_id=enemy_id, text=f"Выйграно раундов {rounds_win_enemy}/2")





# Delete
def zapolnenie():

    user_id = 777

    sql.execute(f"SELECT user_id FROM users WHERE user_id = {user_id}")
    if sql.fetchone() is None:
        sql.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)", (user_id, 1, 1, 5212, 1, 0, "ножницы"))
        db.commit()


    for value in sql.execute("SELECT user_id FROM users WHERE enemy_id = 4321"):
        print(value[0])

# zapolnenie()