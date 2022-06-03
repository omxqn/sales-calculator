
# pip install mysql-connector-python
import mysql.connector
import datetime
global times
global date

from cachetools import cached, TTLCache

cache = TTLCache(maxsize=100, ttl=86400)

@cached(cache)
def start():
    global times
    global date
    global db
    global my_curser
    date = datetime.datetime.now().date()
    times = datetime.datetime.now().time().strftime(f'%H:%M:%S')

    db = mysql.connector.connect(
        host='db4free.net',
        user='sojjadah',
        passwd='sojjadah99',
        database='sojjadah')
    my_curser = db.cursor()
    print("Database connected successfully")
# Create new table
'''
# view table descriptions
my_curser.execute('DESCRIBE id_list')
for i in my_curser:
    print(i)
'''



def new_table(table_name, instractions):
    '''Create new table'''
    try:
        # UNSIGNED there is no - or +
        # Example: instractions =  mention_ID int PRIMARY KEY AUTO_INCREMENT,name VARCHAR(50),id int(20) UNSIGNED,date VARCHAR(50),message VARCHAR(50)
        my_curser.execute(f'CREATE TABLE {table_name} ({instractions})')
        return "Table has been created successfully"
    except Exception:
        return 'This table is already existed'



def delete_all(table_name):
    my_curser.execute(f'DELETE FROM {table_name}')
    return "All data has been deleted"



def add_new(table, item_name, price, sale_type,quantity):  # Insert new details
    '''Add new data in elements'''
    # table = id_list
    try:
        my_curser.execute(
            f'INSERT INTO {table} (item_name, price, sale_type, quantity, date) VALUES {(item_name, price, sale_type, quantity, str(date) + " " + str(times) )}')
        print("committing")
        db.commit()
        print("Data saved successfully in database")
    except Exception:
        print("Error")



def get_table_info(table, id):
    global my_curser
    '''Get infos of the current table'''
    try:
        my_curser.execute(f'SELECT * FROM {table}')
        print("test")
        print(my_curser)
        x = []
        for i in my_curser:
            x.append(i)
            print(i)
        print("Data imported successfully")
        return x

    except Exception:
        print("Error while gathering information from database")


def table_columns(table):
    data = ""
    my_curser.execute(f"SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'{table}'")

    for i in my_curser:
        data += ' ' + i[3]
    data = data.split(" ")
    data.pop(0)

    return data

start()
if __name__ == "__main__":
    #new_table("sale_log",'sale_ID int PRIMARY KEY AUTO_INCREMENT,item_name VARCHAR(300),price VARCHAR(50) ,sale_type VARCHAR(50) ,quantity VARCHAR(50),date VARCHAR(150)')

    '''    f = open('database_cache.txt', 'w')
    f.write(str(my_curser))
    f.close()'''

    #in1 = str(input('item name: '))
    #in2 = str(input('item price: '))
    #in3 = str(input('item type: '))
    #print(add_new(table='sale_log',item_name=in1, price=in2, sale_type=in3))
    #print(get_table_info('sale_log', False))
    '''
    in1 = str(input('item name: '))
    in2 = str(input('item price: '))
    in3 = str(input('item type: '))
    print(date)
    print(add_new(table='sale_log',item_name=in1, price=in2, sale_type=in3))

    in1 = input('Name: ')
    in2 = input('id: ')
    in3 = input('Message: ')'''
    # print(new_table('dm','Message_ID int PRIMARY KEY AUTO_INCREMENT,name VARCHAR(50),id int(20) UNSIGNED,date VARCHAR(50),message VARCHAR(50)'))

    # add_new(table='dm',name='Non',id=1511515,message='Test_message',replied_username=None,downloaded_url=None)

    #new_table("sale_log", 'sale_ID int PRIMARY KEY AUTO_INCREMENT,item_name VARCHAR(300),price VARCHAR(50) ,sale_type VARCHAR(50) ,date VARCHAR(150)')

'''    print('Done... ')
    print(get_table_info('sojjadah', id=True))
    # table_columns('vid')'''
