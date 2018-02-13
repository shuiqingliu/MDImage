# -*- coding: UTF-8 -*-

from  mysql.connector import errors
import mysql.connector
import logging

#set logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)


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
    " `bucket` VARCHAR (20) NOT NULL"
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
def insertData(username,ak,sk,host,bucket):
    add_user = """INSERT INTO bot.user
                (username,ak,sk,host,bucket)
                VALUES (%s, %s, %s, %s,%s)"""
    user_data = (username,ak,sk,host,bucket)
    try:
        cursor.execute(add_user,user_data)
        db.commit()
        return True
    except mysql.connector.Error as err:
        print('Failed to insert data:{}'.format(err))
        return False

#query
def getData(username):
    cursorTemp = db.cursor()
    query = ("select username,ak,sk,host,bucket from bot.user"
             " WHERE username=%s")
    cursorTemp.execute(query,[username])
    result = cursorTemp.fetchall()
    if len(result) == 0:
        return False
    else:
        return result

#update all info
def update(username,ak,sk,host,bucket):
    updateUserInfo = ("update user set ak= %s, sk= %s,host=%s,bucket=%s where username= %s")
    print("DBHelper Upadate: %s",username +':'+ ak +':' +sk + ':' + host)
    try:
        cursor.execute(updateUserInfo,[ak,sk,host,bucket,username])
        db.commit()
        return True
    except mysql.connector.Error as err:
        print('Failed to update user info')
        return False

#update bucket
def updateBucket(username,bucket):
    update = ("update user set bucket=%s where username= %s")
    try:
        cursor.execute(update,[bucket,username])
        db.commit()
        return True
    except mysql.connector.Error as err:
        print(err)
        print('Failed to update user info')
        return False

#return specific user info
def getDetails(username):
    result = getData(username)
    if result != False:
        ak = result[0][1]
        sk = result[0][2]
        host = result[0][3]
        bucket = result[0][4]
        resultList = []
        resultList.extend([ak, sk, host, bucket])
        return resultList
    else:
        return False

def delete(username):
    deleteUsr = """delete from user where username=%s"""
    cursor.execute(deleteUsr,username)
    db.commit()

def main():
    #createTable(cursor)
    #delete('qingliu')
    #insertData('test','23rfff','345dsfff')
    print(getData('qingliu'))


if __name__ == '__main__':
    main()