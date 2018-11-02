var current_sala_pin = 0;
var current_sala_id = 0;
var url_messages;

$(document).ready(function() {
    $.getJSON("/current_created_sala",function(data){
    //alert.(data['username']);
    current_sala_pin = data['pin']
    current_sala_id = data['id']
    url_messages = '/messages/'+current_sala_pin
    $('#sala_name').html(data['name']);
    $('#sala_pin').html('PIN : '+data['pin']);

    var refreshId =  setInterval( function getMessages(){
    $.getJSON(url_messages,function(data){
    var i =0;
    var e='';
    $.each(data, function(){

        e = e + '<div class="incoming_msg"><div class="incoming_msg_img"> <img src="https://ptetutorials.com/images/user-profile.png" alt="sunil"> </div>'
        e = e + '<div class="received_msg"><div class="received_withd_msg">'
        e = e + '<p>'+ data[i]['content']+'<p></div></div></div>'
        i = i+1;

    });
    $('#boxMessage').html(e);
    });
}, 2000 );

     });

    });

$.getJSON(url_messages,function(data_m){
    var i =0;
    var e='';
    $.each(data_m, function(){
        e = e + '<div class="incoming_msg"><div class="incoming_msg_img"> <img src="https://ptetutorials.com/images/user-profile.png" alt="sunil"> </div>'
        e = e + '<div class="received_msg"><div class="received_withd_msg">'
        e = e + '<p>'+ data_m[i]['content']+'<p></div></div></div>'
        i = i+1;
        $('#boxMessage').append(e);
    });
    });

function getMessages(){
    $.getJSON(url_messages,function(data){
    var i =0;
    var e='';
    $.each(data, function(){
        e = e + '<div class="incoming_msg"><div class="incoming_msg_img"> <img src="https://ptetutorials.com/images/user-profile.png" alt="sunil"> </div>'
        e = e + '<div class="received_msg"><div class="received_withd_msg">'
        e = e + '<p>'+ data_m[i]['content']+'<p></div></div></div>'
        i = i+1;
        $('#boxMessage').append(e);
    });
    });

}
function sendMessage(){
    content = $('#txtMessage').val();
    e = '<div class="incoming_msg"><div class="incoming_msg_img"> <img src="https://ptetutorials.com/images/user-profile.png" alt="sunil"> </div>'
    e = e + '<div class="received_msg"><div class="received_withd_msg">'
    e = e + '<p>'+ content+'<p></div></div></div>'
    $('#boxMessage').append(e);
    $('#txtMessage').val("");
    $.ajax({
        url: '/messages',
        type: 'POST',
        contentType:'application/json',
        data: JSON.stringify({
            "content":content,
            "pin":current_sala_pin
        }),
        dataType:'json'
    });
}


