$(document).ready(function () {
    add_exercise();
});

/*
* template: add_exercise.html
* events regarding adding of exercises to the database
* */



function add_exercise() {

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

