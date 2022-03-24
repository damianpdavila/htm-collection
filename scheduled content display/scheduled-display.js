(function () {
    // Suppress site-wide acuity tracking code for testing changes; remove this code on the page containing updated code
    if (window.location.search.toLowerCase().indexOf('acuity-scd-testing') > -1)  
        return;

    var acuity_url_initial = '';
    if (window.addEventListener) {
        // For standards-compliant web browsers
        window.addEventListener("load", checkTimeAndSetDisplay, false);
    }
    else {
        window.attachEvent("onload", checkTimeAndSetDisplay);
    }

    function checkTimeAndSetDisplay() {
        scheduledDisplay();
        let timer = window.setInterval(scheduledDisplay, 5000);
    }

    function scheduledDisplay() {

        /**
         * If need to synchronize to a specific timezone (e.g. like a live event at 9:00am ET), convert the date to UTC and append a 'Z'
         * 
         *        Jan 31, 2021 at 9:00am ET => 2021-31-01T14:00:00Z
         * 
         * Otherwise, all dates are internally converted to local time zone.  e.g. the start date and time will apply to the user's local machine
         * 
         *        start date/time === same start date/time in ANY timezone
         *  */

        let timings = [
            {periodClass : ".day-1", scheduledStart : new Date("2021-01-23T16:39:00Z"), scheduledEnd : new Date("2021-01-23T16:39:00Z")},
            {periodClass : ".day-2", scheduledStart : new Date("2021-01-23T16:39:00Z"), scheduledEnd : new Date("2021-01-23T16:39:00Z")},
            {periodClass : ".day-3", scheduledStart : new Date("2021-01-23T16:39:00Z"), scheduledEnd : new Date("2021-01-23T16:39:00Z")}
        ]

        var nowTime = new Date();
        var elems = [];

        timings.forEach(period => {
            elems = document.querySelectorAll(period.periodClass);
            if (nowTime >= period.scheduledStart && nowTime <= period.scheduledEnd) {
                elems.forEach(elem => {
                    elem.style.display = "block";
                })
            } else {
                elems.forEach(elem => {
                    elem.style.display = "none";
                })
            }           
        });

    };

})();