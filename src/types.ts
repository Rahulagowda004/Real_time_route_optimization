export interface DeliveryOrder {
  id?: string;
  pickupAddress: string;
  address: string;
  city: string;
  status?: "pending" | "delivered";
  predictedTime?: number | null; // Update type to include null
}

export interface PredictionRequest {
  pickupAddress: string;
  address: string;
  city: string;
}

export interface RoutePoint {
  lat: number;
  lng: number;
}

export interface DeliveryMetrics {
  totalDeliveries: number;
  averageTime: number;
  vehicleUtilization: number;
}
