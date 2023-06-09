from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto


button_1 = KeyboardButton('NFT 🎆')
button_2 = KeyboardButton('Личный кабинет 📁')
button_3 = KeyboardButton('Информация ℹ️')
button_4 = KeyboardButton('🧑‍💻 Поддержка')
greet_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_1).add(button_2).row(button_3, button_4)


menu_kb = InlineKeyboardMarkup()
inline_btn_1 = InlineKeyboardButton('📥 Пополнить', callback_data='invest')
inline_btn_2 = InlineKeyboardButton('Вывести 📤', callback_data='un_invest')
inline_btn_3 = InlineKeyboardButton('🖼 Мои NFT 🖼', callback_data='my_nft')
inline_btn_4 = InlineKeyboardButton('💰 Сменить валюту 💰', callback_data='change_wallet')

menu_kb.row(inline_btn_1, inline_btn_2).add(inline_btn_3).add(inline_btn_4)

admin_kb = InlineKeyboardMarkup()
inline_btn_1 = InlineKeyboardButton('🌟 Добавить коллекцию 🌟', callback_data='add_collection')
inline_btn_2 = InlineKeyboardButton('🌟 Добавить NFT к коллекции 🌟', callback_data='add_nft')
inline_btn_3 = InlineKeyboardButton('🌟 Найти мамонта по ID 🌟', callback_data='search_mamont')
admin_kb.add(inline_btn_1).add(inline_btn_2).add(inline_btn_3)

invest = InlineKeyboardMarkup()
inline_btn_1 = InlineKeyboardButton('🌟 CARD [RU] 🌟', callback_data='plus_card')
inline_btn_2 = InlineKeyboardButton('🌟 USDT 🌟', callback_data='plus_usdt')
invest.add(inline_btn_1).add(inline_btn_2)

un_invest = InlineKeyboardMarkup()
inline_btn_1 = InlineKeyboardButton('🌟 CARD 🌟', callback_data='un_card')
inline_btn_2 = InlineKeyboardButton('🌟 CRYPTO 🌟', callback_data='un_crypto')
un_invest.add(inline_btn_1).add(inline_btn_2)

mamont = InlineKeyboardMarkup()
inline_btn_1 = InlineKeyboardButton('🦣 Мои мамонты 🦣', callback_data='my_mamont')
mamont.add(inline_btn_1)


change = InlineKeyboardMarkup()
inline_btn_1 = InlineKeyboardButton('🇷🇺 RUB', callback_data='change_RUB')
inline_btn_2 = InlineKeyboardButton('🇺🇦 UAH', callback_data='change_UAH')
inline_btn_3 = InlineKeyboardButton('🇺🇸 USD', callback_data='change_USD')
inline_btn_4 = InlineKeyboardButton('🇪🇺 EUR', callback_data='change_EUR')
inline_btn_5 = InlineKeyboardButton('🇵🇱 PLN', callback_data='change_PLN')
inline_btn_6 = InlineKeyboardButton('🇧🇾 BLN', callback_data='change_BLN')
change.add(inline_btn_1).add(inline_btn_2).add(inline_btn_3).add(inline_btn_4).add(inline_btn_5).add(inline_btn_6)

