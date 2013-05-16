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
        console.log(data_time);
        console.log(data_time_next);
        $("#id_from_date").val(data_time);
        $("#id_to_date").val(data_time_next);
        $("#id_appointment_to").val(data_profile);
    });

    // Getting all the visits, on current date
    var current_system_date = new Date($("#current-system-date").text()).getTime();
    var work_start_time = new Date($("#work-start-time").text());
    console.log($("#current-system-date").text());
    console.log(current_system_date);

    /* Current time line */
    var table_tr = $('table.table tr');
    var top_gap = table_tr.offsetHeight;
    var vertical_line = "<hr class='current_time' style='width: " + table_tr.width() + "px' />";
    $(".sticky-dock").append(vertical_line);

    /* Visits loading and management */
    $.get('/api/visits/' + current_system_date + '/')
    .done(function(data) {
        var doctor = null;
        var top = null;
        var left = null;
        var visit_start = null;
        var visit_end = null;
        var spacing = null;
        var work_start = new Date();
        for (var i = 0; i < data.length; i++) {
            // Visit start and visit end proper parsing
            visit_end = new Date(Date.parse(data[i].to_date));
            visit_start = new Date(Date.parse(data[i].from_date));

            var time_diff = Math.abs(visit_start.getTime() - work_start_time.getTime());
            var time_diff_end = Math.abs(visit_end.getTime() - visit_start.getTime());

            doctor = $('#doctor-' + data[i].appointment_to);
            spacing_tr = $('table.table tr');
            spacing_td = $('table.table tr td');

            top_gap = (spacing_tr[1].offsetHeight) * (Math.ceil(time_diff / (1000 * 60 * 15)) + 1);
            bottom_gap = (spacing_tr[1].offsetHeight) * (Math.ceil(time_diff_end / (1000 * 60 * 15)));
            top = doctor.position().top + top_gap;

            element_width = spacing_td[1].offsetWidth*0.9;
            element_height = bottom_gap;
            left = doctor.position().left + spacing_td[1].offsetWidth/2 - element_width/2;

            element = "<div class='sticker' style='width: "+ element_width +
                "px; height:" + element_height +
                "px;top: " + top + "px; left: " + left +
                "px; background: " + data[i].problem__color + "'>" +
                "<div class='times'>" + format_time(new Date(data[i].from_date)) +
                " - " + format_time(new Date(data[i].to_date)) + "</div>" +
                "<span class='description'>" + data[i].description + "</span>" +
            "</div>";
            $('.sticky-dock').append(element);
        }
    });

    function format_time(x) {
        var minute = x.getMinutes();
        if (minute.toString().length == 1) {
            minute = '0' + minute.toString();
        }
        return x.getHours() + ':' + minute;
    }

    function format_date(x) {
        var month = x.getMonth() + 1;
        if (month.toString().length == 1) {
            month = '0' + month.toString();
        }
        var day = x.getDate();
        if (day.toString().length == 1) {
            day = '0' + day.toString();
        }
        var minute = x.getMinutes();
        if (minute.toString().length == 1) {
            minute = '0' + minute.toString();
        }
        return x.getFullYear() + '-' + month + '-' + day + ' ' + x.getHours() + ':' + minute;
    }
});
