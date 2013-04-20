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
