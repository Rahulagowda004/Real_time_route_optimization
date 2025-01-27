import { PredictionRequest } from "../types";

const API_BASE_URL = "http://localhost:5000"; // Update to point to Flask backend

interface PredictionResponse {
  predicted_time: number;
  pickup: {
    lat: number;
    lng: number;
  };
  delivery: {
    lat: number;
    lng: number;
  };
}

export async function predictDeliveryTime(
  data: PredictionRequest
): Promise<PredictionResponse> {
  try {
    console.log("Sending prediction request:", data); // Add logging
    const response = await fetch(`${API_BASE_URL}/predict`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    console.log("Raw prediction response:", result);

    // Validate response structure
    if (!result.pickup || !result.delivery) {
      throw new Error("Invalid response format from server");
    }

    console.log("Prediction response:", result); // Add logging
    return result;
  } catch (error) {
    console.error("Error predicting delivery time:", error);
    throw error;
  }
}

export async function geocodeAddress(
  address: string
): Promise<{ lat: number; lng: number }> {
  try {
    const response = await fetch(`${API_BASE_URL}/geocode`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ address }),
    });

    if (!response.ok) {
      throw new Error("Failed to geocode address");
    }

    return await response.json();
  } catch (error) {
    console.error("Error geocoding address:", error);
    throw error;
  }
}
