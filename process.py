import time,MySQLdb
#! /usr/bin/env stap
conn = MySQLdb.connect(host="localhost",user="root",passwd="123456",db="Tree",charset="utf8")
cursor=conn.cursor()
print "connect success!"

#input = open('data')

file_object = open('123.txt')
i=0
try:
   #list_of_all_line = file_object.readlines()
   #print list_of_all_line
   for line in file_object:
     #print line
     s=line.split(':')
     sql = "select * from tree where name="+s[2]
     cursor.execute(sql)
     for row in cursor.fetchall():
        i=i+1     
     if i>1:
        break
     else:
        sql="insert into tree values ("+s[0]+","+s[1]+",'"+s[2]+"','"+s[3]+"')"
        cursor.execute(sql)
finally:
   file_object.close()
#sql="insert into tree values ("+gettimeofday_s()+","+pid()+",'"+pp()+"','"+execname+"')"
#cursor.execute(sql)

#cursor.execute("select * from tree")
#for row in cursor.fetchall():
 # for r in row:
  #  print r
#param = (1,2,'a','b')
#cursor.execute(sql)
#print n

cursor.close()
conn.commit()
conn.close()

