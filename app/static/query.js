
function show_echarts(myChart, data, meta){
    // 基于准备好的dom，初始化echarts实例

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
            data: data[0],
            links: data[1],
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
                            // to many time, cannot decide which to use
                        } else if (params.data.category == 'PRODUCE'){// event topic
                            result += "Type: " + String(params.data.category) + '<br>';
                            result += "Time: " + String(params.data.time).slice(0,16).replace('T', ' ');
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


function show_table(data){
    data = data[0]

    $('.table').remove()
    var table = $('<table/>').addClass('table table-striped');
    var th1 = $('<th/>').html('话题');
    var th2 = $('<th/>').html('频次');
    var th3 = $('<th/>').html('时间');
    var thead = $('<tr/>').append(th1).append(th2).append(th3);
    table.append(thead);

    var tbody = $('<tbody/>');

    for(var row in data){
        var td1 = $('<td/>').html(data[row]['name']);
        var td2 = $('<td/>').html(data[row]['count']);
        var td3 = $('<td/>').html(data[row]['time'].slice(0, 16).replace('T', ' '));

        var tr = $('<tr/>').append(td1).append(td2).append(td3);
        tbody.append(tr);
    }

    table.append(tbody);
    $('#result').append(table);
}


function send_ajax(url, data){
    var result;
    $.ajax({
        url: url,
        data: data,
        type: "POST",
        async: false,
        contentType: "application/json;charset=utf-8",
        // dataType:"json",
        error:function(data){
            console.log("Error: Function event_user() can not get data from server.");
        },
        success:function(data){
            console.log("Success: Function event_user() get data from server.");
            result = data;
        }
     });
    return result;
}



function event_user(){
    var myChart = echarts.init(document.getElementById('result'));
    myChart.showLoading();

    var event_id = Number($("#event-id").val());
    var s_time = $("#s-time").val().replace(" ", "T");
    var e_time = $("#e-time").val().replace(" ", "T");

    var data = {"event_id":event_id, "s_time":s_time, "e_time":e_time};
    data = JSON.stringify(data);

    var url = '/api/event/user';
    var meta = {'title':'Event User Relationship', };
    var result = send_ajax(url, data);

    show_echarts(myChart, result, meta);
}

function event_topic(){
    var myChart = echarts.init(document.getElementById('result'));
    myChart.showLoading();

    var event_id = Number($("#event-id").val());
    var s_time = $("#s-time").val().replace(" ", "T");
    var e_time = $("#e-time").val().replace(" ", "T");

    var data = {"event_id":event_id, "s_time":s_time, "e_time":e_time};
    data = JSON.stringify(data);

    var url = '/api/event/topic';
    var meta = {'title':'Event Topic Relationship', };
    var result = send_ajax(url, data);

    show_echarts(myChart, result, meta);
}


function event_neighbor() {
    var myChart = echarts.init(document.getElementById('result'));
    myChart.showLoading();

    var event_id = Number($("#event-id").val());
    var level = Number($("#level").val());
    var limit = Number($("#limit").val());

    var data = {"event_id":event_id, "level": parseInt(level), 'limit': parseInt(limit)};
    data = JSON.stringify(data);

    var url = '/api/event/neighbor';
    var meta = {'title':'Event neighbor', };
    var result = send_ajax(url, data);

    show_echarts(myChart, result, meta);
}

function event_info() {
    var event_id = Number($("#event-id").val());
    var limit = Number($("#limit").val());
    var e_time = $("#e-time").val().replace(" ", "T");

    var data = {"event_id":event_id, "limit": limit, "e_time": e_time};
    data = JSON.stringify(data);

    var url = '/api/event/info';
    var meta = {'title':'Event top n topic', };
    var result = send_ajax(url, data);

    show_table(result);
}

function user_event() {
    var myChart = echarts.init(document.getElementById('result'));
    myChart.showLoading();

    var user_id = Number($("#user-id").val());
    var s_time = $("#s-time").val().replace(" ", "T");
    var e_time = $("#e-time").val().replace(" ", "T");

    var data = {"user_id":user_id, "s_time":s_time, "e_time":e_time};
    data = JSON.stringify(data);

    var url = '/api/user/event';
    var meta = {'title':'User Event Relationship', };
    var result = send_ajax(url, data);

    show_echarts(myChart, result, meta);

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
                   console.log("False get #name-input typeahead.")
                },
                success:function(data){
                    data = data[0];
                    process(data);
                }// success
            })// ajax
        },//source
    });
    $("#name-input").change(function() {
      var current = $("#name-input").typeahead("getActive");
      if (current) {
        $("#event-id").val(current.event_id);
    }});
    if($('#s-time') != null ){
        $('#s-time').datetimepicker({
            format: 'YYYY-MM-DD HH:mm',
        });
    }
    if($('#e-time') != null){
        $('#e-time').datetimepicker({
            format: 'YYYY-MM-DD HH:mm',
        });
    }
}


function user_event_page(){
    $("#name-input").typeahead({
        source:function(query, process){
            var data = JSON.stringify({'name':query});
            $.ajax({
                type:"POST",
                url:"/api/user/list",
                contentType: "application/json;charset=utf-8",
                data:data,
                //dataType:"json",
                error:function(data){
                   console.log("False get #name-input typeahead.")
                },
                success:function(data){
                    console.log("Success get #name-input typeahead.");
                    process(data);
                }// success
            })// ajax
        },//source
    });
    $("#name-input").change(function() {
      var current = $("#name-input").typeahead("getActive");
      if (current) {
        $("#user-id").val(current.user_id);
    }});
    if($('#s-time') != null ){
        $('#s-time').datetimepicker({
            format: 'YYYY-MM-DD HH:mm',
        });
    }
    if($('#e-time') != null){
        $('#e-time').datetimepicker({
            format: 'YYYY-MM-DD HH:mm',
        });
    }
}