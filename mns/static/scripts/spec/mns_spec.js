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
    it ("should extend one object with another", function() {
        var a = { cat: "garfield" },
            b = { dog: "odie" };
        expect(a.dog).not.toBeDefined();
        mns.extend(a, b);
        expect(a.dog).toBe("odie");
    });
});


describe("mns.define()", function() {
    it("should create a class definition", function() {
        mns.define("Foo", { test:function() { return "hello"; } });
        expect(mns.Foo).toBeDefined();
        var foo = new mns.Foo();
        expect(foo.test).toBeDefined();
        expect(foo.test()).toBe("hello");
        delete mns.Foo;
        delete mns.FooException;
        expect(mns.Foo).not.toBeDefined();
        expect(mns.FooException).not.toBeDefined();
    });
    it("should keep a count of object instances", function() {
        mns.define("Foo", {});
        expect(mns.Foo.__count__).toEqual(0);
        new mns.Foo();
        expect(mns.Foo.__count__).toEqual(1);
        new mns.Foo();
        expect(mns.Foo.__count__).toEqual(2);
        delete mns.Foo;
        delete mns.FooException;
    });
    it("should define a toString() method", function() {
        mns.define("Foo", {});
        var foo = new mns.Foo();
        expect(foo.toString()).toEqual("[object Foo]");
        delete mns.Foo;
        delete mns.FooException;
    });
    it("should create a custom exception", function() {
        mns.define("Bar", { });
        expect(mns.BarException).toBeDefined();
        delete mns.Bar;
        delete mns.BarException;
        expect(mns.Bar).not.toBeDefined();
        expect(mns.BarException).not.toBeDefined();
    });
    it("should raise its custom excpetion", function() {
        mns.define("Foo", { });
        var msg = "",
            obj = new mns.Foo();
        try {
            obj.raise("test");
        } catch (e) {
            msg = e.toString();
        }
        expect(msg).toBe("FooException: test");
        delete mns.Foo;
        delete mns.FooException;
        expect(mns.Foo).not.toBeDefined();
        expect(mns.FooException).not.toBeDefined();
    });

});

describe("mns.mixins", function() {

    it("should be defined as mns.mixins", function() {
        expect(mns.mixins).toBeDefined();
    });

    it("should support 'events' mixin", function(){
        mns.define("MixinTest", {});
        var obj = new mns.MixinTest();
        // ensure mixin methods are not applied
        expect(obj.attachEvent).not.toBeDefined();
        expect(obj.removeEvent).not.toBeDefined();
        // check for mixin method
        expect(obj.mixin).toBeDefined();
        // add mixin
        obj.mixin("events");
        // check that mixin methods are applied
        expect(obj.attachEvent).toBeDefined();
        expect(obj.removeEvent).toBeDefined();
    });
});
