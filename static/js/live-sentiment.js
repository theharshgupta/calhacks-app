var input_change = false;

function sentiment_request() {
    $.ajax({
        method: "POST",
        url: "http://127.0.0.1:5000/test",
        dataType: "json"
    }).done(function(data) {
        console.log(JSON.stringify(data));
        var encoding = {
            "anger": "#ad0505",
            "joy": "#0a8c24",
            "happy": "#0a8c24",
            "excited": "#0a8c24",
            "neutral": "#77777a",
            "distgust": "#2b0505"
        };
    }).fail(function(data){
        console.log("error")
    });
}

function createTextProfile(paragraphObj, text, encoding) {
    var html = "";
    for (const [key, value] of Object.entries(text)) {
        if (value[0] in encoding) {
            html += "<span style='color: " + encoding[value[0]] +
                "' data-toggle='tooltip' data-placement='top' title='" + (value[1] * 100).toFixed(2) + "% confidence'>" + key + "</span>";
        } else {
            html += "<span>" + key + "</span>";
        }
    }

    paragraphObj.html(html);
}

$(document).ready(function () {
    $("#").change(function(this) {
        input_change = true;
    })

    window.setTimeout(function() {
        if(input_change) {
            sentiment_request();
            input_change = false;
        }
    }, 2000);
});

