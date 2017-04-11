console.log('Load nav.js');

function setupGeolocation(navigator) {
    function geoSuccess(position) {
        var latitude  = position.coords.latitude;
        var longitude = position.coords.longitude;
        $("#latitude").html("" + latitude);
        $("#longitude").html("" + longitude);
        $("#commentary").html("The Geolocation Javascript Loaded.");
        console.log(position.coords.latitude, position.coords.longitude);

        var img_block = document.getElementById("img_here");
        var img = new Image();
        img.src = "https://maps.googleapis.com/maps/api/staticmap?center=" + 
            latitude + "," + 
            longitude + 
            "&zoom=15&size=300x300&sensor=false";
        console.log('img.src', img.src);
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