### 需求
1. 小程序用户登录
2. 限制使用次数
3. 管理员管理账号使用情况

#### 本地运行方式(mv local_settings.py.template local_settings.py)
安装本地环境
```shell
pip install -r requirements.txt
```
初始化数据库
```shell
python manager.py migrate
```
创建用户
```shell
python manager.py create_manager
```
运行项目
```shell
python manager.py runserver 9000
```
访问服务
```shell
http://127.0.0.1:9000/admin
```
#### docker部署(删除local_settings.py)
```shell
dcker-compose build && docker-compose up -d
```
#### 创建用户
```shell
docker-compose exec boss python manage.py create_manager
```
访问服务
```shell
http://127.0.0.1:8000/admin
```
