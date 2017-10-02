$(document).ready(function () {
    show_muscles();
    add_exercise();
    by_muscle_group();
    create_training();
    clients_profile_page();
});

function clients_profile_page() {
    var training_sessions = $('.training-session');
    
    training_sessions.on('click', function (event) {
        event.preventDefault();
        var id = $(this).attr('href').split('_')[1];

        $.ajax({
            url: '/clients_profiles',
            data: JSON.stringify({session_id: id}),
            contentType: 'application/json',
            type: 'POST',
            success: function () {

            }
        });
    });
}

function create_training() {
    var table = $('#training-table');
    var add_row = $('#add-exercise-row');
    var remove_row = $('#remove-exercise-row');
    var submit = $('#submit_training');
    var next = 0;
    var training_text = $('#training');
    var checkboxes = $('.checkbox-muscles li input');
    var select_muscle_groups = $('#select-muscle-group');
    var muscle_groups_checked = [];
    var response_object = null;

    select_muscle_groups.on('change', function () {
        if(response_object.length != 0)
        {
            create_training_session_chart(response_object, $("#select-muscle-group option:selected").text());
        }
    });

    checkboxes.each(function () {
       $(this).on('change', function () {
           var val = $(this).attr('value');
           var label = 'muscle_groups_checkbox-' + (val - 1);
           var text = $("label[for="+label+"]").text();
           var selected_user = $('#clients').val();

           if($(this).is(':checked')) {
               muscle_groups_checked.push(val);
               select_muscle_groups.append(new Option(text, val));
           }
           else
           {
               var index = muscle_groups_checked.indexOf($(this).attr('value'));
               muscle_groups_checked.splice(index, 1);
               $("option").remove(":contains("+text+")");
           }

           $.ajax({
               url: '/return_training_session_volumes',
               data: JSON.stringify({muscle_ids: muscle_groups_checked, user_id: selected_user}),
               contentType: 'application/json',
               type: 'POST',
               success: function (response) {
                   response_object = response;
                   if(response.length != 0){
                       create_training_session_chart(response, $("#select-muscle-group option:selected").text());
                   }
               }
           });

       });
    });

    submit.on('click', function (event) {
        event.preventDefault();
        var text = '';
        var counter = 1;
        var form = $('#create_training');

        $('#training-table tr td').each(function () {
            text += $(this).text() + '|';
            if(counter % 5 == 0)
            {
                text += '#';
            }

            counter++;
        });
        training_text.text(text);
        form.submit();
    });
    
    add_row.on('click', function (event) {
        event.preventDefault();

        next += 1;

        var append = '<tr><td>' + next + '.' + '</td><td class="exercise" contenteditable="true"></td><td class="resistance" contenteditable="true"></td><td class="sets" contenteditable="true"></td><td class="reps" contenteditable="true"></td></tr>';

        table.append(append);
    });

    remove_row.on('click', function (event) {
        event.preventDefault();

        next -= 1;

        $('#training-table > tr:last-of-type').remove();
    });

    $(document).on('keyup', '.exercise', function () {
        var exercise_1 = $(this).text();
        var exercise_2 = $(this).val();
        var exercise = "";
        var td = $(this);
        var selected_user = $('#clients').val();

        if(exercise_1.length == 0)
        {
            exercise = exercise_2;
        }
        else if(exercise_2.length == 0)
        {
            exercise = exercise_1;
        }

        $.ajax({
            url: '/return_exercise_data',
            data: JSON.stringify({ex: exercise_1, user_id: selected_user}),
            type: 'POST',
            contentType: 'application/json',
            success: function (response) {
                if(!$.isEmptyObject(response))
                {
                    console.log(response);
                    create_exercise_chart(response);
                }
            }
        });
        
        $.ajax({
            url: '/check_exercise',
            data: {ex: exercise},
            type: 'POST',
            success: function (response) {
                if(response == 'found')
                {
                    td.css('color', 'green');
                }
                else{
                    td.css('color', 'red');
                }
            }
        });
    });

    $(document).on('keyup', '.exercise, .resistance, .sets, .reps', function () {
        var attr = $(this).attr('class');

        switch (attr)
        {
            case 'exercise':
                break;
            case 'resistance':
                break;
            case 'sets':
                break;
            case 'reps':
                break;
        }
    });
}

function show_muscles() {
    /*show sub muscle groups*/
    $('.ajax-main-muscles').on('click', function (event) {
        event.preventDefault();
        var sub_muscle_class = $(this).attr('name');
        var div = $('.' + sub_muscle_class);
        div.toggle();
    });

    /*show muscles*/
    $('.ajax-sub-muscles').on('click', function (event) {
        event.preventDefault();
        var muscle_class = $(this).attr('name');
        var div = $('.' + muscle_class);
        div.toggle();
    });
}

function by_muscle_group() {
    $('.muscles-by-muscle-group').on('click', function () {
        var muscle_id = $(this).attr("id");
        var div = $('#by_muscle_group_div');

        $.ajax({
        url: '/by_muscle_group_load_exercises',
        type: 'POST',
        data: {id: muscle_id},
        success: function (response) {
            div.html(response);
        }
    });
    });

     $(document).on('click', '.by_muscle_group', function (event) {
         event.preventDefault();
         var cls = $(this).attr('href');

         $('.' + cls).toggle();
     });

     $(document).on('click', '.by_muscle_group_exercise', function (event) {
         event.preventDefault();

         var id = $(this).attr('href');
         $('.'+id).toggle();
     });
}

