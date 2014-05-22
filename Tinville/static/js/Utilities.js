/**
 * Created with PyCharm.
 * User: senay
 * Date: 5/20/14
 * Time: 9:46 PM
 * To change this template use File | Settings | File Templates.
 */
        function checkMode() {

                if ($(window).width() < 753) {
                    return 'xs';
                }
                else if ($(window).width() >= 753 && $(window).width() < 992) {
                    return 'sm';
                }
                else if ($(window).width() >= 992 && $(window).width() < 1200) {
                    return 'md';
                }
                else {
                    return 'lg';
                }
         }

        function apply_form_field_error(form_id, fieldname, error) {
            var form = $("#" + form_id)
                input = form.find("#id_" + fieldname),
                container = form.find("#div_id_" + fieldname),
                error_msg = $("<span />").addClass("help-block ajax-error");

            $(error_msg).append("<strong>" + error[0] + "</strong>")
            container.addClass("has-error");
            error_msg.insertAfter(input);
        }

        function clear_form_field_errors(form) {
            $(".ajax-error", $(form)).remove();
            $(".error", $(form)).removeClass("error");
        }

        function django_message(msg, level, messageElement) {
            var levels = {
                warning: 'alert',
                error: 'danger',
                success: 'success',
                info: 'info'
            },
            source = $('#message_template').html(),
            template = Handlebars.compile(source),
            context = {
                'tags': levels[level],
                'message': msg
            },
            html = template(context);

            messageElement.append(html);
        }

        function clear_django_messages(messageElement) {
            messageElement.empty();
        }

        function django_block_message(msg, level, messageElement) {
            var source = $("#message_block_template").html(),
                template = Handlebars.compile(source),
                context = {level: level, body: msg},
                html = template(context);

            messageElement.append(html);
        }

