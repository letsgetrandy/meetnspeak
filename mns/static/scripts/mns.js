/* global google:false */

function TouchMenu(conf) {
    var defaults = {
        handle: "draghandle",
        wrapper: ".body_wrapper",
        openClass: "navopen",
        menu: ".sidenav"
    };
    this.conf = $.extend(defaults, conf);
    this.init();
}

TouchMenu.prototype = {

    openWidth: 260,
    openX: 0,
    startx:0,

    init: function() {
        var self = this;
        self.events = {};

        // enable the touchnav handle
        $("." + this.conf.handle).show();

        // animate closed when a nav link is tapped
        $(".touchnav a").click(function() {
            $("body").removeClass(self.conf.openClass);
        });

        // allow touch-drag on the slidewrapper
        $("body").on("touchstart", self.conf.wrapper, function(event) {
            self.touchstart(event);
        });
        $("body").on("mousedown", self.conf.wrapper, function(event) {
            self.mousedown(event);
        });
    },

    touchstart: function(event) {
        var self = this,
            touches = event.originalEvent.touches;
        if (touches.length == 1) {
            if (!$(event.target).hasClass(self.conf.handle) &&
                    !$("body").hasClass(self.conf.openClass))
            {
                return;
            }
            openX = parseInt($(self.conf.wrapper).css("margin-left"), 10);
            startX = touches[0].pageX;
            $(self.conf.wrapper).css("margin-left", openX + "px");
            $("body").addClass(self.conf.openClass);

            event.preventDefault();

            // cache handles to anonymous functions
            self.events.touchmove = function(event) { self.touchmove(event); };
            self.events.touchend = function(event) { self.touchend(event); };
            self.events.mousemove = function(event) { self.mousemove(event); };
            self.events.mouseup = function(event) { self.mouseup(event); };

            // track movement
            $("body").on("touchmove", self.events.touchmove);
            $("body").on("touchend", self.events.touchend);
            $("body").on("mousemove", self.events.mousemove);
            $("body").on("mouseup", self.events.mouseup);
        }
    },
    touchmove: function(event) {
        var self = this,
            touches = event.originalEvent.touches;
        var offset = openX - (startX - touches[0].pageX);
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
        // stop tracking movement after touchend
        $("body").off("touchmove",self.events.touchmove);
        $("body").off("touchend", self.events.touchend);
        $("body").off("mousemove", self.events.mousemove);
        $("body").off("mouseup", self.events.mouseup);

        // slide to target
        var targetX = (openX === 0) ? self.openWidth : 0;
        $(".body_wrapper").css("margin-left", targetX + "px");
        // clear "navopen" when closing
        if (targetX === 0) {
            $("body").removeClass("navopen");
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


(function(){

    var infowindow;

    function initialize() {
        var mapOptions = {
            zoom: 6,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        map = new google.maps.Map(
                        document.getElementById("map_canvas"), mapOptions);

        // Try HTML5 geolocation
        if(navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                var pos = new google.maps.LatLng(
                                    position.coords.latitude,
                                    position.coords.longitude);

                infowindow = new google.maps.InfoWindow({
                    map: map,
                    position: pos,
                    content: "Location found using HTML5."
                });
                map.setCenter(pos);
            }, function() {
                handleNoGeolocation(true);
            });
        } else {
            // Browser doesn't support Geolocation
            handleNoGeolocation(false);
        }
    }

    function handleNoGeolocation(errorFlag) {
        var content;
        if (errorFlag) {
            content = "Error: The Geolocation service failed.";
        } else {
            content = "Error: Your browser doesn\'t support geolocation.";
        }

        var options = {
            map: map,
            position: new google.maps.LatLng(60, 105),
            content: content
        };
        infowindow = new google.maps.InfoWindow(options);
        map.setCenter(options.position);
    }

    if ($("#map_canvas").length > 0) {
        var map;
        google.maps.event.addDomListener(window, "load", initialize);
    }

    $("a.locate").click(function(event) {
        event.preventDefault();
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function() {
                //
            }, function() {
                //
            });
        }
    });

})();
