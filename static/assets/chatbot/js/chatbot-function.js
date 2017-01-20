$(function(){
    var init = 0;
    $('.input').bind('keydown', function (e) {
        if (e.keyCode == 13) {
            submitChat();
        }
    });
    var bot_msg = function(message, datetime){
        return "<div class=\"row msg_container\">" +
            "                        <div class=\"col-md-10 col-xs-10\">" +
            "                            <div class=\"messages msg_receive\">" +
            "                                <p>"+message+"</p>" +
            "                                <time datetime=\"2009-11-13T20:00\">Recieved• "+datetime+"</time>" +
            "                            </div>" +
            "                        </div>" +
            "                        <div class=\"col-md-2 col-xs-2\">" +
            "                            <img src=\"/static/assets/images/mia.png\" class=\" img-responsive img-circle\">" +
            "                        </div>" +
            "                    </div>";
    };
    var user_msg = function(message, datetime) {
        return "<div class=\"row msg_container\">" +
            "                        <div class=\"col-md-2 col-xs-2\">" +
            "                            <img src=\"/static/assets/images/login.png\" class=\" img-responsive img-circle\">" +
            "                        </div>" +
            "                        <div class=\"col-md-10 col-xs-10\">" +
            "                            <div class=\"messages msg_sent\">" +
            "                                <p>"+message+"</p>" +
            "                                <time datetime=\"2009-11-13T20:00\">Sent• "+datetime+"</time>" +
            "                            </div>" +
            "                        </div>" +
            "                    </div>";
    };
    var chatInitialize = function(){
        if(init==0) {
            // $('.msg_container_base').scrollTop($('.msg_container_base')[0].scrollHeight);
            update_chatbot()
        }
    };
    var updateChat = function (party, text) {

        if (party == 'user') {
            $('.msg_container_base').append(user_msg(text, 'Now'));
        }
        else {
            $('.msg_container_base').append(bot_msg(text, 'Now'));
        }
        $('.msg_container_base').scrollTop($('.msg_container_base')[0].scrollHeight);
    };
    var submitChat = function() {
        $(".msg_container_base").animate({
            scrollTop: $('.msg_container_base').get(0).scrollHeight
        }, 1000);
        $('#loading_id').css({display: "block"});
        $('.input input').attr('disabled', 'disabled');
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
        console.log(st);
        console.log("st+input");
        $.ajax({
            url: '/am/reply/' + st,
            type: 'GET',
            dataType: 'text',
            contentType: "application/text; charset=utf-8",
            success: function (response) {
                updateChat('bot', response);
                updateDashboard();
            },
            error: function (e) {
                console.log(e);
                // $('.msg_container_base').append(bot_msg('Some Error Occured, Please Try Again Later.'));
                $('.input input').removeAttr('disabled');
                $('#loading_id').css({display: "none"});
                $('.msg_container_base').scrollTop($('.msg_container_base')[0].scrollHeight);
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
                st=st.toLowerCase();
                st_1 = ''
                for (i1 = 0; i1 < st.length; i1++)
                {
                    if (st[i1] == '-')
                        temp = ' '
                    else
                        temp=st[i1]

                    st_1=st_1+temp
                }

                st_1=st_1.split(" ");
                string_st=""
                for (k1 = 0; k1 < st_1.length; k1++)
                {
                    if(st_1[k1]=="gt")
                        temp="-"
                    else if (st_1[k1] == 'lt')
                        temp = '-'
                    else if (st_1[k1] == 'eq')
                        temp = '-'
                    else
                        temp = st_1[k1]
                    string_st=string_st+temp
                }
                console.log(string_st);
                console.log("string");
                var str = string_st;
                var patt = new RegExp(/^(\w+)+$/);
                var res_1 = patt.test(str);
                // $('#loading_id1').css({display: "none"});
                if (res_1==true)
                {
                    console.log("amit009");
                }
                else {
                    $('#master_table').html(response);
                }
                $('#loading_id').css({display: "none"});
                $('.input input').removeAttr('disabled');
            },
            error: function (e) {
                console.log(e);
                // $('.msg_container_base').append(bot_msg('Some Error Occured, Please Try Again Later.'));
                $('.input input').removeAttr('disabled');
                $('#loading_id').css({display: "none"});
                $('.msg_container_base').scrollTop($('.msg_container_base')[0].scrollHeight);
            }
        });

    };

    var update_chatbot = function() {
        $.ajax({
            url: '/am/new_view/',
            type: 'GET',
            dataType: 'JSON',
            contentType: "application/json; charset=utf-8",
            success: function (response) {
                for (t=0;t<response.length;t++)
                {
                    if (response[t].send_by=='bot')
                    {
                        $('.msg_container_base').append(bot_msg(response[t].message,response[t].time));
                    }
                    else {
                        $('.msg_container_base').append(user_msg(response[t].message,response[t].time));

                    }
                }
                $('.input input').removeAttr('disabled');
            },
            error: function (e) {
                console.log(e);
                // $('.msg_container_base').append(bot_msg('Some Error Occured, Please Try Again Later.'));
                $('.input input').removeAttr('disabled');
                $('#loading_id').css({display: "none"});
                $('.msg_container_base').scrollTop($('.msg_container_base')[0].scrollHeight);
            }
        });

    };
    chatInitialize();
});
