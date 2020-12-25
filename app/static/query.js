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
        console.log(data);
        $("#result").text(data)
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



