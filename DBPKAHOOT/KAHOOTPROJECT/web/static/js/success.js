function sayHello(name){
    alert("Hello "+name);
}

$.getJSON("/current_user",function(data){
    //alert.(data['username']);
    $('#current_username').html(data['username']);
});

$.getJSON("/users",function(data){
    var i = 0;
    $.each(data,function(){
        e = '<div class="alert" role="alert">';
        e=e+'<img src="/static/images/user_icon.png" width=30px height=30px />';
        e=e+'<div>'+data[i]['username']+'<div>';
        e=e+'<div>';
        i=i+1;
        $("<div/>", {html:e}).appendTo("#users");
    });
});
