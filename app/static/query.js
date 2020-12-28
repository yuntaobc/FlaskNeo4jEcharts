

function show_echarts(myChart, data, meta){
    // 基于准备好的dom，初始化echarts实例
    links = data[1];
    data = data[0];

    // 指定图表的配置项和数据
    var categories = [{
            name: "Event",
            symbolSize: 35,},{
            name: "User",
            symbolSize: 23,},{
            name: "Topic",
            symbolSize: 18,}
        ];
    var option = {
        title: {
            text: meta['title'],
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
            autoCurveness: 3,
            roam: true,
            draggable: true,
            hoverAnimation: true,
            focusNodeAdjacency: true,
            coordinateSystem: null,
            force: {
                repulsion: 70,
                gravity: 0.1,
                friction: 0.4,
                layoutAnimation: true,
            },
            label: {
                show: true,
                position: 'inside',
            },
            emphasis: {
                lineStyle: {
                    width: 7,
                },
                itemStyle: {
                    borderWidth: 1,
                    borderColor: 'rgba(0, 0, 0, 1)',
                    shadowBlur: 1,
                }
            },
            tooltip: {
                formatter: function(params){
                    var result = '';
                    if(params.dataType == 'node'){
                        if(params.data.category == 1){
                            result += 'Name: ' + String(params.data.name) + '<br>';
                            result += 'ID: ' + String(params.data.value);
                        }else if(params.data.category == 0){
                            result += 'Event: ' + String(params.data.name);
                        }else if(params.data.category == 2){
                            result += 'Topic: ' + String(params.data.name) + '<br>';
                            result += 'Count: ' + String(params.data.count) + '<br>';
                            result += 'Time: ' + String(params.data.time).slice(0,16).replace('T', ' ');
                        }
                    } else if (params.dataType == 'edge') {
                        if(params.data.category == 'PARTICIPATE'){// event user
                            result += "Type: " + String(params.data.type) + '<br>';
                            result += "Time: " + String(params.data.time).slice(0,16).replace('T', ' ');
                        } else if (params.data.category == 'COOCCURENCE'){// event event

                        } else if (params.data.category == 'PRODUCE'){// event topic

                        } else if (params.data.category == 'INTERACT'){// user user

                        } else if (params.data.category == 'JOIN'){// user topic

                        } else if (params.data.category == 'RELATED'){// topic topic

                        }
                    }
                    return result;
                }// formatter
            }// tooltip
        }]// serious
    };// option
    // 使用刚指定的配置项和数据显示图表。
    myChart.hideLoading();
    myChart.setOption(option);
}

function event_user(){
    var myChart = echarts.init(document.getElementById('result'));
    myChart.showLoading();

    var event_id = Number($("#event-id").val());
    var s_time = $("#s-time").val().replace(" ", "T");
    var e_time = $("#e-time").val().replace(" ", "T");

    var data = {"event_id":event_id, "s_time":s_time, "e_time":e_time};
    var data = JSON.stringify(data);

    var meta = {'title':'Event User Relationship', };

    $.ajax({
     type:"POST",
     url:"/api/event/user",
     contentType: "application/json;charset=utf-8",
     data:data,
     // dataType:"json",
     error:function(data){
        console.log("Function event_user() can not get data from server.");
     },
     success:function(data){
        console.log("Function event_user() get data from server successful.");
        show_echarts(myChart, data, meta);
     }});
}
function event_user_page(){
    $("#name-input").typeahead({
        source:function(query, process){
            var data = JSON.stringify({'name':query});
            $.ajax({
                type:"POST",
                url:"/api/event/list",
                contentType: "application/json;charset=utf-8",
                data:data,
                //dataType:"json",
                error:function(data){
                   console.log("error")
                   console.log(data);
                },
             success:function(data){
                data = data[0];
                process(data);
              }// success
            })// ajax
        },//source
        displayText:function(item){
            return item.name;
        }
    });
    $("#name-input").change(function() {
      var current = $("#name-input").typeahead("getActive");
      if (current) {
        // console.log(current)
        $("#event-id").val(current.event_id);
    }});
    $('#s-time').datetimepicker({
        format: 'YYYY-MM-DD HH:MM'
    });
    $('#e-time').datetimepicker({
        format: 'YYYY-MM-DD HH:MM'
    });
}