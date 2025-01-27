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
  const markerRef = useRef<L.Marker | null>(null);

  useEffect(() => {
    if (routes.length >= 2) {
      const taxiIcon = L.icon({
        iconUrl: "img/taxi.png",
        iconSize: [70, 70],
      });

      if (!markerRef.current) {
        markerRef.current = L.marker([routes[0].lat, routes[0].lng], {
          icon: taxiIcon,
        }).addTo(map);
      }

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

      routingControlRef.current.on("routesfound", function (e) {
        e.routes[0].coordinates.forEach((coord, index) => {
          setTimeout(() => {
            markerRef.current?.setLatLng([coord.lat, coord.lng]);
          }, 100 * index);
        });
      });

      map.fitBounds([
        [routes[0].lat, routes[0].lng],
        [routes[1].lat, routes[1].lng],
      ]);
    }

    return () => {
      if (routingControlRef.current) {
        map.removeControl(routingControlRef.current);
      }
      if (markerRef.current) {
        map.removeLayer(markerRef.current);
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
