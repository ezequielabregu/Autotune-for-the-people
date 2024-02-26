$(document).ready(function(){
    $("#uploadButton").click(function(){
        $(this).removeClass("btn btn-secondary").addClass("btn btn-outline-warning");
        $(this).val("Processing Audio");
        $(this).prop("disabled", true);
        $("form").submit();
    });
});

//--------------------------------------------------------------------
// force the browser to re-fetch the audio file by appending a timestamp as a query parameter to the audio file URL. This makes the browser think it's a new file and hence it doesn't use the cached version.
var audioElement = document.getElementById('audio-output');
audioElement.src = '../static/audio/output.wav?' + new Date().getTime();