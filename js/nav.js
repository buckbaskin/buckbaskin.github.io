console.log('Load nav.js');

function setupGeolocation(navigator) {
    function geoSuccess(position) {
        var latitude  = position.coords.latitude;
        var longitude = position.coords.longitude;
        $("#latitude").html("" + latitude);
        $("#longitude").html("" + longitude);
        $("#commentary").html("The Geolocation Javascript Loaded.");
        console.log(position.coords.latitude, position.coords.longitude);

        var img = document.getElementById("unique");
        if (img === undefined || img === null || !img) {
            var img_block = document.getElementById("img_here");
            var img = new Image();
            img.id = "unique";
            img_block.appendChild(img);
            img = document.getElementById("unique");
        }
        var img_src ="https://maps.googleapis.com/maps/api/staticmap?center=41.5024294,-81.6082778&zoom=18&size=300x300&sensor=false";
        console.log("img.src 1", img_src);
        img.src = "https://maps.googleapis.com/maps/api/staticmap?center=" + 
            latitude + "," + 
            longitude + 
            "&zoom=18&size=300x300&sensor=false";
        console.log('img.src 2', img.src);
    }

    function geoError(error) {
        $("#commentary").html("There was an error loading the Geolocation.\n"+error.code+"\n"+error.message);
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
    setupGeolocation(window.navigator);
}
setup();