import datetime
import json
import os
import random
import webbrowser as wb
import playsound
import requests

from gtts import gTTS
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import speech_recognition as sr

import Constants as keys
import News

# Khai báo các biến gọi hàm

r = sr.Recognizer()
id = keys.ID
thoigian = datetime.datetime.now().strftime("%H:%M:%S")

# # # Running Bot
print("Bot đang chạy...")

# # # Các hàm chức năng <voice> :

def speak(text):
    tts = gTTS(text=text, lang='vi')
    filename ='voice.mp3'
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

def command():
    with sr.Microphone() as source:
        audio_data = r.record(source, duration = 5)

        try:
            query = r.recognize_google(audio_data, language="vi")
        except:
            query = ""
        return query

def voice(update : Update, context : CallbackContext):
    while True:
        query = command().lower()
        if query == "":
            context.bot.send_message(chat_id=id, text="Tôi đang lắng nghe ?")
            bot = "Tôi đang lắng nghe ?"
            speak(bot)
        elif "xin chào" in query:
            context.bot.send_message(chat_id=id, text=f'{update.effective_user.first_name} : Xin chào' )
            bot = f"Xin chào {update.effective_user.first_name} \nTôi có thể giúp gì cho bạn ?"
            context.bot.send_message(chat_id=id, text=bot)
            speak(bot)
            while True:
                query1 = command().lower()
                if "mấy giờ rồi" in query1:
                    context.bot.send_message(chat_id=id, text=f'{update.effective_user.first_name} : thời gian')
                    bot = datetime.datetime.now().strftime("Bây giờ là : %H:%M:%S")
                    context.bot.send_message(chat_id=id, text=bot)
                    speak(bot)
                    break
                elif "tìm kiếm" in query1:
                    context.bot.send_message(chat_id=id, text=f'{update.effective_user.first_name} : Tìm Kiếm')
                    bot = "Bạn muốn tìm kiếm gì trên Google ?"
                    context.bot.send_message(chat_id=id, text=bot)
                    speak(bot)
                    search = command().lower()
                    context.bot.send_message(chat_id=id, text=f'{update.effective_user.first_name} : {search}')
                    url = f"https://google.com/search?q={search}"
                    wb.get().open(url)
                    context.bot.send_message(chat_id=id, text=f"Kết quả tìm kiếm trên Google cho từ khóa : {search} \n{url}")
                    speak("Kết quả tìm kiếm")
                    break
                elif "youtube" in query1:
                    context.bot.send_message(chat_id=id, text=f'{update.effective_user.first_name} : Youtube')
                    bot = "Bạn muốn tìm kiếm gì trên Youtube ?"
                    context.bot.send_message(chat_id=id, text=bot)
                    speak(bot)
                    search = command().lower()
                    context.bot.send_message(chat_id=id, text=f'{update.effective_user.first_name} : {search}')
                    url = f"https://youtube.com/search?q={search}"
                    wb.get().open(url)
                    context.bot.send_message(chat_id=id, text=f"Kết quả tìm kiếm video trên Youtube cho từ khóa : {search} \n{url}")
                    speak("Kết quả tìm kiếm")
                    break
                elif "chức năng" in query1:
                    context.bot.send_message(chat_id=id, text=f'{update.effective_user.first_name} : {query1}')
                    function_command()
                    break
                elif "tạm biệt" in query1:
                    context.bot.send_message(chat_id=id, text=f'{update.effective_user.first_name} : Tạm biệt')
                    bot = query1
                    context.bot.send_message(chat_id=id, text=bot)
                    speak(bot)
                    break
                else:
                    bot = "Bạn muốn nói gì ?"
                    update.message.reply_text(bot)
                    speak(bot)
            break
        else:
            bot = "Hệ thống không xác định được câu lệnh của bạn..."
            update.message.reply_text(bot)
            speak(bot)
# # # Các hàm chức năng cơ bản :

