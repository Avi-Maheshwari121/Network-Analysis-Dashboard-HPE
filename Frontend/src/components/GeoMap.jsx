import React, { useState, useMemo } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';


export default function GeoMap({ locations = [] }) {
  const [selectedCategory, setSelectedCategory] = useState('All');
  const mapPosition = [20, 0];
  const mapZoom = 2;

  // Group locations by coordinate
  const locationsByCoordinate = useMemo(() => {
    const groups = new Map();
    locations.forEach(loc => {
      if (loc.latitude === undefined || loc.longitude === undefined) return;
      const key = `${loc.latitude},${loc.longitude}`;
      
      if (!groups.has(key)) {
        groups.set(key, []);
      }
      groups.get(key).push(loc);
    });
    return Array.from(groups.values());
  }, [locations]);

  // Category sorting logic
  const categories = useMemo(() => {
    const allCategories = new Set();
    locationsByCoordinate.forEach(group => {
      group.forEach(loc => {
        if (loc.app_info?.category) {
          allCategories.add(loc.app_info.category);
        }
      });
    });
    const sorted = Array.from(allCategories).filter(c => c !== 'Other').sort();
    if (allCategories.has('Other')) {
      sorted.push('Other');
    }
    return ['All', ...sorted];
  }, [locationsByCoordinate]);

  // Filter groups based on the selected category
  const displayGroups = useMemo(() => {
    if (selectedCategory === 'All') {
      return locationsByCoordinate;
    }
    // Keep a group if *any* location in it matches the selected category
    return locationsByCoordinate.filter(group => 
      group.some(loc => loc.app_info?.category === selectedCategory)
    );
  }, [locationsByCoordinate, selectedCategory]);

  const markerCount = displayGroups.length;

  return (
    <div className="bg-base-dark p-4 rounded-lg shadow-md border border-border-dark h-[75vh] flex flex-col">
      {/* Filter and Counter Bar */}
      <div className="mb-4 flex justify-between items-center">
        <div>
          <label htmlFor="category-filter" className="text-text-secondary mr-2">Filter by Category:</label>
          <select
            id="category-filter"
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="bg-base-dark border border-border-dark text-text-primary rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {categories.map(category => (
              <option key={category} value={category} className="bg-base-dark text-text-primary">
                {category}
              </option>
            ))}
          </select>
        </div>
        
        <div className="text-text-secondary text-lg">
          Pins: <span className="font-bold text-teal-400">{markerCount}</span>
        </div>
      </div>

      {/* Map Container */}
      <div className="flex-grow">
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
          
          {displayGroups.map((group, index) => {
            const firstLoc = group[0]; 

            // Create a filtered list *for the popup*
            const locationsToShowInPopup = (selectedCategory === 'All')
              ? group // If 'All' is selected, show the whole group
              : group.filter(loc => loc.app_info?.category === selectedCategory); // Otherwise, filter the group


            return (
              <Marker 
                key={index}
                position={[firstLoc.latitude, firstLoc.longitude]}
              >
                <Popup>
                  <div className="max-h-60 overflow-y-auto pr-2">
                    <h3 className="font-bold text-lg mb-1">{firstLoc.city}, {firstLoc.country}</h3>
                    
                    <hr className="border-border-dark my-2" />
                    
                    {locationsToShowInPopup.map(loc => (
                      <div key={loc.ip} className="mb-2 text-sm">
                        <b>App:</b> {loc.app_info?.app || 'Unknown'} ({loc.app_info?.category || 'Other'})
                        <br />
                        <b>IP:</b> {loc.ip}
                        
                        {(loc.dns_name || loc.hostname) && (
                          <>
                            <br />
                            <b>Hostname:</b> {loc.dns_name || loc.hostname}
                          </>
                        )}
                      </div>
                    ))}
                  </div>
                </Popup>
              </Marker>
            );
          })}
        </MapContainer>
      </div>
    </div>
  );
}