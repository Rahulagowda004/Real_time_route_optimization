import React, { useState, useEffect } from "react";
import { Map } from "./components/Map";
import { Metrics } from "./components/Metrics";
import { OrderForm } from "./components/OrderForm";
import { TrendChart } from "./components/TrendChart";
import { RoutePoint, DeliveryMetrics } from "./types";
import { MapPin } from "lucide-react";

const initialMetrics: DeliveryMetrics = {
  totalDeliveries: 156,
  averageTime: 28,
  vehicleUtilization: 85,
  totalCost: 123.56,
};

function App() {
  const [metrics, setMetrics] = useState<DeliveryMetrics>(initialMetrics);
  const [routes, setRoutes] = useState<RoutePoint[]>([]);
  const [trendData, setTrendData] = useState<any[]>([]);

  useEffect(() => {
    async function fetchMetrics() {
      const response = await fetch("http://localhost:5000/metrics");
      const data = await response.json();
      setMetrics(data);
    }

    async function fetchRoutes() {
      const response = await fetch("http://localhost:5000/routes");
      const data = await response.json();
      setRoutes(data);
    }

    async function fetchTrendData() {
      const response = await fetch("http://localhost:5000/trendData");
      const data = await response.json();
      setTrendData(data);
    }

    fetchMetrics();
    fetchRoutes();
    fetchTrendData();
  }, []);

  const handleOrderSubmit = async (orderData: any) => {
    // Handle order submission logic here
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
