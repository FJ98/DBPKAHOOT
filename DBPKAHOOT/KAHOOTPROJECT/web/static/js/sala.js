var current_sala_pin = 0


$.getJSON("/current_created_sala",function(data){
    //alert.(data['username']);
    current_sala_pin = data['pin']
    $('#sala_name').html(data['name']);
    $('#sala_pin').html('PIN : '+data['pin']);
});


function sendMessage(){
    content = $('#txtMessage').val();
    $.ajax({
        url: '/messages',
        type: 'POST',
        contentType:'application/json',
        data: JSON.stringify({
            "content":content,
            "pin":current_sala_pin,
        }),
        dataType:'json'
    });
    get_messages(current_user_id, current_to_id);
    $('#txtMessage').val("")
}


function get_messages(sala_pin){
    current_to_id = user_to;
    $('#boxMessage').empty();
    var url = "/messages/"+current_user_id+"/"+current_to_id
    $.getJSON(url, function(data){
        var i =0;
        $.each(data, function(){
            user_from = current_user_id;
            user_to = data[i]['id'];
            e = '<div class="alert" role="alert" onclick="get_messages('+user_from+','+user_to+')"> ';
            e = e+'<div>'+data[i]['content']+'</div>';
            e = e+'</div>';
            i = i+1;
            $("<div/>",{html:e}).appendTo("#boxMessage");
        });
       });
}
