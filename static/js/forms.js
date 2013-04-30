$(document).ready(function(){
    $("#client-add-form").submit(function(){ // Catching the form submit
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            success: function(response) {
                $("#client-add-modal .modal-body").html(repsonse);
            }
        });
        return false;
    });
});