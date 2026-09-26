class MapSelector {
  constructor(mapId) {
    this.map = L.map(mapId).setView([28.5383, -81.3792], 16);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(this.map);

    this.spawnMarker = L.marker([28.5383, -81.3792], {
      draggable: true,
      title: "Spawn Point"
    }).addTo(this.map);

    this.spawnMarker.bindPopup("Player Spawn Point").openPopup();
    
    this.map.on('moveend', () => {
      this.updateCoordsDisplay();
    });
  }

  getBounds() {
    const b = this.map.getBounds();
    return [b.getSouth(), b.getWest(), b.getNorth(), b.getEast()];
  }

  getSpawnPoint() {
    const latLng = this.spawnMarker.getLatLng();
    return { lat: latLng.lat, lon: latLng.lng };
  }

  updateCoordsDisplay() {
    const b = this.getBounds();
    const el = document.getElementById('bboxCoords');
    if (el) {
      el.innerText = `BBOX: ${b[0].toFixed(4)}, ${b[1].toFixed(4)}, ${b[2].toFixed(4)}, ${b[3].toFixed(4)}`;
    }
  }
}
window.MapSelector = MapSelector;
