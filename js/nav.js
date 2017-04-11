console.log('Load nav.js');

function setupGeolocation(navigator) {
    navigator.geolocation.getCurrentPosition(function(position) {
        $("#latitude").html("" + position.coords.latitude);
        $("#longitude").html("" + position.coords.longitude);
        $("#commentary").html("The Geolocation Javascript Loaded.");
        console.log(position.coords.latitude, position.coords.longitude);
    });
}

if ("geolocation" in navigator) {
    console.log("Run Geolocation Setup");
    setupGeolocation(window.navigator);
}