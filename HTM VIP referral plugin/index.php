<?php

/**
 * Plugin Name: HTM VIP Referral Helper
 * Description: Saves referral member data and returns referral data to /vipreferral/{active_campaign_contact_id}/ URI
  * Version: 0.2
 */
global $HTMReferralHelper;

class HTMReferralHelper {

    protected
            $defaultReferrer = 6625;

    const
            OPTION_REFERRAL_MEMBER_PREFIX = 'referral_member_';

    public function __construct() {
        if (is_admin()) {
            return;
        }
        add_action('init', array($this, 'init'));
    }

    public function init() {
        $this->maybeSaveReferralMember();
//        add_action('template_redirect', array($this, 'templateRedirect'));
        add_filter('wp_kses_allowed_html', array($this, 'wpKsesAllowedHTML'), 10, 2);
        add_shortcode('referral_member', array($this, 'shortcode'));
        add_shortcode('referral_guest', array($this, 'shortcodeGuest'));
    }

    /**
     * ?r=m&e=genius%40a2m3.com&f=Genius&l=Prodigy&id=941
     */
    public function maybeSaveReferralMember() {

        $referral = filter_input(INPUT_GET, 'r');
        $email = filter_input(INPUT_GET, 'e');
        $firstName = filter_input(INPUT_GET, 'f');
        $lastName = filter_input(INPUT_GET, 'l');
        $activeCampaignId = (int) filter_input(INPUT_GET, 'id');
        if ($referral !== 'm') {
            return;
        }
        $member = array(
            'id' => $activeCampaignId,
            'firstname' => $firstName,
            'lastname' => $lastName,
            'email' => $email,
        );
        $this->saveReferralMember($member);
    }

    public function loadReferralMember($id) {
        $json = json_decode(get_option($this->optionReferral($id)));
        return ((is_object($json)) ? $json : null);
    }

    public function saveReferralMember(array $struct) {
        $data = (object) $struct;
        if (!(int) $data->id) {
            return;
        }
        update_option($this->optionReferral($data->id), json_encode($data));
    }

    public function wpKsesAllowedHTML($allowedposttags, $context) {
        if ($context == 'post') {
            $allowedposttags['input']['value'] = 1;
            $allowedposttags['iframe']['src'] = 1;
        }
        return $allowedposttags;
    }

    public function shortcode($atts) {
        $param = (object) shortcode_atts(array(
                    'var' => null,
                        ), $atts);

        $id = $this->locateReferrerId();
        if ($id === null) {
            $id = (int) filter_input(INPUT_GET, 'id');
        }
        if($id === 0) {
            $id = $this->defaultReferrer();
        }
        $referringMember = $this->loadReferralMember($id);
        if ($referringMember === null) {
            return;
        }
        switch ($param->var) {
            case 'id':
                $output = (int) $referringMember->id;
                break;
            case 'firstname':
                $output = $referringMember->firstname;
                break;
            case 'lastname':
                $output = $referringMember->lastname;
                break;
            case 'email':
                $output = $referringMember->email;
                break;
            default:
                $output = null;
        }

        return esc_html($output);
    }

    public function shortcodeGuest($atts) {
        $param = (object) shortcode_atts(array(
                    'var' => null,
                        ), $atts);

        $output = filter_input(INPUT_GET, $param->var);

        return esc_html($output);
    }

    public function templateRedirect() {

        $isVIPReferralURI = preg_match('/\/vipreferral\//', getenv('REQUEST_URI'));
//        if ((!is_404()) || (!$isVIPReferralURI)) {
        if (!$isVIPReferralURI) {
            return;
        }

        global $post;
        preg_match('/\/vipreferral\/([0-9]+){1,}\/?/', getenv('REQUEST_URI'), $parts);
        $activeCampaignSubscriberId = (( (isset($parts[1])) ) ? (int) $parts[1] : 0);
        wp_die('<pre>' . print_r($activeCampaignSubscriberId, 1) . '</pre><pre>' . print_r($post, 1) . '</pre><pre>' . print_r($parts, 1) . '</pre>');
    }

    protected function defaultReferrer() {
        return $this->defaultReferrer;
    }

    protected function locateReferrerId() {
        $isVIPReferralURI = preg_match('/\/vipreferral\//', getenv('REQUEST_URI'));
        if (!$isVIPReferralURI) {
            return;
        }
        preg_match('/\/vipreferral\/([0-9]+){1,}\/?/', getenv('REQUEST_URI'), $parts);
        return (( (isset($parts[1])) ) ? (int) $parts[1] : 0);
    }

    protected function optionReferral($id) {
        return self::OPTION_REFERRAL_MEMBER_PREFIX . $id;
    }

}

$HTMReferralHelper = new HTMReferralHelper();
