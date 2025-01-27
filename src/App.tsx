import React, { useState } from "react";
import { Map } from "./components/Map";
import { Metrics } from "./components/Metrics";
import { OrderForm } from "./components/OrderForm";
import { TrendChart } from "./components/TrendChart";
import {
  DeliveryOrder,
  RoutePoint,
  DeliveryMetrics,
  PredictionRequest,
} from "./types";
import { MapPin } from "lucide-react";
import { predictDeliveryTime } from "./services/api";

// Example data - in a real app, this would come from an API
const initialRoutes: RoutePoint[] = [
  { lat: 51.505, lng: -0.09 },
  { lat: 51.51, lng: -0.1 },
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
  const [routes, setRoutes] = useState<RoutePoint[]>([]);
  const [metrics, setMetrics] = useState<DeliveryMetrics>(initialMetrics); // Use this state variable
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [predictedTime, setPredictedTime] = useState<number | null>(null); // Add this state

  const handleOrderSubmit = async (
    order: Omit<DeliveryOrder, "id" | "status">
  ) => {
    try {
      setIsLoading(true);
      setError(null);
      setPredictedTime(null); // Reset prediction

      const prediction = await predictDeliveryTime(order);
      console.log("Prediction response:", prediction);

      if (prediction.pickup && prediction.delivery) {
        setRoutes([prediction.pickup, prediction.delivery]);
        setPredictedTime(prediction.predicted_time); // Set the predicted time
      }
    } catch (error) {
      console.error("Error:", error);
      setError(
        error instanceof Error ? error.message : "Failed to predict route"
      );
    } finally {
      setIsLoading(false);
    }
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
          <Metrics metrics={metrics} /> {/* Now using the metrics state */}
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <Map
                routes={routes}
                center={
                  routes.length > 0
                    ? [routes[0].lat, routes[0].lng]
                    : [22.745049, 75.892471]
                }
              />
            </div>
            <div>
              <OrderForm
                onSubmit={handleOrderSubmit}
                isLoading={isLoading}
                predictedTime={predictedTime} // Pass predicted time to OrderForm
              />
            </div>
          </div>
          <TrendChart data={trendData} />
        </div>
      </main>
    </div>
  );
}

export default App;
