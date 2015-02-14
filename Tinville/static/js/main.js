

        // using jQuery
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        var csrftoken = getCookie('csrftoken');

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        function sameOrigin(url) {
            // test that a given url is a same-origin URL
            // url could be relative or scheme relative or absolute
            var host = document.location.host; // host + port
            var protocol = document.location.protocol;
            var sr_origin = '//' + host;
            var origin = protocol + sr_origin;
            // Allow absolute or scheme relative URLs to same origin
            return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                // or any other URL that isn't scheme relative or absolute i.e relative.
                !(/^(\/\/|http:|https:).*/.test(url));
        }

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                    // Send the token to same-origin, relative URLs only.
                    // Send the token only if the method warrants CSRF protection
                    // Using the CSRFToken value acquired earlier
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

        $(document).ready(function () {
            stickyFooter();
        });

        $(window).on('resize', function () {
            stickyFooter();
        });


        function isTooLightYIQ(hexcolor){
          color = new RGBColor(hexcolor);
          var yiq = ((color.r*299)+(color.g*587)+(color.b*114))/1000;
          return yiq >= 128;
        }

        function stickyFooter() {
                // Jon M TBD - Temp hack until we can find a better sticky footer solution :(
                $('.slidingContent2').css('min-height', $(window).height() *.75);
        }




        $("#goToTopOfPage").click(function(){
             $('html, body').animate({ scrollTop: 0 }, 'slow');
        });

        $("#goToTopOfPageXS").click(function(){
             $('html, body').animate({ scrollTop: 0 }, 'slow');
        });
        $(window).resize(function(){
             var mode = checkMode();

            if(mode == 'xs'){
                $("#nonMobileMenContent").css("display","none");
                $("#mobileMenContent").css("display","");

                $("#nonMobileWomenContent").css("display","none");
                $("#mobileWomenContent").css("display","");
            }
            else
            {
                $("#nonMobileMenContent").css("display","");
                $("#mobileMenContent").css("display","none");

                $("#nonMobileWomenContent").css("display","");
                $("#mobileWomenContent").css("display","none");

                $('.navbarSliding').removeAttr( 'style' );
                $('.slidingContent').removeAttr( 'style' );
            }
        });

         $(window).load(function(){
              var mode = checkMode();

            if(mode == 'xs'){
                $("#nonMobileMenContent").css("display","none");
                $("#mobileMenContent").css("display","");

                $("#nonMobileWomenContent").css("display","none");
                $("#mobileWomenContent").css("display","");
            }
            else{
                $("#nonMobileMenContent").css("display","");
                $("#mobileMenContent").css("display","none");

                $("#nonMobileWomenContent").css("display","");
                $("#mobileWomenContent").css("display","none");
            }
        });



        $(window).scroll(function () {
            if ($(window).scrollTop() > 10) {
                $('.navbar-header').css('top', $(window).scrollTop());
            }
          }
        );




        $(document).ready(function() {

                   var menu = "close";

                    $('.menu-toggle').click(function() {
                        if(menu == "close"){
                            $('.slidingContent').css('left','70%');
                            $('.slidingContent').css('opacity','.05');
                            $('.slidingContent').css('position','fixed');
                            $('.slidingContent').css('pointer-events','none');
                            $('.navbarSliding').css('width','70%');
                            $('.navbarSliding').css('left','70%');
                            menu="open";
                        }
                        else{
                            $('.slidingContent').css('left','0%');
                            $('.slidingContent').css('opacity','1');
                            $('.slidingContent').css('position','relative');
                            $('.slidingContent').css('pointer-events','auto');
                            $('.navbarSliding').css('width','0%');
                            $('.navbarSliding').css('left','0%');
                            menu="close";
                        }
            });
            var self = $(this);
            var url = "/load_cart";
                ajax_req = $.ajax({
                    url: url,
                    type: "GET",
                    dataType: 'json',
                    success: function(data, textStatus, jqXHR) {
                        $.each(data, function(index, item)
                        {
                            if (item.msg == ''){
                                item.image = "{{ MEDIA_URL }}" + item.image;
                                AddCartItem(item);
                                cartCount()
                            }
                            else {
                                $('#messageId').html(item.msg);
                                $('#messageModal').modal('show');
                            }
                        });
                    },
                    error: function(data, textStatus, jqXHR) {
                    }
                });

            cartCount();

        });

        $(document).on("submit", ".loginForm", function(e) {
            e.preventDefault();
            var self = $(this),
                url = self.attr("action"),

                ajax_req = $.ajax({
                    url: url,
                    type: "POST",
                    data: {
                        username: self.find("#id_username").val(),
                        password: self.find("#id_password").val(),
                        remember_me : self.find("#id_remember_me").val()
                    },
                    success: function(data, textStatus, jqXHR) {
						if (location.pathname == "/notifications") {
							location.href = "/";
						} else {
							location.reload();
						}
                    },
                    error: function(data, textStatus, jqXHR) {
                        clear_django_messages(self.find(".message_area"));
                        clear_form_field_errors(".loginPopupForm");
                        var errors = $.parseJSON(data.responseText);
                        $.each(errors, function(index, value) {
                            if (index === "__all__") {
                                django_message(value[0], "error", self.find(".message_area"));
                            } else {
                                apply_form_field_error(self[0].id, index, value);
                            }
                        });
                    }
                });
        });


     $("a.dropdown-toggle.hidden-xs").click(function() {
         $("#id_username.textinput.textInput").val("");
         $("#id_password.textinput.textInput").val("");
     });

    $("#navLogin").click(function()
    {
        $("#id_username.textinput.textInput").val("");
        $("#id_password.textinput.textInput").val("");
    });

 var cartTotal;
 var cartJson, cartState;
 cartState = sessionStorage.getItem("cartState");
 cartJson = JSON.parse(cartState || "{}");

      function cartCount()
      {
          ajax_req = $.ajax({
                url: "/total_cart_items",
                type: "GET",
                success: function(data, textStatus, jqXHR) {
                    if (data.count > 0){
                        $('#cartCountId').text(data.count);
                        $('#cartCountId').removeClass("hidden");
                        $('#carttotal').removeClass("hidden");
                        $('#divider').removeClass("hidden");
                        $('#shoppingcartcheckout').removeClass("hidden");
                        $('#noItem').addClass("hidden");
                        $('#tagIconId').removeClass("tinvilleDrayGray");
                        $('#tagIconId').addClass("tinvilleOrange");
                    }
                    else{
                        $('#cartCountId').addClass("hidden");
                        $('#carttotal').addClass("hidden");
                        $('#divider').addClass("hidden");
                        $('#shoppingcartcheckout').addClass("hidden");
                        $('#noItem').removeClass("hidden");
                        $('#tagIconId').removeClass("tinvilleOrange");
                        $('#tagIconId').addClass("tinvilleDrayGray");
                    }
                },
                error: function(data, textStatus, jqXHR) {
                }
            });
      }
