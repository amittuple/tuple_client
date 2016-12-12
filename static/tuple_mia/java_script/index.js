$(function() {
    var you = 'You';
    var robot = 'tuple-mia';

    var delayStart = 400;
    var delayEnd = 800;

    var bot = new chatBot();
    var chat = $('.chat');
    var waiting = 0;
    $('.busy').text(robot + ' is typing...');

    var submitChat = function () {

        var input = $('.input input').val();
        if (input == "/send") {
            document.getElementById("demo1").click();
        }
        if (input == "/refresh") {
            updateDashboard()
        }
        if (input == '') return;

        $('.input input').val('');
        updateChat(you, input);

        var reply = bot.respondTo(input);
        if (reply == null) return;

        var latency = Math.floor((Math.random() * (delayEnd - delayStart)) + delayStart);
        $('.busy').css('display', 'block');
        waiting++;
        setTimeout(function () {
            if (typeof reply === 'string') {
                updateChat(robot, reply);
            } else {
                for (var r in reply) {
                    updateChat(robot, reply[r]);
                }
            }

            if (--waiting == 0) $('.busy').css('display', 'none');

        }, latency);

    }
    var updateChat = function (party, text) {

        var style = 'you';
        if (party != you) {
            style = 'other';
        }
        var line = $('<div><span class="party"></span> <span class="text"></span></div>');
        line.find('.party').addClass(style).text(party + ':');
        line.find('.text').text(text);
        chat.append(line);
        chat.stop().animate({scrollTop: chat.prop("scrollHeight")});
    }
    $('.input').bind('keydown', function (e) {
        if (e.keyCode == 13) {
            submitChat();

        }
    });
    $('.input a').bind('click', submitChat);
    updateChat(robot, 'Hi there. Try typing something!');
    function chatBot() {
        this.input;
        this.respondTo = function (input) {
            function myfunction() {
                var robot = 'tuple-mia';
                st = ''
                for (i = 0; i < input.length; i++) {
                    if (input[i] == 'high')
                        temp = '> 70000'
                    else if (input[i] == '<')
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

                        updateChat(robot, response);
                        updateDashboard();

                    },
                    failure: function (errMsg) {

                    }
                });
            }

            myfunction();
        }
        this.match = function (regex) {
            return new RegExp(regex).test(this.input);
        }
    }

    function updateDashboard()
    {
        $.ajax({
            url: '/dashboard/',
            type: 'GET',
            dataType: 'text',
            contentType: "application/text; charset=utf-8",
            success: function (response) {
                $('#master_table').html(response);

            }
        });
    }
});
