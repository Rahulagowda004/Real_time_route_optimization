import { useState } from "react";
import { DeliveryOrder } from "../types";
import { PackagePlus, Clock } from "lucide-react";

interface OrderFormProps {
  onSubmit: (order: Omit<DeliveryOrder, "id" | "status">) => Promise<void>;
  isLoading?: boolean;
  predictedTime?: number | null; // Update type to include null
}

export function OrderForm({
  onSubmit,
  isLoading,
  predictedTime,
}: OrderFormProps) {
  const [formData, setFormData] = useState({
    pickupAddress: "",
    address: "",
    city: "",
  });

  const cityOptions = ["Urban", "Metropolitan", "Semi-Urban"];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await onSubmit(formData); // Simplified to just pass form data
    } catch (error) {
      console.error("Form submission error:", error);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg">
      <div className="flex items-center space-x-2 mb-4">
        <PackagePlus className="w-6 h-6 text-blue-500" />
        <h2 className="text-xl font-semibold">New Delivery Order</h2>
      </div>

      {predictedTime && (
        <div className="mb-4 p-3 bg-green-50 rounded-md flex items-center space-x-2">
          <Clock className="w-5 h-5 text-green-500" />
          <span className="text-green-700">
            Predicted delivery time: {predictedTime.toFixed(2)} minutes
          </span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">
            Pickup Address
          </label>
          <input
            type="text"
            required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            value={formData.pickupAddress}
            onChange={(e) =>
              setFormData((prev) => ({
                ...prev,
                pickupAddress: e.target.value,
              }))
            }
            placeholder="Enter pickup address"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">
            Delivery Address
          </label>
          <input
            type="text"
            required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            value={formData.address}
            onChange={(e) =>
              setFormData((prev) => ({ ...prev, address: e.target.value }))
            }
            placeholder="Enter delivery address"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">
            City Type
          </label>
          <select
            required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            value={formData.city}
            onChange={(e) =>
              setFormData((prev) => ({ ...prev, city: e.target.value }))
            }
          >
            <option value="">Select city type</option>
            {cityOptions.map((city) => (
              <option key={city} value={city}>
                {city}
              </option>
            ))}
          </select>
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 transition-colors disabled:opacity-50"
        >
          {isLoading ? "Predicting..." : "Submit Order"}
        </button>
      </form>
    </div>
  );
}
