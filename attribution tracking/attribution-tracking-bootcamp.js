    //* -- Begin bootcamp attribution tracking -- */

    document.addEventListener('DOMContentLoaded', function() {

        // Suppress site-wide bootcamp tracking code (if used) for testing changes; remove this code on the page containing updated code
        if (window.location.search.toLowerCase().indexOf('bootcamp-testing') > -1) { 
            return true;
        }

        var UTM_SOURCE = 'htm_utm_source';
        var UTM_MEDIUM = 'htm_utm_medium';
        var UTM_CAMPAIGN = 'htm_utm_campaign';
        var UTM_TERM = 'htm_utm_term';
        var UTM_CONTENT = 'htm_utm_content';

        var utm_params = {
            'utm_source': '',
            'utm_medium': '',
            'utm_campaign': '',
            'utm_content': '',
            'utm_term': '',
        };

        // Get best source for UTM parameters
        if (window.location.search.toLowerCase().indexOf('utm_source') > -1) {
            utm_params = parseUtm(utm_params, window.location.search);
        } else {
            if (getCookieValue(UTM_SOURCE)) {
                utm_params['utm_source'] = getCookieValue(UTM_SOURCE);
                utm_params['utm_medium'] = getCookieValue(UTM_MEDIUM);
                utm_params['utm_campaign'] = getCookieValue(UTM_CAMPAIGN);
                utm_params['utm_content'] = getCookieValue(UTM_CONTENT);
                utm_params['utm_term'] = getCookieValue(UTM_TERM);
            } else {
                if (document.referrer.trim()) {
                    utm_params['utm_source'] = 'referrer';
                    utm_params['utm_medium'] = 'website';
                    utm_params['utm_campaign'] = encodeURIComponent(document.referrer);
                    utm_params['utm_content'] = '';
                    utm_params['utm_term'] = '';
                } else {
                    utm_params['utm_source'] = 'direct';
                    utm_params['utm_medium'] = 'website';
                    utm_params['utm_campaign'] = encodeURIComponent(window.location.href);
                    utm_params['utm_content'] = '';
                    utm_params['utm_term'] = '';
                }
            }
        }
        // Prep the bootcamp query string
        var bootcamp_param = '';
        for (const term in utm_params) {
            // Infusionsoft form is strict about certain characters; remove valid URL chars that are on the "unwise/unsafe" list
            if (utm_params[term] == null) utm_params[term] = "";
            bootcamp_param = bootcamp_param + '&' + term + '=' + utm_params[term].replace(/[{}\|\\\^\[\]`]/g, "");;
        }
        bootcamp_param = '?' + bootcamp_param.substring(1);

        // const bootcamp_src = 'education.infusionsoft.com/app/orderForms/Business-Plan-Boot-Camp-4-Week-Program';
        const bootcamp_src = 'education.infusionsoft';
        var bootcamp_src_utm;

        // Append the bootcamp query string on any bootcamp iframes
        jQuery('a').map(function(idx, obj) {
            if ( jQuery(obj).attr('href') && ( jQuery(obj).attr('href').toLowerCase().includes(bootcamp_src.toLowerCase()) ) ) {
                bootcamp_src_utm = jQuery(obj).attr('href') + bootcamp_param;
                jQuery(obj).attr('href', bootcamp_src_utm);
            }
        });

        function getCookieValue(cookieName) {
            var b = document.cookie.match('(^|;)\\s*' + cookieName + '\\s*=\\s*([^;]+)');
            return b ? b.pop() : '';
        }
        function parseUtm(utm_params, param_string) {
            const urlParams = new URLSearchParams(param_string);
    
            for (const term in utm_params) {
                urlParams.get(term) == null ? utm_params[term] = "" : utm_params[term] = urlParams.get(term);
            }
            return utm_params;
        }
    
    });


    //* -- End bootcamp attribution tracking  */