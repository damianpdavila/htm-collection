<?php

/**
 * Standalone full-page usage of the shortcode plugin code.  
 * Intended to be used in an iframe on a client page as an easy way to make the AC call non-blocking.
 * Otherwise, if use the shortcode in the client page, the page will block on the thermometer because the AC calls take so long.
 * 
 */

?>
<!DOCTYPE html>
<html lang=en>
    <head>
        <meta charset="utf-8">
    </head>
    <body>
    <style>
    html {
        overflow: hidden;
        background-color: #fff;
    }
    .thermometer {
        padding: 3px;
        border: 2px solid #ddd;
        border-radius: 25px;
    }
    .box {
    background: linear-gradient(to top, #eee 30%, #ccc);
    height: 30px;
    position: relative;
    width: 100%;
    border-radius: 25px;
    }
    .box.fixed {
        width: 600px;
    }
    .box:before {
        background: linear-gradient(to right, 
    transparent 0%, transparent 10%, 
    #999 10%, #999 10.5%, 
    transparent 10.5%, transparent 20%, 
    #999 20%, #999 20.5%, 
    transparent 20.5%, transparent 30%, 
    #999 30%, #999 30.5%, 
    transparent 30.5%, transparent 40%, 
    #999 40%, #999 40.5%, 
    transparent 40.5%, transparent 50%, 
    #999 50%, #999 50.5%, 
    transparent 50.5%, transparent 60%, 
    #999 60%, #999 60.5%, 
    transparent 60.5%, transparent 70%, 
    #999 70%, #999 70.5%, 
    transparent 70.5%, transparent 80%, 
    #999 80%, #999 80.5%, 
    transparent 80.5%, transparent 90%, 
    #999 90%, #999 90.5%, 
    transparent 90.5%);
        content: "";
        height: 60%;
        left: -.5%;
        position: absolute;
        top: 20%;
        width: 100%;
    }
    .fill {
        background: rgba(255, 0, 0, .75);
        height: 100%;
        left: 0;
        position: absolute;
        top: 0;
        z-index: 1;
        border-radius: 25px 0 0 25px;
        text-align: right;
    }
    .fill p {
        color: #fff;
        margin: .4em .1em;
        display: inline-block;
        text-shadow: 1px 1px 2px #000;
    }
    .thermometer .tick-values span {
        position: absolute;
        font-weight: 400;
        font-family: Arial, Helvetica, sans-serif;
        font-size: 14px;
        color: #fff;
        text-shadow: 1px 1px 3px #000;
        transform: rotate(45deg);
        transform-origin: 0px 10px;
    }
    .thermometer .tick-values span:nth-child(1) {
        left: 20%;
    }
    .thermometer .tick-values span:nth-child(2) {
        left: 40%;
    }
    .thermometer .tick-values span:nth-child(3) {
        left: 60%;
    }
    .thermometer .tick-values span:nth-child(4) {
        left: 80%;
    }
    .thermometer .tick-values span:nth-child(5) {
        left: 100%;
    }
    </style>
    <div class="thermometer">
        <div class="box">
            <?php 
                $args = array(
                    'account' => 'LF500',
                    'countonly' => 'True',
                    'listid' => '17',
                    'tagname' => '2020 Law Firm 500 Ticket Purchased',
                    'segmentid' => ''
                );
                $sale_value = 47;
                $sales_goal = 10000;
                $sales_cnt = htmac_retrieve_contacts($args);
                $sales_amt = $sales_cnt * $sale_value;
                $sales_pct = $sales_amt/$sales_goal > 1 ? 100 : $sales_amt/$sales_goal*100;
                echo '<div class="fill" style="width: ' . $sales_pct . '%">';
                echo '<p>$' . $sales_amt . '</p>';
                echo '</div>';
            ?>
        </div>
        <div class="tick-values">
            <span>2,000</span>
            <span>4,000</span>
            <span>6,000</span>
            <span>8,000</span>
            <span>10,000</span>
        </div>
    </div>
    </body>
</html>
<?php

/**
 * Function htmac_retrieve_contacts returns contact records from AC based on a list and/or a tag and/or a segment.
 * @return array list of contacts
 * -OR-
 * @return string count of contacts
 * 
 * Parameters to be passed in :
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

function htmac_retrieve_contacts($params) {

    // 7Dec2020:  After event so disabling; remove these returns when ready to re-enable
    return 134;
    // *


    $ac_account = htmlspecialchars($params['account']);
    $count_only = htmlspecialchars($params['countonly']);
    $list_id = htmlspecialchars($params['listid']);
    $tag_name = htmlspecialchars($params['tagname']);
    $tag_name_encoded =  urlencode($tag_name);
    $segment_id = htmlspecialchars($params['segmentid']);
        
        
    if ($ac_account == "LF500") {
        define("ACTIVECAMPAIGN_URL", "https://lawfirm500.api-us1.com");
        define("ACTIVECAMPAIGN_API_KEY", "ACAPIHERE");
    } else {
        define("ACTIVECAMPAIGN_URL", "https://howtomanage.api-us1.com");
        define("ACTIVECAMPAIGN_API_KEY", "ACAPIHERE");    
    }
    require_once("wp-content/plugins/htm-activecampaign/includes/ActiveCampaign.class.php");

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
            if (is_object($contact) && property_exists($contact, "id")) {
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
        return count($contacts_list);
    } else {
        return "<p class='htmac-contacts'>" . json_encode($contacts_list) . "</p>";
    }

}

?>