/* global mns:true */

mns.define("MapGeo", {

    __init__: function(config) {
        var defaults = {
            mapdiv: null,
            on_geo: null,
            on_geocode: null
        };
        this.init(mns.extend(defaults, config));
    },

    init: function (config)
    {
        this.config = config;
        this.geo_complete = false;
        this.map_complete = false;
        this.map = null;
        this.info_window = null;
        this.overlays = [];
        this.geo_position = null;

        if (config.mapdiv) {
            this.init_maps(config.mapdiv);
        }
        //this.init_geo();
    },

    init_geo: function (success, fail)
    {
        if (!success) {
            success = this.geo_success;
        }
        if (!fail) {
            fail = this.geo_fail;
        }
        var self = this;
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                function(position) { success(self, position); },
                function() { fail(self, true); });
        } else {
            fail(self, false);
        }
    },

    geo_fail: function (self, supported)
    {
        if (self.config.on_geo_fail) {
            self.config.on_geo_fail(supported);
        } else {
            var s;
            if (supported) {
                s = "An error occurred while getting your location.";
            } else {
                s = "Your browser doesn't support geolocation.";
            }
            if (self.map_loaded) {
                var pos = new google.maps.LatLng(60, 105);
                self.show_info_window(pos, s);
            }
        }
    },

    geo_success: function (self, position)
    {
        self.geo_position = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
        };
        if (self.map_complete) {
            var pos = new google.maps.LatLng(
                                position.coords.latitude,
                                position.coords.longitude);

            self.show_info_window(pos, "Location found using HTML5.");
        }
        if (self.config.on_geo) {
            self.config.on_geo(self.geo_position);
        }
    },

    init_maps: function (mapdiv)
    {
        var mapOptions = {
            zoom: 6,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        this.map = new google.maps.Map(
                        document.getElementById(mapdiv), mapOptions);
        this.map_complete = true;
    },

    show_info_window: function(pos, message)
    {
        //TODO: check if it exists
        this.infowindow = new google.maps.InfoWindow({
            map: this.map,
            position: pos,
            content: message
        });
        this.map.setCenter(pos);
    },

    hide_info_window: function()
    {
        if (this.infowindow) {
            this.infowindow.setMap(null);
        }
    },

    geocode: function(address)
    {
        var self = this;
        $.ajax({
            url:'http://maps.googleapis.com/maps/api/geocode/json?address=' +
                address + '&sensor=false',
            data: {
                address: address,
                sensor: false
            },
            type: 'GET',
            dataType: 'json'
        }).done(function(data) {
            if (data.results.length) {
                var r = data.results[0], fmt = [];
                for (var i=0; i<r.address_components.length; i++) {
                    if (r.address_components[i].types.join(',').match(/locality|country/)) {
                        fmt.push(r.address_components[i].short_name);
                    }
                }
                if (self.config.on_geocode) {
                    self.config.on_geocode({
                        lat: r.geometry.location.lat,
                        lng: r.geometry.location.lng,
                        description: fmt.join(', ')
                    });
                }
            }
        }).fail(function() {
            //console.log('error');
        }).always(function() {
            //console.log('done');
        });
    }
});
