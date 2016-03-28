
# GUI处理函数自动获取工具帮助文档

本工具的设计目的是为了设计一款Linux系统上的GUI处理函数自动获取的工具，最初想法是设计一款全自动的处理函数自动获取工具，但是在设计和实现的过程中受“删选依据无法设定”等因素的限制，所以在我们想在开始设置一款半自动函数获取工具，以下是我们对该工具的设计思路：

1. 首先在Linux系统上将环境配置好，其中包括System的安装、相应的应用调试符号表。
 * System的安装：
   * 在/etc/apt/sources.list.d/目录下面新建一个debuginfo_debs.list文件内容如下：
    deb http://ddebs.ubuntu.com trusty main restricted universe multiverse      
    deb http://ddebs.ubuntu.com trusty-updates main restricted universe multiverse
    其中trusty是对应ubuntu版本的发行代号可以通过
    cat /etc/lsb-release  | grep DISTRIB_CODENAME 命令得到。
   * 然后执行以下命令：
     apt-get update
     在执行完这句话后可能会报错，报错后执行以下命令，然后在将此命令执行一遍。
sudo apt-key adv –keyserver keyserver.ubuntu.com –recv-keys XXXXXX
 * 安装systemtap: apt-get install systemtap
 * 符号表的安装：
先用apt-cache search 应用名来寻找相应应用的符号表
例如：apt-cache search vlc 能找到其相应的符号表为vlc-dbg
2. 相应应用动态链接库的定位：首先利用strace来获取大量与相关应用有关的动态链接库，然后利用正则表达式来过滤出无用的动态链接库，从而获得有用的动态链接库。在这部分由于需要肉眼进行筛选，所以在此处我们暂时指定所需应用的动态链接库。例如：vlc的动态链接库的位置为/usr/lib/vlc/plugins/gui/libqt4_plugin.so.
3. 利用systemtap进行函数的获取：在进行函数获取时需要辅助利用数据库，在进行本工具设计时利用的数据库为mysql数据库。在利用systemtap对Linux系统GUI处理函数的获取时需要利用数据库对其进行删选。在这里我们对获取函数的数目进行函数获取，阈值大于等于2过滤掉。
 * 首先利用Systemtap对某一应用进行每一个操作的函数信息，执行语句为：sudo stap –e ‘probe process(/usr/lib/vlc/plugins/gui/libqt4_plugin.so).function(“*”).call{printf(“%d : %d : %s :%s \n”,gettimeofday_s(),pid(),pp(),execname());} >> 123.txt
 * 然后利用数据库对上一步提取的数据进行筛选
   * Mysql数据库的安装：
      * 首先检测系统是否安装mysql数据库：sudo netstat –tap | grep mysql
      * 如果数据库没有安装成功的话，则继续安装Mysql数据库：sudo apt-get install mysql-server mysql-client
在此安装过程中会让你输入root用户(管理MySQL数据库用户，非Linux系统用户)密码，按照要求输入即可。
      * 测试安装是否成功： sudo netstat -tap | grep mysql
      * 也可通过登录MySQL测试：在终端输入 mysql -uroot -p 接下来会提示你输入密码，输入正确密码，即可进入。
   * 建数据库：create database Tree
   * 建表：create table tree(time int,pid int, pp char(100),name char(50),num int);
4. 然后执行process.py脚本就可筛选出我们希望获得的函数。最后再从这些获取的函数中手工的筛选出最终的目标函数。
