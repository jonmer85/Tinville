function checkMode(){if($(window).width()<753){return'xs';}
else if($(window).width()>=753&&$(window).width()<992){return'sm';}
else if($(window).width()>=992&&$(window).width()<1200){return'md';}
else{return'lg';}}
function apply_form_field_error(form_id,fieldname,error){var form=$("#"+form_id)
input=form.find("#id_"+fieldname),container=form.find("#div_id_"+fieldname),error_msg=$("<span />").addClass("help-block ajax-error");$(error_msg).append("<strong>"+error[0]+"</strong>")
container.addClass("has-error");error_msg.insertAfter(input);}
function clear_form_field_errors(form){$(".ajax-error",$(form)).remove();$(".error",$(form)).removeClass("error");}
function django_message(msg,level,messageElement){var levels={warning:'alert',error:'danger',success:'success',info:'info'},source=$('#message_template').html(),template=Handlebars.compile(source),context={'tags':levels[level],'message':msg},html=template(context);messageElement.append(html);}
function clear_django_messages(messageElement){messageElement.empty();}
function django_block_message(msg,level,messageElement){var source=$("#message_block_template").html(),template=Handlebars.compile(source),context={level:level,body:msg},html=template(context);messageElement.append(html);}
var feedbackToggle;(function($){feedbackToggle=function(){$('#feedback_tab, #feedback_panel').toggle();}
$(document).ready(function(){$('#feedback_tab button, #feedback_panel button').click(feedbackToggle);$('#feedback_form').submit(function(e){e.preventDefault();var action=this.action;$.ajax(action,{'type':'POST','data':$(this).serialize(),'success':function(data,textStatus,jqXHR){alert("Your feedback has been successfully submitted, thank you.");$("#feedback_panel form textarea").val("");feedbackToggle();},'error':function(jqXHR,textStatus,errorThrown){if(jqXHR.status==400)
{var errors="The following field error(s) ocurred: \n";errors+=jqXHR.responseText;alert(errors);}
else if(jqXHR.responseText!=''){alert("The following error ocurred: \n"+jqXHR.responseText);}
else{alert('An unknown error occurred.');}}});});});})(jQuery);