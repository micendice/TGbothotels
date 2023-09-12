# Информация о боте и как им пользоваться
| <!-- -->                                                                      |<!-- -->|
|-------------------------------------------------------------------------------|-----|
| ![Bot search result example](botworksdisplay.jpg "Bot search result example") |  Репозиторий содержит программные модули Телеграм бота. <br><br> Основная функция бота - подбор отелей из базы сайта hotels.com <br>по параметрам, задаваемым пользователем. <br><br>Поиск осуществляется по базе данных <br>hotels.com через обращение к API сайта rapidapi.com.<br> В связи с ограничениями hotels.com не предоставляет результаты поиска<br> по базе отелей в России, поэтому бот принимает ввод местоположения отеля<br> только на латинице.<br><br>Обращение к API сайта реаализовано через модуль request.<br> Работа с файлом базы данных - через ORM peewee. <br><br>Представленный код является дипломной работой М.М. Жиркова,<br> выполненной в рамках курса Skillbox "Профессия Python-разработчик"|

## Установка и запуск бота
1. Клонируйте репозиторий с Github
1. Установите виртуальное окружение
2. Установите зависимости `pip install -r requirements.txt`
3. Получите токен у @Botfather
4. Получите ключ для работы с сайтом hotels.com через API сайта rapidapi.com [здесь](https://rapidapi.com/apidojo/api/hotels4/ "https://rapidapi.com/apidojo/api/hotels4/")
5. Создайте в корневой директории файл `.env` и разместите в нем полученные ранее значения констант<br> BOT_TOKEN, RAPID_API_KEY, HOST_API.   <br>Например, так: 
```
BOT_TOKEN = "Токен, полученный от @Botfather"
RAPID_API_KEY = "Ключ для доступа к API, полученный от Rapidapi.com"
HOST_API = "Адрес хоста, полученный от Rapidapi.com. Скорее всего: https://hotels4.p.rapidapi.com" 
```
7. Для начала работы бота запустите файл main.py
___

## Последовательность работы бота
### Начало работы с ботом - команда **\start.** 
Бот выводит информацию о командах меню, доступных пользователю:
1. Поиск самых дешевых отелей - команда **\low**
2. Поиск самых дорогих отелей - команда **\high**
3. Поиск отелей по параметру из списка параметров (звездность отеля, отзывы клиентов, рекомендации,<br> близость к центру города, релевантность) - команда **\custom**
4. Вывод истории запросов пользователя - команда **\history**

Выбор нужной опции поиска осуществляется через меню или набором команды.
___
### Ввод параметров для поиска по командам **\low**, **\high**, **\custom**
Определение параметров для поиска организовано в виде диалога с пользователем.\
Этапы диалога:
1. Местоположение отеля\
        Контроль ввода: Только буквы латинского алфавита и дефис\
        Вывод результатов: Выбор пользователем нужного варианта из списка, возвращенного hotels.com на запрос,<br> содержащий строку пользователя.
2. Количество показываемых отелей.\
        Контроль ввода: Только цифры в диапазоне от 1 до константы MAX_HOTEL_DISPLAYED
3. Необходимость вывода фотографий.\
        Контроль ввода: кнопки "ДА" или "НЕТ"
4. Если фотографии выводятся, то количество выводимых фотографий.\
        Контроль ввода: Только цифры в диапазоне от 1 до константы MAX_PHOTO_DISPLAYED
5. Количество взрослых гостей.\
        Контроль ввода: кнопки со значениями от 1 до 4
6. Количество детей.\
        Контроль ввода: кнопки со значениями от 0 до 4
7. Возрасты детей (если применимо).\
        Контроль ввода: кнопки со значениями от 1 до 17
8. Даты заезда и выезда из отеля.\
        Контроль ввода: Выбор дат из календаря. Дата заезда не может стоять дальше значения константы<br>          SEARCH_INTERVAL
        от текущей даты. <br>Дата заезда не может быть ранее текущей даты, дата выезда не может быть ранее даты заезда \
        и стоять дальше, чем дата заезда на величину константы MAX_STAY.
9. Вывод собранных параметров поиска и подтверждение правильности пользователем.<br>
        Контроль ввода: кнопки "ДА" или "НЕТ"
### Выполнение поиска
При нажатии кнопки "ДА" формируются необходимые запросы к hotels.com:
+ выбор отелей по параметрам 
+ получение данных о цене
+ получение ссылок для последующего отображения фотографий
<br> На основании полученных ответов формируются и отображаются медиапакеты\
В файл базы данных записывается информация о запросе.
<br> При нажатии кнопки "НЕТ" при подтверждении правильности диалог возвращается к первому этапу (Местоположение отеля)\
### Выполение команды  **\history**<br>
Из файла базы данных через SQL-запрос извлекается и выводится информация о последних 10 запросах текущего пользователя.
___
### Команды по умолчанию
*\start* - запускает бота и список пользовательских команд\
*\help* - выводит список пользовательских команд\
*\echo* - выводит сообщение при вводе некорректных данных \
*\menu* - выводит меню пользовательских команд 
___
Константы хранятся в config_data/config.py



[def]: .botworksdisplay.jpg " Пример вывода результатов поиска"