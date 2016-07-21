(function() {
    var doctype = '<?xml version="1.0" standalone="no"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">';

    svgAsBase64 = function(el) {
        var xmlns = "http://www.w3.org/2000/xmlns/";

        var outer = document.createElement("div");
        var clone = el.cloneNode(true);
        var width, height;
        if (el.tagName == 'svg') {
            width = getDimension(el, clone, 'width');
            height = getDimension(el, clone, 'height');
        } else if (el.getBBox) {
            var box = el.getBBox();
            width = box.x + box.width;
            height = box.y + box.height;
            clone.setAttribute('transform', clone.getAttribute('transform').replace(/translate\(.*?\)/, ''));

            var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg')
            svg.appendChild(clone)
            clone = svg;
        } else {
            console.error('Attempted to render non-SVG element', el);
            return;
        }

        clone.setAttribute("version", "1.1");
        clone.setAttributeNS(xmlns, "xmlns", "http://www.w3.org/2000/svg");
        clone.setAttributeNS(xmlns, "xmlns:xlink", "http://www.w3.org/1999/xlink");
        clone.setAttribute("width", width);
        clone.setAttribute("height", height);
        clone.setAttribute("viewBox", [0, 0, width, height].join(" "));

        outer.appendChild(clone);

        var css = styles(el);
        var s = document.createElement('style');
        s.setAttribute('type', 'text/css');
        s.innerHTML = "<![CDATA[\n" + css + "\n]]>";
        var defs = document.createElement('defs');
        defs.appendChild(s);
        clone.insertBefore(defs, clone.firstChild);

        var svg = doctype + outer.innerHTML;
        var uri = 'data:image/svg+xml;base64,' + window.btoa(reEncode(svg));
        return uri;
    }

    function styles(el, selectorRemap) {
        var css = "";
        var sheets = document.styleSheets;
        for (var i = 0; i < sheets.length; i++) {
            try {
                var rules = sheets[i].cssRules;
            } catch (e) {
                console.warn("Stylesheet could not be loaded: " + sheets[i].href);
                continue;
            }

            if (rules != null) {
                for (var j = 0; j < rules.length; j++) {
                    var rule = rules[j];
                    if (typeof(rule.style) != "undefined") {
                        var match = null;
                        try {
                            match = el.querySelector(rule.selectorText);
                        } catch (err) {
                            console.warn('Invalid CSS selector "' + rule.selectorText + '"', err);
                        }
                        if (match) {
                            var selector = selectorRemap ? selectorRemap(rule.selectorText) : rule.selectorText;
                            css += selector + " { " + rule.style.cssText + " }\n";
                        } else if (rule.cssText.match(/^@font-face/)) {
                            css += rule.cssText + '\n';
                        }
                    }
                }
            }
        }
        return css;
    }

    function getDimension(el, clone, dim) {
        var v = (el.viewBox && el.viewBox.baseVal && el.viewBox.baseVal[dim]) ||
            (clone.getAttribute(dim) !== null && !clone.getAttribute(dim).match(/%$/) && parseInt(clone.getAttribute(dim))) ||
            el.getBoundingClientRect()[dim] ||
            parseInt(clone.style[dim]) ||
            parseInt(window.getComputedStyle(el).getPropertyValue(dim));
        return (typeof v === 'undefined' || v === null || isNaN(parseFloat(v))) ? 0 : v;
    }

    function reEncode(data) {
        data = encodeURIComponent(data);
        data = data.replace(/%([0-9A-F]{2})/g, function(match, p1) {
            var c = String.fromCharCode('0x' + p1);
            return c === '%' ? '%25' : c;
        });
        return decodeURIComponent(data);
    }
})();
