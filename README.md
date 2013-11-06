meetnspeak
==========

Meetnspeak is the engine that runs Spikizi (http://www.spikizi.com/)

This app is open-source. You are free to copy and use any code in this
repository. Contributions are encouraged. Useful enhancements will find their
way into the live app, and may also be ported to the mobile clients.

How you can contribute
----------------------

This is currently a one-man project. I'm moving fast and doing as much as I
can, but progress would come much faster and code would be much better with
the help of some specialized help.

**Python/Django** I've been working with python for a little more than a
year now, but it's not my area of expertise, and I'm certain there are places
where my syntax could be improved, cleaned up, or debugged.

**Javascript** I'm looking for more ways to add support for Firefox's WebAPIs
and FirefoxOS, in order to improve the experience.

**CSS/UI** Anything that can be done to improve the cohesiveness of the design,
or to enhance/improve the user's experience is welcome.

**Unit tests** When you're one person moving quickly to add new features, the
first corner that gets cut is the writing of unit tests. Any help adding unit
tests (both Django and Jasmine) is much appreciated.

**Testing** Perhaps my biggest need of all is for as many people as possible
to [use the app](http://www.spikizi.com/) and provide feedback: bug reports,
feature requests, etc.

Again, *any* help is appreciated!


Roadmap
-------

Django proves to be far too heavy of a framework for this lightweight app. I'm
currently working to move all the logic away to either Node.js or Flask.

Javascript has grown to a point where it needs MVC. I'm currently moving all
JS code toward a simple MVC based on Riot.js, though I'm willing to consider
Backbone.
