'use strict';


const myLocation = {lat: 33.8591744, long: -83.918848};
const mapOptions = {
    zoom: 2, 
    center: myLocation,
    mapTypeId: google.maps.MapTypeId.ROADMAP
};


//create the map
const map = new google.maps.Map(document.getElementById("googleMap"), mapOptions);