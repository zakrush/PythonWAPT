import sys
global history
history = []

def request(flow):

    url = flow.request.url
    try:
        f = open('./httplogs.txt', 'a+')
        if url not in history:
            f.write(url +'\n')
            history.append(url)
        else:
            pass
    finally:
        f.close() #после проверки работоспособности попробовать открытие вынести за условие
            #также добавить обработку ошибки неоткрытия и не закрытия файла (стандартная конструкция)
