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
        console.log("success");
//        console.log(data);
//        data_ = JSON.stringify(data)
//        console.log(typeof(data));
//        $("#result").text(data_)
        // 基于准备好的dom，初始化echarts实例
        links = data[1];
        data = data[0];
        console.log(data)
        console.log(links)
        var myChart = echarts.init(document.getElementById('result'));

        // 指定图表的配置项和数据
        var option = {
            title: {
                text: 'Event User Relationship'
            },
            tooltip: {},
            legend: {
                data:['销量']
            },
            series: [{
                type: 'graph',
                coordinateSystem: null,
                hoverAnimation: true,
                layout : 'force',
                roam : true,
                data: data,
                links: links,
            }]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
     }});
}
