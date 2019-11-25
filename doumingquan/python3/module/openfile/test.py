

# with open('1.txt','rb') as f:
#     t = f.readlines()
# f.close()
# print(t[-1])
# print(type(t))
s= 2222222222
with open('1.txt','wb') as f:
    f.write(str(s)+"\n")
