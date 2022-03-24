<script type="text/javascript">
	jQuery(document).ready(function() {

        // get amount value from shortcode
        var current_amt = jQuery("span.htmac-contacts").text();
        current_amt = parseInt(current_amt) * 47;
        // set amount value in thermometer
        jQuery("div.fill p").text("$" + current_amt);
        // set thermometer level
        var pct = (current_amt / 10000) * 100;
        jQuery("div.fill").css("width", pct.toString()+"%" );
		
    })
</script>