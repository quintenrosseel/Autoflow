var $ = require('jquery');

module.exports = function dashboard(){
    $(document).ready(function() {

        // Init Google Map API on the center of brussels
        var map;

        var trafficLightStyle =[
            {featureType: "poi",
             elementType: "labels",
             stylers: [{ visibility: "off" }]
            },
            {featureType: 'transit',
             elementType: 'labels.icon',
             stylers: [{visibility: 'off'}]
            }
        ];

        initMap = function() {
            map = new google.maps.Map(document.getElementById('map'), {
                center: {lat: 50.848141, lng: 4.351043},
                zoom: 13,
                mapTypeId: google.maps.MapTypeId.ROADMAP,
                streetViewControl: false,
                mapTypeControl: false,
                fullscreenControl: false,
                scaleControl: false,
                styles: trafficLightStyle
            });



            var locations = [
                ['loc1', 50.848141, 4.351043, 4],
                ['Loc2', 50.853458, 4.365423, 5]
            ];


            // Custom Icon for Traffic light.

            var icon = {
                url: '../images/traffic_light.svg', // url
                scaledSize: new google.maps.Size(11, 11), // scaled size
                origin: new google.maps.Point(0,0), // origin
                anchor: new google.maps.Point(0, 0) // anchor
            };

/*            var marker = new google.maps.Marker({
                position: {lat: 50.848141, lng: 4.351043},
                map: map,
                icon: icon,
                title: '#Traffic Light ID'
            });

            var marker2 = new google.maps.Marker({
                position: {lat: 50.853458, lng: 4.365423},
                map: map,
                icon: icon,
                title: '#Traffic Light ID2'
            });*/

            var marker, i;
            console.log(locations.length);
            for (i = 0; i < locations.length; i++) {
                console.log(i);
                marker = new google.maps.Marker({
                    position: new google.maps.LatLng(locations[i][1], locations[i][2]),
                    map: map,
                    icon: icon,
                    title: '#Traffic Light ID2'
                });

                marker.addListener('click', (function (marker, i) {
                    return function () {
                       // infowindow.setContent(locations[i][0]);
                       // infowindow.open(map, marker);
                       // console.log("Marker");
                        console.log(i);
                    }
                })(marker, i));
            }

            marker.addListener('click', function() {
                //infowindow.open(map, marker);
                console.log(this);
            });



            // Add event listener to zoom event (in order to scale circles)
    /*          google.maps.event.addListener(map, 'zoom_changed', function() {
                var zoomLevel = map.getZoom();
                cityCircle.setRadius(getCustomRadiusForZoom(zoomLevel));
            });*/


            /*
           var startRadius = 60;


           function getCustomRadiusForZoom(level) {
               //console.log(level);
               return startRadius - (level * 2)
           }*/

        }
    });
};
