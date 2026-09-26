document.addEventListener('DOMContentLoaded', () => {
  const mapSelector = new MapSelector('map');
  const btn = document.getElementById('generateBtn');
  const statusEl = document.getElementById('status');

  btn.addEventListener('click', async () => {
    btn.disabled = true;
    statusEl.innerText = "Querying OpenStreetMap & Gathering Signs...";

    const payload = {
      bbox: mapSelector.getBounds(),
      spawn: mapSelector.getSpawnPoint(),
      version: document.getElementById('version').value,
      spawnCars: document.getElementById('spawnCars').checked,
      renderMapSigns: document.getElementById('renderMapSigns').checked
    };

    try {
      const response = await fetch('/api/generate-world', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error(`Server returned status ${response.status}`);
      }

      statusEl.innerText = "Downloading World Save ZIP...";
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `OSM_World_${payload.version}.zip`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      statusEl.innerText = "World successfully generated!";
    } catch (err) {
      console.error(err);
      statusEl.innerText = "Error generating world. See console.";
    } finally {
      btn.disabled = false;
    }
  });
});
