import { useState } from 'react';
import { DeliveryOrder, PredictionRequest } from '../types';
import { PackagePlus, Clock } from 'lucide-react';
import { predictDeliveryTime } from '../services/api';

interface OrderFormProps {
  onSubmit: (order: Omit<DeliveryOrder, 'id' | 'status'>) => void;
}

export function OrderForm({ onSubmit }: OrderFormProps) {
  const [formData, setFormData] = useState({
    pickupAddress: '',
    address: '',
    city: '',
  });
  const [predictedTime, setPredictedTime] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const cityOptions = ['Urban', 'Metropolitan', 'Semi-Urban'];

  const handlePredict = async () => {
    if (!formData.pickupAddress || !formData.address || !formData.city) {
      setError('Please fill in all required fields');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const predictionRequest: PredictionRequest = {
        pickupAddress: formData.pickupAddress,
        address: formData.address,
        city: formData.city,
      };

      const predicted = await predictDeliveryTime(predictionRequest);
      setPredictedTime(predicted);
    } catch (err) {
      setError('Failed to predict delivery time');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!predictedTime) {
      setError('Please get a delivery time prediction first');
      return;
    }

    onSubmit({
      ...formData,
      predictedTime,
    });

    setFormData({
      pickupAddress: '',
      address: '',
      city: '',
    });
    setPredictedTime(null);
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg">
      <div className="flex items-center space-x-2 mb-4">
        <PackagePlus className="w-6 h-6 text-blue-500" />
        <h2 className="text-xl font-semibold">New Delivery Order</h2>
      </div>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Pickup Address</label>
          <input
            type="text"
            required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            value={formData.pickupAddress}
            onChange={(e) => setFormData(prev => ({ ...prev, pickupAddress: e.target.value }))}
            placeholder="Enter pickup address"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Delivery Address</label>
          <input
            type="text"
            required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            value={formData.address}
            onChange={(e) => setFormData(prev => ({ ...prev, address: e.target.value }))}
            placeholder="Enter delivery address"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700">City Type</label>
          <select
            required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            value={formData.city}
            onChange={(e) => setFormData(prev => ({ ...prev, city: e.target.value }))}
          >
            <option value="">Select city type</option>
            {cityOptions.map(city => (
              <option key={city} value={city}>
                {city}
              </option>
            ))}
          </select>
        </div>

        {error && (
          <div className="text-red-500 text-sm">{error}</div>
        )}

        {predictedTime && (
          <div className="flex items-center space-x-2 p-3 bg-blue-50 rounded-md">
            <Clock className="w-5 h-5 text-blue-500" />
            <span className="text-blue-700">
              Predicted delivery time: {predictedTime} minutes
            </span>
          </div>
        )}
        
        <div className="grid grid-cols-2 gap-4">
          <button
            type="button"
            onClick={handlePredict}
            disabled={isLoading}
            className="w-full bg-gray-100 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-200 transition-colors disabled:opacity-50"
          >
            {isLoading ? 'Predicting...' : 'Predict Time'}
          </button>
          
          <button
            type="submit"
            disabled={!predictedTime || isLoading}
            className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 transition-colors disabled:opacity-50"
          >
            Submit Order
          </button>
        </div>
      </form>
    </div>
  );
}