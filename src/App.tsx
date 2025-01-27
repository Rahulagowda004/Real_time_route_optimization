import React, { useState } from "react";
import { Map } from "./components/Map";
import { Metrics } from "./components/Metrics";
import { OrderForm } from "./components/OrderForm";
import { TrendChart } from "./components/TrendChart";
import { DeliveryOrder, RoutePoint, DeliveryMetrics } from "./types";
import { MapPin } from "lucide-react";

// Example data - in a real app, this would come from an API
const initialRoutes: RoutePoint[] = [
  { lat: 51.505, lng: -0.09 },
  { lat: 51.51, lng: -0.1 },
  { lat: 51.515, lng: -0.09 },
];

const initialMetrics: DeliveryMetrics = {
  totalDeliveries: 156,
  averageTime: 28,
  vehicleUtilization: 85,
};

const trendData = Array.from({ length: 24 }, (_, i) => ({
  timestamp: new Date(2024, 0, 1, i).toISOString(),
  deliveryTime: 20 + Math.random() * 20,
  traffic: 40 + Math.random() * 60,
  temperature: 15 + Math.random() * 10,
}));

function App() {
  const [routes] = useState<RoutePoint[]>(initialRoutes);
  const [metrics] = useState<DeliveryMetrics>(initialMetrics);

  const handleOrderSubmit = (order: Omit<DeliveryOrder, "id" | "status">) => {
    console.log("New order:", order);
    // In a real app, this would be sent to an API
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center space-x-2">
            <MapPin className="w-8 h-8 text-blue-500" />
            <h1 className="text-2xl font-bold text-gray-900">
              Route Optimization Dashboard
            </h1>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        <div className="space-y-6">
          <Metrics metrics={metrics} />

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <Map routes={routes} center={[51.505, -0.09]} />
            </div>
            <div>
              <OrderForm onSubmit={handleOrderSubmit} />
            </div>
          </div>

          <TrendChart data={trendData} />
        </div>
      </main>
    </div>
  );
}

export default App;
