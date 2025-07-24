$(document).ready(function () {
    //DISPLAY MESSAGE
    eel.expose(DisplayMessage)
    function DisplayMessage(message) {
        $(".siri-message li:first").text(message);
        $(".siri-message").textillate('start');
    }

//DISPLAY HOOD
    eel.expose(showHood)
    function showHood() {
        $("#Oval").attr("hidden",false);
        $("#Siriwave").attr("hidden",true);
    }
});
