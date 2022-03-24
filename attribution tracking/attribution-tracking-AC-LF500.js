<!-- Attribution tracking code starts here -->
<script type="text/javascript">
jQuery(document).ready(function() {

    // Suppress site-wide UTM code for testing changes; remove this code on the page containing updated UTM code
    if (window.location.search.toLowerCase().indexOf('utm-testing') > -1) { 
        return true;
    }

    var UTM_SOURCE = 'lf500_utm_source';
    var UTM_MEDIUM = 'lf500_utm_medium';
    var UTM_CAMPAIGN = 'lf500_utm_campaign';
    var UTM_TERM = 'lf500_utm_term';
    var UTM_CONTENT = 'lf500_utm_content';
    var cookieMaxAge = 60 * 60 * 24 * 365;  // would "remember" the original lead source for up to a year or until overwritten

    if (window.location.search.toLowerCase().indexOf('utm_source') > -1) { 
        // store UTM params in cookies for later use

        // clear all UTM cookies in case some parms were omitted in query string (otherwise previous cookie parms can "bleed through")
        document.cookie = UTM_SOURCE + "= ;path=/ ;samesite=lax ;max-age=-1";
        document.cookie = UTM_MEDIUM + "= ;path=/ ;samesite=lax ;max-age=-1";
        document.cookie = UTM_CAMPAIGN + "= ;path=/ ;samesite=lax ;max-age=-1";
        document.cookie = UTM_TERM + "= ;path=/ ;samesite=lax ;max-age=-1";
        document.cookie = UTM_CONTENT + "= ;path=/ ;samesite=lax ;max-age=-1";
        
        var match;
        var pl           = /\+/g;  // Regex for replacing addition symbol with a space
        var search       = /([^&=]+)=?([^&]*)/g;
        var decode       = function (s) { return decodeURIComponent(s.replace(pl, " ")); };
        var query        = window.location.search.substring(1);

        while (match = search.exec(query))
        {
            document.cookie = 'lf500_' + decode(match[1]) + '=' + decode(match[2]) + " ;path=/ ;samesite=lax ;max-age=" + cookieMaxAge.toString();
        }

    };
    if ( getCookieValue(UTM_SOURCE) ) {
        // define hidden fields for form(s)
        var html_source = '<div class="_form_element _field47 _full_width "><input type="hidden" name="field[47]" value="' + getCookieValue(UTM_SOURCE) + '" data-name="utm_source_latest"></div>';
        var html_medium = '<div class="_form_element _field48 _full_width "><input type="hidden" name="field[48]" value="' + getCookieValue(UTM_MEDIUM) + '" data-name="utm_medium_latest"></div>';
        var html_campaign = '<div class="_form_element _field49 _full_width "><input type="hidden" name="field[49]" value="' + getCookieValue(UTM_CAMPAIGN) + '" data-name="utm_campaign_latest"></div>';
        var html_content = '<div class="_form_element _field50 _full_width "><input type="hidden" name="field[50]" value="' + getCookieValue(UTM_CONTENT) + '" data-name="utm_content_latest"></div>';
        var html_term = '<div class="_form_element _field51 _full_width "><input type="hidden" name="field[51]" value="' + getCookieValue(UTM_TERM) + '" data-name="utm_term_latest"></div>';
        // add hidden UTM fields to any/all ActiveCampaign forms on the page so they can be saved into the contact record
        jQuery('form._form ._form-content').append(html_source);
        jQuery('form._form ._form-content').append(html_medium);
        jQuery('form._form ._form-content').append(html_campaign);
        jQuery('form._form ._form-content').append(html_content);
        jQuery('form._form ._form-content').append(html_term);
    };
    function getCookieValue(cookieName) {
        var b = document.cookie.match('(^|;)\\s*' + cookieName + '\\s*=\\s*([^;]+)');
        return b ? b.pop() : '';
    }
});
</script>
<!-- Attribution tracking code ends here -->