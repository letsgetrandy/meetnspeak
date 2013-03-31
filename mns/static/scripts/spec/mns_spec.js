/*global describe:false, it:false, expect:false, beforeEach:false */

describe("mns namespace", function() {

    it ("should define the namespace", function() {
        expect(mns).toBeDefined();
    });
    it ("should render templated objects", function() {
        var obj = {foo:"Hello", bar:"World"},
            template = "[[foo]] [[bar]]!",
            s = mns.render(obj, template);
        expect(s).toEqual("Hello World!");
    });
    it ("should populate language drop-downs", function() {
        setFixtures('<select id="foo"><option value="3">Advanced' +
                    '</option></select>');
        mns.langOptions("#foo");
        var s = $("#foo");
        expect(s.find("option").length).toBe(5);
        expect(s.val()).toBe("3");
    });
});


describe("TouchMenu class", function() {

    beforeEach(function(){

    });

    it ("should hide for non-touch user-agents", function() {

        setFixtures('<div class="handle"></div>');

        var tm = new TouchMenu({
            ua: "MSIE 9.0",
            handle: ".handle"
        });
        expect($(".handle")).not.toBeVisible();
        tm.cleanup();
    });

    it ("should show for mobile user-agents", function() {

        setFixtures('<div class="handle"></div>');

        var tm = new TouchMenu({
            ua: "Mobile Safari",
            handle: ".handle"
        });
        expect($(".handle")).toBeVisible();
        tm.cleanup();

    });

    xit ("should toggle open/closed when clicked", function() {

        setFixtures('<div class="handle"></div>');

        var tm = new TouchMenu({
                ua: "mobile safari",
                openClass: "navopen",
                handle: "handle"
            }),
            down = new jQuery.Event("mousedown", {originalEvent:{}}),
            up = new jQuery.Event("mouseup", {originalEvent:{}});

        // starts closed
        expect($("body")).not.toHaveClass("navopen");

        // should open
        $(".handle").trigger(down).trigger(up);
        expect($("body")).toHaveClass("navopen");

        // should close
        $(".handle").trigger(down).trigger(up);
        expect($("body")).not.toHaveClass("navopen");

        tm.cleanup();
    });

});
