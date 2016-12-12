// function chatBot() {
//
// 	// current user input
// 	this.input;
//
// 	/**
// 	 * respondTo
// 	 *
// 	 * return nothing to skip response
// 	 * return string for one response
// 	 * return array of strings for multiple responses
// 	 *
// 	 * @param input - input chat string
// 	 * @return reply of chat-bot
// 	 */
// 	this.respondTo = function(input) {
//
//
// 		function myfunction() {
// 			alert('hi');
// 			var robot = 'Buddy';
//     // $("button").click(function(){
//         $.ajax({
//         url: '/am/reply/',
//         type: 'GET',
//         // data: {'obj': "test string"},
//         dataType: 'text',
//         contentType: "application/text; charset=utf-8",
//         success: function(response) {
//                    alert('the responce is:'+response);
// 			updateChat(robot, response);
// 			alert('special');
//             },
// 			failure: function(errMsg) {
//             alert(errMsg);
//         }
//         });
//     		// });
// 		// });
//
// 		}
//
//
// 		myfunction();
//
//
//
//
// 	// alert(input);
// 	// var u="localhost:8000/am/reply/iii";
// 	// alert(u);
//     //
//      //    	$.ajax({url: u+ input,
//      //    	 success: function(result){updateChat('Buddy', result)}
//      //    	    });
// //
// //		this.input = input.toLowerCase();
// //
// //		if(this.match('(hi|hello|hey|hola|howdy)(\\s|!|\\.|$)'))
// //			return "um... hi?";
// //		if(this.match('(amit)(\\s|!|\\.|$)'))
// //			return "amit is developer";
// //
// //		if(this.match('what[^ ]* up') || this.match('sup') || this.match('how are you'))
// //			return "this github thing is pretty cool, huh?";
// //
// //		if(this.match('l(ol)+') || this.match('(ha)+(h|$)') || this.match('lmao'))
// //			return "what's so funny?";
// //
// //		if(this.match('^no+(\\s|!|\\.|$)'))
// //			return "don't be such a negative nancy :(";
// //
// //		if(this.match('(cya|bye|see ya|ttyl|talk to you later)'))
// //			return ["alright, see you around", "good teamwork!"];
// //
// //		if(this.match('(dumb|stupid|is that all)'))
// //			return ["hey i'm just a proof of concept", "you can make me smarter if you'd like"];
// //
// //		if(this.input == 'noop')
// //			return;
// //
// //		return input + " what?";
// 	}
//
// 	/**
// 	 * match
// 	 *
// 	 * @param regex - regex string to match
// 	 * @return boolean - whether or not the input string matches the regex
// 	 */
// 	this.match = function(regex) {
//
// 		return new RegExp(regex).test(this.input);
// 	}
// }
