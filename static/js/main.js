$(document).ready(function() {
    // Add client modal
    $('#client-add-modal').modal({'show': false});
    // Add visit modal
    $('#visit-add-modal').modal({'show': false});
    // Add pet modal
    $("#pet-add-modal").modal({'show': false});
    // Visit table event description
    $("#table-visit td a").click(function(event) {
        // Collect the data
        var data_profile = event.target.parentNode.getAttribute('data-profile');
        var data_time = event.target.parentNode.getAttribute('data-time');
        var data_time_next = event.target.parentNode.getAttribute('data-time-next');
        $("#id_from_date").val(data_time);
        $("#id_to_date").val(data_time_next);
        $("#id_appointment_to").val(data_profile);
    });
    // Getting all the visits, on current date

    var current_system_date = new Date($("#current-system-date").text()).getTime();
    console.log($("#current-system-date").text());
    console.log(current_system_date);
    $.get('/api/visits/' + current_system_date + '/')
    .done(function(data) {
        console.log(data);
    });
});
