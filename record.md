### 记录

#### csv导入数据

```bash
neo4j-admin import \
     --database order \
     --id-type=INTEGER \
     --nodes=Customer=customers.csv \
     --nodes=Product=products.csv \
     --nodes=Order="orders_header.csv,orders1.csv,orders2.csv" \
     --relationships=CONTAINS="order_details.csv" \
     --relationships=ORDERED="customer_orders_header.csv,orders1.csv,orders2.csv" \
     --trim-strings=true

neo4j-admin import \
     --database twitter \
     --id-type=INTEGER \
     --nodes=Event=event.csv \
     --nodes=User=user.csv \
     --nodes=Topic=topic.csv \
     --relationships=COOCCURENCE=event_event.csv \
     --relationships=PARTICIPATE=event_user.csv \
     --trim-strings=true

```


#### 测试neopython返回的数据

```python
match p=(u:User {user_id:322})-[r:PARTICIPATE]-(e:Event) return u,r,e limit 1

<Record 
u=<Node id=321 labels=frozenset({'User'}) properties={'name': 'Waheed Kakar', 'unique_id': 'khankakar47', 'user_id': 322}> 
r=<Relationship id=639831 
nodes=(
<Node id=321 labels=frozenset({'User'}) properties={'name': 'Waheed Kakar', 'unique_id': 'khankakar47', 'user_id': 322}>, 
<Node id=564 labels=frozenset({'Event'}) properties={'event_name': '#WeStandWithKochai', 'event_id': 19}>) 
type='PARTICIPATE' properties={'type': '转发', 'time': neo4j.time.DateTime(2019, 9, 28, 1, 53, 0.0, tzinfo=<UTC>)}>
e=<Node id=564 labels=frozenset({'Event'}) properties={'event_name': '#WeStandWithKochai', 'event_id': 19}>>
```


#### 测试对结果进行过滤后的效率 发现稍微增加了时间

```python
match p=(u:User {user_id:322})-[r:PARTICIPATE]-(e:Event) with collect([u.unique_id, u.name]) as u, collect([e.event_name]) as e, r as r return u,r,e limit 1

 [[[['khankakar47', 'Waheed Kakar']], <Relationship id=775319 nodes=(<Node id=321 labels=frozenset() properties={}>, <Node id=564 labels=frozenset() properties={}>) type='PARTICIPATE' properties={'type': '评论', 'time': neo4j.time.DateTime(2019, 9, 28, 3, 40, 0.0, tzinfo=<UTC>)}>, [['#WeStandWithKochai']]]]
```

#### 检查echarts的数据格式 

```
# 测试样例
data: [{
      id: "user_1",
      name: "Myriel",
      value: 'user_1',
      category: 0,
      label: {
        show: true,
        position: 'inside'
      }
      formater: "{c}"
    }, {
      id: "user_2",
      name: "Napoleon",
      value: 'user_2',
      category: 0
    }, {
      id: "user_3",
      name: "MlleBaptistine",
      value: 'user_3',
      category: 1
    }],
links: [{
      id: "0",
      source: "user_1",
      target: "user_2"
    }, {
      id: "1",
      source: "user_1",
      target: "user_3"
    }, {
      id: "2",
      source: "user_2",
      target: "user_3"
    }],
```


#### Import all Test data

```bash
neo4j-admin import \
     --database twitter \
     --id-type=INTEGER \
     --nodes=Event=event.csv \
     --nodes=User=user.csv \
     --nodes=Topic=topic.csv \
     --relationships=COOCCURENCE=event_event.csv \
     --relationships=PRODUCE=event_topic.csv \
     --relationships=PARTICIPATE=event_user.csv \
     --relationships=JOIN=user_topic.csv \
     --relationships=INTERACT=user_user.csv \
     --trim-strings=true
```

### 部分数据格式

