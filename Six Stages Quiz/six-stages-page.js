jQuery(document).ready(function( $ ) {

    const showStage = function(mutationsList=null, observer=null) {
        $("#challenge-section").hide();
        $(".require-email").show();
        $(".require-email").animate({
            opacity: 1
            }, 1500, "linear");
        // unless a hashtag is specified, scroll to top
        if ( location.hash ) {
            setTimeout( () => {
                document.getElementById(location.hash.slice(1)).scrollIntoView();
                }, 1500);
        } else {
            window.scrollTo(0, 0);
        }

    };

    /* ===== Monitor the AC form submission and if successful show calc form and scroll to it ==== */

    const observer = new MutationObserver(showStage);
    observer.observe($("._form-thank-you")[0], {childList: true});

    /* ===== Bypass the AC form submission to simplify testing ==== */

    let params = new URLSearchParams(location.search);
    if (params.has('bypass')) showStage();
});