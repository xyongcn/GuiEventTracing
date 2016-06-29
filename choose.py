#!/usr/python
import time,MySQLdb

conn = MySQLdb.connect(host="localhost",user="root",passwd="123456",db="Tree",charset="utf8")
cursor=conn.cursor()
print "connect success!"
file_object = open('1234.txt')
try:
   for line in file_object:
     s=line.split('  ')
     ss=s[2].split('"')
     if s[2].find(".moc") == -1 & s[2].find("util") ==-1 & s[2].find("component") & s[2].find("lambda") == -1:
       sql="insert into tree values ("+s[0]+","+s[1]+",'"+ss[3]+"','"+s[3]+"','"+s[4]+"')"
       cursor.execute(sql)
finally:
   file_object.close()
sql="select * from tree group by function,para having count(function)=1 and count(para)=1";
#sql = "select * from tree";
cursor.execute(sql)

#cursor.execute("truncate table tree")
for row in cursor.fetchall():
   sql="insert into tree1(time,function,name,para) values ('"+row[0]+"','"+row[2]+"','"+row[3]+"','"+row[4]+"')"
   cursor.execute(sql)   
sql= "select * from tree1 order by time"
cursor.execute(sql)
i=1
for row in cursor.fetchall():
   sql="update tree1 set num='"+str(i)+"' where time="+row[0]
   cursor.execute(sql)
   i=i+1
   cursor.execute("select substr("+row[0]+",1,10) from tree1")
   for r in cursor.fetchall():
      sql1="update tree1 set time = '"+r[0]+"' where time="+row[0]
      cursor.execute(sql1)
      break
sql = "select time,function,name,min(num) from tree1 group by time"
cursor.execute(sql)
for r in cursor.fetchall():
    sql = "select * from tree1 where num="+r[3]
    cursor.execute(sql)
    for row in cursor.fetchall():
        print row[0]
        print row[1]
        print row[2]
        print row[3]
        break
cursor.execute("truncate table tree")
cursor.execute("truncate table tree1")
cursor.close()
conn.commit()
conn.close()
