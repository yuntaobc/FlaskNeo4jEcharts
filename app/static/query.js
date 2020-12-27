function event_user(){
    var myChart = echarts.init(document.getElementById('result'));
    myChart.showLoading();

    var event_id = Number($("#event-id").val());
    var s_time = $("#s-time").val().replace(" ", "T");
    var e_time = $("#e-time").val().replace(" ", "T");

    var event_id = 7;
    var s_time = '2019-09-01T15:09';
    var e_time = '2019-10-01T15:09';

    var data = {"event_id":event_id, "s_time":s_time, "e_time":e_time};
    var data = JSON.stringify(data);

    $.ajax({
     type:"POST",
     url:"/api/event/user",
     contentType: "application/json;charset=utf-8",
     data:data,
     // dataType:"json",
     error:function(data){
        console.log("error")
     },
     success:function(data){
        console.log("success");

        // 基于准备好的dom，初始化echarts实例
        links = data[1];
        data = data[0];

        // 指定图表的配置项和数据
        var categories = [
            {name: "Event"},
            {name: "User"},
            {name: "Topic"}
        ];
        var option = {
            title: {
                text: 'Event User Relationship'
            },
            legend: {
                data: [
                    {name: "Event"},
                    {name: "User"},
                    {name: "Topic"}
                ],
                type: 'plain',
                orient: 'vertical',
                right: 20
            },
            tooltip: {
                trigger: 'item',
            },
            series: [{
                data: data,
                links: links,
                categories: categories,
                type: 'graph',
                layout : 'force',
                roam: true,
                draggable: true,
                hoverAnimation: true,
                coordinateSystem: null,
                force: {
                    repulsion: 70,
                    gravity: 0.1,
                    friction: 0.4,
                    layoutAnimation: true
                },
                symbolSize: 15,
                label: {
                    show: true,
                    position: 'inside',
                },
                tooltip: {
                    formatter: function(params){
                        if(params.data.category == 1){
                            var result = 'User name: ' + String(params.data.name) + '<br>';
                            result += 'Unique ID: ' + String(params.data.value);
                        }else if(params.data.category == 0){
                            var result = 'Event name: ' + String(params.data.name);
                        }else if(params.data.category == 2){
                            var result = 'Topic name: ' + String(params.data.name);
                        }
                        console.log("formatter");
                        return result;
                    }
                },
            }]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.hideLoading();
        myChart.setOption(option);
     }});
}
