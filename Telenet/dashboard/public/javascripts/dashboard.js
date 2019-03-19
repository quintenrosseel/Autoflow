var $ = require('jquery');

var nodes = require('../../public/data/nodes');

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


            // Custom Icon for Traffic light.

            var icon = {
                url: '../images/traffic_light.svg', // url
                scaledSize: new google.maps.Size(6, 6), // scaled size
                origin: new google.maps.Point(0,0), // origin
                anchor: new google.maps.Point(0, 0) // anchor
            };

            var marker, i;
            for (i = 0; i < nodes.length; i++) {
                var node = nodes[i];
                marker = new google.maps.Marker({
                    position: new google.maps.LatLng(node.lat, node.long),
                    map: map,
                    icon: icon,
                    optimized: false,
                    id: node.id
                });

                marker.addListener('click', (function (marker, i) {
                    return function () {
                        //console.log(marker.id);
                        updateNodeDetail(marker);
                    }
                })(marker, i));
            }
        };

        var trafficLightWrapper = $('#traffic_light_info');

        function updateNodeDetail(marker) {
            trafficLightWrapper.html(marker.id);
        }
    });
};
