<!-- AC form validation code starts here -->
<script type="text/javascript">
jQuery(document).ready(function($) {

    // Suppress site-wide validation code for testing changes; remove this code on the page containing updated UTM code
    if (window.location.search.toLowerCase().indexOf('acv-testing') > -1) { 
        return true;
    }

    // hook any forms with website-address field; 
    // note originally tried hooking submit event but couldn't get it to stop submitting due to AC quirk
    $("input[data-name='website_address']").parents('form').find('button._submit').click( function(event) {
        
        let acv_url = $(this).parents('form').find('input[data-name="website_address"]').val().trim();

        if (acv_url && !isValidUrl(acv_url) ) {
            event.stopImmediatePropagation();
            event.preventDefault();
            alert("Oops, you should enter your WEBSITE address here, e.g., www.mylawoffice.com");
            $(this).parents('form').find('input[data-name="website_address"]').css("border", "4px solid #f37c7b").val("").focus();
        }

    });

    function isValidUrl(string) {

        if (string && string.length > 1 && !string.toLowerCase().startsWith("http")  ) {
            string = 'http:' + string; //dummy protocol so that URL constructor works
        }
        try {
          new URL(string);
        } catch (_) {
          return false;  
        }
      
        return true;
    }

});
</script>
<!-- AC form validation code ends here -->