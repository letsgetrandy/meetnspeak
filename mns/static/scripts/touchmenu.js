/* global mns:true */

mns.define("TouchMenu", {

    openWidth: 260,
    openX: 0,
    startx:0,
    events:{},

    __init__: function(conf) {
        var defaults = {
            handle : "#draghandle",
            wrapper: ".body_wrapper",
            menu   : ".sidenav",
            openClass: "navopen"
        };
        this.conf = $.extend(defaults, conf);
        var self = this;

        // enable the touchnav handle
        $(this.conf.handle).css("display", "");

        // animate closed when a nav link is tapped
        $(self.conf.menu).find("a").click(function() {
            $("body").removeClass(self.conf.openClass);
            $(self.conf.wrapper).css("margin-left", "0px");
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

    // cache a handle to an event wrapper
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
            conf = this.conf,
            touches = event.originalEvent.touches;
        if (touches.length == 1) {
            if (!$(event.target).is(conf.handle) &&
                    !$("body").hasClass(conf.openClass))
            {
                return;
            }
            self.openX = parseInt($(conf.wrapper).css("margin-left"), 10);
            self.startX = touches[0].pageX;
            $(conf.wrapper).css("margin-left", self.openX + "px");
            $("body").addClass(conf.openClass);

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
        if (offset > self.conf.openWidth) {
            offset = self.conf.openWidth;
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
});
