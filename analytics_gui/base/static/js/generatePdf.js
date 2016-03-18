$("#generate-pdf").click(function(event) {
    event.preventDefault();
    $("#wait").show();
    var svgList = document.getElementsByTagName("svg");
    timelineSetting();
    var timeline = document.getElementById("chart-events-timeline");
    var atm_index_chart = document.getElementById("atm-index-chart");
    var total_op_report_chart = document.getElementById("total-operations-report-chart");
    var operations_report_chart = document.getElementById("operations-report-chart");
    var errors_report_chart = document.getElementById("errors-report-chart");
    var amount_report_chart = document.getElementById("amount-report-chart");
    var array = Array.prototype.slice.call(svgList);
    array.push(timeline);
    array.push(atm_index_chart);
    array.push(total_op_report_chart);
    array.push(operations_report_chart);
    array.push(errors_report_chart);
    array.push(amount_report_chart);
    generatePdf(array);
});

generatePdf = function(array) {
    data = {}
    data['timeline_height'] = document.getElementById("chart-events-timeline").offsetHeight;
    getDataFilters(data);

    operations_table = readTable('operations-table');
    time_line_table = readTable('timeline-table');
    resolution = d3.select("#id_resolution")[0][0].value;

    for (var i = 0; i < array.length; i++) {
        if (array[i].id !== '' && array[i].tagName.toLowerCase() == 'svg') {
            data[array[i].id] = svgAsBase64(array[i]);
        } else if(array[i].tagName.toLowerCase() == 'div') {
            data[array[i].id] = getImageData(array[i]);
        }
    }

    if (resolution != '') {
        data['resolution'] = resolution;
    }

    data['time_line'] = time_line_table;
    data['operations'] = operations_table;

    $.ajax({
        url: "generate_pdf/",
        type: "POST",
        data: data,
        // handle a successful response
        success: function(json) {
            file_content = JSON.parse(json)["file"];
            $("#wait").hide();
            convertBase64ToPDF("report.pdf", file_content);
            resetTimeline();
        },
        // handle a non-successful response
        error: function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            $("#wait").hide();
        }
    });
};

// This function gets cookie with a given name
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

/*
The functions below will create a header with csrftoken
*/

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

convertBase64ToPDF = function (name, base64) {
    var blob = b64toBlob(base64, 'application/pdf');
    var a = document.createElement("a");

    //Helper function that converts base64 to blob
    function b64toBlob(b64Data, contentType, sliceSize) {
        contentType = contentType || '';
        sliceSize = sliceSize || 512;

        var byteCharacters = atob(b64Data);
        var byteArrays = [];

        for (var offset = 0; offset < byteCharacters.length; offset += sliceSize) {
            var slice = byteCharacters.slice(offset, offset + sliceSize);

            var byteNumbers = new Array(slice.length);
            for (var i = 0; i < slice.length; i++) {
                byteNumbers[i] = slice.charCodeAt(i);
            }

            var byteArray = new Uint8Array(byteNumbers);

            byteArrays.push(byteArray);
        }

        var blob = new Blob(byteArrays, { type: contentType });
        return blob;
    }

    fileURL = URL.createObjectURL(blob);
    document.body.appendChild(a);
    a.href = fileURL;
    a.download = name;
    a.click();
    document.body.removeChild(a);
}

getImageData = function(element) {
    element = svgToCanvas(element);
    if (element.tagName.toLowerCase() == "div") {
        var html2obj = html2canvas(element);
        var queue = html2obj.parse();
        var canvas = html2obj.render(queue);
        var data = canvas.toDataURL('image/png');
    } else if (element.tagName.toLowerCase() == "canvas") {
        var data = element.toDataURL('image/png');
    }

    return data;
    // return data.split(",")[1];
}