# Chào
def start_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Xin chào {update.effective_user.first_name}')
    speak(f'Chào mừng {update.effective_user.first_name} đã đến với Telebot')

# Trợ giúp
def help_command(update: Update, context: CallbackContext):
    output = "Xin chào, đây là trung tâm trợ giúp! \nCú pháp '/function' để xem chức năng \nPhản hồi chất lượng project, vui lòng gửi mail về --> thaiducng.com \nCảm ơn bạn đã sử dụng dịch vụ của chúng tôi..."
    update.message.reply_text(output)
    speak(output)

# Tin tức
def news_command(update: Update, context: CallbackContext):
    try:
        limit_news = int(context.args[0])  # Lấy tham số từ input truyền vào -> cào về bao nhiêu tin
        news = News.GetNews(limit_news)
        for x in range(0, len(news)):  # Deserialize dữ liệu json trả về từ file News.py lúc nãy
            message = json.loads(news[x])
            update.message.reply_text(message['title'] + "\n"
                                      + message['link'] + "\n" + message['description'])
        context.bot.send_message(chat_id=id, text="Đã cập nhật lúc : " + thoigian)
    except (IndexError, ValueError):
        update.message.reply_text('Vui lòng chọn số lượng tin hiển thị!!')
        speak("Vui lòng chọn số lượng tin hiển thị")
    speak("Đã cập nhật lúc : " + thoigian)

# Thời gian
def time_command(update: Update, context: CallbackContext):
    speak(thoigian)
    update.message.reply_text("Hôm nay là: " + datetime.datetime.now().strftime("%y-%m-%d, %H:%M:%S"))


# Random số
def random_command(update: Update, context : CallbackContext):
    num = random.randint(1,100)
    output = "Con số của bạn là : " + str(num)
    update.message.reply_text("Con số của bạn là : " + str(num))
    speak(output)

# Hiển thị thông tin
def info_command(update: Update, context: CallbackContext):
    thongtin = "Xin chào, đây là project của nhóm 2.\n\nGiảng viên : Nguyễn Hoàng Anh. \n\nThành viên nhóm : \n\n1. Bùi Thái Dương \n2. Vũ Lê Long \n3. Phạm Công Tiến \n4. Trần Minh Đức \n5. Mai Hoàng Tiến\n\nPhiên bản : 1.0\nNgôn ngữ : Python\n\nLiên hệ :\notline : 0345664593\nMomo : 0345664593 - Bùi Thái Dương"
    speak(thongtin)
    update.message.reply_text(thongtin)

# Danh sách chức năng
def function_command(update: Update, context: CallbackContext):
    update.message.reply_text("DANH SÁCH CHỨC NĂNG\n"
                              "********************************************************\n"
                              "Chức Năng Cơ Bản \n \n"
                              "1./start    : Khởi động.\n"
                              "2./help     : Xem trợ giúp\n"
                              "3./function : Xem chức năng\n"
                              "4./info     : Xem thông tin\n"
                              "5./time     : Xem ngày giờ\n \n"
                              "Tin Tức \n \n"
                              "6./news + <num> : Xem tin tức\n"
                              "7./auto     : Tự động cập nhật tin tức mỗi 30 phút\n"
                              "8./stop     : Ngưng cập nhật tin tức\n"
                              "9./covid    : Xem số liệu covid theo thời gian thực\n \n"
                              "10./weather + <city> : Thời tiết"
                              "Ramdom \n \n"
                              "10./rq        : Quotes ngẫu nhiên\n"
                              "11./random   : Lấy số ngẫu nhiên (trong khoảng 0 đến 100)\n \n"
                              "Tìm kiếm\n \n"
                              "12./search + <sth>  : Tìm kiếm trên Google\n \n"
                              "***./voice   : Tổ hợp tính năng bằng giọng nói\n"
                              "********************************************************")

