import codecs

async def open(file_name):
    with codecs.open(str(file_name), 'r', 'utf-8') as file:
        value = eval(str(file.readline()))
        file.close()
        
    return value

async def write(file_name, source):
    with codecs.open(str(file_name), 'w', 'utf-8') as file:
        value = file.write(str(source))
        file.close()

    return value