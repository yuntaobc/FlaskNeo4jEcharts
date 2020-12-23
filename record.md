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

```Cypher
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

`match p=(u:User {user_id:322})-[r:PARTICIPATE]-(e:Event) with collect([u.unique_id, u.name]) as u, collect([e.event_name]) as e, r as r return u,r,e limit 1`

 > [[[['khankakar47', 'Waheed Kakar']], <Relationship id=775319 nodes=(<Node id=321 labels=frozenset() properties={}>, <Node id=564 labels=frozenset() properties={}>) type='PARTICIPATE' properties={'type': '评论', 'time': neo4j.time.DateTime(2019, 9, 28, 3, 40, 0.0, tzinfo=<UTC>)}>, [['#WeStandWithKochai']]]]


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


#### Import all data

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
