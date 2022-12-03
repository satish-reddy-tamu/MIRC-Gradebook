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
                    $("#course_div").html(data['html_form'])
                    $("#course_popup").modal("show");
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
                        $("#course_popup").modal("hide");
                        location.reload();
                    } else {
                        $("#course_popup").modal("hide");
                        $("#course_div").html(data['html_form']);
                        $("#course_popup").modal("show");
                    }
                },
                error: function (response) {
                    $("#course_popup").modal("hide");
                    location.reload();
                }
            });
            return false;
        };
        $("body").on('click', '#add_course_btn', loadForm);
        $("body").on('click', '#update_course_btn', loadForm);
        $("body").on('click', '#enroll_profiles_btn', loadForm);
        $("body").on('submit', '#course_form', saveForm);
    }) /* document ready */


})(window, document, jQuery)
