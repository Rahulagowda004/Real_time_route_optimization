const API_BASE_URL = 'http://localhost:5000'; // Update to point to Flask backend

export async function predictDeliveryTime(data: PredictionRequest): Promise<number> {
  try {
    const response = await fetch(`${API_BASE_URL}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error('Failed to predict delivery time');
    }

    const result = await response.json();
    return result.predicted_time;
  } catch (error) {
    console.error('Error predicting delivery time:', error);
    throw error;
  }
}

export async function geocodeAddress(address: string): Promise<{ lat: number; lng: number }> {
  try {
    const response = await fetch(`${API_BASE_URL}/geocode`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ address }),
    });

    if (!response.ok) {
      throw new Error('Failed to geocode address');
    }

    return await response.json();
  } catch (error) {
    console.error('Error geocoding address:', error);
    throw error;
  }
}