from jdbcs import jdbc_connect
# 导入一个本地类 实例化
dbt=jdbc_connect("localhost", "root", "root", "test")
str1="select * from score"
#学生集合
students=dbt.select(str1)
print(students)
# insert_str="insert into student values('王五1',18,'sa51df321s')"
# print(dbt.insert(insert_str)
# print(students))
# students=dbt.select(str1)
# update_str="update student set name='王二麻子' where name='王五'"
# print(dbt.update(update_str))

delete_str="delete from student where name='王二麻子'"
dbt.delete(delete_str)
print(dbt.select(str1))