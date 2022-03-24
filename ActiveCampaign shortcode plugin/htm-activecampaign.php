<?php

/*
Plugin Name:  HTM-ActiveCampaign
Version: 1.0
Description: Simple WP access to HTM ActiveCampaign accounts.  Allows AC data retrieval into posts/pages via shortcodes.
Author: Damian Davila
Author URI: https://www.moventisusa.com/
License: GPLv2 or later
License URI: https://www.gnu.org/licenses/gpl-2.0.html
Text Domain: htmac
*/

/**
 * Shortcode [htmac_contacts] returns contact records from AC based on a list and/or a tag and/or a segment.
 * @return array list of contacts
 * -OR-
 * @return string count of contacts
 * 
 * Parameters to be passed in on shortcode attributes:
 * 
 * $ac_account:     the AC account, either "LF500" or "HTMASLF"
 * $count_only:     True/False - return count of retrieved records or actual records
 * $list_id:        the numeric list ID, not the name, of the AC list from which to retrieve contacts
 * $tag_name:       the tag name used to select contacts
 * $segment_id:     the numeric segment ID from which to retrieve contacts
 * 
 * API details at https://www.activecampaign.com/api/example.php?call=contact_list
 * 
 */

add_shortcode( 'htmac_contacts', 'htmac_retrieve_contacts' );

function htmac_retrieve_contacts($atts) {

    $params = shortcode_atts( array(
        'account' => 'LF500',
        'countonly' => 'True',
        'listid' => '',
        'tagname' => '',
        'segmentid' => ''
        ), $atts );

    $ac_account = esc_attr($params['account']);
    $count_only = esc_attr($params['countonly']);
    $list_id = esc_attr($params['listid']);
    $tag_name = esc_attr($params['tagname']);
    $tag_name_encoded =  urlencode($tag_name);
    $segment_id = esc_attr($params['segmentid']);
        
        
    if ($ac_account == "LF500") {
        define("ACTIVECAMPAIGN_URL", "https://lawfirm500.api-us1.com");
        define("ACTIVECAMPAIGN_API_KEY", "GET THIS FROM THE AC DEVELOPER CONSOLE");
    } else {
        define("ACTIVECAMPAIGN_URL", "https://howtomanage.api-us1.com");
        define("ACTIVECAMPAIGN_API_KEY", "GET THIS FROM THE AC DEVELOPER CONSOLE");
    }
    require_once("includes/ActiveCampaign.class.php");

	$ac = new ActiveCampaign(ACTIVECAMPAIGN_URL, ACTIVECAMPAIGN_API_KEY);

	/*
	 * Test API Credentials
	 */

	if (!(int)$ac->credentials_test()) {
		echo "<p>Access denied: Invalid credentials (URL and/or API key).</p>";
		exit();
	}
	
	/*
	 * Retrieve contacts in given list and/or with given tag name and/or with given segment
	 */

    $api_url_contact = "contact/list?full=0";

    if ($list_id != null) {
        $api_url_contact .= "&filters[listid]={$list_id}";
    }
    if ($tag_name_encoded != null ) {
        $api_url_contact .= "&filters[tagname]={$tag_name_encoded}";
    } 
    if ($segment_id != null) {
        $api_url_contact .= "&filters[segmentid]={$segment_id}";
    }
    $ac->version(1);

    /**
     * Extract contact records from result object. Contacts are stored as embedded objects:
     * 
     *      result(Object) { <numeric key, ascending from 0> => { 'id'=>'contact id', ...} } 
     * 
     * Note: results limited to 20 contacts per request. Must do manual paging.
     */
    $max_returned_contacts = 20;
    $max_contacts = 200;
    $max_pages = $max_contacts / $max_returned_contacts;
    $contacts_list = [];

    for ($page = 1; $page <= $max_pages; $page++) {
        $contacts_on_pg = 0;
        $contacts_object = $ac->api($api_url_contact . "&page=" . $page);
    
        foreach($contacts_object as $key => $contact) {
            if (property_exists($contact, "id")) {
                array_push($contacts_list, $contact);
                $contacts_on_pg++;
            }
        }
        // if partial or empty result set, then reached the end
        if ($contacts_on_pg < $max_returned_contacts) {
            break;
        }
    }


    if (strtolower($count_only) == "true") {
        return "<span class='htmac-contacts'>" . count($contacts_list) . "</span>";
    } else {
        return "<p class='htmac-contacts'>" . json_encode($contacts_list) . "</p>";
    }

}

?>