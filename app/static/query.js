function event_user(){
    var name = $("#event_user").find("#event_name").val();
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
