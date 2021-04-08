###### 更新包:

- pip3 freeze > requirements.txt  
  代码规范:
- black 路径
  静态代码检测:
- mypy 路径

###### 数据库相关

1. Flask-Migrate 管理数据库：
   - 初始化：flask db init [已初始化，该步骤可以不执行]
   - register.database 文件：
     - 把表类 import 到 register_plugin 中
     - flask db migrate -m "xxxx" 生成迁移脚本
     - flask db upgrade 更新数据库，有则更新，无则创建

###### 更新包命令行

pip freeze > requirements.txt
