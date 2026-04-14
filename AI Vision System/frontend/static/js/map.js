document.addEventListener('DOMContentLoaded', () => {
    // Initialize Map on Serengeti center
    const map = L.map('map').setView([-2.3333, 34.8333], 10);

    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; OpenStreetMap &copy; CARTO',
        subdomains: 'abcd',
        maxZoom: 20
    }).addTo(map);

    const markers = [];

    window.updateMapAlerts = function (alerts) {
        // Clear old markers
        markers.forEach(m => map.removeLayer(m));
        markers.length = 0;

        if (alerts.length === 0) return;

        alerts.forEach(alert => {
            const marker = L.circleMarker([alert.lat, alert.lon], {
                radius: 10,
                fillColor: alert.severity === 'High' ? '#ef4444' : '#f59e0b',
                color: '#fff',
                weight: 1,
                opacity: 0.8,
                fillOpacity: 0.6
            }).addTo(map);

            marker.bindPopup(`<b>${alert.type}</b><br>${alert.message}`);
            markers.push(marker);
        });

        // Zoom to fit markers
        const group = new L.featureGroup(markers);
        map.fitBounds(group.getBounds().pad(0.5));
    };
});
