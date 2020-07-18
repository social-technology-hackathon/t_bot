#-------------------------------------------
# Find @BotFather on telegram
# write  '/start'
# write '/newbot'
# get token, use for bot
#-------------------------------------------

import telebot
from telebot import types

bot = telebot.TeleBot("")

user_id = ''
name = ''
surname = ''
vote = ''
verification = ''

condidates_dict = {
    # 'Бабарико':'Babariko',
    # 'Цепкало':'Tsepkalo',
    'Лукашенко': 'Lukashenko',
    'Тихановская': 'Tsikhanovskaya',
    'Черечень': 'Cherachan',
    'Дмитриев': 'Dmitriev',
    'Канопатская': 'Kanopatskaya'
}


@bot.message_handler(content_types=['text', 'document'])
def get_messages(message):
    # add variant for document -> send somewhere
    global user_id


    condidates = types.InlineKeyboardMarkup()
    for key, value in condidates_dict.items():
        new_candidate = types.InlineKeyboardButton(text=key, callback_data=value)
        condidates.add(new_candidate)


    message_to_user = 'Я за честные выборы. Можно проголосовать анонимно и с подтвержением. \n За кого Вы проголосовали?'
    bot.send_message(message.from_user.id, text=message_to_user, reply_markup=condidates)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global user_id
    global condidate

    user_id = call.from_user.id

    if call.data in condidates_dict.values():
        for key, value in condidates_dict.items():
            if value == call.data:
                condidate = key

        bot.send_message(call.from_user.id, "Вы проголосовали за {}".format(condidate))
        # send somewhere 'condidate'

    if call.data in ['yes', 'no']:
        if call.data == 'yes':
            print("Revieve photo")


    # it will loop. If you want to recieve more docs. passport/selfie/ drive licence
    validate = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton(text='Да - добавить селфи/фото водительского удостоверения/любой другой документ подтверждающий личность', callback_data='yes')
    validate.add(yes)

    no = types.InlineKeyboardButton(text='Нет. Вы не будуте включены список подтверденных.', callback_data='no')
    validate.add(no)

    message = 'Хотите подтвердить свой голос?'
    bot.send_message(call.from_user.id, text=message, reply_markup=validate)


bot.polling(none_stop=True, interval=0)