```python
[
  <Node id=552 labels=frozenset({'Event'}) properties={'name': '#RedForKashmir', 'event_id': 7}>, 
  [<Relationship id=2014932 
    nodes=(
      <Node id=552 labels=frozenset({'Event'}) properties={'name': '#RedForKashmir', 'event_id': 7}>, 
      <Node id=749 labels=frozenset({'Event'}) properties={'name': '#Kashmir', 'event_id': 204}>
    )
    type='COOCCURENCE' 
    properties={'type': '共现', 'time': neo4j.time.DateTime(2019, 9, 28, 3, 13, 0.0, tzinfo=<UTC>)}, 
   <Relationship id=2001767 
    nodes=(
      <Node id=749 labels=frozenset({'Event'}) properties={'name': '#Kashmir', 'event_id': 204}>,
      <Node id=749 labels=frozenset({'Event'}) properties={'name': '#Kashmir', 'event_id': 204}>) type='COOCCURENCE' 
    properties={'type': '共现', 'time': neo4j.time.DateTime(2019, 9, 28, 23, 26, 0.0, tzinfo=<UTC>)}>
  ],

 <Node id=749 labels=frozenset({'Event'}) properties={'name': '#Kashmir', 'event_id': 204}>]


[
  [<Node id=1615 labels=frozenset({'Topic'}) properties={'name': 'assault', 'count': '1004', 'topic_id': 524, 'time': neo4j.time.DateTime(2019, 9, 28, 0, 0, 0.0, tzinfo=<UTC>)}>],
  [<Node id=1613 labels=frozenset({'Topic'}) properties={'name': 'regime', 'count': '1006', 'topic_id': 522, 'time': neo4j.time.DateTime(2019, 9, 28, 0, 0, 0.0, tzinfo=<UTC>)}>], 
  [<Node id=1612 labels=frozenset({'Topic'}) properties={'name': 'hand', 'count': '1009', 'topic_id': 521, 'time': neo4j.time.DateTime(2019, 9, 28, 0, 0, 0.0, tzinfo=<UTC>)}>], [<Node id=1610 labels=frozenset({'Topic'}) properties={'name': 'friends', 'count': '1010', 'topic_id': 519, 'time': neo4j.time.DateTime(2019, 9, 28, 0, 0, 0.0, tzinfo=<UTC>)}>], [<Node id=1608 labels=frozenset({'Topic'}) properties={'name': 'report', 'count': '1019', 'topic_id': 517, 'time': neo4j.time.DateTime(2019, 9, 28, 0, 0, 0.0, tzinfo=<UTC>)}>], [<Node id=1606 labels=frozenset({'Topic'}) properties={'name': 'oto', 'count': '1022', 'topic_id': 515, 'time': neo4j.time.DateTime(2019, 9, 28, 0, 0, 0.0, tzinfo=<UTC>)}>], [<Node id=1601 labels=frozenset({'Topic'}) properties={'name': 'reason', 'count': '1035', 'topic_id': 510, 'time': neo4j.time.DateTime(2019, 9, 28, 0, 0, 0.0, tzinfo=<UTC>)}>], [<Node id=1593 labels=frozenset({'Topic'}) properties={'name': 'attack', 'count': '1041', 'topic_id': 502, 'time': neo4j.time.DateTime(2019, 9, 28, 0, 0, 0.0, tzinfo=<UTC>)}>], [<Node id=1586 labels=frozenset({'Topic'}) properties={'name': 'TH', 'count': '1046', 'topic_id': 495, 'time': neo4j.time.DateTime(2019, 9, 28, 0, 0, 0.0, tzinfo=<UTC>)}>], [<Node id=1587 labels=frozenset({'Topic'}) properties={'name': 'Indonesia', 'count': '1046', 'topic_id': 496, 'time': neo4j.time.DateTime(2019, 9, 28, 0, 0, 0.0, tzinfo=<UTC>)}>], [<Node id=1584 labels=frozenset({'Topic'}) properties={'name': 'girl', 'count': '1051', 'topic_id': 493, 'time': neo4j.time.DateTime(2019, 9, 28, 0, 0, 0.0, tzinfo=<UTC>)}>], [<Node id=1579 labels=frozenset({'Topic'}) properties={'name': 'Here', 'count': '1056', 'topic_id': 488, 'time': neo4j.time.DateTime(2019, 9, 28, 0, 0, 0.0, tzinfo=<UTC>)}>], [<Node id=1577 labels=frozenset({'Topic'}) properties={'name': 'Act', 'count': '1059', 'topic_id': 486, 'time': neo4j.time.DateTime(2019, 9, 28, 0, 0, 0.0, tzinfo=<UTC>)}>], [<Node id=1573 labels=frozenset({'Topic'}) properties={'name': 'hope', 'count': '1071', 'topic_id': 482, 'time': neo4j.time.DateTime(2019, 9, 28, 0, 0, 0.0, tzinfo=<UTC>)}>], [<Node id=1572 labels=frozenset({'Topic'}) properties={'name': 'HKPolice', 'count': '1073', 'topic_id': 481, 'time': neo4j.time.DateTime(2019, 9, 28, 0, 0, 0.0, tzinfo=<UTC>)}>], [<Node id=1098 labels=frozenset({'Topic'}) properties={'name': 'police', 'count': '10822', 'topic_id': 7, 'time': neo4j.time.DateTime(2019, 9, 28, 0, 0, 0.0, tzinfo=<UTC>)}>], [<Node id=1566 labels=frozenset({'Topic'}) properties={'name': 'Uyghur', 'count': '1088', 'topic_id': 475, 'time': neo4j.time.DateTime(2019, 9, 28, 0, 0, 0.0, tzinfo=<UTC>)}>], [<Node id=1564 labels=frozenset({'Topic'}) properties={'name': 'So', 'count': '1088', 'topic_id': 473, 'time': neo4j.time.DateTime(2019, 9, 28, 0, 0, 0.0, tzinfo=<UTC>)}>], [<Node id=1561 labels=frozenset({'Topic'}) properties={'name': 've', 'count': '1093', 'topic_id': 470, 'time': neo4j.time.DateTime(2019, 9, 28, 0, 0, 0.0, tzinfo=<UTC>)}>], [<Node id=1560 labels=frozenset({'Topic'}) properties={'name': 'San', 'count': '1093', 'topic_id': 469, 'time': neo4j.time.DateTime(2019, 9, 28, 0, 0, 0.0, tzinfo=<UTC>)}>]]

{id: 1615, name: "assault", count: "1004", time: "2019-09-28T00:00:00.000000000+00:00", category: 2}
```



