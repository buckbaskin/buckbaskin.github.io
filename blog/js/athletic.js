let print = console.log;

function sensor_config() {
    return {frequency: 50};
}

function location_config() {
    return {
        enableHighAccuracy: true,
        timeout: 200,
        maximumAge: 0
    };
}

function accelerometer_config() {
    var config = sensor_config();
    config.referenceFrame = 'device';
    return config;
}

function ask_permission(name, happy_path) {
    navigator.permissions.query({ name: name })
        .then(result => {
            if (result.state === 'denied') {
                console.log('Permission to use " + name + " sensor is denied.');
                return false;
            }
            happy_path();
            return true;
        });

}

function accelerometer_setup() {

    print("accelerometer_setup");

    let acl = null;

    try {
        acl = new Accelerometer(accelerometer_config());
        acl.addEventListener('error', event => {
            if (event.error.name === 'NotAllowedError') {
                // Branch to code for requesting permission.
            } else if (event.error.name === 'NotReadableError' ) {
                console.log('Cannot connect to the sensor.');
            }
        });
        acl.addEventListener('reading', () => {
            console.log("Acceleration along the X-axis " + acl.x);
            console.log("Acceleration along the Y-axis " + acl.y);
            console.log("Acceleration along the Z-axis " + acl.z);
        });
    } catch (error) {
        // Handle construction errors.
        if (error.name === 'SecurityError') {
            // See the note above about feature policy.
            console.log('Sensor construction was blocked by a feature policy.');
        } else if (error.name === 'ReferenceError') {
            console.log('Sensor is not supported by the User Agent.');
        } else {
            throw error;
        }
    }
}

function gyroscope_setup() {}
function magnetometer_setup() {}
function geolocation_setup() {
    window.trainer.statusHistory = {1: 0, 2: 0, 3: 0, 'success': 0};
    function success(position) {
        const current_time = Date.now();
        window.trainer.statusHistory.success += 1;

        const position_time = position.timestamp;

        const coords = position.coords;
        const latitude  = coords.latitude;
        const longitude = coords.longitude;
        const metersError = coords.accuracy;
        const speed = coords.speed;
        const heading = coords.heading;
        const altitude = coords.altitude;

        window.trainer.latest = {
            coords,
            latitude,
            longitude,
            metersError,
            altitude,
            speed,
            heading,
        };
        window.trainer.latest_text = {};
        Object.assign(window.trainer.latest_text, window.trainer.latest);
        clean_latest(window.trainer.latest_text);

        if (window.trainer.start_time === undefined) {
            window.trainer.start_time = current_time; 
        }
        window.trainer.end_time = current_time;

        if (!!speed && !!heading) {
        }
        print('speed and heading: ', speed, heading);

        print('position');
        print(position.coords);

        const time_delta = current_time - position_time;
        print("delta", time_delta);
        print("lat, long: ", latitude, longitude);
    }

    function error(error) {
        const code = error.code;

        window.trainer.statusHistory[code] += 1;
        if (window.trainer.statusHistory[code] <= 1) {
            if (code == 1) {
                print("Location permission denied");
            }
            if (code == 2) {
                print("Location unavailable");
            }
            if (code == 3) {
                print("Location timed out :(");
            }
        }
    }

    if(!navigator.geolocation) {
        print('Geolocation is not supported by your browser');
    } else {
        print('Locating...');
        navigator.geolocation.watchPosition(success, error, location_config());
    }
}

function clean_latest(latest) {
    const options = ["latitude", "longitude", "metersError", "speed", "heading", "altitude"];
    for (const index in options) {
        try {
            latest[options[index]] = latest[options[index]].toPrecision(10);
        } catch (error) {}
    }
}

function render_once() {
    print('render');
    if (window.trainer.content_element === undefined) {
        window.trainer.content_element = document.getElementById('content');
    }

    const latest = window.trainer.latest_text;

    for (const key in latest) {
        var element = document.getElementById(key);
        if (element === null) {
            continue;
        }
        if (latest[key] === null) {
            continue;
        }
        print(key, latest[key]);
        element.textContent = latest[key]; 
    }
}

function setup() {
    window.trainer = {
        runtime: 100,
    };

    ask_permission('accelerometer', accelerometer_setup);
    ask_permission('gyroscope', gyroscope_setup);
    ask_permission('magnetometer', magnetometer_setup);
    ask_permission('geolocation', geolocation_setup);

    window.trainer.renderId = window.setInterval(render_once, 1000);
    window.setTimeout(teardown, window.trainer.runtime * 1000);
}

function humanizeGeolocationErrors(statusHistory) {
    statusHistory.permission_denied = statusHistory[1];
    statusHistory.unavailable = statusHistory[2];
    statusHistory.timed_out = statusHistory[3];

    statusHistory.totalEvents = statusHistory.permission_denied + statusHistory.unavailable + statusHistory.timed_out + statusHistory.success;

    return statusHistory;
}

function teardown() {
    const trainer = window.trainer;
    navigator.geolocation.clearWatch(window.trainer.watchID);
    window.clearInterval(trainer.intervalId);
    window.clearInterval(trainer.renderId);

    print("Tearing down geolocation");
    print("Run time: ", (trainer.end_time - trainer.start_time) / 1000.0);
    print("Error codes: ", humanizeGeolocationErrors(window.trainer.statusHistory));
}

setup();

