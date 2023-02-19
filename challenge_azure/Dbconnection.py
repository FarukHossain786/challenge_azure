import logging
import mysql.connector
import pymongo
logging.basicConfig(filename='log/app.log',filemode='w', level=logging.INFO)
# import mysql.connector
#create user 'user'@'%' identified by 'password'
class DB():
    def __init__(self):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="password",
                database="ineuron"
            )

            self.mydb = mydb
        except Exception as ex:
            logging.info('Database connection issue', ex)
    def mydb(self):
        return self.mydb

    def mongo(self):
        client = pymongo.MongoClient("mongodb+srv://hossainf114:password_mongo@cluster0.s1pyppv.mongodb.net/?retryWrites=true&w=majority")
        db = client.inuron
        return db





    def create_table(self):
        cursor = self.mydb.cursor()

        try:
            cursor.execute('DROP TABLE `course`, `curriculum`, `featurs`, `instructors`, `instructor_course`, `learn`, `requirements`, `sub_curriculum`')
        except:
            logging.info('Table drop issue')
        
        try:
            cursor.execute('create table course(id int auto_increment primary key, name varchar(200), description longtext, image varchar(100), start_date varchar(100), dout_time varchar(100), course_time varchar(100))')
        except:
            logging.info('Table already exist course')
        
        try:
            cursor.execute('create table featurs(id int auto_increment primary key, course_id int, feature varchar(150))')
        except:
            logging.info('Table already exist featurs')

        try:    
            cursor.execute('create table learn(id int auto_increment primary key, course_id int, learn varchar(150))')
        except:
            logging.info('Table already exist learn')
        
        try:
            cursor.execute('create table requirements(id int auto_increment primary key, course_id int, requirement varchar(150))')
        except:
            logging.info('Table already exist requirements')
        
        try:
            cursor.execute('create table instructors(id int auto_increment primary key, main_id varchar(100), name varchar(100), description longtext)')
        except:
            logging.info('Table already exist instructors')
        
        try:
            cursor.execute('create table instructor_course(id int auto_increment primary key, instrectur_id varchar(100), course_id int)')
        except:
            logging.info('Table already exist instructor_course')
        
        try:
            cursor.execute('create table curriculum(id int auto_increment primary key, course_id int, title varchar(150))')
        except:
            logging.info('Table already exist curriculum')
        
        try:
            cursor.execute('create table sub_curriculum(id int auto_increment primary key, course_id int, curriculum_id int, title varchar(150))')
        except:
            logging.info('Table already exist sub_curriculum')
            