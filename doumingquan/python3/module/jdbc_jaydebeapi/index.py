import jaydebeapi
# pip install JayDeBeApi
# conn=jaydebeapi.connect('com.mysql.jdbc.Driver',['jdbc:mysql://localhost:3306/test','hive','hive'],'/data/users/huser/lan/codes/useJPype/mysql-connector-java-5.1.36/mysql-connector-java-5.1.36-bin.jar')
# 其中mysql的用户名和密码都是hive,最后一个参数是驱动的jar包
conn=jaydebeapi.connect('oracle.jdbc.driver.OracleDriver','jdbc:oracle:thin:@127.0.0.1:1521/orcl',['hwf_model','hwf_model'],'E:/pycharm/lib/ojdbc14.jar')
url = 'jdbc:oracle:thin:@127.0.0.1:1521/orcl'
user = 'hwf_model'
password = 'hwf_model'
dirver = 'oracle.jdbc.driver.OracleDriver'
jarFile = 'E:\\pycharm\\lib\\ojdbc14.jar'
sqlStr = 'select * from dual'
# conn=jaydebeapi.connect('oracle.jdbc.driver.OracleDriver','jdbc:oracle:thin:@127.0.0.1:1521/orcl',['hwf_model','hwf_model'],'E:/pycharm/lib/ojdbc14.jar')
conn = jaydebeapi.connect(dirver, url, [user, password], jarFile)


curs=conn.cursor()
curs.execute('create table CUSTOMER("ID" INTEGER not null primary key,"NAME" varchar not null)')
curs.execute("insert into CUSTOMER values(1,'John')")
curs.execute("select * from CUSTOMER")
curs.fetchall()
[(1,u'John')]
