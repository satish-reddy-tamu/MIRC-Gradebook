'use strict';
(function (w, d, $) {
    $(d).ready(function () {
        let loadForm = function (e) {
            let btn = $(this);
            $.ajax({
                url: btn.attr("href"),
                type: 'get',
                dataType: 'json',
                success: function (data) {
                    $("#evaluation_div").html(data['html_form'])
                    $("#evaluation_popup").modal("show");
                }
            });
            return false;
        };

        let saveForm = function () {
            let form = $(this);
            $.ajax({
                url: form.attr("action"),
                data: form.serialize(),
                type: form.attr("method"),
                dataType: 'json',
                success: function (data) {
                    console.log(data)
                    if (data['form_is_valid']) {
                        $("#evaluation_popup").modal("hide");
                        location.reload();
                    } else {
                        $("#evaluation_popup").modal("hide");
                        $("#evaluation_div").html(data['html_form']);
                        $("#evaluation_popup").modal("show");
                    }
                },
                error: function (response) {
                    $("#evaluation_popup").modal("hide");
                    location.reload();
                }
            });
            return false;
        };
        $("body").on('click', '#add_evaluation_btn', loadForm);
        $("body").on('click', '#add_grade_function_btn', loadForm);
        $("body").on('click', '#update_evaluation_btn', loadForm);
        $("body").on('submit', '#evaluation_form', saveForm);
    }) /* document ready */


})(window, document, jQuery)