$(function() {

    cartState = sessionStorage.getItem("cartState");
    cartJson = JSON.parse(cartState || "{}");

    aggregateTotal();

    var _IsOpen = cartJson["IsOpen"];


});

$("#mobileNavButton").click(function()
{
    navbarClicked();
});

function navbarClicked()
{
    cartState = sessionStorage.getItem("cartState");
    cartJson = JSON.parse(cartState || "{}");
    var IsOpen = false;

    cartJson["IsOpen"] = IsOpen;
    sessionStorage.setItem("cartState", JSON.stringify(cartJson));
}

function cartToggleBtn()
{
    cartState = sessionStorage.getItem("cartState");
    cartJson = JSON.parse(cartState || "{}");
    var IsOpen = cartJson["IsOpen"];
    if(IsOpen === undefined || IsOpen === true)
        IsOpen = false;
    else
        IsOpen = true;

    cartJson["IsOpen"] = IsOpen;
    sessionStorage.setItem("cartState", JSON.stringify(cartJson));
}
function LoadCartItemDiv(cartItem)
{
    var rowdiv =  $('<div/>', {
        'class':'row'
    });
    var cartitemdiv =  $('<li/>', {
        'class':'shoppingcartitem col-xs-12',
        'id' : "lineId" + cartItem.Id
    });

    var itemThumbnail = $('<img/>', {'src':cartItem.image, 'class': 'img-responsive shoppingcartthumbnail'});
    var thumbnailDiv = $('<div/>', {'class': 'shoppingcartthumbnaildiv'});
    itemThumbnail.appendTo(thumbnailDiv);
    thumbnailDiv.appendTo(cartitemdiv);

    var itemInfoDiv = $('<div/>', {'class' : 'shoppingcartiteminfo'});

    var itemTitle = $('<div/>', {'class':'shoppingcartitemTitle ','text':cartItem.title});
    itemTitle.appendTo(itemInfoDiv);

    var itemDescription = $('<div/>', {'class':'shoppingcartitemDescription', 'text':"Color: " + cartItem.color});
    itemDescription.appendTo(itemInfoDiv);
    var itemSize = $('<div/>', {'class':'shoppingcartitemDescription', 'text':"Size: " + cartItem.size});
    itemSize.appendTo(itemInfoDiv);

    var itemQty = $('<div/>', {'class':'shoppingcartitemQty', 'text':"Qty:" + cartItem.qty});
    itemQty.appendTo(itemInfoDiv);

    itemInfoDiv.appendTo(cartitemdiv);
    var removeBtnDiv = $('<div/>', {'class':'shoppingcartremovebtn'});
    var delBtnId = 'deleteBtnId_' + cartItem.Id;
    var removeBtn = $('<a/>', { 'onclick' : 'RemoveCartItem(' + cartItem.Id + ')', 'id' : delBtnId,
        'class' : 'shoppingcartBtn', 'html' : '<img src="{{ STATIC_URL }}img/delete.png" width="20" height="20">'
    });
    removeBtn.appendTo(removeBtnDiv);
    removeBtnDiv.appendTo(cartitemdiv);
    var price = '$' + (cartItem.qty * cartItem.price);
    var priceDiv = $('<div/>', {'class':'shoppingcartitemPrice', 'text': price});
    priceDiv.appendTo(cartitemdiv);
    cartitemdiv.appendTo(rowdiv);

    rowdiv.appendTo("#shoppingcartitems");



     $(".shoppingcartitemTitle").text(function(index, currentText) {
            return currentText.substr(0, 15);
        });
}


