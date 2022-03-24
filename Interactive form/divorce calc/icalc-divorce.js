jQuery(document).ready(function( $ ) {

    const showCalculator = function(mutationsList=null, observer=null) {
        $("#entry-form").hide();
        $("#calc-form").show();
        $('html, body').animate({
            scrollTop: ($('#calc-form').offset().top)
         },1500);
         $("#calc-form").animate({
            opacity: 1
          }, 3000, "linear", function() {
            $("#you-reasonable").focus();
          });
    };

    /* ===== Monitor the AC form submission and if successful show calc form and scroll to it ==== */

    const observer = new MutationObserver(showCalculator);
    observer.observe($("._form-thank-you")[0], {childList: true});

    /* ===== Bypass the AC form submission to simplify testing ==== */

    let params = new URLSearchParams(location.search);
    if (params.has('bypass')) showCalculator();
    
    /* ======  Style the ActiveCampaign form ===== */

    $("._form-content input[name='firstname']").attr("placeholder","How your friends call you");
    $("._form-content input[name='lastname']").attr("placeholder","How your teachers called you");
    $("._form-content input[name='email']").attr("placeholder","Top Secret Private Email no one will see");
    $("._form-content input[name='phone']").attr("placeholder","To confirm you are not a robot");
    $("#_form_210_submit").text("START CALCULATING");
    $("._form-content select").removeAttr("multiple");
    
    /* ======  Handle the ActiveCampaign form ===== */

    /* -- Only necessary if processing goal input fields in AC form
    $( "form.form-goals input" ).submit( function( event ) {
        event.preventDefault();
        // Do validation and calculations as necessary
        calc_values();
        //this.submit();
    });
    */

    // Initialize the odometer display
    window.odometerOptions = {
        format: '(,ddd)(.dd)', // Change how digit groups are formatted, and how many digits are shown after the decimal point
        duration: 3500 // Change how long the javascript expects the CSS animation to take
      };

    /* ======  Handle the divorce calculator ===== */

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
  
  });