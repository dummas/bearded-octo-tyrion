$(document).ready(function(){
    $("#id_color").colorpicker();
    $("#client-add-form").submit(function(){ // Catching the form submit
        $.ajax({
            contentType: 'application/json',
            data: JSON.stringify($(this).serializeObject()),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            success: function(response) {
                console.log("Success");
                $("#client-add-modal .modal-body").html(response);
                $("#client-add-form-submit").attr('disabled', 'disabled');
            },
            failure: function(response) {
                console.log("Failure");
                $("#client-add-modal .modal-body").html(response);
            }
        });
        return false;
    });
    $("#pet-add-form").submit(function() {
        $.ajax({
            contentType: 'application/json',
            data: JSON.stringify($(this).serializeObject()),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            success: function(response) {
                $("#pet-add-modal .modal-body").html(response);
                $("#pet-add-form-submit").attr('disabled', 'disabled');
            },
            failure: function(response) {
                console.log("Failure");
                $("#pet-add-modal .modal-body").html(response);
            }
        });
        return false;
    });
    $("#visit-add-form").submit(function() {
        $.ajax({
            contentType: 'application/json',
            data: JSON.stringify($(this).serializeObject()),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            success: function(response) {
                $("#visit-add-modal .modal-body").html(response);
                $("#visit-add-form-submit").attr('disabled', 'disabled');
            },
            failure: function(response) {
                console.log("Failure");
                $("#visit-add-modal .modal-body").html(response);
            }
        });
        return false;
    });
    $("#doctor-add-form").submit(function() {
        $.ajax({
            contentType: 'application/json',
            data: JSON.stringify($(this).serializeObject()),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            success: function(response) {
                $("#doctor-add-modal .modal-body").html(response);
                $("#doctor-add-form-submit").attr('disabled', 'disabled');
            },
            failure: function(response) {
                console.log("Failure");
                $("#doctor-add-modal .modal-body").html(response);
            }
        });
        return false;
    });
    $("#problem-add-form").submit(function() {
        $.ajax({
            contentType: 'application/json',
            data: JSON.stringify($(this).serializeObject()),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            success: function(response) {
                $("#problem-add-modal .modal-body").html(response);
                $("#problem-add-form-submit").attr('disabled', 'disabled');
            },
            failure: function(response) {
                console.log("Failure");
                $("#problem-add-modal .modal-body").html(response);
            }
        });
        return false;
    });
});

$.fn.serializeObject = function(){
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name]) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};