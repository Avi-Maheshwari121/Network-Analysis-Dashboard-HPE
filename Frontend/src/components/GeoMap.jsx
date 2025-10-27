import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css'; // Import Leaflet's CSS

export default function GeoMap({ locations = [] }) {
  const mapPosition = [20, 0]; // A neutral starting map position
  const mapZoom = 2;

  return (
    <div className="bg-base-dark p-4 rounded-lg shadow-md border border-border-dark h-[75vh]">
      <MapContainer 
        center={mapPosition} 
        zoom={mapZoom} 
        scrollWheelZoom={true} 
        style={{ height: '100%', width: '100%', borderRadius: '8px', backgroundColor: '#1f2937' }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {locations.map((loc, index) => (
          <Marker key={`${loc.ip}-${index}`} position={[loc.latitude, loc.longitude]}>
            <Popup>
              <b>IP:</b> {loc.ip}<br />
              <b>Location:</b> {loc.city}, {loc.country}
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}