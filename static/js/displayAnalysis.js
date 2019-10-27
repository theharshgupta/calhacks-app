$(document).ready(function () {
    if (res != null) {
        data = JSON.parse(res);
        var encoding = {
            "anger": "#ad0505",
            "joy": "#0a8c24",
            "happy": "#0a8c24",
            "excited": "#0a8c24",
            "neutral": "#77777a",
            "distgust": "#2b0505"
        };

        createTextProfile($("#textAnalysis"), data["text"], encoding);
        createAudioProfile($("#audioAnalysis"), data["audio"], encoding);
        $(function () {
            $('[data-toggle="tooltip"]').tooltip()
        })
    } else {
        console.log("Error")
    }
});

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

function createAudioProfile(paragraphObj, text, encoding) {
    var html = "";
    for (const [key, value] of Object.entries(text)) {
        if (value in encoding) {
            html += "<span style='color: " + encoding[value] + "' " +
                "data-toggle='tooltip' data-placement='top' title='Emotion: " + value + "'>"
                + key + "</span > ";
        } else {
            html += "<span>" + key + "</span>";
        }
    }

    paragraphObj.html(html);
}
