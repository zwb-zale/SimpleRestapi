### 项目说明
```
本项目可以快速搭建一个简易的restapi服务

本项目已经包含一些数据库资料的增删改查接口，如需要新增或者替换这些接口，可修改yaml文件

项目采用的数据库是mysql，如需修改mssql，可自行修改
```
### 项目搭建
```
1.由于本项目用的数据库是mysql，需要先安装mysql，并建数据库
进入【MYSQL与RESTAPI部署流程】文件夹，打开 必看下载地址.txt，下载最新版离线安装mysql安装包
按【第一步，数据库安装步骤，按图片顺序执行】里的图片顺序完成安装，注意mysql的密码设置，本项目中使用的密码是mysql123456789
你可以自行修改密码，修改完后需要进入后端项目的config.py文件，将原始密码替换掉
2.安装完mysql后，需要建里数据库，本项目后端中的数据库名称是smartking，如果你用的数据库名称不是这个，请在config.py文件中替换
以上完成了mysql淡妆与配置，目前数据库中没有任何表。

3.进入wechatservicepy，运行create_new_table_run.py，运行成功后会自动在数据库中新建一个名为wechatphone的表，如果需要修改表名，
进入models_base.py，找到__tablename__，修改对应的字符串即可
```

### run
```
python run.py
```

### swagger debug:
```
http://localhost:8887/wechatservicepy/v1.0/ui/

```

