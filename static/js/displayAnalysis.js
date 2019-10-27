$(document).ready(function () {    
    if(data) {
        console.log(data);
        createWordProfile($("#textAnalysis"), data[1]);
        createWordProfile($("#audioAnalysis"), data[0]);
    } else {
        console.log("Error")
    }
});

function createWordProfile(paragraphObj, text) {
    var html = "";
    for (const [key, value] of Object.entries(text)) {
        //cur = "<span style=\"color: " + encoding[value] + "\">" + key + "</span>";
        cur = "<span>" + key + "</span>";

    }

    paragraphObj.text(html)
}