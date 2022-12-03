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
                    $("#profile_div").html(data['html_form'])
                    $("#profile_popup").modal("show");
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
                        $("#profile_popup").modal("hide");
                        location.reload();
                    } else {
                        $("#profile_popup").modal("hide");
                        $("#profile_div").html(data['html_form']);
                        $("#profile_popup").modal("show");
                    }
                },
                error: function (response) {
                    $("#profile_popup").modal("hide");
                    location.reload();
                }
            });
            return false;
        };
        $("body").on('click', '#add_profile_btn', loadForm);
        $("body").on('click', '#update_profile_btn', loadForm);
        $("body").on('submit', '#profile_form', saveForm);

    }) /* document ready */


})(window, document, jQuery)
