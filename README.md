#### 环境

- Ubuntu 20.04 LTS 
- Python 3.8.5 
- Echarts 5.0 
- Flask 1.1 
- Neo4j 4.2 

#### 安装Echarts

> ECharts 提供用于关系数据可视化的关系图、treemap、旭日图
> 
> 多种数据格式无需转换直接使用
> ECharts 内置的 dataset 属性（4.0+）支持直接传入包括二维表，key-value 等多种格式的数据源，
> 
> 千万数据的前端展现
> ECharts 同时提供了对流加载（4.0+）的支持，你可以使用 WebSocket 或者对数据分块后加载，加载多少渲染多少！
> 
> v4.9
> [Feature] [graph] 关系图支持节点间多条关系边. #12590 (wf123537200)
> 


#### 配置Neo4j


安装python环境：
  ```bash 
    pip3 install neo4j
    Installing collected packages: neo4j
    Successfully installed neo4j-4.2.0
  ```


修改配置,更改import路径(Didn't use)
- /etc/neo4j/neo4j.conf

- 取消下面的注释

    `dbms.security.allow_csv_import_from_file_urls=true`

- 变更路径

    `# dbms.directories.import=/var/lib/neo4j/import`
 
    `dbms.directories.import=/home/yuntaobc/neoimport`

创建新的数据库

 - 默认用户neo4j没有管理员权限 没用
   https://neo4j.com/docs/operations-manual/4.1/configuration/password-and-user-recovery/#recover-unassigned-admin-role
 - 使用一个hack方法
   https://stackoverflow.com/questions/60429947/error-occurs-when-creating-a-new-database-under-neo4j-4-0

#### Import data

把数据文件放到自定义的目录下面
使用neo4j-admin工具倒入
示例

```cypher
neo4j-admin import \
     --database order \
     --id-type=INTEGER \
     --nodes=Customer=customers.csv \
     --nodes=Product=products.csv \
     --nodes=Order="orders_header.csv,orders1.csv,orders2.csv" \
     --relationships=CONTAINS="order_details.csv" \
     --relationships=ORDERED="customer_orders_header.csv,orders1.csv,orders2.csv" \
     --trim-strings=true
```

导入之前默认twitter|neo4j，导入之后出现上面的错误

> Could not connect with the "neo4j://" scheme to this Neoj server. Automatic retry using the "bolt://" scheme in a moment...

```bash
ERROR neo4j database "twitter" is unavailable, its status is "unknown."
```

把neo4j配置文件中默认连接的数据库修改成neo4j|twitter都不行
删除两个文件夹里的数据库文件，重新导入，切换配置文件可行

### 数据库中数据问题

事件A与事件B之间的关系很多,在不同的时间共现了很多次：


### 编写后端查询API

测试查询语句

```Cypher
match p=(u:User)-[r:PARTICIPATE]-(e:Event {event_id:24}) where datetime('20190928T0500') < r.time < datetime('20190928T2000') return u,e,r

match p=(u:User)-[r:PARTICIPATE]-(e:Event {event_id:24})  return u,e,r

match (u:User {user_id:53})-[r:PARTICIPATE]-(e:Event) with e.event_id as ID, e.event_name as Name, size(collect(e.event_name)) as Times return ID,Name,Times order by Times DESC
```

### Front Content

USE this things:
- flask_bootstrap
- flask_wtf
- bootstrap-3-typeahead
- getdatepicker
- bootstrap
- jQuery
- Echarts



### 启动

```bash
python3 manage.py runserver 
```
