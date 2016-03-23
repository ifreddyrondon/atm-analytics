$("#generate-pdf").click(function(event) {
    event.preventDefault();
    $("#wait").show();
    timelineSetting();
    var svgList = document.getElementsByTagName("svg");
    var timeline = document.getElementById("chart-events-timeline");
    var atm_index_chart = document.getElementById("atm-index-chart");
    var total_op_report_chart = document.getElementById("total-operations-report-chart");
    var operations_report_chart = document.getElementById("operations-report-chart");
    var errors_report_chart = document.getElementById("errors-report-chart");
    var amount_report_chart = document.getElementById("amount-report-chart");

    exportDomElementsToPng(
        timeline, atm_index_chart, total_op_report_chart,
        operations_report_chart, errors_report_chart, amount_report_chart,
        svgList
    );
});

timelineSetting = function() {
    var timelineWindow = window.timeline.getWindow();

    window.timeline.setOptions({
        min: timelineWindow.start,
        max: timelineWindow.end
    });
};

resetTimeline = function() {
    window.timeline.setOptions({});
}

function exportDomElementsToPng(
            timeline, atm_index_chart, total_op_report_chart,
            operations_report_chart, errors_report_chart, amount_report_chart,
            svgList
        ) {
    domtoimage
        .toPng(timeline)
        .then(function (timelineData) {
            data = {};

            var img = new Image();
            img.onload = function() {
                var height = timeline.offsetHeight,
                    width = timeline.offsetWidth;
                data[timeline.id.replace(/-/g, "_")] = removeImageBlanks(img/*, width, height*/);
            }
            img.src = timelineData;

            domtoimage
                .toPng(atm_index_chart)
                .then(function(atm_index_chart_data) {
                    data[atm_index_chart.id.replace(/-/g, "_")] = atm_index_chart_data;
                    domtoimage
                        .toPng(total_op_report_chart)
                        .then(function(total_op_report_chart_data) {
                            data[total_op_report_chart.id.replace(/-/g, "_")] = total_op_report_chart_data;
                            domtoimage
                                .toPng(operations_report_chart)
                                .then(function(operations_report_chart_data){
                                    data[operations_report_chart.id.replace(/-/g, "_")] = operations_report_chart_data;
                                    domtoimage
                                        .toPng(errors_report_chart)
                                        .then(function(errors_report_chart_data){
                                            data[errors_report_chart.id.replace(/-/g, "_")] = errors_report_chart_data;
                                            domtoimage
                                                .toPng(amount_report_chart)
                                                .then(function(amount_report_chart_data){
                                                    data[amount_report_chart.id.replace(/-/g, "_")] = amount_report_chart_data;
                                                    setAllAttr(data, svgList);
                                                }).catch(showError);
                                        }).catch(showError);
                                }).catch(showError);
                        }).catch(showError);
            }).catch(showError);
        }).catch(showError);
};

function setAllAttr(data, svgList) {
    for(var i = 0; i < svgList.length; i++) {
        if(svgList[i].id !== "") {
            data[svgList[i].id.replace(/-/g, "_")] = svgAsBase64(svgList[i]);
        }
    }

    var tmpImage = new Image();

    tmpImage.onload = function() {
        data['timeline_height'] = this.height;
        setFinalAttr(data);
    }
    tmpImage.src = data['chart_events_timeline'];
};


function setFinalAttr(data) {
    getDataFilters(data);
    operations_table = readTable('operations-table');
    data['operations_height'] = document.getElementById('operations-table').rows.length;
    time_line_table = readTable('timeline-table');
    resolution = $("#id_resolution").val();

    if (resolution != '') {
        data['resolution'] = resolution;
    }

    data['time_line'] = time_line_table;
    data['operations'] = operations_table;

    postPdfData(data);
};

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

function postPdfData(data) {
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

function convertBase64ToPDF(name, base64) {
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
};

function removeImageBlanks(imageObject/*, imgWidth, imgHeight*/) {
    var imgWidth = imageObject.width,
    imgHeight = imageObject.height,
    canvas = document.createElement('canvas');
    canvas.setAttribute("width", imgWidth);
    canvas.setAttribute("height", imgHeight);
    var context = canvas.getContext('2d');
    context.drawImage(imageObject, 0, 0);

    var imageData = context.getImageData(0, 0, imgWidth, imgHeight),
        data = imageData.data,
        getRBG = function(x, y) {
            var offset = imgWidth * y + x;
            return {
                red:     data[offset * 4],
                green:   data[offset * 4 + 1],
                blue:    data[offset * 4 + 2],
                opacity: data[offset * 4 + 3]
            };
        },
        isTransparent = function (rgb) {
            // many images contain noise, as the white is not a pure #fff white
            return rgb.opacity == 0;
        },
        scanY = function (fromTop) {
            var offset = fromTop ? 1 : -1;

            // loop through each row
            for(var y = fromTop ? 0 : imgHeight - 1; fromTop ? (y < imgHeight) : (y > -1); y += offset) {

                // loop through each column
                for(var x = 0; x < imgWidth; x++) {
                    var rgb = getRBG(x, y);
                    if (!isTransparent(rgb)) {
                        return y;
                    }
                }
            }
            return null; // all image is transparent
        },
        scanX = function (fromLeft) {
            var offset = fromLeft? 1 : -1;

            // loop through each column
            for(var x = fromLeft ? 0 : imgWidth - 1; fromLeft ? (x < imgWidth) : (x > -1); x += offset) {

                // loop through each row
                for(var y = 0; y < imgHeight; y++) {
                    var rgb = getRBG(x, y);
                    if (!isTransparent(rgb)) {
                        return x;
                    }
                }
            }
            return null; // all image is white
        };

    var cropHeight = scanY(false);

    // finally crop the guy
    if (Math.abs(cropHeight - imgHeight) < 100) {
        cropHeight = imgHeight;
    }

    canvas.height = cropHeight;
    canvas.getContext("2d").drawImage(imageObject,
        0, 10, imgWidth, cropHeight,
        0, 0, imgWidth, cropHeight);

    return canvas.toDataURL();
};

function showError(error) {
    console.error('oops, something went wrong!', error);
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

// Ajax setup
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
