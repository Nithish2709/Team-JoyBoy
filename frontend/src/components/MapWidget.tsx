import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import Badge from './Badge';

// Fix for default Leaflet icon paths in React
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

// Custom Icon for anomalies
const anomalyIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

type Hotspot = {
  id: string;
  name: string;
  lat: number;
  lng: number;
  severity: 'danger' | 'warning';
  issue: string;
};

const mockHotspots: Hotspot[] = [
  { id: '1', name: 'FPS 034 - Anna Nagar', lat: 13.0850, lng: 80.2100, severity: 'danger', issue: 'Critical Stock Variance' },
  { id: '2', name: 'FPS 102 - T. Nagar', lat: 13.0400, lng: 80.2330, severity: 'warning', issue: 'POS Device Offline' },
  { id: '3', name: 'FPS 088 - Mylapore', lat: 13.0334, lng: 80.2673, severity: 'danger', issue: 'Ghost Lifting Suspected' },
  { id: '4', name: 'FPS 214 - Velachery', lat: 12.9815, lng: 80.2180, severity: 'warning', issue: 'Low Stock Alert' },
  { id: '5', name: 'FPS 012 - Madurai', lat: 9.9252, lng: 78.1198, severity: 'danger', issue: 'Shop Closed Unscheduled' },
];

export default function MapWidget() {
  const centerPosition: [number, number] = [11.1271, 78.6569]; // Center of Tamil Nadu

  return (
    <div className="h-full w-full rounded-lg overflow-hidden border border-slate-200 dark:border-slate-700 z-0 relative isolate">
      <MapContainer 
        center={centerPosition} 
        zoom={6} 
        scrollWheelZoom={false} 
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a>'
          url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
        />
        {mockHotspots.map((spot) => (
          <Marker 
            key={spot.id} 
            position={[spot.lat, spot.lng]} 
            icon={anomalyIcon}
          >
            <Popup className="custom-popup">
              <div className="p-1">
                <h4 className="font-bold text-slate-900 mb-1">{spot.name}</h4>
                <p className="text-sm text-slate-600 mb-2">{spot.issue}</p>
                <Badge variant={spot.severity}>{spot.severity.toUpperCase()}</Badge>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}
