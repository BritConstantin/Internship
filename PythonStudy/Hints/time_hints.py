import datetime


t =  datetime.datetime.now()
# print('{}{}{}-{}:{}:{}.000'.
#                 format(t[0],t[1],t[2],t[3],t[4],t[5]))
# 52=20210125-15:48:14.331
print(t.strftime("%Y%m%d-%H:%M:%S.000"))
t = datetime.datetime.now() + datetime.timedelta(seconds=30)
print(t.strftime("%Y%m%d-%H:%M:%S.000"))
