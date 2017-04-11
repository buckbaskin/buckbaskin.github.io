console.log('Load nav.js');

function setupGeolocation(navigator) {
    function geoSuccess(position) {
        $("#latitude").html("" + position.coords.latitude);
        $("#longitude").html("" + position.coords.longitude);
        $("#commentary").html("The Geolocation Javascript Loaded.");
        console.log(position.coords.latitude, position.coords.longitude);

        var img_block = document.getElementById("img_here");
        var img = new Image();
        img.src = "https://maps.googleapis.com/maps/api/staticmap?center=" + latitude + "," + longitude + "&zoom=15&size=300x300&sensor=false";
        img_block.appendChild(img);
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