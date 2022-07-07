HELP: str = str(
'''
Что конкретно вас интересует:\n
1) Работа с таблтцой:
    /help sheet\n
2) Как забанить участника Амино:
    /help ban\n
3) Работа с ботом по категориям:
    /help category\n
4) Работа с ботом по защите чата:
    /help chat_notify_guard\n
4) Показать запросы на вступление в сообщество:
    /requests
'''
        )

HELP_BAN: str = str(
'''
1) Забанить участника: /ban (link) (причина)\n
2) Разбанить участника: /unban (link) (причина)\n
3)Забанить n число последних участников: /ban recent (количество)\n\n
Пример:
/ban recent 50
/ban http://aminoapps.com/p/tscygh пидор
/unban http://aminoapps.com/p/tscygh уже не пидор\n
Наличие причины не обязательно.\n
Пример:
/ban http://aminoapps.com/p/tscygh
/unban http://aminoapps.com/p/tscygh
'''
)

HELP_SHEETS: str = str(
'''
/sheets init - проиницилизировать гугл таблицу.
/sheets init [spreadsheets_id] - указать id гугл таблицы и проинициализировать.
Пример:
/sheets init
/sheets init SDsdasdW1SDdsad44512SDd234\n
/sheets get - вернуть строки за два дня до сегодня, за сегодня и за два дня вперед.
Пример: /sheets get\n
/sheets get today - вернуть строку таблицы за сегодня.
Пример: /sheets get today\n
/sheets get [дата] - вернуть строку таблицы за эту дату.
Пример: /sheets get 31.02.2077\n
/sheets write [дата] [кто сделал] [рассылка] [замены по подборкам] [ивенты] -
сделать запись на дату. [дата] и [кто сделал] - обязательные поля, остальное можно пропустить
Пример: /sheets write 15.03.22 Тони\n
Ссылка на таблицу:
https://docs.google.com/spreadsheets/d/1LEnUx5tF7itw_iDJsfCNzn_wuy4dMQR3imi6DrwMLPs/edit#gid=0
'''
)

HELP_CATEGORY: str = str(
'''
1) Запуск бота: /category start\n
2) Остановка бота: /category stop\n
3) Перезапуск бота: /category restart\n
4) Список скрытых постов: /category hiden list\n
5) Список всей активности скрытий/расскрытий: /category list #В разработке\n
6) Лог бота: /category log #В разработке\n
'''
)

HELP_CHAT_NOTIFY_GUARD: str = str(
'''
Запуск бота возможен только после выбора чата, в котором он будет работать\n\n
1) Запустить бота: /chat_notify_guard start\n
2) Остановить бота: /chat_notify_guard stop\n
3) Перезапустить бота: /chat_notify_guard restart\n
4) Получить список доступных чатов: /chat_notify_guard get\n
5) Обновить список доступных чатов: /chat_notify_guard update\n
6) Задать список чатов на которые распространяется защита: /chat_notify_guard set (номер чатов)\n
        Пример: /chat_notify_guard set 1 3 6 9
'''
)

HELP_EXCEPT: str = str('Неверно указана команда')
