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
                    $("#student_evaluations_edit_div").html(data['html_form'])
                    $("#student_evaluations_edit_popup").modal("show");
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
                        $("#student_evaluations_edit_popup").modal("hide");
                        location.reload();
                    } else {
                        $("#student_evaluations_edit_popup").modal("hide");
                        $("#student_evaluations_edit_div").html(data['html_form']);
                        $("#student_evaluations_edit_popup").modal("show");
                    }
                },
                error: function (response) {
                    $("#student_evaluations_edit_popup").modal("hide");
                    location.reload();
                }
            });
            return false;
        };
        $("body").on('click', '#update_eval_btn', loadForm);
        $("body").on('submit', '#student_evaluations_edit_form', saveForm);
    }) /* document ready */


})(window, document, jQuery)