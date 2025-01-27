export interface DeliveryOrder {
  id: string;
  pickupAddress: string;
  address: string;
  city: string;
  status: "pending" | "in-progress" | "delivered";
  predictedTime?: number;
}

export interface PredictionRequest {
  pickupAddress: string;
  address: string;
  city: string;
}

export interface RoutePoint {
  lat: number;
  lng: number;
  order?: DeliveryOrder;
}

export interface DeliveryMetrics {
  totalDeliveries: number;
  averageTime: number;
  vehicleUtilization: number;
}
