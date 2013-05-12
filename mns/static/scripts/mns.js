/* global google:false, mns:true */

window.mns = {

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
        //if (mns[name]) {
        //    throw new Error("[object " + name + "] already exists.");
        //}
        // constructor
        c = mns[name] = function() {
            this.constructor.count += 1;
            var fn = this.__init__;
            if (fn) {
                fn.apply(this, [].slice.call(arguments));
            }
        };
        // prototype
        c.prototype = proto || {};
        c.prototype.constructor = c;
        c.prototype.raise = function(message) {
            throw new mns[this.constructor.alias + "Exception"](message);
        };
        c.prototype.toString = function() {
            return "[object " + this.constructor.alias + "]";
        };
        c.alias = name;
        c.count = 0;

        // exception class
        n = name + "Exception";
        c = mns[n] = function(message) {
            mns.Exception.call(this, message);
        };
        c.prototype.name = n;
    }
}

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
