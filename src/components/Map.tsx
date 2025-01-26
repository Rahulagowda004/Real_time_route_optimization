import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet';
import { RoutePoint } from '../types';
import { Truck } from 'lucide-react';

interface MapProps {
  routes: RoutePoint[];
  center: [number, number];
}

export function Map({ routes, center }: MapProps) {
  return (
    <div className="h-[500px] w-full rounded-lg overflow-hidden shadow-lg">
      <MapContainer
        center={center}
        zoom={13}
        className="h-full w-full"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {routes.map((point, index) => (
          <Marker key={index} position={[point.lat, point.lng]}>
            {point.order && (
              <Popup>
                <div className="p-2">
                  <h3 className="font-semibold">{point.order.customerName}</h3>
                  <p className="text-sm">{point.order.address}</p>
                  <p className="text-xs text-gray-500">
                    Requested: {new Date(point.order.requestedTime).toLocaleTimeString()}
                  </p>
                </div>
              </Popup>
            )}
          </Marker>
        ))}
        <Polyline 
          positions={routes.map(point => [point.lat, point.lng])}
          color="#3B82F6"
          weight={3}
          opacity={0.7}
        />
      </MapContainer>
    </div>
  );
}