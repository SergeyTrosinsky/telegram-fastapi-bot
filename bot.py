import telebot
import requests
from db_operations import *

# Вставьте сюда свой токен, полученный от @BotFather
TOKEN = "8711384882:AAHbeZKmssJZQ0FMSa6egyRclWAJ7j-B9w0"

bot = telebot.TeleBot(TOKEN)

# Обработчики команд 
@bot.message_handler(commands=['start'])
def start(message):
    help_text = """
Привет! Я бот для управления спортивной базой данных.
Доступные команды:

/add_sportsman Имя Фамилия ГГГГ-ММ-ДД Разряд ID_клуба
    Добавить спортсмена. Пример: /add_sportsman Иван Петров 2000-01-01 КМС 1

/add_trener Имя Фамилия Стаж
    Добавить тренера. Пример: /add_trenер Сергей Иванов 10

/show_by_sport Вид_спорта [разряд]
    Показать спортсменов по виду спорта. Пример: /show_by_sport Футбол
    С фильтром: /show_by_sport Футбол КМС

/show_by_trener Фамилия_тренера [разряд]
    Показать спортсменов тренера. Пример: /show_by_trener Петров
    С фильтром: /show_by_trener Петров КМС

/show_prizers Название_соревнования
    Показать призёров соревнования. Пример: /show_prizers Кубок Москвы по футболу

/show_multiple_sports
    Показать спортсменов, занимающихся более чем одним видом спорта

/club_stats ГГГГ-ММ-ДД ГГГГ-ММ-ДД
    Статистика по клубам за период. Пример: /club_stats 2024-01-01 2024-12-31

/update_rank ID_спортсмена Новый_разряд
    Обновить разряд спортсмена. Пример: /update_rank 1 МС

/delete_sportsman ID_спортсмена
    Удалить спортсмена. Пример: /delete_sportsman 1
"""
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['add_sportsman'])
def add_sportsman_cmd(message):
    try:
        parts = message.text.split()
        # формат: /add_sportsman Имя Фамилия Дата_рождения Разряд ID_клуба
        if len(parts) != 6:
            bot.reply_to(message, "Неверный формат. Используйте: /add_sportsman Имя Фамилия ГГГГ-ММ-ДД Разряд ID_клуба")
            return
        _, ima, familia, data, razryad, id_kluba = parts
        add_sportsman(ima, familia, data, razryad, int(id_kluba))
        bot.reply_to(message, f"Спортсмен {ima} {familia} добавлен.")
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

@bot.message_handler(commands=['add_trener'])
def add_trener_cmd(message):
    try:
        parts = message.text.split()
        if len(parts) != 4:
            bot.reply_to(message, "Неверный формат. Используйте: /add_trener Имя Фамилия Стаж")
            return
        _, ima, familia, stazh = parts
        add_trener(ima, familia, int(stazh))
        bot.reply_to(message, f"Тренер {ima} {familia} добавлен.")
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

@bot.message_handler(commands=['show_by_sport'])
def show_by_sport_cmd(message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "Неверный формат. Используйте: /show_by_sport Вид_спорта [разряд]")
            return
        vid = parts[1]
        min_razryad = parts[2] if len(parts) > 2 else None
        rows = get_sportsmen_by_sport(vid, min_razryad)
        if not rows:
            bot.reply_to(message, f"Нет спортсменов по виду '{vid}'.")
        else:
            text = f"Спортсмены, занимающиеся {vid}:\n"
            for row in rows:
                text += f"{row[0]} {row[1]}, разряд: {row[2]}\n"
            bot.reply_to(message, text)
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

@bot.message_handler(commands=['show_by_trener'])
def show_by_trener_cmd(message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "Неверный формат. Используйте: /show_by_trener Фамилия_тренера [разряд]")
            return
        trener_fam = parts[1]
        min_razryad = parts[2] if len(parts) > 2 else None
        rows = get_sportsmen_by_trener(trener_fam, min_razryad)
        if not rows:
            bot.reply_to(message, f"Нет спортсменов у тренера {trener_fam}.")
        else:
            text = f"Спортсмены, тренирующиеся у {trener_fam}:\n"
            for row in rows:
                text += f"{row[0]} {row[1]}, разряд: {row[2]}\n"
            bot.reply_to(message, text)
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

@bot.message_handler(commands=['show_prizers'])
def show_prizers_cmd(message):
    try:
        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            bot.reply_to(message, "Неверный формат. Используйте: /show_prizers Название_соревнования")
            return
        sorev = parts[1]
        rows = get_prizers(sorev)
        if not rows:
            bot.reply_to(message, f"Нет призёров для соревнования '{sorev}'.")
        else:
            text = f"Призёры соревнования '{sorev}':\n"
            for row in rows:
                text += f"{row[0]} {row[1]} — {row[2]} место, награда: {row[3]}\n"
            bot.reply_to(message, text)
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

@bot.message_handler(commands=['show_multiple_sports'])
def show_multiple_sports_cmd(message):
    rows = get_sportsmen_with_multiple_sports()
    if not rows:
        bot.reply_to(message, "Нет спортсменов, занимающихся более чем одним видом спорта.")
    else:
        text = "Спортсмены, занимающиеся более чем одним видом спорта:\n"
        for row in rows:
            text += f"{row[0]} {row[1]}: {row[2]}\n"
        bot.reply_to(message, text)

@bot.message_handler(commands=['club_stats'])
def club_stats_cmd(message):
    try:
        parts = message.text.split()
        if len(parts) != 3:
            bot.reply_to(message, "Неверный формат. Используйте: /club_stats ГГГГ-ММ-ДД ГГГГ-ММ-ДД")
            return
        start = parts[1]
        end = parts[2]
        rows = get_club_stats_by_period(start, end)
        if not rows:
            bot.reply_to(message, "Нет данных за указанный период.")
        else:
            text = f"Клубы и количество участвовавших спортсменов ({start} – {end}):\n"
            for row in rows:
                text += f"{row[0]}: {row[1]} спортсменов\n"
            bot.reply_to(message, text)
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

@bot.message_handler(commands=['update_rank'])
def update_rank_cmd(message):
    try:
        parts = message.text.split()
        if len(parts) != 3:
            bot.reply_to(message, "Неверный формат. Используйте: /update_rank ID_спортсмена Новый_разряд")
            return
        _, s_id, new_rank = parts
        update_sportsman_rank(int(s_id), new_rank)
        bot.reply_to(message, f"Разряд спортсмена {s_id} обновлён на '{new_rank}'.")
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

@bot.message_handler(commands=['delete_sportsman'])
def delete_sportsman_cmd(message):
    try:
        parts = message.text.split()
        if len(parts) != 2:
            bot.reply_to(message, "Неверный формат. Используйте: /delete_sportsman ID_спортсмена")
            return
        _, s_id = parts
        delete_sportsman(int(s_id))
        bot.reply_to(message, f"Спортсмен с ID {s_id} удалён.")
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")
        


@bot.message_handler(commands=['api_sportsmen'])
def api_sportsmen_cmd(message):
    try:
        resp = requests.get("http://127.0.0.1:8000/sportsmen", timeout=5)
        if resp.status_code != 200:
            bot.reply_to(message, "Ошибка API")
            return
        data = resp.json()
        text = "Спортсмены (данные через API):\n"
        for s in data["sportsmen"]:
            text += f"{s['Ima']} {s['Familia']} — {s['Razryad']}\n"
        bot.reply_to(message, text)
    except Exception as e:
        bot.reply_to(message, f"Ошибка подключения к API: {e}")

# Запуск бота
if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()