d3.select("#generate-pdf").on("click", function() {
    var svgList = document.getElementsByTagName("svg");
    var time_line = document.getElementById("chart-events-timeline");
    var array = Array.prototype.slice.call(svgList);
    array.push(time_line);
    generatePdf(array);
});

generatePdf = function(array) {
    data = {}
    var time_line_name = ""
    var time_line_data = ""
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

    $.ajax({
        url: "generate_pdf/",
        type: "POST",
        data: data,
        // handle a successful response
        success: function(json) {
            file_content = JSON.parse(json)["file"];
            convertBase64ToPDF("report.pdf", file_content);
        },
        // handle a non-successful response
        error: function(xhr, errmsg, err) {
            /*$('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom*/
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
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
    var html2obj = html2canvas(element);
    var queue = html2obj.parse();
    var canvas = html2obj.render(queue);
    var data = canvas.toDataURL('image/png');
    return data.split(",")[1];
}