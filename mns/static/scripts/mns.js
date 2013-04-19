/* global google:false */

if (typeof mns == "undefined") {
    var mns = {

        render: function(obj, template)
        {
            var re, v;
            re = new RegExp("\\[\\[([^\\]]+)\\]\\]");
            while (match = re.exec(template)) {
                val = obj[match[1]] || '';
                template = template.replace(match[0], val);
            }
            return template;
        },

        langOptions: function(selector)
        {
            var s = "",
                levels = ["Beginner", "Intermediate", "Advanced",
                        "Fluent", "Native"],
                val = $(selector).val();
            [1,2,3,4,5].map( function(val, idx) {
                s += mns.render(
                        {value:2 * parseInt(val, 10) - 1, label:levels[idx]},
                        "<option value=\"[[value]]\">[[label]]</option>"
                    );
            });
            $(selector).html(s);
            if (val) {
                $(selector).val(val);
            }
            return s;
        },

        extend: function(defaults, options)
        {
            for (o in options) {
                defaults[o] = options[o];
            }
            return defaults;
        }
    }
}

function Pattern() {
    if (arguments.length) {
        var arg = arguments[0];
        if(arg.jquery) {
            this._template = arg.html();
        } else if (arg.innerHTML) {
            this._template = arg.innerHTML;
        } else if (typeof arg == "string") {
            this._template = arg;
        } else {
            throw "Invalid pattern argument";
        }
    } else {
        this._template = "";
    }
}
Pattern.prototype = {

    // to ease string concatenation
    append: function(s) {
        this._template += s;
        return this;
    },

    // for console logging
    toString: function() {
        return "[Pattern]: " + this._template;
    },

    // render an object through the "template", into a string
    render: function (data)
    {
        // allow repeating when an array is passed
        if (!(data instanceof Array)) {
            data = [data];
        }
        // the actual templating
        var idx, val, out="",
            re = new RegExp("\\[\\[([^\\]]+)\\]\\]");
        for (idx in data) {
            var match, obj = data[idx],
                template = this._template;
            while (match = re.exec(template)) {
                switch(match[1].charAt(0)) {
                // branch-for-true
                case "?":
                    template = this.branch(match[1],
                                !!obj[match[1].substring(1)], template);
                    break;
                // branch-for-false
                case "!":
                    template = this.branch(match[1],
                                !obj[match[1].substring(1)], template);
                    break;
                // default behavior
                default:
                    val = obj[match[1]] || "";
                    template = template.replace(match[0], val);
                    break;
                }
            }
            out += template;
        }
        return out;
    },

    // helper function, for the branch-if-true or branch-if-false logic
    branch: function (tag, cond, template)
    {
        var tagvar = tag.substring(1),
            endtag = "[[" + tagvar + tag.charAt(0) + "]]",
            a = template.indexOf("[[" + tag + "]]"),
            b = template.indexOf(endtag);
        if (b < 0) {
            throw ("missing endtag: " + endtag);
        }
        if (cond) {
            template = template.substring(0, a) +
                template.substring(a + 4 + tag.length, b) +
                template.substring(b + endtag.length);
        } else {
            template = template.substring(0, a) +
                template.substring(b + endtag.length);
        }
        return template;
    }
}

function TouchMenu(conf) {
    var defaults = {
        handle: "#draghandle",
        wrapper: ".body_wrapper",
        openClass: "navopen",
        menu: ".sidenav",
        ua: navigator.userAgent
    };
    this.conf = $.extend(defaults, conf);
    if (this.checkUserAgent()) {
        this.init();
    } else {
        $(this.conf.handle).hide();
    }
}

