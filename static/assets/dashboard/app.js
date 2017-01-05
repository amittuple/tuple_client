$(function() {
    var generateUUID = function() {
        var d = new Date().getTime();
        if (window.performance && typeof window.performance.now === "function") {
            d += performance.now(); //use high-precision timer if available
        }
        var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
            var r = (d + Math.random() * 16) % 16 | 0;
            d = Math.floor(d / 16);
            return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
        });
        return uuid;
    }

    //For CLTV
    var blocks = document.getElementsByClassName('cltv-color');
    for(var i=0; i< blocks.length; i++){
        id = 'cltv-' + generateUUID();
        blocks[i].id = id;
        cltv=parseInt(document.getElementById(id).innerHTML);
        if(cltv > 50000) { document.getElementById(id).style.backgroundColor='#20dad3 '};
        if(cltv > 75000){ document.getElementById(id).style.backgroundColor='#ffa05d'};
        if(cltv < 45000){ document.getElementById(id).style.backgroundColor='white'};
        if(cltv < 30000){ document.getElementById(id).style.backgroundColor='#20dad3'};
    }

    // For Churn
    var blocks = document.getElementsByClassName('churn-color');
    for(var i=0; i< blocks.length; i++){
        id = 'churn-' + generateUUID();
        blocks[i].id = id;
        churn=parseInt(document.getElementById(id).innerHTML);
        if(churn > 50) { document.getElementById(id).style.backgroundColor='white'};
        if(churn > 75){ document.getElementById(id).style.backgroundColor='#ffa05d'};
        if(churn < 45){ document.getElementById(id).style.backgroundColor='#20dad3'};
        if(churn < 30){ document.getElementById(id).style.backgroundColor='#ffa05d'};
    }

    // For High Convertor
    var blocks = document.getElementsByClassName('high-convertor-color');
    for(var i=0; i< blocks.length; i++){
        id = 'high-convertor-' + generateUUID();
        blocks[i].id = id;
        convertor=parseInt(document.getElementById(id).innerHTML);
        if(convertor > 50) { document.getElementById(id).style.backgroundColor='#20dad3 '};
        if(convertor > 75){ document.getElementById(id).style.backgroundColor='#ffa05d'};
        if(convertor < 50){ document.getElementById(id).style.backgroundColor='white'};
    }
});