svgToCanvas = function(targetElem) {
    var svgElems = targetElem.getElementsByTagName("svg");

    if (svgElems.length == 1) {
        var svg = svgElems[0].outerHTML;
        var canvas = document.createElement('canvas');
        canvg(canvas, svg);
        return canvas;
    } else {
        return targetElem;
    }
}

readTable = function(id) {
    var table = document.getElementById(id);
    var data = {}
    var date = []
    var error = []
    var mount = []
    var atm = []
    //gets rows of table
    var rowLength = table.rows.length;

    //loops through rows
    for (i = 1; i < rowLength; i++) {

        //gets cells of current row
        var cells = table.rows.item(i).cells;

        //gets amount of cells of current row
        var cellLength = cells.length;

        //loops through each cell in current row
        for(var j = 1; j < cellLength; j++) {
            switch(j) {
                case 1: // Date
                    date.push(cells.item(j).innerHTML);
                    break;
                case 2: // Error
                    error.push(cells.item(j).innerHTML);
                    break;
                case 3: // Mount
                    mount.push(cells.item(j).innerHTML);
                    break;
                case 4:
                    atm.push(cells.item(j).innerHTML);
                    break;
            }
        }
    }

    data['Fecha'] = date;
    data['Error'] = error;
    data['Monto'] = mount;
    data['ATM'] = atm;

    return data;
}

getDataFilters = function(data) {
    data['critical_filter'] = document.getElementById("timeline-filter-critical-erros").checked;
    data['important_filter'] = document.getElementById("timeline-filter-important-erros").checked;
    data['no_error_filter'] = no_error = document.getElementById("timeline-filter-no-erros").checked;

    data['date_filter'] = document.getElementById("timeline-calendar-picker").value;
    if (document.getElementById("timeline-windows-event-calendar-picker") != null) {
        data['date_windows_filter'] = document.getElementById("timeline-windows-event-calendar-picker").value;
    }

    if (document.getElementById("timeline-filter-replenishment-events") != null) {
        data['timeline_filter_replenishment_events'] = document.getElementById("timeline-filter-replenishment-events").checked
    }

    filters = []
    window_filters = undefined

    $("#timeline-filter-errors")
        .next()
        .find(".select2-selection__rendered")
        .children().each(function() {
        if($(this).attr("title") != undefined) {
            filters.push($(this).attr("title"));
        }
    });

    if (document.getElementById("timeline-filter-windows-errors") != null) {
        window_filters = []
        $("#timeline-filter-windows-errors")
            .next()
            .find(".select2-selection__rendered")
            .children().each(function() {
            if($(this).attr("title") != undefined) {
                window_filters.push($(this).attr("title"));
            }
        });
    }

    if (filters.length == 0) {
        data['filters'] = "All";
    } else {
        data['filters'] = filters.join(", ");
    }

    if (window_filters != undefined) {
        if (window_filters.length == 0) {
            data['window_filters'] = "All";
        } else {
            data['window_filters'] = window_filters.join(", ");
        }
    }

    var dates_text = $("#timeline-dynamic-range-dates").text()
    var length = dates_text.length

    data['timeline_dynamic_range_dates_1'] = dates_text.slice(0, length/2);
    data['timeline_dynamic_range_dates_2'] = dates_text.slice(length/2, length);
    data['timeline_dynamic_missing_amount'] = $("#timeline-dynamic-missing-amount").text();
    data['timeline_dynamic_number_windows_events'] = $("#timeline-dynamic-number-windows-events").text();
    // TODO: Falta por añadir
    // console.log($(".well .percent-result .dynamic-analysis").text());
    data['timeline_dynamic_critic_errors_vs_critic_errors'] = $("#timeline-dynamic-critic-errors-vs-critic-errors").text();
}

timelineSetting = function() {
    var timelineWindow = window.timeline.getWindow();

    window.timeline.setOptions({
        min: timelineWindow.start,
        max: timelineWindow.end
    });
}

resetTimeline = function() {
    window.timeline.setOptions({});
}