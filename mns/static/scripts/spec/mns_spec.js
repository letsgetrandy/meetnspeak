/*global describe:false, it:false, expect:false, beforeEach:false */

describe("TouchMenu class", function() {

    beforeEach(function(){

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

    it ("should hide for non-touch user-agents", function() {

        setFixtures('<div class="handle"></div>');

        var tm = new TouchMenu({
            ua: "msie 9.0",
            handle: "handle"
        });
        expect($(".handle")).not.toBeVisible();
        tm.cleanup();
    });

});
