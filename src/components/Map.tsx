import { useEffect, useRef } from "react";
import { MapContainer, TileLayer, Marker, useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { RoutePoint } from "../types";

// Import routing machine after leaflet
import "leaflet-routing-machine/dist/leaflet-routing-machine.css";
import "leaflet-routing-machine";

interface MapProps {
  routes: RoutePoint[];
  center: [number, number];
}

interface RouteDirection {
  distance: number;
  duration: number;
  instructions: string[];
  path: Array<[number, number]>; // Add this to store route coordinates
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

      // Capture route details and send to backend
      routingControlRef.current.on("routesfound", async function (e) {
        const route = e.routes[0];
        const directions: RouteDirection = {
          distance: route.summary.totalDistance,
          duration: route.summary.totalTime,
          instructions: route.instructions.map(
            (instruction) => instruction.text
          ),
          path: route.coordinates.map((coord) => [coord.lat, coord.lng]),
        };

        try {
          const response = await fetch(
            "http://localhost:5000/route-directions",
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                pickup: routes[0],
                delivery: routes[1],
                directions,
              }),
            }
          );
          const data = await response.json();
          console.log("Route saved:", data);
        } catch (error) {
          console.error("Failed to send route directions:", error);
        }
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
