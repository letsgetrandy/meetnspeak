/* global google:false */

(function(){

    var openWidth = 260;
    var openX = 0;
    var startX = 0;

    function touchstart(event) {
        var touches = event.originalEvent.touches;
        if(touches.length == 1) {
            if (event.target.id != 'draghandle' &&
                    !$('body').hasClass('navopen'))
            {
                return;
            }
            openX = parseInt($('#wrapper').css('margin-left'), 10);
            startX = touches[0].pageX;
            $('#wrapper').css('margin-left', openX+'px');
            $('body').addClass('navopen');

            // track movement
            event.preventDefault();
            $('body').on('touchmove', touchmove);
            $('body').on('touchend', touchend);
            $('body').on('mousemove', mousemove);
            $('body').on('mouseup', mouseup);
        }
    }
    function touchmove(event) {
        var touches = event.originalEvent.touches;
        var offset = openX - (startX - touches[0].pageX);
        if (offset > 240) {
            offset = 240;
        }
        if (offset < 0) {
            offset = 0;
        }
        $('#wrapper').css('margin-left', offset+'px');
    }
    function touchend() {
        // stop tracking movement after touchend
        $('body').off('touchmove', touchmove);
        $('body').off('touchend', touchend);
        $('body').off('mousemove', mousemove);
        $('body').off('mouseup', mouseup);

        // slide to target
        var targetX = (openX == 0) ? openWidth : 0;
        $('#wrapper').css('margin-left', targetX+'px');
        // clear "navopen" when closing
        if (targetX == 0) {
            $('body').removeClass('navopen');
        } else {
            $('#sidenav').scrollTop(0);
        }
    }

    // mock touch events with the mouse
    function mousedown(event) {
        event.originalEvent.touches = [event];
        touchstart(event);
    }
    function mousemove(event) {
        event.originalEvent.touches = [event];
        touchmove(event);
    }
    function mouseup(event) {
        event.originalEvent.touches = [event];
        touchend(event);
    }

    // enable the touchnav handle
    $('#draghandle').show();

    // animate closed when a nav link is tapped
    $('#touchnav a').click(function(event) {
        $('body').removeClass('navopen');
    });

    // allow touch-drag on the slidewrapper
    $('body').on('touchstart', '#wrapper', touchstart);
    $('body').on('mousedown', '#wrapper', mousedown);

})();


(function(){

    var infowindow;

    function initialize() {
        var mapOptions = {
            zoom: 6,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        map = new google.maps.Map(
                        document.getElementById('map_canvas'), mapOptions);

        // Try HTML5 geolocation
        if(navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                var pos = new google.maps.LatLng(
                                    position.coords.latitude,
                                    position.coords.longitude);

                infowindow = new google.maps.InfoWindow({
                    map: map,
                    position: pos,
                    content: 'Location found using HTML5.'
                });
                map.setCenter(pos);
            }, function() {
                handleNoGeolocation(true);
            });
        } else {
            // Browser doesn't support Geolocation
            handleNoGeolocation(false);
        }
    }

    function handleNoGeolocation(errorFlag) {
        var content;
        if (errorFlag) {
            content = 'Error: The Geolocation service failed.';
        } else {
            content = 'Error: Your browser doesn\'t support geolocation.';
        }

        var options = {
            map: map,
            position: new google.maps.LatLng(60, 105),
            content: content
        };
        var infowindow = new google.maps.InfoWindow(options);
        map.setCenter(options.position);
    }

    if ($('#map_canvas').length > 0) {
        var map;
        google.maps.event.addDomListener(window, 'load', initialize);
    }

    $('a.locate').click(function(event) {
        event.preventDefault();
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                //
            }, function() {
                //
            });
        }
    });

})();
