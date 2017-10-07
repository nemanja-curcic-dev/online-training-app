$(document).ready(function () {
    global();
});

function global() {
    // globals
    var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    var d = new Date();
    var current_month = d.getMonth();
    var current_year = d.getFullYear();

    (function initial_set_up() {
        var selected_month = $('#selected_month');

        var current_month_and_year = months[current_month] + ' ' + current_year;

        selected_month.html(current_month_and_year);

        fetch_training_session_data(current_month + 1, current_year);
        load_days_of_month(current_year, current_month);
    }());

    (function change_month() {
        var back = $('#month_back');
        var forward = $('#month_forward');

        var selected_month = $('#selected_month');

        back.on('click', function (event) {
            event.preventDefault();
            current_month -= 1;

            if(current_month == -1)
            {
                current_month = 11;
                current_year -= 1;
            }

            fetch_training_session_data(current_month + 1, current_year);

            var current_month_and_year = months[current_month] + ' ' + current_year;
            selected_month.html(current_month_and_year);
            load_days_of_month(current_year, current_month);
        });

        forward.on('click', function (event) {
            event.preventDefault();
            current_month += 1;

            if(current_month == 12)
            {
                current_month = 0;
                current_year += 1;
            }

            fetch_training_session_data(current_month + 1, current_year);

            var current_month_and_year = months[current_month] + ' ' + current_year;
            selected_month.html(current_month_and_year);
            load_days_of_month(current_year, current_month);
        });
    }());

    function load_days_of_month(year, month) {
        var firstDay = new Date(year, month, 1).getDay();

        var days_in_current_month = daysInMonth(month, year);
        var days_in_last_month = daysInMonth(month - 1, year);
        var day_counter = 1;
        var current_day_counter = 1;
        var reverse_day_counter = 1;
        var number_of_rows = 0;
        var days = [];
        var table_body = $('#calendar_body');
        var table_body_content = '';

        if(firstDay == 0 && month != 1)
        {
            number_of_rows = 6;
        }
        else if(firstDay == 1 && month == 1)
        {
            number_of_rows = 4;
        }
        else{
            number_of_rows = 5;
        }

        if(firstDay == 0)
        {
            firstDay = 7;
        }

        for(var i = 1; i <= number_of_rows * 7; i++)
        {
            if(i < firstDay)
            {
                var day_number_1 = daysInMonth(month - 1, year) - (firstDay - 1) + reverse_day_counter;
                var day_date_1 = new Date(year, month - 1, days_in_last_month - (firstDay - 1) + reverse_day_counter);
                days.push([day_number_1, day_date_1, false]);
                reverse_day_counter += 1;
            }
            else if(i >= days_in_current_month + firstDay)
            {
                var day_number_2 = day_counter;
                var day_date_2 = new Date(year, month + 1, day_counter);
                days.push([day_number_2, day_date_2, false]);
                day_counter += 1;
            }
            else{
                var day_number_3 = new Date(year, month, current_day_counter).getDate();
                var date_number_3 = new Date(year, month, current_day_counter);
                days.push([day_number_3, date_number_3, true]);
                current_day_counter += 1;
            }
        }

        style_days_and_add_content(table_body_content, days, table_body, number_of_rows);

    }

    function style_days_and_add_content(table_body_content, days, table_body, number_of_rows)
    {
        var counter = 0;

        for(var j = 0; j < number_of_rows; j++)
        {
            table_body_content += '<tr>';

            for(var k = 0; k < 7; k++)
            {
                if(days[counter][1].toDateString() == new Date().toDateString())
                {
                    table_body_content += '<td  class="current-day" data="' + days[counter][1].toDateString() +'">' + days[counter][0] + '</td>';
                    counter += 1;
                }
                else if(!days[counter][2])
                {
                    table_body_content += '<td class="not-current-month-days" data="' + days[counter][1].toDateString() +'">' + days[counter][0] + '</td>';
                    counter += 1;
                }
                else{
                    table_body_content += '<td class="current-month-days" data="' + days[counter][1].toDateString() +'">' + days[counter][0] + '</td>';
                    counter += 1;
                }
            }

            table_body_content += '</tr>';
        }

        table_body.html(table_body_content);
    }

    function daysInMonth(month,year) {
        return new Date(year, month + 1, 0).getDate();
    }

    function fetch_training_session_data(month, year)
    {
        $.ajax({
            url: '/calendar_data',
            data: JSON.stringify({month: month, year: year}),
            type: 'POST',
            contentType: 'application/json',
            success: function (response) {
                var data = JSON.parse(response);
                var dates = Object.keys(data);
                var trainings_current_month = $('#trainings_current_month');

                trainings_current_month.html('Trainings done in selected month: ' + dates.length);

                $('td').each(function (index, element) {
                    if(dates.indexOf($(element).attr('data')) != -1)
                    {
                        var el = $(element);
                        var ind = el.attr('data');
                        var tooltip_text = "";

                        for(var i = 0; i < data[ind][1].length; i++)
                        {
                            if(i == data[ind][1].length - 1)
                            {
                                tooltip_text += data[ind][1][i];
                            }
                            else{
                                tooltip_text += data[ind][1][i] + "/";
                            }
                        }

                        el.css('background-color', '#337ab7');
                        var day_number = el.text();
                        var a = $("<a>",
                            {id: data[ind][0], href: '#', title: tooltip_text});
                        a.attr('data-toggle', 'tooltip');
                        a.attr('class', 'calendar_link');
                        a.text(day_number);
                        el.text('');
                        el.html(a);
                    }
                });

                $('[data-toggle="tooltip"]').tooltip();

                $('.calendar_link').on('click', function (event) {
                    event.preventDefault();
                    var id = $(this).attr('id');

                    $.ajax({
                        url: '/clients_training_session',
                        data: JSON.stringify({session_id: id}),
                        contentType: 'application/json',
                        type: 'POST',
                        success: function (response) {
                            var data = JSON.parse(response);
                            var exercises_table = $('<table>', {class:'table-training-sessions'});
                            var headings = "<thead><th></th><th>Exercise</th><th>Resistance</th>" +
                                "<th>Sets</th><th>Reps</th></thead>";

                            var rows = "<tbody>";

                            for(var i = 0; i < data.length; i++)
                            {
                                rows += "<tr>";

                                for(var j = 0; j < data[i].length; j++)
                                {
                                    rows += "<td>" + data[i][j] + "</td>";
                                }

                                rows += "</tr>";
                            }

                            rows += "</tbody>";

                            exercises_table.html(headings + rows);

                            $('#training-session-exercises').html(exercises_table);
                        }
                    })
                });
            }
        });
    }
}
