jQuery(document).ready(function( $ ) {

/*    <script> */
        jQuery(document).ready(function(){
            jQuery('.quiz').slick({
                dots: true,
                draggable: true,
                swipe: true
            });
            /*
            jQuery(".quiz #stage-1").click(function(event){
                event.stopImmediatePropagation();
                jQuery("html").css("cursor", "progress");
                window.location.replace("https://howtomanageasmalllawfirm.com/stage-1/");
            });
            jQuery(".quiz #stage-2").click(function(event){
                event.stopImmediatePropagation();
                jQuery("html").css("cursor", "progress");
                window.location.replace("https://howtomanageasmalllawfirm.com/stage-2/");
            });
            jQuery(".quiz #stage-3").click(function(event){
                event.stopImmediatePropagation();
                jQuery("html").css("cursor", "progress");
                window.location.replace("https://howtomanageasmalllawfirm.com/stage-3/");
            });
            jQuery(".quiz #stage-4").click(function(event){
                event.stopImmediatePropagation();
                jQuery("html").css("cursor", "progress");
                window.location.replace("https://howtomanageasmalllawfirm.com/stage-4/");
            });
            jQuery(".quiz #stage-5").click(function(event){
                event.stopImmediatePropagation();
                jQuery("html").css("cursor", "progress");
                window.location.replace("https://howtomanageasmalllawfirm.com/stage-5/");
            });
            jQuery(".quiz #stage-6").click(function(event){
                event.stopImmediatePropagation();
                jQuery("html").css("cursor", "progress");
                window.location.replace("https://howtomanageasmalllawfirm.com/stage-6/");
            });
            */
            jQuery(".submit-quiz button").prop("disabled", true);
            var stage = 0;
            var selected;
            jQuery(".quiz .revenue").change(function(event){
                selected = $(".quiz .revenue input[type='radio']:checked");
                if (selected.length > 0) {
                    stage = selected.val();
                    jQuery(".submit-quiz button").prop("disabled", false);
                }                
            });
            jQuery(".submit-quiz button").click(function(event){
                // event.stopImmediatePropagation();
                jQuery("html").css("cursor", "progress");
                window.location.replace("https://howtomanageasmalllawfirm.com/stage-" + stage + "-quiz/");
            });

            jQuery(".quiz .click-next .custom-control").click(function(){
                // delay scrolling the question so user can see clicked radio button
                setTimeout(() => {
                    jQuery('.quiz').slick('slickNext');
                }, 400);
            });
            jQuery('button.slick-arrow').addClass('fas');
        });
/*     </script> */

    /* ======  Handle the divorce calculator ===== */

    /* --------

    // If tab out of last input, force it back to first input field
    $('#spouse-source').keydown(function(e) {
        var code = e.keyCode || e.which;
        if (code === 9) {  
            e.preventDefault();
            $("#you-reasonable").focus();
        }
    });    

    $("#kids").click( function(event) {
        // show or hide kid section when toggle checkbox
        if ($( "#kids" ).prop( "checked" )) {
            $("#kid-section").animate({
                height: 225
              }, 500, "linear", function() {
                $("#kid-section").height("auto");
              });
        } else {
            $("#kid-section").animate({
                height: 0
              }, 500, "linear");
            $("#num-kids").val("0");
            $("#special-needs").val("");
        }
    });

    $("input[name='your-priority'], input[name='spouse-priority']").click( function(event) {
        // if 'want it all' show call us modal
        var yourPri = $('input[name="your-priority"]:checked').attr('id');
        var spousePri = $('input[name="spouse-priority"]:checked').attr('id');
        if (yourPri == "yp-high" || spousePri == "sp-high") {
            $("#call-now-modal").modal('show');
            event.preventDefault();
        }
    });

    $("#calc-form input, #calc-form select, #calc-form textarea").change( function(event) {
        // delay the calculation a bit so user has chance to notice it
        setTimeout(() => {
            calc_values(event.target);
        }, 100);
    });

    var calc_values = function(changed_element) {

        var yourReasonable = edit_numeric( $("#your-reasonable option:selected").val().trim() );
        var yourPriority = edit_numeric( $('input[name="your-priority"]:checked').val().trim() );
        var yourIncome = edit_numeric( $("#your-income").val().trim() );
        var yourSource = edit_numeric( $("#your-source option:selected").val().trim() );
        var numKids = edit_numeric( $("#num-kids").val().trim() );
        var specialNeeds = $("#special-needs").val().trim();

        var spouseReasonable = edit_numeric( $("#spouse-reasonable option:selected").val().trim() );
        var spousePriority = edit_numeric( $('input[name="spouse-priority"]:checked').val().trim() );
        var spouseIncome = edit_numeric( $("#spouse-income").val().trim() );
        var spouseSource = edit_numeric( $("#spouse-source option:selected").val().trim() );

        var time;
        var cost;
        var alimony;
        var support;

        // time in months
        time = 3 
            + yourReasonable 
            + spouseReasonable 
            + (numKids > 0 ? 3 : 0) 
            + ( (numKids > 0) && (specialNeeds.length > 0) ? 3 : 0)
            + (yourIncome > 1000000 ? 6 : 0)
            + (spouseIncome > 1000000 ? 6 : 0)
            + (yourSource == 1 ? 3 : 0)
            + (spouseSource == 1 ? 3 : 0);

        // priority is a multiplier: 1, 1.5, 2, etc.
        time = time * yourPriority * spousePriority;

        cost = 3000 + (time * 500);

        alimony = yourIncome / 12 / 2;
        alimony = alimony * (spouseIncome > yourIncome ? 0 : 1);
        // priority is a multiplier: 1, 1.5, 2, etc.
        // impact to alimony is fractional
        alimony = alimony * (1 + (spousePriority * 0.1));

        support = numKids * ( (numKids > 0) && (specialNeeds.length > 0) ? 1000 : 500 );

        // Overlay the edited value back into the input field
        var orig_input = $(changed_element);
        if ( orig_input.is( "#your-income" ) ) $("#your-income").val(display_numeric(yourIncome, 0));
        if ( orig_input.is( "#spouse-income" ) ) $("#spouse-income").val(display_numeric(spouseIncome, 0));

        // Display the calc values
        $("#output-time").text( display_numeric(time, 0));
        $("#output-cost").text( display_numeric(cost, 0));
        $("#output-alimony").text( display_numeric(alimony, 0));
        $("#output-childsupport").text( display_numeric(support, 0));

    };

    var edit_numeric = function(the_value) {
        // remove any non-numeric characters except decimal point
        var edited_value = the_value.replace(/[$,a-zA-Z-]+/g,"");
        if ( isNaN(edited_value) || edited_value === "" ) {
            edited_value = 0;
        }
        return parseFloat(edited_value);
    };

    var display_numeric = function(the_value, decimals=0, currency_sym="") {
        // format number for display, using comma and decimal point (US-specific)
        var formatted;
        if (currency_sym == "") {
            formatted = the_value.toFixed(decimals);
        } else {
            formatted = the_value.toLocaleString('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: decimals });
        }
        return formatted;
        
    };

    ----- */
  
  });