<!-- Attribution tracking code starts here -->
<script type="text/javascript">
jQuery(document).ready(function() {

    // Suppress site-wide UTM code for testing changes; remove this code on the page containing updated UTM code
    if (window.location.search.toLowerCase().indexOf('utm-testing') > -1) { 
        return true;
    }

    var UTM_SOURCE = 'htm_utm_source';
    var UTM_MEDIUM = 'htm_utm_medium';
    var UTM_CAMPAIGN = 'htm_utm_campaign';
    var UTM_TERM = 'htm_utm_term';
    var UTM_CONTENT = 'htm_utm_content';
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
            document.cookie = 'htm_' + decode(match[1]) + '=' + decode(match[2]) + " ;path=/ ;samesite=lax ;max-age=" + cookieMaxAge.toString();
        }

    };
    if ( getCookieValue(UTM_SOURCE) ) {
        // define hidden fields for form(s)
        var html_source = '<div class="_form_element _field76 _full_width "><input type="hidden" name="field[76]" value="' + getCookieValue(UTM_SOURCE) + '" data-name="utm_source_latest"></div>';
        var html_medium = '<div class="_form_element _field77 _full_width "><input type="hidden" name="field[77]" value="' + getCookieValue(UTM_MEDIUM) + '" data-name="utm_medium_latest"></div>';
        var html_campaign = '<div class="_form_element _field78 _full_width "><input type="hidden" name="field[78]" value="' + getCookieValue(UTM_CAMPAIGN) + '" data-name="utm_campaign_latest"></div>';
        var html_content = '<div class="_form_element _field79 _full_width "><input type="hidden" name="field[79]" value="' + getCookieValue(UTM_CONTENT) + '" data-name="utm_content_latest"></div>';
        var html_term = '<div class="_form_element _field80 _full_width "><input type="hidden" name="field[80]" value="' + getCookieValue(UTM_TERM) + '" data-name="utm_term_latest"></div>';
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
    // Store referring URL to help identify attribution for direct visits and mis-configured campaigns
    // Except if field already being used (bootcamp participant pages); just skip it
    if ( jQuery("[data-name='form_originating_url']").length == 0 ) {
        var html_referrer = '<div class="_form_element _field65 _full_width "><input type="hidden" name="field[65]" value="' + document.referrer + '" data-name="form_originating_url"></div>';
        jQuery('form._form ._form-content').append(html_referrer);
    }
});
</script>
<!-- Attribution tracking code ends here -->