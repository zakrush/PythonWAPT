import sys
global history
history = []

def request(context, flow):

    url = flow.request.url
    if url not in history:
        f = open('httplogs.txt', 'a+')
        f.write(url +'/n')
        history.append(url)
        f.close() #после проверки работоспособности попробовать открытие вынести за условие
        #также добавить обработку ошибки неоткрытия и не закрытия файла (стандартная конструкция)
    else:
        pass