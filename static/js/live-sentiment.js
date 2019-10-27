var input_change = false;

function sentiment_request() {
    $.ajax({
        method: "POST",
        url: "http://127.0.0.1:5000/live-sentiment",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify({
            "text": $("#input-text").val()
        })
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

        createTextProfile($("outputAnalysis"), data, encoding);
    }).fail(function(data){
        console.log("error")
    });
}

function createTextProfile(paragraphObj, text, encoding) {
    var text = "";
    for (const [key, value] of Object.entries(text)) {
        if (value[0] in encoding) {
            text += "<span style='color: " + encoding[value[0]] +
                "' data-toggle='tooltip' data-placement='top' title='" + (value[1] * 100).toFixed(2) + "% confidence'>" + key + "</span>";
        } else {
            text += "<span>" + key + "</span>";
        }
    }

    paragraphObj.val(text);
}

$(document).ready(function () {
    $("#input-text").on("keyup keydown", function() {
        input_change = true;
    })

    window.setInterval(function() {
        if(input_change) {
            sentiment_request();
            input_change = false;
        }
    }, 2000);
});

