
jQuery(document).ready(function( $ ) {

    /* ===== Monitor the AC form submission and if successful show calc form and scroll to it ==== */

    // ### TODO:  NEED TO UPDATE OBSERVER CODE FOR PROPER SELECTORS

    const observer = new MutationObserver(function(mutationsList, observer) {
        $("#divorce-calc").show();
        $('html, body').animate({
           scrollTop: ($('#divorce-calc').offset().top)
        },1500);
        $("#divorce-calc input#inputIncome").focus();
    });
    observer.observe($("._form-thank-you")[0], {childList: true});
    
    //$("._form-content select").removeAttr("multiple");  // only necessary for ActiveCampaign forms
    
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
    $('#divorce-calc #inputHours').keydown(function(e) {
        var code = e.keyCode || e.which;
        if (code === 9) {  
            e.preventDefault();
            $("#divorce-calc input#inputIncome").focus();
        }
    });    

    $("#divorce-calc input").change( function(event) {
        // force default jQuery form validation
        //$("#divorce-calc button").prop('disabled', false);
        //$("#divorce-calc button").click();
        $("#divorce-calc button").prop('disabled', true);
        setTimeout(() => {
            calc_values(event.target);
        }, 10);
    });

    var calc_values = function(changed_element) {
  
          var income = edit_numeric( $("#divorce-calc #inputIncome").val().trim() );
          var margin = edit_numeric( $("#divorce-calc #inputMargin").val().trim() );
          var weeks = edit_numeric( $("#divorce-calc #inputWeeks").val().trim() );
          var hours = edit_numeric( $("#divorce-calc #inputHours").val().trim() );

          var annualRevenue;
          var weeklyRevenue;
          var hourlyRate;

            if (margin == 0) {
                annualRevenue = 0;
            } else {
                annualRevenue = income / margin * 100;
            }
            if ( weeks > 52 ) {
                weeklyRevenue = 0;
            } else {
                weeklyRevenue = annualRevenue / (52 - weeks);
            }
            if ( hours == 0 ) {
                hourlyRate = 0;
            } else {
                hourlyRate = weeklyRevenue / hours;
            }

          // Overlay the edited value back into the input field
          var orig_input = $(changed_element);
          if ( orig_input.is( "#divorce-calc #inputIncome" ) ) $("#divorce-calc #inputIncome").val(display_numeric(income, 0));
          if ( orig_input.is( "#divorce-calc #inputMargin" ) ) $("#divorce-calc #inputMargin").val(display_numeric(margin, 0));
          if ( orig_input.is( "#divorce-calc #inputWeeks" ) ) $("#divorce-calc #inputWeeks").val(display_numeric(weeks, 0));
          if ( orig_input.is( "#divorce-calc #inputHours" ) ) $("#divorce-calc #inputHours").val(display_numeric(hours, 0));

          // Display the calc values
          $("#divorce-calc #outputAnnualRevenue").text( display_numeric(annualRevenue, 0));
          $("#divorce-calc #outputWeeklyRevenue").text( display_numeric(weeklyRevenue, 0));
          $("#divorce-calc #outputHourlyRate").text( display_numeric(hourlyRate, 2));
        /*
        $("#divorce-calc #outputAnnualRevenue").text( annualRevenue);
        $("#divorce-calc #outputWeeklyRevenue").text( weeklyRevenue);
        $("#divorce-calc #outputHourlyRate").text( hourlyRate);
        */

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
