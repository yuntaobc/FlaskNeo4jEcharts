function event_user(){
    var event_id = $("#event_id").val();
    var event_id = 61;

    var s_time = $("#s_time").val();
    var e_time = $("#e_time").val();
    var data = {"event_id":event_id, "s_time":s_time, "e_time":e_time};
    var data = JSON.stringify(data);

    $.ajax({
     type:"POST",
     url:"/api/event/user",
     contentType: "application/json;charset=utf-8",
     data:data,
     //dataType:"json",
     error:function(data){
        console.log("error")
        console.log(data);
     },
     success:function(data){
        console.log("success")
//        console.log(typeof(data));
//        data_ = JSON.stringify(data)
//        console.log(typeof(data));
//        $("#result").text(data_)
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('result'));

        // 指定图表的配置项和数据
        var option = {
            title: {
                text: 'ECharts 入门示例'
            },
            tooltip: {},
            legend: {
                data:['销量']
            },
            xAxis: {
                data: ["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"]
            },
            yAxis: {},
            series: [{
                name: '销量',
                type: 'bar',
                data: [5, 20, 36, 10, 10, 20]
            }]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
     }});
}

function event_list(){
    var name = $("#event_user").find("#name").val();
    var data = JSON.stringify({"name":name})

    $.ajax({
     type:"POST",
     url:"/event/list",
     contentType: "application/json;charset=utf-8",
     data:data,
     //dataType:"json",
     error:function(data){
        console.log("error")
        console.log(data);
     },
     success:function(data){
        console.log("success")
        console.log(data);
        $("#result").text(data)
     }});
}



