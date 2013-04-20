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
