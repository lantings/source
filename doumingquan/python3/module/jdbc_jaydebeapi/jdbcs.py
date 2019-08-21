import pymysql

class jdbc_connect:
    cursor="";
    db=False;

    def __init__(self,host,username,password,database):
        try:
            jdbc_connect.db = pymysql.connect(host, username,password, database, charset="utf8");
            jdbc_connect.cursor = self.db.cursor();
        except BaseException:
            print("连接数据库异常")
            self.db.close()

    def  select(self,sql):
        jdbc_connect.cursor.execute(sql);
        students=self.cursor.fetchall();
        return students;

    def insert(self,sql):
       try:
        jdbc_connect.cursor.execute(sql);
        jdbc_connect.db.commit();
       except pymysql.DataError:
            jdbc_connect.db.rollback();
            print("执行添加操作失败")
            return "1"
       else:
           return "0"

    def update(self,sql):
        try:
            jdbc_connect.cursor.execute(sql);
            jdbc_connect.db.commit();
        except pymysql.DataError:
            jdbc_connect.db.rollback();
            print("执行修改操作失败")
            return "1"
        else:
            return "0"

    def delete(self,sql):
        try:
            jdbc_connect.cursor.execute(sql);
            jdbc_connect.db.commit();
        except pymysql.DataError:
            jdbc_connect.db.rollback();
            print("执行删除操作失败")
            return "1"
        else:
            return "0"

    def closedb(self):
        try:
            self.cursor.close();
            self.db.close();
        except BaseException:
            print("db close error")
