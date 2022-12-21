"use strict";

// function initMap() {
//   const myLocation = { lat: 33.8591744, lng: -83.918848 };

//   const mapOptions = {
//     zoom: 11,
//     center: myLocation,
//     // mapTypeId: google.maps.MapTypeId.ROADMAP
//   };
//   //create the map
//   const map = new google.maps.Map(
//     document.querySelector("#googleMap"),
//     mapOptions
//   );
// }

function initMap() {
    const myLocation = { lat: 33.76298, lng: -84.39502 };
    const directionsRenderer = new google.maps.DirectionsRenderer();

    const mapOptions = {
        zoom: 7,
        center: myLocation,
    };
    //create the map
    const map = new google.maps.Map(
        document.querySelector("#googleMap"),
        mapOptions
    );

    directionsRenderer.setMap(map);
}

function calcRoute(event) {
    event.preventDefault();
    const directionsService = new google.maps.DirectionsService();
    const directionsRenderer = new google.maps.DirectionsRenderer();
    var start = document.getElementById("from").value;
    var end = document.getElementById("to").value;
    var request = {
        origin: start,
        destination: end,
        travelMode: "DRIVING",
    };
    let map;
    directionsService
        .route(request)
        .then((response) => {
            directionsRenderer.setDirections(response);
            const mapOptions = {
                zoom: 7,
            };
            //create the map
            map = new google.maps.Map(
                document.querySelector("#googleMap"),
                mapOptions
            );

            directionsRenderer.setMap(map);
        })
        .then(() => {
            //to-do: call the /map/weather ajax
            // console.log(start,end)
            const url = `/map/waypoints?from=${start}&to=${end}`
            console.log('****URL***', url)
            return fetch(url)          
        })
        .then((response) => response.json())
        .then((waypoints) => {
            console.log(waypoints)
            //TODO:start adding markers here
            markers(map,waypoints)
        })

        .catch((e) => console.log("Directions request failed due to " + status));
}

document.querySelector("#map-route").addEventListener("submit", calcRoute);

//https://developers.google.com/maps/documentation/javascript/examples/directions-panel

function markers(map,waypoints) {
    

    for (const waypoint of waypoints) {
        renderMarker(waypoint, map);
    }
}

function renderMarker(waypoint, map) {
    const {lat,lng} = waypoint;
    const q = `${lat},${lng}`;

    fetch(`/waypoint-weather?q=${q}`)
    .then((response) => response.json())
    .then((responseJson) => {
        console.log(responseJson);
        const weatherMarker = new google.maps.Marker({
            position: waypoint,
            map,
            icon: responseJson.forecast_icon,
            title: responseJson.forecast_text
          });
    }) 
}


    //  Markers location.lat and location.lon need to equal each waypoint lat, lng. Need a for loop
    //  once the data is being looped through so that all waypoints are assigned, the markers can be assigned to each one.
    //the weather conditions need to pull from current.condition.text and the icon can be from current.condition.icon
    // the images that are imported for icons need to be assigned to image for the certain weather conditions. 

    



window.initMap = initMap;
