/*global google:false, mns:true */

window.mns = {

    render: function(obj, template)
    {
        var re, v, match;
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
        for (var o in options) {
            defaults[o] = options[o];
        }
        return defaults;
    },

    // base Exception prototype
    Exception: function(message)
    {
        this.message = message || "";
        this.toString = function() {
            return this.name + ": " + this.message;
        };
    },


    // helper for declaring classes in the 'mns' namespace
    define: function(name, proto)
    {
        "use strict";
        var c, n;

        //constructor
        c = mns[name] = function() {
            var count,
                fn;

            count = this.constructor.__count__ += 1;
            this.constructor.prototype.__count__ = count;

            fn = this.__init__;
            if (fn) {
                fn.apply(this, [].slice.call(arguments));
            }
        };

        //class attributes
        c.__alias__ = name;
        c.__count__ = 0;
        c.__class__ = {};

        //prototype attributes
        c.prototype = proto || {};
        c.prototype.constructor = c;
        c.prototype.__alias__ = c.__alias__;
        c.prototype.__count__ = c.__count__;
        c.prototype.__class__ = c.__class__;
        c.prototype.toString = function() {
            return "[object " + this.__alias__ + "]";
        };
        c.prototype.raise = function(message) {
            throw new mns[this.__alias__ + "Exception"](message);
        };
        // poor man's multiple inheritance
        c.prototype.mixin = function(mixins) {
            if (typeof mixins == "string") {
                mixins = [mixins];
            }
            for (var i in mixins) {
                var mxn = mns.mixins[mixins[i]];
                if (mxn) {
                    for (var fn in mxn) {
                        mns[name].prototype[fn] = mxn[fn];
                    }
                }
            }
        };

        //exception class
        n = name + "Exception";
        c = mns[n] = function(message) {
            mns.Exception.call(this, message);
        };
        c.prototype.name = n;
    },

    mixins: {
        // common prototype for event handling
        "events": {
            // object events
            "listeners": {},
            // cache a handle to an event wrapper
            "attachEvent": function(evt, target) {
                var self = this;
                self.removeEvent(evt);
                self.listeners[evt] = function(event) {
                    self[evt](event);
                };
                $("body").on(evt, target || null, this.listeners[evt]);
            },
            // remove listener for the given event
            "removeEvent": function(events) {
                if (typeof events == 'string') {
                    events = [events];
                }
                while (events.length) {
                    var evt = events.shift();
                    if (this.listeners[evt]) {
                        $("body").off(evt, this.listeners[evt]);
                        delete this.listeners[evt];
                    }
                }
            }
        }
    }
};

$(document).on("touchstart", ".switch", function(event) {
    var self = $(this),
        startX = event.pageX,
        endX = event.pageX;
    self.on("touchmove", function(event) {
        //if(!event.originalEvent.touches) {
        //    event.originalEvent.touches = [event];
        //}
        var t = event.originalEvent.touches[0];
        endX = t.pageX;
    });
    self.on("touchend", function(event) {
        self.off("touchmove");
        self.off("touchend");
        if (endX - startX > 10) {
            self.find("input.on").click();
            //console.log("slide right");
        } else
        if (endX - startX < -10) {
            self.find("input.off").click();
            //console.log("slide left");
        }
    });
});
