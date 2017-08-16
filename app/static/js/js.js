$(document).ready(function () {
    admin_ajax();

    $(document).on('click', '.main_muscle_groups', function (event) {
        $('.sub_muscle_groups').css('display', 'block');
    });

    $(document).on('click', '.ajax-main-muscles', function (event) {
        event.preventDefault();
        var sub_muscle_class = $(this).attr('name');
        var div = $('.' + sub_muscle_class);
        div.toggle();
    });

    $(document).on('click', '.ajax-sub-muscles', function (event) {
        event.preventDefault();
        var muscle_class = $(this).attr('name');
        var div = $('.' + muscle_class);
        div.toggle();
    });

    $(document).on('click', '.ajax-muscles', function (event) {
        event.preventDefault();
        var txt_area = $('#exercises_added');
        var select_field = $('#muscles_involved');

        var div_dismiss = '<div style="font-size: 0.7em; margin-bottom: 1%;" class="alert alert-info alert-dismissable">' +
            '<button name="' + $(this).attr("id") + '" style="font-size: 1.6em; margin-left: 1%;" class="close stabilizer" type="button">T</button>' +
            '<button name="' + $(this).attr("id") + '" style="font-size: 1.6em; margin-left: 1%;" class="close synergist" type="button">S</button>' +
            '<button name="' + $(this).attr("id") + '" style="font-size: 1.6em; margin-left: 13%;" class="close prime-mover" type="button">P</button>' +
            '<button name="' + $(this).attr("id") + '" style="font-size: 1.6em;" type="button" class="close delete-muscle" data-dismiss="alert">X</button>' +
            '' + $(this).html() + '</div>';
        var option = '<option selected="selected" id="' + "select_" + $(this).attr("id") + '" value="' + $(this).attr("id") + '">' + $(this).html() + '</option>';

        txt_area.append(div_dismiss);
        select_field.append(option);
    });

    $(document).on('click', '.delete-muscle', function () {
        var selected_id = '#select_' + $(this).attr("name");
        $(selected_id).remove();
    });

    $(document).on('click', '.prime-mover, .stabilizer, .synergist', function (event) {
        event.preventDefault();
        var selected_id = '#select_' + $(this).attr("name");
        var selected_class = $(this).attr('class');

        switch (selected_class)
        {
            case 'close prime-mover':
                $(selected_id).attr('name', '10');
                $(this).css('color', 'green');
                break;
            case 'close stabilizer':
                $(selected_id).attr('name', '5');
                $(this).css('color', 'green');
                break;
            case 'close synergist':
                $(selected_id).attr('name', '1');
                $(this).css('color', '#green');
                break;
            default:
                break;
        }
    })

});

function admin_ajax() {
    var elements = $('.admin-ajax');
    var content_area = $('#main-content-area');

    elements.on('click', function (event) {
        event.preventDefault();

        var route = $(this).attr('name');

        $.ajax({
            url: route,
            type: 'POST',
            success: function (response) {
                content_area.html(response);
            }
        });
    })
}


