import logging
import traceback
import sys

logfile = 'log_1.log'

log = logging.getLogger("my_log")
log.setLevel(logging.INFO)
FH = logging.FileHandler(logfile, encoding='utf-8')
## задаем базовый формат сообщения в логе
basic_formater = logging.Formatter('%(asctime)s : [%(levelname)s] : %(message)s')
FH.setFormatter(basic_formater)
log.addHandler(FH)

## функция для записи в лог сообщений об ошибке
def error_log(line_no):
                          #задаем формат ошибочных сообщений, добавляем номер строк
    err_formater = logging.Formatter('%(asctime)s : [%(levelname)s][LINE ' + line_no + '] : %(message)s')
                         #устанавливаем формат ошибок в логгер
    FH.setFormatter(err_formater)
    log.addHandler(FH)
    # пишем сообщение error
    log.error(traceback.format_exc())
    # возвращаем базовый формат сообщений
    FH.setFormatter(basic_formater)
    log.addHandler(FH)

