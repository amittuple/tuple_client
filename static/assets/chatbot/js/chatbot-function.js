$(function(){
    var init = 0;
    $('.input').bind('keydown', function (e) {
        if (e.keyCode == 13) {
            submitChat();
        }
    });
    var bot_msg = function(message, datetime){
        return "<div class=\"row msg_container base_sent\">" +
            "                        <div class=\"col-md-10 col-xs-10\">" +
            "                            <div class=\"messages msg_sent\">" +
            "                                <p>"+message+"</p>" +
            "                                <time datetime=\"2009-11-13T20:00\">Recieved• "+datetime+"</time>" +
            "                            </div>" +
            "                        </div>" +
            "                        <div class=\"col-md-2 col-xs-2 avatar\">" +
            "                            <img src=\"http://www.bitrebels.com/wp-content/uploads/2011/02/Original-Facebook-Geek-Profile-Avatar-1.jpg\" class=\" img-responsive \">" +
            "                        </div>" +
            "                    </div>";
    };
    var user_msg = function(message, datetime) {
        return "<div class=\"row msg_container base_receive\">" +
            "                        <div class=\"col-md-2 col-xs-2 avatar\">" +
            "                            <img src=\"http://www.bitrebels.com/wp-content/uploads/2011/02/Original-Facebook-Geek-Profile-Avatar-1.jpg\" class=\" img-responsive \">" +
            "                        </div>" +
            "                        <div class=\"col-md-10 col-xs-10\">" +
            "                            <div class=\"messages msg_receive\">" +
            "                                <p>"+message+"</p>" +
            "                                <time datetime=\"2009-11-13T20:00\">Sent• "+datetime+"</time>" +
            "                            </div>" +
            "                        </div>" +
            "                    </div>";
    };
    var chatInitialize = function(){
        if(init==0) {
            $('.msg_container_base').append(bot_msg('Welcome, To Tuple MIA. Please Write Something Below.', 'Now'));
            init = init + 1;
        }
    };
    var updateChat = function (party, text) {

        if (party == 'user') {
            $('.msg_container_base').append(user_msg(text, 'Now'));
        }
        else {
            $('.msg_container_base').append(bot_msg(text, 'Now'));
        }
        // $('#chat_window_1').animate({scrollBottom: 10});
        $('.msg_container_base').animate({scrollTop: $('.msg_container_base').height});
    };
    var submitChat = function() {
        var input = $('.input input').val();
        if (input == "/send") {
            document.getElementById("demo1").click();
        }
        if (input == "/refresh") {
            updateDashboard();
        }
        if (input == '') return;
        $('.input input').val('');
        updateChat('user', input);
        submitInput(input);
    };
    var submitInput = function (input) {
        st = ''
        for (i = 0; i < input.length; i++) {
            if (input[i] == '<')
                temp = 'lt'
            else if (input[i] == '>')
                temp = 'gt'
            else if (input[i] == '=')
                temp = 'eq'
            else if (input[i] == ' ')
                temp = '-'
            else temp = input[i]
            st = st + temp
        }

        $.ajax({
            url: '/am/reply/' + st,
            type: 'GET',
            dataType: 'text',
            contentType: "application/text; charset=utf-8",
            success: function (response) {

                updateChat('bot', response);
                updateDashboard();

            },
            failure: function (errMsg) {

            }
        });
    };
    var updateDashboard = function(){
        $.ajax({
            url: '/dashboard/',
            type: 'GET',
            dataType: 'text',
            contentType: "application/text; charset=utf-8",
            success: function (response) {
                $('#master_table').html(response);
            }
        });
    };
    chatInitialize();
});