### 最终数据导入

```bash
./neo4j-admin import \
     --database twitter \
     --id-type=INTEGER \
     --trim-strings=true \
     --nodes=Event=event.csv \
     --nodes=Topic=topic.csv \
     --nodes=User=user.csv \
     --relationships=COOCCURENCE=event_event.csv \
     --relationships=PARTICIPATE=event_user.csv \
     --relationships=PRODUCE=event_topic.csv \
     --relationships=INTERACT=user_user.csv \
     --relationships=JOIN=user_topic.csv \
     --relationships=RELATED=topic_topic.csv

```

1. 与话题相关的表的时间格式不对

2. 用户表里的id字段有nan

3. user表有未处理的数据

4. user表id字段数值很大

5. user_topic 重复表头

```bash
# User的id字段数字很大，统一改称STRING
neo4j-admin import \
  --database twitter \
  --high-io=true \
  --skip-bad-relationships=true \
  --skip-duplicate-nodes=true \
  --max-memory=10G \
  --nodes=User=user.csv \
  --nodes=Event=event.csv \
  --nodes=Topic=topic.csv \
  --relationships=COOCCURENCE=event_event.csv \
  --relationships=PARTICIPATE=event_user.csv \
  --relationships=PRODUCE=event_topic.csv \
  --relationships=INTERACT=user_user.csv \
  --relationships=JOIN=user_topic.csv \
  --relationships=RELATED=topic_topic.csv 

```


```bash
IMPORT DONE in 6m 4s 882ms. 
Imported:
  2201523 nodes
  214236146 relationships
  269076259 properties
Peak memory usage: 1.087GiB
There were bad entries which were skipped and logged into /media/yuntaobc/E/Ubuntu/neo-data/final/import.report 


IMPORT DONE in 7m 37s 994ms. 
Imported:
  1903034 nodes
  202484808 relationships
  253754618 properties
Peak memory usage: 257.1MiB
There were bad entries which were skipped and logged into /home/yuntaobc/Programs/neo4j-community/bin/final/import.report

```
#### Directory

```cypher
CREATE INDEX ON :User(user_id)
CREATE INDEX ON :Event(event_id)
CREATE INDEX ON :Event(topic_id)
```