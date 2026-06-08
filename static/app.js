document.addEventListener("DOMContentLoaded", () => {
    if (!document.body.className) {
        document.body.className = "default";
    }

    const mapEl = document.getElementById('map');
    if (!mapEl) return;

    const map = L.map('map').setView([20, 0], 2);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    map.on('click', function(e) {
        const lat = e.latlng.lat;
        const lon = e.latlng.lng;
        window.location.href = `/location?lat=${lat}&lon=${lon}`;
    });

    const locationButton = document.getElementById('location-button');
    if (locationButton) {
        locationButton.addEventListener('click', function(event) {
            event.preventDefault();
            if (!navigator.geolocation) {
                alert("Geolocation not supported");
                return;
            }
            navigator.geolocation.getCurrentPosition(function(position) {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                window.location.href = `/location?lat=${lat}&lon=${lon}`;
            }, function() {
                alert("Unable to fetch location");
            });
        });
    }
});