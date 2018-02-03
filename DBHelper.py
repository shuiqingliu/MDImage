# -*- coding: UTF-8 -*-

from  mysql.connector import errors
import mysql.connector


db = mysql.connector.connect(user='root',password='qingliu.',database='bot',buffered=True)
cursor = db.cursor()
TABLES = {}

#create table statement
TABLES['bot'] = (
    "CREATE TABLE `user` ("
    " `username` varchar(20) NOT NULL ,"
    " `ak` VARCHAR(40) NOT NULL ,"
    " `sk` VARCHAR(40) NOT NULL ,"
    " `host` VARCHAR(40) NOT NUll ,"
    " PRIMARY  KEY (`username`)"
    ") ENGINE=InnoDB"
)

#create user table
def createTable(cursor):
    try:
        tableList = """show tables"""
        cursor.execute(tableList)
        for table in cursor:
            if table[0] =='user':
                print('user table exists')
                return True
        cursor.execute(TABLES['bot'])
        return True
    except mysql.connector.Error as err:
        print('Failed creating table :{}'.format(err))
        return False

#inset in to 
def insertData(username,ak,sk,host):
    add_user = """INSERT INTO bot.user
                (username,ak,sk,host)
                VALUES (%s, %s, %s, %s)"""
    user_data = (username,ak,sk,host)
    try:
        cursor.execute(add_user,user_data)
        db.commit()
        return True
    except mysql.connector.Error as err:
        print('Failed to insert data:{}'.format(err))
        return False

#查询
def getData(username):
    query = ("select username,ak,sk,host from bot.user"
             " WHERE username=%s")
    cursor.execute(query,[username])
    if cursor == None:
        return False
    else:
        return cursor.fetchall()

def update(username,ak,sk,host):
    update = ("update user set ak= %s, sk= %s,host=%s where username= %s")
    try:
        cursor.execute(update,[ak,sk,host,username])
        db.commit()
        return True
    except mysql.connector.Error as err:
        print('Failed to update user info')
        return False

def delete(username):
    deleteUsr = """delete from user where username=%s"""
    cursor.execute(deleteUsr,username)
    db.commit()

def main():
    #createTable(cursor)
    #delete('qingliu')
    #insertData('test','23rfff','345dsfff')
    result = getData('test')
    if result == None:
        print("未找到")
    else:
        print(result)

if __name__ == '__main__':
    main()