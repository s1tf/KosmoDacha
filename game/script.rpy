# Вы можете расположить сценарий своей игры в этом файле.

# Инициализируем Python переменные
init python:

    # Загружаем файл с данными игры
    import copy
    import json
    with renpy.open_file('data.json', encoding='utf-8') as f:
        data_on_start = json.load(f)

    # Цвета
    COLOR_GREEN = '#7CFC00'
    COLOR_RED = '#FF0000'
    COLOR_YELLOW = '#FFFF00'

    def get_color(value):
        """  Возвращаем цвет в завимимости от значения силы тела/духа """
        if value <= 30:
            return COLOR_RED
        elif value < 70:
            return COLOR_YELLOW
        else:
            return COLOR_RED

# Инициализируем данные
init:
    image bg bg = 'bg.jpeg'  # https://www.artstation.com/artwork/1X1r8

# Задаём переменные
default data = copy.deepcopy(data_on_start)
default day = 1
default health = 50
default spirit = 50

# Экран количества дней
screen screen_day():
    text 'День: {color=#7CFC00}[day]{/color}/10':
        xalign 0.02 yalign 0.02

# Экран бодрости тела
screen screen_body():

    $ color = get_color(health)
    text 'Бодрость тела: {color=[color]}[health]{/color}/100':
        xalign 0.20 yalign 0.02


# Экран бодрости духа
screen screen_spirit():
    if spirit >= 50:
        text 'Бодрость духа: {color=#FFFF00}[spirit]{/color}/100':
            xalign 0.50 yalign 0.02
    else:
        text 'Бодрость духа: {color=#FF0000}[spirit]{/color}/100':
            xalign 0.50 yalign 0.02

# Игра начинается здесь:
label start:

    # 1. Показываем фон
    scene bg bg

    # 2. Показываем состояние игрока
    show screen screen_day
    show screen screen_body
    show screen screen_spirit

    # Выводим на экран описание дня
    $ day_description = data['days'][str(day)]['description']
    '[day_description]'

    # Если в этот день есть специальное событие, отображаем его
    # Если специального события нет, выбираем событие из пула случайных событий
    $ actions = data['days'][str(day)].get('actions')
    if actions:
        pass
    else:
        # Перемешиваем варианты действий, чтобы они были случайными
        $ renpy.random.shuffle(data['actions'])

        # Выбираем событие из пула случайных событий
        $ actions = data['actions']

    # Выбираем варианты действий
    $ action0 = actions[0]
    $ action1 = actions[1]
    $ action2 = actions[2]
    menu:

        '[action0[0]]':
            $ action = action0

        '[action1[0]]':
            $ action = action1

        '[action2[0]]':
            $ action = action2

# Если у выполненного действия было дочернее действие, добавляем дочернее действие в пул всех действий
if len(action) == 5:
    $ data['actions'].append(action[4])

# Удаляем выполненное действие из общего пула действий
if not data['days'][str(day)].get('actions'):
    $ data['actions'].remove(action)

# Выводим на экран результат операции
"[action[1]]"

# Выводим на экран изменения в бодрости тела
$ stat_change = ''
if action[2]:
    $ number = '{color=#FF0000}' + f'{action[2]}' +'{/color}' if action[2] < 0 else '{color=#7CFC00}' + f'+{action[2]}' +'{/color}'
    $ stat_change += f'Бодрость тела: {number}. '

# Выводим на экран изменения в бодрости духа
if action[3]:
    $ number = '{color=#FF0000}' + f'{action[3]}' +'{/color}' if action[3] < 0 else '{color=#7CFC00}' + f'+{action[3]}' +'{/color}'
    $ stat_change += f'Бодрость духа: {number}. '

# Меняем статы игрока, сообщаем ему об этом
'[stat_change]'
if health + action[2] < 0:
    $ health = 0
else:
    $ health += action[2]

if spirit + action[3] < 0:
    $ spirit = 0
else:
    $ spirit += action[3]

# Если статы игрока упали до нуля, конец игры
if health < 1 or spirit < 1:

    # Составляем текст прощального сообщения
    $ days_left = 10 - day
    $ text = ''
    if days_left == 1:
        $ text = 'оставался всего один день'
    if days_left == 2:
        $ text = 'оставалось всего два дня'
    if days_left == 3:
        $ text = 'оставалось всего три дня'
    if days_left == 4:
        $ text = 'оставалось всего четыре дня'
    if days_left == 5:
        $ text = 'оставалось всего пять дней'
    if days_left == 6:
        $ text = 'оставалось всего шесть дней'


    menu:
        'Мне [text]. Увы, силы покинули меня...':
            return

# Прибавляем новый день
$ day += 1

# Возвращаемся к началу нового дня
jump start