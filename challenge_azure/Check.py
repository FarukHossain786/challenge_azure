from challenge_azure import Dbconnection
class Database():
    def connect(self):
        mydb = Dbconnection.DB()
        connection = mydb.mydb
        cursor = connection.cursor()
        cursor.execute('insert into featurs(course_id, feature) values(1, 54)')
        connection.commit()

    def create_table(self):
        mydb = Dbconnection.DB()
        mydb.create_table()


    def mongo_test(self):
        connection = Dbconnection.DB()
        mongo_db= connection.mongo()
        return mongo_db
