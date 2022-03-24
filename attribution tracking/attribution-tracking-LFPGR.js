<!-- Supplemental attribution tracking code for lawfirmpandemicgrowthresources.com starts here -->
<script type="text/javascript">
jQuery(document).ready(function() {

    // Suppress site-wide UTM code for testing changes; remove this code on the page containing updated UTM code
    if (window.location.search.toLowerCase().indexOf('utm-pgr-testing') > -1) { 
        return true;
    }
    // This is supplemental code to the standard attribution tracking script.
    // Append any query string parameters onto the outbound link of each resource.
    // Necessary so that we can retain the UTM params that hit the LFPGR home page.
    // Because cookies set in this domain won't be available in the destination domains of the resource links.

    var the_query_string = window.location.search.substring(1);

    jQuery("[href*='htm_query_string']").each(function(idx, elem) {
        var new_href=jQuery(elem).attr('href').replace(/htm_query_string/gi, the_query_string );
        jQuery(elem).attr('href', new_href);
    })

});
</script>
<!-- Supplemental attribution tracking code for lawfirmpandemicgrowthresources.com ends here -->