/*
* template: add_exercise.html
* events regarding adding of exercises to the database
* */
function add_exercise() {
    /*
    * create dismissable div inside div #exercises_added
    * add values to the list that is not shown but sent to the view function
    * */
    $('.ajax-muscles').on('click', function (event) {
        event.preventDefault();
        var div_area = $('#exercises_added');
        var select_field = $('#muscles_involved');

        var div_dismiss = '<div style="font-size: 0.7em; margin-bottom: 1%;" class="alert alert-info alert-dismissable">' +
            '<button name="' + $(this).attr("id") + '" style="font-size: 1.6em; margin-left: 1%;" class="close stabilizer" type="button">T</button>' +
            '<button name="' + $(this).attr("id") + '" style="font-size: 1.6em; margin-left: 1%;" class="close synergist" type="button">S</button>' +
            '<button name="' + $(this).attr("id") + '" style="font-size: 1.6em; margin-left: 13%;" class="close prime-mover" type="button">P</button>' +
            '<button name="' + $(this).attr("id") + '" style="font-size: 1.6em;" type="button" class="close delete-muscle" data-dismiss="alert">X</button>' +
            '' + $(this).html() + '</div>';
        var option = '<option selected="selected" id="' + "select_" + $(this).attr("id") + '" value="' + $(this).attr("id") + '">' + $(this).html() + '</option>';

        div_area.append(div_dismiss);
        select_field.append(option);
    });

    /*remove selected muscle from div #exercises_added*/
    $(document).on('click', '.delete-muscle', function () {
        var selected_id = '#select_' + $(this).attr("name");
        $(selected_id).remove();
    });

    /*
    * assign the priority of the muscle to the exercise
    * */
    $(document).on('click','.prime-mover, .stabilizer, .synergist', function (event) {
        event.preventDefault();
        var selected_id = '#select_' + $(this).attr("name");
        var selected_class = $(this).attr('class');

        switch (selected_class)
        {
            case 'close prime-mover':
                $(selected_id).attr('value', function() { return $(selected_id).attr("value") + "/10" });
                $(this).css('color', 'green');
                break;
            case 'close synergist':
                $(selected_id).attr('value', function() { return $(selected_id).attr("value") + "/5" });
                $(this).css('color', 'green');
                break;
            case 'close stabilizer':
                $(selected_id).attr('value', function() { return $(selected_id).attr("value") + "/1" });
                $(this).css('color', 'green');
                break;
            default:
                break;
        }
    })
}

// global reference for charts, so that they can be destroyed before redrawing
var charts_sessions = [];
var chart_exercises = [];

function create_exercise_chart(exercise_data) {
    var NUM_OF_CHARTS = 3;
    var labels = ['sets', 'reps', 'weight'];
    var background_colors = ['blue', 'green', 'yellow'];
    var dates = Object.keys(exercise_data);
    var data = [];
    var sets = [];
    var reps = [];
    var weight = [];

    dates.reverse();

    if(chart_exercises.length != 0)
    {
        for(var k = 0; k < NUM_OF_CHARTS; k++)
        {
            chart_exercises[k].destroy();
        }
    }

    for(var j = 0; j < dates.length; j++)
    {
        sets.push(exercise_data[dates[j]][0]);
        reps.push(exercise_data[dates[j]][1]);
        weight.push(exercise_data[dates[j]][2]);
    }

    data.push(sets);
    data.push(reps);
    data.push(weight);

    for(var i = 0; i < NUM_OF_CHARTS; i++)
    {
        var canvas_id = '#canvas_exercise_' + i;
        var canvas = $(canvas_id)[0].getContext('2d');

        chart_exercises[i] = new Chart(canvas, {
            type: 'bar',
            data: {
                labels: dates,
                datasets: [{
                    label: labels[i],
                    data: data[i],
                    backgroundColor: background_colors[i]
                }]
            },
            options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                            }
                        }],
                xAxes: [{
                    ticks: {
                        beginAtZero:true
                            }
                        }]
                    }
                }
        });
    }
}

function create_training_session_chart(training_session_data, muscle_group)
{
    var chart_labels = ['sets', 'reps', 'weight', 'time'];
    var background_colors = ['blue', 'green', 'purple', 'yellow'];
    var key = muscle_group.toLowerCase();
    var data = [];
    var dates = [];
    var sets = [];
    var reps = [];
    var weight = [];
    var time = [];
    var NUM_OF_CHARTS = 4;

    if(charts_sessions.length != 0)
    {
         for(var k = 0; k < NUM_OF_CHARTS; k++)
        {
            charts_sessions[k].destroy();
        }
    }

    for(var j = 0; j < training_session_data.length; j++)
    {
        dates.push(training_session_data[j]['date']);
        sets.push(training_session_data[j][key]['sets']);
        reps.push(training_session_data[j][key]['reps']);
        weight.push(training_session_data[j][key]['weight']);
        time.push(training_session_data[j][key]['time']);
    }

    data.push(sets);
    data.push(reps);
    data.push(weight);
    data.push(time);

    for(var i = 0; i < NUM_OF_CHARTS; i++)
    {
        var canvas_id = '#canvas_session_' + i;
        var canvas = $(canvas_id)[0].getContext('2d');

        canvas.clearRect(0, 0, canvas.width, canvas.height);

        charts_sessions[i] = new Chart(canvas, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: key + " [" + chart_labels[i] + "]",
                    data: data[i],
                    backgroundColor: background_colors[i]
                }]
            },
            options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                            }
                        }]
                    }
                }
        });
    }

}