TouchMenu.prototype = {

    openWidth: 260,
    openX: 0,
    startx:0,
    events:{},

    checkUserAgent: function() {
        var rx = /android|iphone|ipod|ipad|blackberry|touch|tablet|mobile safari|iemobile|windows phone/i;
        return !!rx.test(this.conf.ua);
    },

    init: function() {
        var self = this;

        // enable the touchnav handle
        $(this.conf.handle).css("display", "");  // show();

        // animate closed when a nav link is tapped
        $(self.conf.menu + " a").click(function() {
            $("body").removeClass(self.conf.openClass);
        });
        // add listeners
        this.attachEvent("touchstart", self.conf.wrapper);
        this.attachEvent("mousedown", self.conf.wrapper);
    },

    cleanup: function() {
        var evts = ["touchstart", "touchmove", "touchend",
                    "mousedown", "mousemove", "mouseup"];
        for (var evt in evts) {
            this.removeEvent(evt);
        }
    },

    // cash a handle to an event wrapper
    attachEvent: function(evt, target) {
        var self = this;
        self.removeEvent(evt);
        this.events[evt] = function(event) {
            self[evt](event);
        };
        $("body").on(evt, target || null, this.events[evt]);
        //return this.events[evt];
    },

    // remove listener for the given event
    removeEvent: function(evt) {
        if (this.events[evt]) {
            $("body").off(evt, this.events[evt]);
        }
    },

    touchstart: function(event) {
        var self = this,
            touches = event.originalEvent.touches;
        if (touches.length == 1) {
            if ($(event.target).attr("id") != self.conf.handle.substring(1) &&
                    !$("body").hasClass(self.conf.openClass))
            {
                return;
            }
            self.openX = parseInt($(self.conf.wrapper).css("margin-left"), 10);
            self.startX = touches[0].pageX;
            $(self.conf.wrapper).css("margin-left", self.openX + "px");
            $("body").addClass(self.conf.openClass);

            event.preventDefault();
            self.attachEvent("touchmove");
            self.attachEvent("touchend");
            self.attachEvent("mousemove");
            self.attachEvent("mouseup");
        }
    },
    touchmove: function(event) {
        var self = this,
            touches = event.originalEvent.touches;
        var offset = self.openX - (self.startX - touches[0].pageX);
        if (offset > 240) {
            offset = 240;
        }
        if (offset < 0) {
            offset = 0;
        }
        $(self.conf.wrapper).css("margin-left", offset + "px");
    },
    touchend: function(event) {
        var self = this;
        self.removeEvent("touchmove");
        self.removeEvent("touchend");
        self.removeEvent("mousemove");
        self.removeEvent("mouseup");

        // slide to target
        var targetX = (self.openX === 0) ? self.openWidth : 0;
        $(self.conf.wrapper).css("margin-left", targetX + "px");
        // clear "navopen" when closing
        if (targetX === 0) {
            $("body").removeClass(self.conf.openClass);
        } else {
            $(self.conf.menu).scrollTop(0);
        }
    },

    // mock touch events with the mouse
    mousedown: function(event) {
        event.originalEvent.touches = [event];
        this.touchstart(event);
    },
    mousemove: function(event) {
        event.originalEvent.touches = [event];
        this.touchmove(event);
    },
    mouseup: function(event) {
        event.originalEvent.touches = [event];
        this.touchend(event);
    }
};

function MapGeo (config) {
    var defaults = {
        mapdiv: null,
        on_geo: null,
        on_geocode: null
    };
    this.init(mns.extend(defaults, config));
}
MapGeo.prototype = {
    init: function (config)
    {
        this.config = config;
        this.geo_complete = false;
        this.map_complete = false;
        this.map = null;
        this.info_window = null;
        this.overlays = [];
        this.geo_position = null;

        if (config.mapdiv) {
            this.init_maps(config.mapdiv);
        }
        //this.init_geo();
    },

    init_geo: function (success, fail)
    {
        if (!success) {
            success = this.geo_success;
        }
        if (!fail) {
            fail = this.geo_fail;
        }
        var self = this;
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                function(position) { success(self, position); },
                function() { fail(self, true); });
        } else {
            fail(self, false);
        }
    },

    geo_fail: function (self, supported)
    {
        if (self.config.on_geo_fail) {
            self.config.on_geo_fail(supported);
        } else {
            var s;
            if (supported) {
                s = "An error occurred while getting your location.";
            } else {
                s = "Your browser doesn't support geolocation.";
            }
            if (self.map_loaded) {
                var pos = new google.maps.LatLng(60, 105);
                self.show_info_window(pos, s);
            }
        }
    },

    geo_success: function (self, position)
    {
        self.geo_position = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
        };
        if (self.map_complete) {
            var pos = new google.maps.LatLng(
                                position.coords.latitude,
                                position.coords.longitude);

            self.show_info_window(pos, "Location found using HTML5.");
        }
        if (self.config.on_geo) {
            self.config.on_geo(self.geo_position);
        }
    },

    init_maps: function (mapdiv)
    {
        var mapOptions = {
            zoom: 6,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        this.map = new google.maps.Map(
                        document.getElementById(mapdiv), mapOptions);
        this.map_complete = true;
    },

    show_info_window: function(pos, message)
    {
        //TODO: check if it exists
        this.infowindow = new google.maps.InfoWindow({
            map: this.map,
            position: pos,
            content: message
        });
        this.map.setCenter(pos);
    },

    hide_info_window: function()
    {
        if (this.infowindow) {
            this.infowindow.setMap(null);
        }
    },

    geocode: function(address)
    {
        var self = this;
        $.ajax({
            url:'http://maps.googleapis.com/maps/api/geocode/json?address=' +
                address + '&sensor=false',
            data: {
                address: address,
                sensor: false
            },
            type: 'GET',
            dataType: 'json'
        }).done(function(data) {
            if (data.results.length) {
                var r = data.results[0], fmt = [];
                for (var i=0; i<r.address_components.length; i++) {
                    if (r.address_components[i].types.join(',').match(/locality|country/)) {
                        fmt.push(r.address_components[i].short_name);
                    }
                }
                if (self.config.on_geocode) {
                    self.config.on_geocode({
                        lat: r.geometry.location.lat,
                        lng: r.geometry.location.lng,
                        description: fmt.join(', ')
                    });
                }
            }
        }).fail(function() {
            //console.log('error');
        }).always(function() {
            //console.log('done');
        });
    }
};
