/*global describe:false, it:false, expect:false, beforeEach:false */

describe("TouchMenu class", function() {

    beforeEach(function(){

    });

    it ("should hide for non-touch user-agents", function() {

        setFixtures('<div class="handle"></div>');

        var tm = new TouchMenu({
            ua: "msie 9.0",
            handle: "handle"
        });
        expect($(".handle")).not.toBeVisible();
        tm.cleanup();
    });

    it ("should show for mobile user-agents", function() {

        setFixtures('<div class="handle"></div>');

        var tm = new TouchMenu({
            ua: "mobile safari",
            handle: "handle"
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
