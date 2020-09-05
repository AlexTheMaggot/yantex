import telebot

bot = telebot.TeleBot('1051471905:AAEf8-enWvdUxNtCAHuUcb0QmNBaWa0am98')
print('Success initial bot token')

products = [
    {
        'id': '1',
        'category': 'Первая категория',
        'name': 'Первый товар первой категории',
        'price': '100',
        'ordered': False,
    },
    {
        'id': '2',
        'category': 'Первая категория',
        'name': 'Второй товар первой категории',
        'price': '100',
        'ordered': False,
    },
    {
        'id': '3',
        'category': 'Вторая категория',
        'name': 'Первый товар второй категории',
        'price': '100',
        'ordered': False,
    }
]
print('Success initial product base')

cart_items = []
print('Success initial empty cart')

beginning = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
categories = telebot.types.KeyboardButton('Категории')
about = telebot.types.KeyboardButton('О нас')
contacts = telebot.types.KeyboardButton('Контакты')
cart = telebot.types.KeyboardButton('Корзина')
beginning.add(categories, about, contacts, cart)
print('Success initial beginning reply markup')

category_list = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
first_category = telebot.types.KeyboardButton('Первая категория')
second_category = telebot.types.KeyboardButton('Вторая категория')
third_category = telebot.types.KeyboardButton('Третья категория')
fourth_category = telebot.types.KeyboardButton('Четвертая категория')
fifth_category = telebot.types.KeyboardButton('Пятая категория')
category_list.add(first_category, second_category, third_category, fourth_category, fifth_category, cart)
print('Success initial category_list reply keyboard')


@bot.message_handler(commands=['start', ])
def welcome(message):
    test = 0
    for user in cart_items:
        for select_user in user:
            if select_user == message.from_user.id:
                test = 1
    if test == 0:
        cart_items.append([message.from_user.id, ])
        print('Added new user: ' + str(message.chat.id))
    else:
        print('User already exists')
    bot.send_message(message.chat.id, "Success start", reply_markup=beginning)
    print(cart_items)


@bot.message_handler()
def working(message):
    if message.text == 'Категории':
        bot.send_message(message.chat.id, "Выберите категорию", reply_markup=category_list)
    elif message.text == 'О нас':
        bot.send_message(message.chat.id, "Вот О нас")
    elif message.text == 'Контакты':
        bot.send_message(message.chat.id, "Вот контакты")
    elif message.text == 'Первая категория':
        for n in products:
            if n['category'] == 'Первая категория':
                product = telebot.types.InlineKeyboardMarkup()
                callback_data = 'ordered' + n['id']
                order = telebot.types.InlineKeyboardButton(text='Заказать', callback_data=callback_data)
                product.add(order)
                message_text = n['name'] + '\r\n\r\n' + 'Цена: ' + n['price'] + ' сум'
                bot.send_message(message.chat.id, str(message_text), reply_markup=product)
    elif message.text == 'Корзина':
        cart_message = ''
        total_cost = 0
        print(cart_items)
        for n in cart_items:
            if n[0] == message.chat.id:
                cart_message += 'Товары в корзине:\r\n\r\n'
                if n[1]:
                    for c in products:
                        if c['ordered'] is True:
                            if c['id'] == n[1][0]:
                                cost = c['price']
                                total_cost += int(cost)
                                cart_message += c['name'] + ' - ' + n[1][1] + ' шт.\r\n'

        if total_cost == 0:
            bot.send_message(message.chat.id, 'Ваша корзина пуста')
        else:
            cart_message += '\r\n' + 'Общая стоимость: ' + str(total_cost)
            bot.send_message(message.chat.id, cart_message)
    else:
        bot.send_message(message.chat.id, "Используйте меню для управления")

    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        for q in products:
            callback_data_input = 'ordered' + q['id']
            if call.data == callback_data_input:
                q['ordered'] = True
                for w in cart_items:
                    if w[0] == call.from_user.id:
                        w.append([q['id'], '1'])
                        print(cart_items)
                bot.answer_callback_query(call.id, show_alert=False, text='Добавлено в корзину')


bot.polling()
