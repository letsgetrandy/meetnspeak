/* global mns:true */

mns.define("Pattern", {

    __init__: function() {
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
    },

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
});
