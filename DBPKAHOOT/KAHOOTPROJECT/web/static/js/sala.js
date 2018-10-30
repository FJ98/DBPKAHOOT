$.getJSON("/current_sala",function(data){
    //alert.(data['username']);
    $('#sala_name').html(data['name']);
    $('#sala_pin').html('PIN : '+data['pin']);
});