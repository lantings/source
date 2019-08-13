
file_path = 'data.txt'
file= open(file_path, 'r', encoding='utf-8')
# 逐行读取数据
for line in file.readlines():
    uid = "null"
    screen_name = "null"
    gender = "null"
    fans_no = 0
    description = "null"
    is_followed = "0"
    if line:
        linelist = line.split()
        # print(linelist[0])
        uid = linelist[0] if len(linelist[0]) > 0 else "null"
        print(uid)
        screen_name = list[1] if len(list[1]) > 0 else "null"
        gender = list[2] if list[2] in ['f', 'm'] else 'n'
        fans_no = int(list[3]) if type(int(list[3])).__name__ == 'int' else 0
        description = list[4] if len(list[4]) > 0 else "null"

        # mysql入库操作
        # sql = """
        #     insert into wbuser (uid,screen_name,gender,fans_no,description,is_followed) VALUES ('%s','%s','%s','%d','%s','%s')"""

    else:
        break
