console.log('Load nav.js');

function setupGeolocation(navigator) {
    function geoSuccess(position) {
        $("#latitude").html("" + position.coords.latitude);
        $("#longitude").html("" + position.coords.longitude);
        $("#commentary").html("The Geolocation Javascript Loaded.");
        console.log(position.coords.latitude, position.coords.longitude);
    }

    function geoError() {
        $("#commentary").html("There was an error loading the Geolocation.");
    }

    var geo_options = {
        enableHighAccuracy: true,
        maximumAge: 0
    };

    // navigator.geolocation.getCurrentPosition(geoSuccess);
    var watchID = navigator.geolocation.watchPosition(geoSuccess);
}

function setup() {
    $("#setupRan").html("Javascript Setup ran");
}

if ("geolocation" in navigator) {
    console.log("Run Geolocation Setup");
    setupGeolocation(window.navigator);
}
setup();