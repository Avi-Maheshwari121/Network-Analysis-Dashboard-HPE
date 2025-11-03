import React from 'react';
import GeoMap from '../components/GeoMap';
import StatusBanner from '../components/StatusBanner';

export default function GeoMapPage({ geolocations, wsConnected, error, metrics }) {
  
  return (
    <div>
      <StatusBanner 
        connected={wsConnected} 
        error={error} 
        metrics={metrics}
      />
      <h1 className="text-lg font-bold text-primary-accent mb-1">Traffic Geolocation Map</h1>
      <p className="text-s text-text-secondary mb-4">
        This map displays the geographic location of public destination IP addresses captured during the entire session.
      </p>
      <GeoMap locations={geolocations} />
      
    </div>
  );
}