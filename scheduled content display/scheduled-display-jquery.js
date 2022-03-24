jQuery(document).ready(function() {

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

    timings.forEach(period => {
        if (nowTime >= period.scheduledStart && nowTime <= period.scheduledEnd) {
            jQuery(period.periodClass).show();
        } else {
            jQuery(period.periodClass).hide();
        }           
    });

})