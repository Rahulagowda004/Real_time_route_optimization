import { useEffect, useRef } from "react";
import { MapContainer, TileLayer, Marker, useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet-routing-machine";
import { RoutePoint } from "../types";

interface MapProps {
  routes: RoutePoint[];
  center: [number, number];
}

function RoutingMachineControl({ routes }: { routes: RoutePoint[] }) {
  const map = useMap();
  const routingControlRef = useRef<L.Routing.Control | null>(null);

  useEffect(() => {
    if (routes.length >= 2) {
      if (routingControlRef.current) {
        map.removeControl(routingControlRef.current);
      }

      routingControlRef.current = L.Routing.control({
        waypoints: [
          L.latLng(routes[0].lat, routes[0].lng),
          L.latLng(routes[1].lat, routes[1].lng),
        ],
        show: false,
        addWaypoints: false,
        routeWhileDragging: false,
        fitSelectedRoutes: true,
        showAlternatives: false,
      }).addTo(map);

      // Hide the control container
      const container = routingControlRef.current.getContainer();
      container.style.display = "none";

      map.fitBounds([
        [routes[0].lat, routes[0].lng],
        [routes[1].lat, routes[1].lng],
      ]);
    }

    return () => {
      if (routingControlRef.current) {
        map.removeControl(routingControlRef.current);
      }
    };
  }, [map, routes]);

  return null;
}

export function Map({ routes, center }: MapProps) {
  return (
    <div className="h-[500px] w-full rounded-lg overflow-hidden shadow-lg">
      <MapContainer center={center} zoom={13} className="h-full w-full">
        <TileLayer
          attribution='&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
          url="http://{s}.tile.osm.org/{z}/{x}/{y}.png"
        />
        <RoutingMachineControl routes={routes} />
        {routes.map((point, index) => (
          <Marker key={index} position={[point.lat, point.lng]} />
        ))}
      </MapContainer>
    </div>
  );
}
