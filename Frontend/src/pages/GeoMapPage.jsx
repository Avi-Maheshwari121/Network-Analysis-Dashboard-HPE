import React from 'react';
import GeoMap from '../components/GeoMap';

export default function GeoMapPage({ geolocations, wsConnected, error, metrics }) {
  
  return (
    <div>
      <h1 className="text-3xl font-bold mb-6 text-text-primary">Traffic Geolocation Map</h1>
      <p className="text-text-secondary mb-4">
        This map displays the geographic location of public destination IP addresses captured during the entire session.
      </p>
      <GeoMap locations={geolocations} />
      
    </div>
  );
}