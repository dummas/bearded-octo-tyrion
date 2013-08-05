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
        $('#id_client').val(null);
        $('#id_pet').val(null);
        $("#id_id").val(null);
        $('#id_problem').val(null);
        $('#id_description').val(null);
        $('#visit-add-form').attr('method', 'post');
        $('#visit-add-modal').modal({'show': true});
        return false;
    });

    // Color picker
    $("#id_color").colorpicker();

    /**
     * This is only valid to day view
     */

    // Getting current system date
    var current_system_date = new Date($("#current-system-date").text()).getTime();
    // Getting work start time
    // This is used to know the start of the element
    var work_start_time = new Date($("#work-start-time").text());

    var current_view = $("#current-view").text();

    /*
     * If the current system date exists
     */
    if (current_view == 'days') {
        // Vertical line is used to indicate the current time
        load_vertical_line();
        // Loading visits on particular date
        load_days_view(current_system_date);
    } else if (current_view == 'weeks') {
        load_weeks_view();
    } else if (current_view == 'months') {
        load_months_view();
    }

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


    function load_weeks_view() {
        var rows = $('table.table-week-view tr')[1];
        var date = null;
        var length = 0;
        /* jshint multistr: true */
        var template = "<div id='{#sticker-id}' \
            data-id={#data-id}\
            data-from-date={#data-from-date}\
            data-to-date={#data-to-date}\
            data-problem={#data-problem}\
            data-description={#data-description}\
            data-client={#data-client}\
            data-pet={#data-pet}\
            data-appointment-to={#data-appointment-to}\
            data-appointment-by={#data-appointment-by}\
            style='top: {#top}px; left: {#left}px; width: {#width}px; height: {#height}px' \
            class='sticker'>\
            <span class='color-code-bar' style='background: {#background}'></span>\
            {#time} {#content}\
            </div>";

        var visit_end = 0;
        var visit_start = 0;
        var time_diff = 0;
        var time_diff_end = 0;
        var top_gap = 0;
        var bottom_gap = 0;
        var top = 0;

        var spacing_tr = $('table.table tr');
        var spacing_td = $('table.table tr td');

        // Element dimensions calculations
        var element_width = spacing_td[1].offsetWidth*0.90;
        var element_height = bottom_gap+20;

        // Looping
        $(rows.cells).each(function(index, element) {
            date = element.getAttribute('data-date');
            if (date !== null) {
                timestamp_date = new Date(date).getTime();
                if (timestamp_date === null) {
                    return;
                }
                $.getJSON('/api/visits/' + timestamp_date + '/', function(data) {
                    length = data.length;
                    if (length > 0) {
                        for (i=0; i < length; i++) {

                            sticker_id = "sticker-" + data[i].id;
                            // Visit start and visit end proper parsing
                            visit_end = new Date(Date.parse(data[i].to_date));
                            visit_start = new Date(Date.parse(data[i].from_date));
                            // Calculating time difference from the work_start_time
                            // time_diff = Math.abs(visit_start.getTime() - work_start_time.getTime());
                            time_diff = Math.abs(visit_start.getTime() - new Date(rows.cells[index].getAttribute('data-date')).getTime());
                            // And from the visit_start
                            time_diff_end = Math.abs(visit_end.getTime() - visit_start.getTime());
                            top_gap = (spacing_tr[1].offsetHeight) * (Math.ceil(time_diff / (1000 * 60 * 15)) + 1);
                            // Bottom gap indicates the end of the ticker
                            bottom_gap = (spacing_tr[1].offsetHeight) * (Math.ceil(time_diff_end / (1000 * 60 * 15)));
                            top = $(rows.cells[index]).position().top + top_gap + 2 - 35;
                            left = $(rows.cells[index]).position().left + spacing_td[1].offsetWidth/2 - element_width/2 - 5;

                            /**
                             * Loop throught all the existsing stickers
                             */
                            $(".sticker").each(function(index, element) {
                                sticker_from_date = element.getAttribute('data-from-date');
                                sticker_to_date = element.getAttribute('data-to-date');
                                if (sticker_from_date == data[i].from_date) {
                                    element_width = element_width / 2;
                                    // top = top + 15;
                                    left = left + element_width + 11;
                                    element.style.width = element_width + 'px';
                                }
                            });

                            element = template
                                .replace('{#time}', format_time(new Date(data[i].from_date)) + ' - ' + format_time(new Date(data[i].to_date)))
                                .replace('{#sticker-id}', sticker_id)
                                .replace('{#content}', data[i].description)
                                .replace('{#top}', top)
                                .replace('{#left}', left)
                                .replace('{#height}', element_height)
                                .replace('{#width}', element_width)
                                .replace('{#background}', data[i].problem.color)
                                .replace('{#data-id}', data[i].id)
                                .replace('{#data-from-date}', data[i].from_date)
                                .replace('{#data-to-date}', data[i].to_date)
                                .replace('{#data-problem}', data[i].problem_id)
                                .replace('{#data-description}', '"' +  data[i].description + '"')
                                .replace('{#data-client}', '"' + data[i].client.first_name + ' ' + data[i].client.last_name + '"')
                                .replace('{#data-pet}', data[i].pet.name)
                                .replace('{#data-appointment-to}', data[i].appointment_to.id)
                                .replace('{#data-appointment-by}', data[i].appointment_by.id);

                            $('.sticky-dock').append(element);
                        }
                    }
                    load_sticker_response();
                });
            }
        });
    }

    /**
     * Loading months view
     * 
     * @return {[type]} [description]
     */
    function load_months_view() {
        var elements = $('table.table-month-view td');
        var i = 0;
        var date = null;
        var entry = null;
        var length = 0;
        var entry_data = Object;
        /* jshint multistr: true */
        var template = "<div id='{#sticker-id}' \
            data-id={#data-id}\
            data-from-date={#data-from-date}\
            data-to-date={#data-to-date}\
            data-problem={#data-problem}\
            data-description={#data-description}\
            data-client={#data-client}\
            data-pet={#data-pet}\
            data-appointment-to={#data-appointment-to}\
            data-appointment-by={#data-appointment-by}\
            class='month-sticker'>\
            <span class='color-code-bar' style='background: {#background}'></span>\
            {#time}\
            </div>";
        elements.each(function(index, element) {
            date = element.getAttribute('data-date');
            if (date !== null) {
                date = new Date(date).getTime();
                $.getJSON('/api/visits/' + date + '/', function(data) {
                    length = data.length;
                    if (length > 0) {
                        for(i=0; i < length; i++) {
                            sticker_id = "sticker-" + data[i].id;
                            entry = template
                                .replace('{#time}', format_time(new Date(data[i].from_date)) + ' - ' + format_time(new Date(data[i].to_date)))
                                .replace('{#sticker-id}', sticker_id)
                                .replace('{#background}', data[i].problem.color)
                                .replace('{#data-id}', data[i].id)
                                .replace('{#data-from-date}', data[i].from_date)
                                .replace('{#data-to-date}', data[i].to_date)
                                .replace('{#data-problem}', data[i].problem_id)
                                .replace('{#data-description}', '"' +  data[i].description + '"')
                                .replace('{#data-client}', '"' + data[i].client.first_name + ' ' + data[i].client.last_name + '"')
                                .replace('{#data-pet}', data[i].pet.name)
                                .replace('{#data-appointment-to}', data[i].appointment_to.id)
                                .replace('{#data-appointment-by}', data[i].appointment_by.id);
                            $(element).append(entry);
                        }
                    }
                    load_sticker_response();
                });
            }
        });
    }

    /**
     * Displaying the vertical line
     * 
     * @return {[type]} [description]
     */
    function load_vertical_line() {
        // Current dates
        var current_system_date = new Date($("#current-system-date").text()).getTime();
        var work_start_time = new Date($("#work-start-time").text()).getTime();
        // Spacing
        var spacing_tr = $('table.table tr');
        // Time difference
        var time_diff = Math.abs(work_start_time - new Date().getTime());
        var top_gap = (spacing_tr[1].offsetHeight) * (Math.ceil(time_diff / (1000 * 60 * 15)));
        top_gap = top_gap + $('table.table').offset().top;
        debugger;
        if (top_gap > $('table.table').height()) {
            top_gap = $('table.table').height() + $('table.table').offset().top - 20;
        }

        var vertical_line = "<hr class='current_time' style='width: " +
            spacing_tr.width() + "px; " +
            "top: " + top_gap + "px;' />";
        $(".sticky-dock").append(vertical_line);
    }

    /**
     * Function to load sticker response
     * 
     * @return {[type]} [description]
     */
    function load_sticker_response() {
        var visit_id = [];
        var from_date = [];
        var to_date = [];
        var client = [];
        var telephone = [];
        var pet = [];
        var problem = [];
        var description = [];
        var appointment_to = [];
        var appointment_by = [];
        $('.sticker, .month-sticker').each(function(index) {
            $(this).click(function(event) {
                /**
                 * Collect the data
                 */
                visit_id[index] = event.target.getAttribute('data-id');
                from_date[index] = format_date(new Date(Date.parse(event.target.getAttribute('data-from-date'))));
                to_date[index] = format_date(new Date(Date.parse(event.target.getAttribute('data-to-date'))));
                client[index] = event.target.getAttribute('data-client');
                telephone[index] = event.target.getAttribute('data-telephone');
                pet[index] = event.target.getAttribute('data-pet');
                problem[index] = event.target.getAttribute('data-problem');
                description[index] = event.target.getAttribute('data-description');
                appointment_to[index] = event.target.getAttribute('data-appointment-to');
                appointment_by[index] = event.target.getAttribute('data-appointment-by');
                /**
                 * Fill in the form
                 */
                $("#id_id").val(visit_id[index]);
                $('#id_from_date').val(from_date[index]);
                $('#id_to_date').val(to_date[index]);
                $('#id_client').val(client[index]);
                $('#id_telephone').val(telephone[index]);
                $('#id_pet').val(pet[index]);
                $('#id_problem').val(problem[index]);
                $('#id_description').val(description[index]);
                $('#id_appointment_to').val(appointment_to[index]);
                $('#id_appointment_by').val(appointment_by[index]);
                /**
                 * Change the form method
                 */
                $('#visit-add-form').attr('method', 'put');
                /**
                 * Show the modal
                 */
                $('#visit-add-modal').modal({'show': true});
            });
        });
    }

    /**
     * Load_visits populates the calendar input with the data
     * 
     * @param  {[type]} current_system_date [description]
     * @return {[type]}                     [description]
     */
    function load_days_view(current_system_date) {
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
            var sticker_id = null;
            for (var i = 0; i < data.length; i++) {

                // Visit start and visit end proper parsing
                visit_end = new Date(Date.parse(data[i].to_date));
                visit_start = new Date(Date.parse(data[i].from_date));

                // Calculating time difference from the work_start_time
                var time_diff = Math.abs(visit_start.getTime() - work_start_time.getTime());
                // And from the visit_start
                var time_diff_end = Math.abs(visit_end.getTime() - visit_start.getTime());

                // Search the doctor
                doctor = $('#doctor-' + data[i].appointment_to.id);

                // Calculate the spacings
                spacing_tr = $('table.table tr');
                spacing_td = $('table.table tr td');

                // Check if the doctor exists in the table
                if (doctor.length !== 0) {

                    console.log(data[i].client.telephone);

                    sticker_id = "sticker-" + data[i].id;
                    // Top gap indicates the start of the sticker
                    top_gap = (spacing_tr[1].offsetHeight) * (Math.ceil(time_diff / (1000 * 60 * 15)) + 1);
                    // Bottom gap indicates the end of the ticker
                    bottom_gap = (spacing_tr[1].offsetHeight) * (Math.ceil(time_diff_end / (1000 * 60 * 15) - 1));
                    top = doctor.position().top + top_gap + 2;

                    element_width = spacing_td[1].offsetWidth*0.95;
                    element_height = bottom_gap+20;
                    left = doctor.position().left + spacing_td[1].offsetWidth/2 - element_width/2;

                    /* jshint multistr: true */
                    template = "<div id='{#sticker-id}' \
                        data-id={#data-id}\
                        data-from-date={#data-from-date}\
                        data-to-date={#data-to-date}\
                        data-problem={#data-problem}\
                        data-description={#data-description}\
                        data-client={#data-client}\
                        data-telephone={#data-telephone}\
                        data-pet={#data-pet}\
                        data-appointment-to={#data-appointment-to}\
                        data-appointment-by={#data-appointment-by}\
                        style='top: {#top}px; left: {#left}px; width: {#width}px; height: {#height}px' \
                        class='sticker'>\
                        <span class='color-code-bar' style='background: {#background}'></span>\
                        {#time} {#content}\
                        </div>";

                    element = template
                        .replace('{#time}', format_time(new Date(data[i].from_date)) + ' - ' + format_time(new Date(data[i].to_date)))
                        .replace('{#sticker-id}', sticker_id)
                        .replace('{#content}', data[i].pet.name + ', ' + data[i].description)
                        .replace('{#top}', top)
                        .replace('{#left}', left)
                        .replace('{#height}', element_height)
                        .replace('{#width}', element_width)
                        .replace('{#background}', data[i].problem.color)
                        .replace('{#data-id}', data[i].id)
                        .replace('{#data-from-date}', data[i].from_date)
                        .replace('{#data-to-date}', data[i].to_date)
                        .replace('{#data-problem}', data[i].problem_id)
                        .replace('{#data-description}', '"' +  data[i].description + '"')
                        .replace('{#data-client}', '"' + data[i].client.first_name + ' ' + data[i].client.last_name + '"')
                        .replace('{#data-telephone}', '"' + data[i].client.telephone + '"')
                        .replace('{#data-pet}', data[i].pet.name)
                        .replace('{#data-appointment-to}', data[i].appointment_to.id)
                        .replace('{#data-appointment-by}', data[i].appointment_by.id);

                    $('.sticky-dock').append(element);
                }
            }
            load_sticker_response();
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
        var hour = x.getHours();
        if (minute.toString().length == 1) {
            minute = '0' + minute.toString();
        }
        if (hour.toString().length == 1) {
            hour = '0' + hour.toString();
        }
        return hour + ':' + minute;
    }

    /**
     * format_date gives a standard interpretation of date
     * 
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

    /**
     * Type Ahead
     */
    $('#id_client').typeahead({
        ajax: {
            url: '/api/clients/',
            method: 'get',
            triggerLength: 1
        },
        display: 'full_name'
    });
    $("#id_pet").typeahead({
        ajax: {
            url: '/api/pets/',
            method: 'get',
            triggerLength: 1
        }
    });
});
