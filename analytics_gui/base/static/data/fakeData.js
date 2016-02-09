/**
 * Created by freddyrondon on 1/26/16.
 */

/* EVENTS DATA */
// create dataset
var endTime = Date.now();
var month = 30 * 24 * 60 * 60 * 1000;
var startTime = endTime - 6 * month;

function createEvent(name, maxNbEvents) {
    maxNbEvents = maxNbEvents | 100;
    var event = {
        name: name,
        dates: []
    };
    var max = Math.floor(Math.random() * maxNbEvents);
    for (var j = 0; j < max; j++) {
        var time = (Math.random() * (endTime - startTime)) + startTime;
        event.dates.push(new Date(time));
    }

    return event;
}