# Cập nhật số ca Covid toàn cầu
def covid_command(update : Update, context: CallbackContext):
    r = requests.get('https://coronavirus-19-api.herokuapp.com/all')
    data = r.json()
    output = f'SỐ LIỆU COVID TOÀN CẦU \n\nTổng số ca nhiễm : {data["cases"]} \nTử Vong : {data["deaths"]} \nĐã khỏi : {data["recovered"]}\nTheo số liệu từ : worldometers.info/coronavirus)'
    update.message.reply_text(output)
    speak(output)

# Random quotes
def random_quote(update, context):
    # fetch data from the api
    response = requests.get('http://quotes.stormconsultancy.co.uk/random.json')
    data = response.json()
    # send message
    context.bot.send_message(chat_id=update.effective_chat.id, text=data['quote'])

# Hàm trả về của tin tức tự động
def callback_auto_message(context):
    limit_news = 6  # Lấy tham số từ input truyền vào -> cào về bao nhiêu tin
    news = News.GetNews(limit_news)
    for x in range(0, len(news)):  # Deserialize dữ liệu json trả về từ file News.py lúc nãy
        message = json.loads(news[x])
        tintuc = message['title'] + "\n" + message['link'] + "\n" + message['description']
        context.bot.send_message(chat_id=id, text=tintuc)
    context.bot.send_message(chat_id=id, text="Đã cập nhật lúc : " + thoigian)

# Hàm lấy tin tức tự động
def start_auto_messaging(update, context):
    chat_id = update.message.chat_id
    context.job_queue.run_repeating(callback_auto_message, 10, context=chat_id, name=str(chat_id))
    # context.job_queue.run_once(callback_auto_message, 3600, context=chat_id)
    # context.job_queue.run_daily(callback_auto_message, time=datetime.time(hour=9, minute=22), days=(0, 1, 2, 3, 4, 5, 6), context=chat_id)

# Hàm hủy lấy tin tự động
def stop_notify(update, context):
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text='Stopping automatic messages!')
    job = context.job_queue.get_jobs_by_name(str(chat_id))
    job[0].schedule_removal()

# Hàm tìm kiếm
def search(update : Update, context):
    search = str(context.args[0])
    url = f"https://google.com/search?q={search}"
    context.bot.send_message(chat_id=id, text="Kết quả tìm kiếm : " + url)
    wb.get().open(url)

# Hàm thời tiết
def weather(update : Update, context):
    api_key = "b4750c6250a078a943b3bf920bb138a0"
    city = str(context.args[0])
    url = "http://api.openweathermap.org/data/2.5/weather?appid=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(url)
    data = json.loads(response.text)
    if data["cod"] != "404":
        # lấy value của key main
        city_res = data["main"]
        # nhiệt độ hiện tại
        current_temperature = city_res["temp"]
        # áp suất hiện tại
        current_pressure = city_res["pressure"]
        # độ ẩm hiện tại
        current_humidity = city_res["humidity"]
        # thời gian mặt trời
        suntime = data["sys"]
        # thông tin thêm
        wthr = data["weather"]
        # mô tả thời tiết
        weather_description = wthr[0]["description"]
        # Lấy thời gian hệ thống cho vào biến now
        now = datetime.datetime.now()
        # hiển thị thông tin với người dùng
        content = f"""
        Thời tiết {city} ngày {now.day} tháng {now.month} năm {now.year}
        Thời tiết hiện tại : {weather_description}
        Nhiệt độ trung bình là {current_temperature} độ C
        Áp suất không khí là {current_pressure} héc tơ Pascal
        Độ ẩm là {current_humidity}%
        """
        update.message.reply_text(content)
        speak(content)
    else:
        # nếu tên thành phố không đúng thì nó nói dòng dưới 227
        update.message.reply_text("Không tìm thấy địa chỉ của bạn")
        speak("Không tìm thấy địa chỉ của bạn")

# ---------------------------------------------------------
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
    dp.add_handler(CommandHandler("voice", voice))
    dp.add_handler(CommandHandler("search", search))
    dp.add_handler(CommandHandler("weather", weather))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()