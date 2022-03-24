// Star Wars intro.

/* Determine the type of device because certain animations don't work on iOS/Mac/Safari */
/* Suppress intro on reload (since it takes so long) */
/* Key classes:
   NoScroll - suppress entire sequence
   PartialScroll - show scroll, suppress intro and logo (doesn't work in WebKit browsers for whatever reason)
   FullScroll - show all 3

   ### Not relevant to Star Wars intro per se, but part of initial implementation: 
   Hide the bonus download until after a set period of time
   Also set whether pre-show, during show, or after show 
*/

jQuery(function(){

    var now = new Date();
    var show_start = new Date("Aug 8 2019 15:00:00 GMT-0400");
    var show_end = new Date("Aug 8 2019 23:59:59 GMT-0400");

    console.info("Currently: " + now);

    if (now >= show_start && now < show_end) {
        document.body.classList.add("during-show");
    }
    else if (now < show_start) {
        document.body.classList.add("preshow");
    }
    else if (now >= show_end) {
        document.body.classList.add("after-show");
    }
    
    var afterShowDownloadTimeout = 0;
    var showScrollIntro = true;

    if (performance.navigation.type == 1) {
       // reloaded so skip 
        console.info( "This page is reloaded" );
        document.body.classList.add("NoScroll");
        afterShowDownloadTimeout = 10;
        showScrollIntro = false;
    } 
    else {
        console.info( "This page is not reloaded");
        afterShowDownloadTimeout = 2700000;  // time in milliseconds
    }

    if (showScrollIntro) {
        console.info( "showScrollIntro true: " + showScrollIntro);
        // Set body class per device type
        if (navigator.userAgent.indexOf("iPhone") != -1  ||
            navigator.userAgent.indexOf("Macintosh") != -1 ||
            navigator.userAgent.indexOf("iPad") != -1 ||
            navigator.userAgent.indexOf("Android") != -1 ) {
                document.body.classList.add("PartialScroll");
        }
        else {
            document.body.classList.add("FullScroll");
        }
    }

    // Initially hide the element
    document.querySelector(".after-show-download").style.visibility = "hidden";
    // Timeout is in milliseconds => 1 hr == 3600000
    setTimeout( function(){ document.querySelector(".after-show-download").style.visibility = "visible"; }, afterShowDownloadTimeout);   

});