function aggregateTotal()
{
    var url = "/cart_total";
    ajax_req = $.ajax({
        url: url,
        type: "GET",
        success: function(data, textStatus, jqXHR) {
            $('#carttotal').text('Total: $' + data.total);
        },
        error: function(data, textStatus, jqXHR) {
        }
    });
}

function AddCartItem(cartItem)
{
    if ($("#lineId" + cartItem.Id).length === 0){
        LoadCartItemDiv(cartItem);
        aggregateTotal();
    }


}

function RemoveCartItem(itemId)
{
    var self = $(this);
    var url = "/delete_item_to_cart";

    var ajax_req = $.ajax({
            url: url,
            type: "POST",
            data: {
                Id: itemId
            },
            success: function(data, textStatus, jqXHR) {
            },
            error: function(data, textStatus, jqXHR) {
            }
        });

    $('#lineId'+itemId).remove();

    aggregateTotal();
    cartCount();
}

    $("#shoppingcartitems").slimScroll({});


        window.ParsleyValidator
          .addValidator('cardnum', function (value) {
            return Stripe.card.validateCardNumber(value);
          }, 32)
          .addMessage('en', 'cardnum', 'Invalid card number');
        window.ParsleyValidator
          .addValidator('cardexpiry', function (value) {
            var month = $("[data-stripe='exp-month']")[0].value;
            var year = $("[data-stripe='exp-year']")[0].value;
            return Stripe.card.validateExpiry(month, year);
          }, 33)
          .addMessage('en', 'cardexpiry', 'Invalid card expiration date');
        window.ParsleyValidator
          .addValidator('cardcvc', function (value) {
            return Stripe.card.validateCVC(value);
          }, 34)
          .addMessage('en', 'cardcvc', 'Invalid card verification code');

     $("[data-parsley-group='cardexpiry']").keyup(function() {
          $("[data-parsley-group='cardexpiry']").each( function() {
              $( this ).parsley().validate();
          })
        });


     $(".parsley-form").parsley({
        successClass: 'has-success',
        errorClass: 'has-error',
        classHandler: function(el) {
            return el.$element.closest(".form-group");
        },
        errorsWrapper: "<span class=\'help-block\'></span>",
        errorTemplate: "<span></span>"
    });

    //for each element that is classed as 'pull-down', set its margin-top to the difference between its own height and the height of its parent
    $('.pull-down').each(function() {
        $(this).css('margin-top', $(this).parent().height()-$(this).height())
    });

    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        stickyFooter();
    });

        $(document).ready(function()
        {
            var mode = checkMode();
            if(mode == 'xs' || mode == 'sm') {
                $('#mobileModal').modal('show');
            }
        });