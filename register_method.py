import codecs
import codecs_method

async def reg(message):
    db = await codecs_method.open('users.json')
    
    if message['from']['id'] not in db:
        db[message['from']['id']] = {'num': 0, 'balance': 0, 'set_collection': 0, 'name': 0, 'price': 0, 'tag': 0, 'blockchain': 0, 'photo_id': 0, 'invest': 0, 'wallet': 'USD', 'referals': [], 'ver': '❌ Не верифицирован', 'username': 0, 'user_id_add': 0, 'nft': {}, 'ref_mamonta': None}
    
    db[message['from']['id']]['username'] = message['from']['username']
    await codecs_method.write('users.json', db)
    
    return db