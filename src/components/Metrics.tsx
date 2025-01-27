import { Card, Metric, Text } from "@tremor/react";
import { Clock, Truck, DollarSign, BarChart3 } from "lucide-react";
import { DeliveryMetrics } from "../types";

interface MetricsProps {
  metrics: DeliveryMetrics;
}

export function Metrics({ metrics }: MetricsProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      <Card decoration="top" decorationColor="blue">
        <div className="flex items-center space-x-2">
          <Clock className="w-6 h-6 text-blue-500" />
          <Text>Average Delivery Time</Text>s
        </div>
        <Metric>{metrics.averageTime} mins</Metric>
      </Card>

      <Card decoration="top" decorationColor="green">
        <div className="flex items-center space-x-2">
          <Truck className="w-6 h-6 text-green-500" />
          <Text>Vehicle Utilization</Text>
        </div>
        <Metric>{metrics.vehicleUtilization}%</Metric>
      </Card>

      <Card decoration="top" decorationColor="purple">
        <div className="flex items-center space-x-2">
          <BarChart3 className="w-6 h-6 text-purple-500" />
          <Text>Total Deliveries</Text>
        </div>
        <Metric>{metrics.totalDeliveries}</Metric>
      </Card>
    </div>
  );
}
