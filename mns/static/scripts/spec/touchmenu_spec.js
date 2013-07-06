/*global describe:false, it:false, expect:false, beforeEach:false */

describe("TouchMenu", function() {

    beforeEach(function(){
        affix('.body_wrapper .handle');
    });

    it ("should show for mobile user-agents", function() {

        var tm = new mns.TouchMenu({
            handle: ".handle"
        });
        expect($(".handle")).toBeVisible();
        tm.cleanup();
    });

    it("should open when handle is touched while closed", function() {
        var tm = new mns.TouchMenu({
                handle: ".handle"
            }),
            start = new jQuery.Event("touchstart", {originalEvent:{}}),
            end   = new jQuery.Event("touchend", {originalEvent:{}});
        start.originalEvent.touches = [start];
        end.originalEvent.touches = [end];

        // simulate tap
        $(".handle").trigger(start).trigger(end);
        expect($(".body_wrapper").css("margin-left")).toBe("260px");
    });

    it("should close when handle is touched while open", function() {
        var tm = new mns.TouchMenu({
                handle: ".handle"
            });
            start = new jQuery.Event("touchstart", {originalEvent:{}}),
            end   = new jQuery.Event("touchend", {originalEvent:{}});
        start.originalEvent.touches = [start];
        end.originalEvent.touches = [end];

        // open the nav
        $(".handle").trigger(start).trigger(end);
        expect($(".body_wrapper").css("margin-left")).toBe("260px");

        // simulate tap
        $(".handle").trigger(start).trigger(end);
        expect($(".body_wrapper").css("margin-left")).toBe("0px");
    });

    it("should allow to drag wrapper closed", function() {
        var tm = new mns.TouchMenu({
                handle: ".handle"
            }),
            start = new jQuery.Event("touchstart", {originalEvent:{}}),
            move  = new jQuery.Event("touchmove", {originalEvent:{}}),
            end   = new jQuery.Event("touchend", {originalEvent:{}});
        start.originalEvent.touches = [start];
        move.originalEvent.touches = [move];
        end.originalEvent.touches = [end];

        // open the nav
        $(".handle").trigger(start).trigger(end);
        expect($(".body_wrapper").css("margin-left")).toBe("260px");

        // simulate touch-drag 140px left
        start.originalEvent.touches[0].pageX = 270;
        move.originalEvent.touches[0].pageX = 150;
        $(".handle").trigger(start).trigger(move);
        expect($(".body_wrapper").css("margin-left")).toBe("140px");

        // end touch drag
        end.originalEvent.touches[0].pageX = 100;
        $(".handle").trigger(end);
        expect($(".body_wrapper").css("margin-left")).toBe("0px");
    });

    it("should close when a nav link is tapped", function() {
        affix(".sidenav a");
        var tm = new mns.TouchMenu({
                handle: ".handle"
            });
            start = new jQuery.Event("touchstart", {originalEvent:{}}),
            end   = new jQuery.Event("touchend", {originalEvent:{}});
        start.originalEvent.touches = [start];
        end.originalEvent.touches = [end];

        // open the nav
        $(".handle").trigger(start).trigger(end);
        expect($(".body_wrapper").css("margin-left")).toBe("260px");

        $(".sidenav a").click();
        expect($(".body_wrapper").css("margin-left")).toBe("0px");
    });

    it("should allow mouse to simulate touch events", function() {
        var tm = new mns.TouchMenu({
                handle: ".handle"
            });
            down  = new jQuery.Event("mousedown", {originalEvent:{}}),
            drag  = new jQuery.Event("mousemove", {originalEvent:{}}),
            up    = new jQuery.Event("mouseup", {originalEvent:{}});

        // simulate click
        $(".handle").trigger(down).trigger(up);
        expect($(".body_wrapper").css("margin-left")).toBe("260px");

        // simulate mouse drag 140px left
        down.pageX = 270;
        drag.pageX = 150;
        $(".handle").trigger(down).trigger(drag);
        expect($(".body_wrapper").css("margin-left")).toBe("140px");

        // end mouse drag
        up.pageX = 100;
        $(".handle").trigger(up);
        expect($(".body_wrapper").css("margin-left")).toBe("0px");
    });
});
