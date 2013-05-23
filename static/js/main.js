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
        // Assign the value
        $("#id_from_date").val(data_time);
        $("#id_to_date").val(data_time_next);
        $("#id_appointment_to").val(data_profile);
    });

    // Getting all the visits, on current date
    var current_system_date = new Date($("#current-system-date").text()).getTime();
    var work_start_time = new Date($("#work-start-time").text());
    
    if (current_system_date) {
        load_vertical_line();
        load_visits(current_system_date);
    }

    /**
     * Checking then the client field has changed
     * @return {[type]} [description]
     */
    $("#id_client").change(function() {
        var client_id = $(this).val();
        load_pets(client_id);
    });

    /**
     * Date picker part
     */
    $("#div_id_from_date .controls .input-append").datetimepicker({
        format: 'yyyy-MM-dd hh:mm',
        pickSeconds: false
    });
    $("#div_id_to_date .controls .input-append").datetimepicker({
        format: 'yyyy-MM-dd hh:mm',
        pickSeconds: false
    });
    $("#div_id_start .controls .input-append").datetimepicker({
        format: 'yyyy-MM-dd hh:mm',
        pickSeconds: false
    });
    $("#div_id_end .controls .input-append").datetimepicker({
        format: 'yyyy-MM-dd hh:mm',
        pickSeconds: false
    });

    function load_vertical_line() {
        // Current dates
        var current_system_date = new Date($("#current-system-date").text()).getTime();
        var work_start_time = new Date($("#work-start-time").text()).getTime();
        // Spacing
        var spacing_tr = $('table.table tr');
        // 
        var time_diff = Math.abs(work_start_time - new Date().getTime());
        var top_gap = (spacing_tr[1].offsetHeight) * (Math.ceil(time_diff / (1000 * 60 * 15)));
        top_gap = top_gap + $('table.table').offset().top;

        var vertical_line = "<hr class='current_time' style='width: " +
            spacing_tr.width() + "px; " +
            "top: " + top_gap + "px;' />";
        $(".sticky-dock").append(vertical_line);
    }

    /**
     * load_visits populates the calendar input with the data
     * @param  {[type]} current_system_date [description]
     * @return {[type]}                     [description]
     */
    function load_visits(current_system_date) {
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
    }

    /**
     * Function to fill the pet field, depending on the client field entry
     * @param  {int} client_id [client id from the system]
     * @return {[type]}           [description]
     */
    function load_pets(client_id) {
        var options = $("#id_pet");
        options.find('option').remove().end();
        $.get('/api/pets/' + client_id + '/')
        .done(function(data) {
            $.each(data, function() {
                console.log(this);
                options.append($('<option />').val(this.id).text(this.name));
            });
        });
    }

    /**
     * [format_time description]
     * @param  {[type]} x [description]
     * @return {[type]}   [description]
     */
    function format_time(x) {
        var minute = x.getMinutes();
        if (minute.toString().length == 1) {
            minute = '0' + minute.toString();
        }
        return x.getHours() + ':' + minute;
    }

    /**
     * format_date gives a standard interpretation of date
     * @param  {Date} x date input
     * @return string '2012-01-01 24:59:59'
     */
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
