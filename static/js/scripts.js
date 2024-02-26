$(document).ready(function(){
    $("#uploadButton").click(function(){
        $(this).removeClass("btn btn-secondary").addClass("btn btn-outline-warning");
        $(this).val("Processing Audio");
        $(this).prop("disabled", true);
        $("form").submit();
    });
});

