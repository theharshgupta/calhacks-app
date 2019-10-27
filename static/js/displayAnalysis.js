$(document).ready(function () {
    $("$audioSubmit").submit(function () {
        var file = new FormData($("#audioForm"))
        $.ajax({
            method: "POST",
            url: window.location.href,
            data: file,
            dataType: "json",
            success: function(data) {
                console.log(data);
                createWordProfile($("#textAnalysis"), data[1]);
                createWordProfile($("audioAnalysis"), data[0]);
            },
            error: function(error) {
                console.log(error)
            }
        });
    });
});

function createWordProfile(paragraphObj, text) {
    var html = "";
    for (const [key, value] of Object.entries(text)) {
        //cur = "<span style=\"color: " + encoding[value] + "\">" + key + "</span>";
        cur = "<span>" + key + "</span>";

    }

    paragraphObj.text(html)
}