/**
 * Created by freddyrondon on 1/26/16.
 */

/* EVENTS DATA */
// create dataset
var eventsData = [];
var names = ["Lorem", "Ipsum", "Dolor", "Sit", "Amet", "Consectetur", "Adipisicing", "elit", "Eiusmod tempor", "Incididunt"];
var endTime = Date.now();
var month = 30 * 24 * 60 * 60 * 1000;
var startTime = endTime - 6 * month;

function createEvent(name, maxNbEvents) {
    maxNbEvents = maxNbEvents | 100;
    var event = {
        name: name,
        dates: []
    };
    // add up to 200 events
    var max = Math.floor(Math.random() * maxNbEvents);
    for (var j = 0; j < max; j++) {
        var time = (Math.random() * (endTime - startTime)) + startTime;
        event.dates.push(new Date(time));
    }

    return event;
}
// create 10 events
for (var i = 0; i < 10; i++) {
    eventsData.push(createEvent(names[i]));
}