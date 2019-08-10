import json
import urllib.request
from datetime import date, datetime
import pyodbc 

# Коннект к API и получение JSON файла
url = 'https://online.moysklad.ru/api/remap/1.1/entity/customerorder'
username = 'admin@b4959285'
password = 'e148b97e73'
p = urllib.request.HTTPPasswordMgrWithDefaultRealm()

p.add_password(None, url, username, password)

handler = urllib.request.HTTPBasicAuthHandler(p)
opener = urllib.request.build_opener(handler)
urllib.request.install_opener(opener)

page = urllib.request.urlopen(url).read()
page = page.decode('utf8').replace("'", '"')

data = json.loads(page)

# Проверка сегоднешних заказов в JSON файле и обновление их в базе данніх.
today = date.today()
for index in range(len(data.get('rows'))):
    order = []
    if today == datetime.strptime(data.get('rows')[index].get('moment'), '%Y-%m-%d %H:%M:%S').date():
        order.append(data.get('rows')[index].get('id'))
        order.append(data.get('rows')[index].get('name'))
        order.append(data.get('rows')[index].get('moment'))
        order.append(data.get('rows')[index].get('sum'))
        order = tuple(order)
        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server}; SERVER=maxbicotest.database.windows.net; Database=TestSPlist;  UID=TestTask; PWD=TestDev20191;')

        cursor = conn.cursor()
        cursor.execute('SELECT * FROM EduardDmitriuk.Orders')

        cursor.execute('''
                INSERT INTO EduardDmitriuk.Orders (id, name, moment, sum)
                VALUES
                {}
                '''.format(order))
        conn.commit()
