import os
import sqlite3

from typing import List, Set

def execute_query(query_sql: str) -> List:
    '''
    Функция для выполнения запроса
    :param query_sql: запрос
    :return: результат выполнения запроса
    '''
    db_path = os.path.join(os.getcwd(), 'chinook.db')
    connection = sqlite3.connect(db_path)
    cur = connection.cursor()
    result = cur.execute(query_sql).fetchall()
    connection.close()
    return result

def unwrapper(records: List) -> None:

    for record in records:
        print(*record)


def get_employees():
    query_sql = '''
        SELECT *
    	    FROM employees;
    '''
    result = execute_query(query_sql)
    unwrapper(result)

# get_employees()

def get_customers(state_name=None, city_name=None) -> None:
    query_sql = '''
        SELECT FirstName
              ,City 
              ,State
          FROM customers
        '''
    filter_query = 'WHERE '
    if city_name and state_name:
        filter_query += f"City = '{city_name}' and State = '{state_name}'"
        query_sql += filter_query
    if city_name and not state_name:
        filter_query += f"City = '{city_name}'"
        query_sql += filter_query
    if state_name and not city_name:
        filter_query += f"State = '{state_name}'"
        query_sql += filter_query
    return unwrapper(execute_query(query_sql))


# get_customers(city_name='Budapest')



def get_uniqye_customers() -> Set:
    query_sql = '''
        SELECT FirstName
            FROM customers;
    '''
    names = execute_query(query_sql)
    unique_names = set()
    for name in names:
        unique_names.add(name[0])
    return len(unique_names)


# print(get_uniqye_customers())

# 1) Реалізувати функцію, яка порахує прибуток по таблиці invoice_items. Сума по замовленню = UnitPrice * Quantity. Прибуток = сумма замовлень. Якщо вирішуєте через sql, то необхідно для суми викрористати агрегатну функцію sum.


def get_sum_invoice() -> int or float:
    query_sql = '''
            SELECT UnitPrice
            , Quantity
            FROM invoice_items;
        '''
    summ = 0
    datas = execute_query(query_sql)
    for data in datas:
        sum = data[0]*data[1]
        summ +=sum
    print(round(summ, 2))

get_sum_invoice()

# 2) Реалізувати функцію, которая виведе повторювані FirstName з таблиці customers і кількість їх входжень в таблицю. Результат має виглядати як:
# Тобто виводимо тільки ті імена, які повторюються більше одного разу.

def get_repeat_customers() -> dict:
    query_sql = '''
        SELECT FirstName
            FROM customers;
    '''
    names = execute_query(query_sql)
    counter = {}

    for elem in names:
        counter[elem] = counter.get(elem, 0) + 1

    doubles = {element: count for element, count in counter.items() if count > 1}

    for key, value in doubles.items():
        print(key, value)

get_repeat_customers()