import json
from datetime import datetime
import random
import requests

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters

import Constants as keys
import News

print("Bot Starting....")


def start_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Chào {update.effective_user.first_name}')


def help_command(update: Update, context: CallbackContext):
    update.message.reply_text("Xin chào, đây là trung tâm trợ giúp! \nCú pháp'/function' để xem chức năng \nPhản hồi chất lượng project, vui lòng gửi mail về 'drsmile6969@gmail.com'" + "\n" + "Hotline : 0345664593" + "\n" + "Ủng hộ nhóm : Momo 0345664593 - Bùi Thái Dương")


def news_command(update: Update, context: CallbackContext):
    try:
        limit_news = int(context.args[0])  # Lấy tham số từ input truyền vào -> cào về bao nhiêu tin
        news = News.GetNews(limit_news)
        for x in range(0, len(news)):  # Deserialize dữ liệu json trả về từ file News.py lúc nãy
            message = json.loads(news[x])
            update.message.reply_text(message['title'] + "\n"
                                      + message['link'] + "\n" + message['description'])
    except (IndexError, ValueError):
        update.message.reply_text('Vui lòng chọn số lượng tin hiển thị!!')


def time_command(update: Update, context: CallbackContext):
    update.message.reply_text("Hôm nay là: " + datetime.now().strftime("%d-%m-%y, %H:%M:%S"))

def random_command(update: Update, context: CallbackContext):
    num = random.randint(1,100)
    update.message.reply_text("Con số của bạn là : " + str(num))

def info_command(update: Update, context: CallbackContext):
    update.message.reply_text("Xin chào, đây là project của nhóm 2.\nGiảng viên : Nguyễn Hoàng Anh. \nThành viên nhóm : \n1. Bùi Thái Dương \n2.Vũ Lê Long \n3. Phạm Công Tiến \n4. Trần Minh Đức \n5. Mai Hoàng Tiến")

def function_command(update: Update, context: CallbackContext):
    update.message.reply_text("Danh sách chức năng :" + "\n" + "1./start : khởi động." + "\n" + "2./help : xem trợ giúp" + "\n" + "3./random : lấy số ngẫu nhiên (trong khoảng 0 đến 100)" + "\n" + "4./time : xem ngày giờ" + "\n" + "5./news + số lượng bản tin : xem tin tức" + "\n" + "6./covid : xem số liệu covid theo thời gian thực" + "\n7./info : xem thông tin")

def covid_command(update : Update, context: CallbackContext):
    r = requests.get('https://coronavirus-19-api.herokuapp.com/all')
    data = r.json()
    update.message.reply_text(f'Thông tin covid-19 toàn cầu : \nTổng số ca nhiễm : {data["cases"]} \nTử Vong : {data["deaths"]} \nĐã khỏi : {data["recovered"]}')

def random_quote(update, context):
    # fetch data from the api
    response = requests.get('http://quotes.stormconsultancy.co.uk/random.json')
    data = response.json()
    # send message
    context.bot.send_message(chat_id=update.effective_chat.id, text=data['quote'])

def callback_auto_message(context):
    context.bot.send_message(chat_id='-1001714174905', text='Automatic message!')


def start_auto_messaging(update, context):
    chat_id = update.message.chat_id
    context.job_queue.run_repeating(callback_auto_message, 10, context=chat_id, name=str(chat_id))
    # context.job_queue.run_once(callback_auto_message, 3600, context=chat_id)
    # context.job_queue.run_daily(callback_auto_message, time=datetime.time(hour=9, minute=22), days=(0, 1, 2, 3, 4, 5, 6), context=chat_id)


def stop_notify(update, context):
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text='Stopping automatic messages!')
    job = context.job_queue.get_jobs_by_name(str(chat_id))
    job[0].schedule_removal()


#---------------------------------------------------------
# Function dùng để xác định lỗi gì khi có thông báo lỗi
def error(update: Update, context: CallbackContext):
    print(f"Update {update} cause error {context.error}")

def main():
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("news", news_command))
    dp.add_handler(CommandHandler("time", time_command))
    dp.add_handler(CommandHandler("random", random_command))
    dp.add_handler(CommandHandler("info", info_command))
    dp.add_handler(CommandHandler("function", function_command))
    dp.add_handler(CommandHandler("covid", covid_command))
    dp.add_handler(CommandHandler('rq', random_quote))
    dp.add_handler(CommandHandler("auto", start_auto_messaging))
    dp.add_handler(CommandHandler("stop", stop_notify))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


main()
