jQuery(document).ready(function() {
    jQuery('.quiz').slick({
        dots: true,
        draggable: true,
        swipe: true,
        customPaging: function(slider, i) {
            var thumb = jQuery(slider.$slides[i]).data();
            return '<a>' + (i + 1) + '</a>';
        }
    });
    /* ===== Only submit quiz if all questions answered ==== */
    jQuery(".submit-quiz button").prop("disabled", true);
    var stage = 0;
    var selected;
    var ansCurrentSituation;
    var ansChallenge;
    var ansIdealOutcome;
    var ansDrivesMe;
    var ansRevenue;

    jQuery(".quiz").change(function(event) {
        ansCurrentSituation = jQuery('input[name="answer-current-situation"]:checked').parent().find('label').text();
        ansChallenge = jQuery('input[name="answer-challenge"]:checked').parent().find('label').text();
        ansIdealOutcome = jQuery('input[name="answer-ideal-outcome"]:checked').parent().find('label').text();
        ansDrivesMe = jQuery('input[name="answer-drives-me"]:checked').parent().find('label').text();
        ansRevenue = jQuery('input[name="answer-revenue"]:checked').parent().find('label').text();

        if (ansCurrentSituation.length > 0 &&
            ansChallenge.length > 0 &&
            ansIdealOutcome.length > 0 &&
            ansDrivesMe.length > 0 &&
            ansRevenue.length > 0) {

            selected = jQuery(".quiz .revenue input[type='radio']:checked");
            if (selected.length > 0) {
                stage = selected.val();
            }
            jQuery(".submit-quiz button").prop("disabled", false);
        }

    });


    jQuery(".submit-quiz button").click(function(event) {
        jQuery("#six-stages-quiz-section").hide();
        jQuery("#result-header-section").show(500);
        jQuery("#result-section").show(500);
        let result_stage_section = ".result-" + stage;
        jQuery(result_stage_section).show(500);
        jQuery('html, body').animate({
                scrollTop: jQuery("#result-header-section").offset().top,
            },
            500,
            'linear'
        )
        storeAnswers();
        storePageUrl();
        jQuery(result_stage_section + " input[name='firstname']").focus();
    });

    jQuery(".quiz .click-next .custom-control").click(function() {
        // delay scrolling the question so user can see clicked radio button
        setTimeout(() => {
            jQuery('.quiz').slick('slickNext');
        }, 400);
    });
    jQuery('button.slick-arrow').addClass('fas');


    /* ===== Monitor the AC form submissions for all 6 stages and if any successful go to stage page ==== */

    const showStage = function(mutationsList = null, observer = null) {
        jQuery(".form-frame p").hide();
        let target_page = "https://howtomanageasmalllawfirm.com/stage-" + stage + "-quiz/?bypass=true";
        window.location.href = target_page;
    };
    const observer = new MutationObserver(showStage);

    jQuery("._form-thank-you").each(function(idx) {
        observer.observe(this, { childList: true });
    })

    /* ===== Load the answers into hidden form fields ==== */

    const storeAnswers = function() {

        // define hidden fields for form(s)
        let form_ansCurrentSituation = '<div class="_form_element _field151 _full_width "><input type="hidden" name="field[151]" value="' + ansCurrentSituation + '" data-name="six_stages_quiz_my_current_situation"></div>';
        let form_ansChallenge = '<div class="_form_element _field152 _full_width "><input type="hidden" name="field[152]" value="' + ansChallenge + '" data-name="six_stages_quiz_my_challenge"></div>';
        let form_ansDrivesMe = '<div class="_form_element _field154 _full_width "><input type="hidden" name="field[154]" value="' + ansDrivesMe + '" data-name="six_stages_quiz_what_drives_me"></div>';
        let form_ansIdealOutcome = '<div class="_form_element _field153 _full_width "><input type="hidden" name="field[153]" value="' + ansIdealOutcome + '" data-name="six_stages_quiz_my_ideal_outcome"></div>';
        let form_ansRevenue = '<div class="_form_element _field155 _full_width "><input type="hidden" name="field[155]" value="' + ansRevenue + '" data-name="six_stages_quiz_my_annual_revenue"></div>';

        // add hidden fields to any/all ActiveCampaign forms on the page so they can be saved into the contact record
        jQuery('form._form ._form-content').append(form_ansCurrentSituation);
        jQuery('form._form ._form-content').append(form_ansChallenge);
        jQuery('form._form ._form-content').append(form_ansDrivesMe);
        jQuery('form._form ._form-content').append(form_ansIdealOutcome);
        jQuery('form._form ._form-content').append(form_ansRevenue);

    }

    /* ===== Load the page URL into hidden form field for use in ActiveCampaign automation ==== */

    const storePageUrl = function() {

        let pageUrl = window.location.href;

        // define hidden fields for form(s)
        let form_quizUrl = '<div class="_form_element _field157 _full_width "><input type="hidden" name="field[157]" value="' + pageUrl + '" data-name="six_stages_quiz_referring_url"></div>';

        // add hidden field to any/all ActiveCampaign forms on the page so they can be saved into the contact record
        jQuery('form._form ._form-content').append(form_quizUrl);

    }
});