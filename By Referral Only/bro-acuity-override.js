/**
 *  Disable Acuity scheduler widget and present the user with the By Referral Only selection page.
 */

(function () {
    // Suppress site-wide acuity disable code to enable testing; remove this code on the page containing updated code
    if (window.location.search.toLowerCase().indexOf('acuity-disable-testing') > -1)  
        return;

    if (window.addEventListener) {
        // For standards-compliant web browsers
        window.addEventListener("load", disableAcuityScheduler, false);
    }
    else {
        window.attachEvent("onload", disableAcuityScheduler);
    }

    function disableAcuityScheduler() {

        // Set click handler on all Acuity forms (technically on the parent container)
        const acuity_schedulers = document.querySelectorAll("iframe[src*='acuityscheduling.com']");

        acuity_schedulers.forEach(function(scheduler){
                
            // Must reset pointer-events so that clicks pass up to the parent container
            scheduler.style.setProperty("pointer-events", "none");

            // Set the handler on the parent container
            if (scheduler.parentElement.addEventListener) {
                scheduler.parentElement.addEventListener("click", popupBro);
            }
            else {
                scheduler.attachEvent("onclick", popupBro);
            }

        })

        // If any schedulers on page, create the pop-up

        const BRO_CONTAINER_ID = "bro-popup-container";
        const BRO_POPUP_DISMISS_ID = "bro-popup-dismiss-container";

        const broContainerSection = 
              '<style>'
            + '#' + BRO_CONTAINER_ID + '{' 
            + '    display: none;'
            + '    background-color: #fff;'
            + '    max-width: 1160px;'
            + '    width: 100vw;'
            + '    z-index: 10000;'
            + '    border: 1px solid #eee;'
            + '    box-shadow: 3px 3px 9px #eee;'
            + '    margin-left: calc((100vw - 1160px) / 2);'            
            + '}'
            + '#' + BRO_CONTAINER_ID + '.show {'
            + '    display: inline-block;'
            + '    visibility: visible;'
            + '    -webkit-animation: fadeIn 1s;'
            + '    animation: fadeIn 1s;'
            + '}'
            + '#' + BRO_CONTAINER_ID + ' .hide {'
            + '    display: none;'
            + '    visibility: hidden;'
            + '    -webkit-animation: fadeIn 1s;'
            + '    animation: fadeIn 1s;'
            + '}'
            + '#bro-popup-dismiss-container {'
            + '    text-align: right; margin-top: 50px; margin-right: 50px;'
            + '}'
            + '#bro-popup-dismiss-container span {'
            + '    right: 100%; font-size: 20px; background-color: transparent; border-radius: 0; padding: .25em .75em; box-shadow: none;'
            + '    border: 2px solid #aaa; color: #aaa;'
            + '}'
            + '#bro-popup-dismiss-container span:hover {'
            + '    color: black;'
            + '}'
            + '@-webkit-keyframes fadeIn {'
            + '    from {opacity: 0;} '
            + '    to {opacity: 1;}'
            + '}'
            + '@keyframes fadeIn {'
            + '    from {opacity: 0;}'
            + '    to {opacity:1 ;}'
            + '}'
            + '</style>'
        ;
        const broIntroSection = 
              '<div id="bro-intro-section" class="avia-section main_color avia-section-default avia-no-border-styling avia-bg-style-scroll  avia-builder-el-22  el_after_av_section  el_before_av_section    container_wrap fullsize" style="background-image: ">'
            + '<p id="' + BRO_POPUP_DISMISS_ID + '"><a href="#"><span >X</span></a></p>'
            + '<div class="container"><div class="template-page content  av-content-full alpha units"><div class="post-entry post-entry-type-page post-entry-56092"><div class="entry-content-wrapper clearfix">' 
            + '<div class="flex_column av_one_full  flex_column_div av-zero-column-padding first  avia-builder-el-23  avia-builder-el-no-sibling  " style="border-radius:0px; "><div style="padding-bottom:10px; color:#a00606;font-size:30px;" class="av-special-heading av-special-heading-h3 custom-color-heading blockquote modern-quote  avia-builder-el-24  el_before_av_heading  avia-builder-el-first  heavy-title first-heading av-inherit-size "><h3 class="av-special-heading-tag  av-mini-font-size-overwrite av-mini-font-size-20" itemprop="headline">NOTICE AUGUST 1, 2021:</h3><div class="special-heading-border"><div class="special-heading-inner-border" style="border-color:#a00606"></div></div></div>' 
            + '<div style="padding-bottom:10px; margin:0 0 0 0; font-size:35px;" class="av-special-heading av-special-heading-h3 custom-color-heading blockquote modern-quote  avia-builder-el-25  el_after_av_heading  el_before_av_textblock  heavy-title av-inherit-size "><h3 class="av-special-heading-tag  av-mini-font-size-overwrite av-mini-font-size-22" itemprop="headline">DUE TO OVERWHELMING DEMAND, AT THIS TIME WE CAN ACCEPT NEW ENGAGEMENTS BY REFERRAL-ONLY.</h3><div class="special-heading-border"><div class="special-heading-inner-border"></div></div></div>' 
            + '<section class="av_textblock_section " itemscope="itemscope" itemtype="https://schema.org/CreativeWork"><div class="avia_textblock title-font av_inherit_color  av-mini-font-size-overwrite av-mini-font-size-17" style="font-size:22px; " itemprop="text"><p style="text-align: left;">If you already know one of our 500 Member Law Firms for which we serve as CEO, COO &amp;/or CFO and you’d like to ask your colleague or friend to make a referral for you, please click <span style="color: #a00606;"><strong><a style="color: #a00606;" href="https://howtomanageasmalllawfirm.com/by-referral-member/">HERE</a></strong></span> to begin that process.</p>' 
            + '<p style="text-align: left;">If you do not yet know one of our Members who can vouch for you, or if you’d like to be introduced to the owner of one of our Member law firms to ask if what we do for them “is really that great” (it is), how their business and their whole life has improved since we stepped-in as a Small Law Firm Management Advisor for their firm, there’s good news for you.</p>' 
            + '</div></section>' 
            + '<div style="padding-bottom:10px; margin-top:35px; font-size:28px;" class="av-special-heading av-special-heading-h3 custom-color-heading blockquote modern-quote  avia-builder-el-27  el_after_av_textblock  el_before_av_textblock  heavy-title av-inherit-size "><h3 class="av-special-heading-tag  av-mini-font-size-overwrite av-mini-font-size-18" itemprop="headline">WE HAVE DOZENS OF SUCCESSFUL LAW FIRM OWNERS  WHO HAVE VOLUNTEERED TO SPEAK WITH YOU.</h3><div class="special-heading-border"><div class="special-heading-inner-border"></div></div></div>' 
            + '<section class="av_textblock_section " itemscope="itemscope" itemtype="https://schema.org/CreativeWork"><div class="avia_textblock title-font av_inherit_color  av-mini-font-size-overwrite av-mini-font-size-17" style="font-size:22px; " itemprop="text"><p style="text-align: left;">Please click <span style="color: #a00606;"><a style="color: #a00606;" href="https://howtomanageasmalllawfirm.com/by-referral-intro/"><strong>HERE</strong></a></span> to begin your journey through the looking glass and then if you like what you hear (you will be salivating) you may ask them to make a referral for you.</p>' 
            + '</div></section>' 
            + '<div style="height:1px" class="hr hr-invisible   avia-builder-el-29  el_after_av_textblock  el_before_av_textblock  "><span class="hr-inner "><span class="hr-inner-style"></span></span></div>' 
            + '<section class="av_textblock_section " itemscope="itemscope" itemtype="https://schema.org/CreativeWork"><div class="avia_textblock heavy-title av_inherit_color  av-mini-font-size-overwrite av-mini-font-size-15" style="font-size:20px; color:#a00606; " itemprop="text"><p style="text-align: left;"><a href="https://howtomanageasmalllawfirm.com/by-referral-only-faq/">FAQ’s Related To This Announcement</a></p>' 
            + '</div></section>' 
            + '<div style="height:30px" class="hr hr-invisible   avia-builder-el-31  el_after_av_textblock  avia-builder-el-last  "><span class="hr-inner "><span class="hr-inner-style"></span></span></div></div>'             
            + '</div></div></div><!-- close content main div --></div></div>'
        ;
        const broButtonSection = 
              '<div id="bro-selection-section" class="avia-section main_color avia-section-small avia-no-border-styling avia-bg-style-scroll  avia-builder-el-32  el_after_av_section  avia-builder-el-last    container_wrap fullsize" style="background-image: "><div class="container"><div class="template-page content  av-content-full alpha units"><div class="post-entry post-entry-type-page post-entry-56092"><div class="entry-content-wrapper clearfix">' 
            + '<section class="avia_codeblock_section  avia_code_block_4" itemscope="itemscope" itemtype="https://schema.org/CreativeWork"><div class="avia_codeblock " itemprop="text"> <style>' 
            + '.heavy-title, .heavy-title .av-special-heading-tag {' 
            + '    font-family: "Montserrat", sans-serif;' 
            + '    font-weight: 800;' 
            + '}' 
            + '#bro-selection-section {' 
            + '    border: 0;' 
            + '}' 
            + '.lp-button span.avia_iconbox_title {' 
            + '    font-weight: 700;' 
            + '    font-family: "Montserrat", sans-serif;' 
            + '}' 
            + '.lp-selection {' 
            + '    border-right: 1px solid #eee;' 
            + '}' 
            + '@media only screen and (max-width: 767px) {' 
            + '.lp-selection {' 
            + '    border-right: none;' 
            + '}' 
            + '}' 
            + '</style> </div></section>' 
            + '<div class="flex_column av_one_full  flex_column_div av-zero-column-padding first  avia-builder-el-34  el_after_av_codeblock  el_before_av_one_half  " style="border-radius:0px; "><div style="padding-bottom:10px; color:#4f5c64;font-size:40px;" class="av-special-heading av-special-heading-h3 custom-color-heading blockquote modern-quote modern-centered  avia-builder-el-35  el_before_av_hr  avia-builder-el-first  heavy-title av-inherit-size "><h3 class="av-special-heading-tag  av-mini-font-size-overwrite av-mini-font-size-22" itemprop="headline">PLEASE SELECT ONE</h3><div class="special-heading-border"><div class="special-heading-inner-border" style="border-color:#4f5c64"></div></div></div>' 
            + '<div style=" margin-top:10px; margin-bottom:29px;" class="hr hr-custom hr-center hr-icon-no   avia-builder-el-36  el_after_av_heading  avia-builder-el-last  "><span class="hr-inner   inner-border-av-border-thin" style=" width:25%; border-color:#1c1c1c;"><span class="hr-inner-style"></span></span></div></div><div class="flex_column av_one_half  flex_column_div first  avia-builder-el-37  el_after_av_one_full  el_before_av_one_half   column-top-margin" style="margin-top:30px; border-radius:0px; "><div class="avia-button-wrap avia-button-center  avia-builder-el-38  avia-builder-el-no-sibling  lp-button"><a href="https://howtomanageasmalllawfirm.com/by-referral-member/" class="avia-button avia-button-fullwidth   avia-icon_select-no avia-color-theme-color " style="color:#ffffff; "><span class="avia_iconbox_title">I Already Know A Member of HTM</span><span class="avia_button_background avia-button avia-button-fullwidth avia-color-theme-color"></span></a></div></div><div class="flex_column av_one_half  flex_column_div av-zero-column-padding   avia-builder-el-39  el_after_av_one_half  el_before_av_hr  column-top-margin" style="margin-top:30px; border-radius:0px; "><div class="avia-button-wrap avia-button-center  avia-builder-el-40  avia-builder-el-no-sibling  lp-button"><a href="https://howtomanageasmalllawfirm.com/by-referral-intro/" class="avia-button avia-button-fullwidth   avia-icon_select-no avia-color-theme-color " style="color:#ffffff; "><span class="avia_iconbox_title">I Don’t Know A Member of HTM</span><span class="avia_button_background avia-button avia-button-fullwidth avia-color-theme-color"></span></a></div></div><div style="height:50px" class="hr hr-invisible   avia-builder-el-41  el_after_av_one_half  avia-builder-el-last  "><span class="hr-inner "><span class="hr-inner-style"></span></span></div>' 
            + '</div></div></div><!-- close content main div --> <!-- section close by builder template -->		</div><!--end builder template--></div>'
        ;
        const popupHtml = broContainerSection + broIntroSection + broButtonSection;

        if (acuity_schedulers) {
            const placeholder = document.createElement('div');
            placeholder.id = BRO_CONTAINER_ID
            placeholder.innerHTML = popupHtml;

            // insert the div in the standard body section for the theme so the default styles inherit properly
            let parentElement = document.getElementById("main");
            let theFirstChild = parentElement.firstChild;
            parentElement.insertBefore(placeholder, theFirstChild);
            var popupElement = placeholder.firstElementChild;

            // Set the handler on the popup dismiss button
            const exitButton = document.querySelector("#" + BRO_CONTAINER_ID + " span");
            if (exitButton.addEventListener) {
                exitButton.addEventListener("click", popupBroDismiss);
            }
            else {
                exitButton.attachEvent("onclick", popupBroDismiss);
            }
            
        }

        // On click, display pop-up for BRO
        function popupBro() {

            if (typeof popupElement !== "undefined") {
                let popupContainer = document.getElementById(BRO_CONTAINER_ID);
                // Adjust left margin if offscreen (usually on mobile); margin will be negative
                let popupStyle = popupContainer.currentStyle || window.getComputedStyle(popupContainer);
                if ( popupStyle.marginLeft.slice(0, 1) == "-" ) {
                    popupContainer.style.marginLeft = 0;
                }
                popupContainer.classList.add("show");
                window.scrollTo(0, 0);
            }
            return;
        }

        // On click, hide pop-up for BRO
        function popupBroDismiss() {

            let popupContainer = document.getElementById(BRO_CONTAINER_ID);
            popupContainer.classList.remove("show");
            popupContainer.classList.add("hide");

            return;
        }


    }

})();