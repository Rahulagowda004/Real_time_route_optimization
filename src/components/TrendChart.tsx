import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { format } from 'date-fns';

interface TrendData {
  timestamp: string;
  deliveryTime: number;
  traffic: number;
  temperature: number;
}

interface TrendChartProps {
  data: TrendData[];
}

export function TrendChart({ data }: TrendChartProps) {
  return (
    <div className="bg-white p-6 rounded-lg shadow-lg">
      <h2 className="text-xl font-semibold mb-4">Delivery Trends</h2>
      <div className="h-[300px]">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="timestamp" 
              tickFormatter={(value) => format(new Date(value), 'HH:mm')}
            />
            <YAxis yAxisId="left" />
            <YAxis yAxisId="right" orientation="right" />
            <Tooltip 
              labelFormatter={(value) => format(new Date(value), 'PP p')}
            />
            <Legend />
            <Line
              yAxisId="left"
              type="monotone"
              dataKey="deliveryTime"
              stroke="#3B82F6"
              name="Delivery Time (mins)"
            />
            <Line
              yAxisId="right"
              type="monotone"
              dataKey="traffic"
              stroke="#EF4444"
              name="Traffic Index"
            />
            <Line
              yAxisId="right"
              type="monotone"
              dataKey="temperature"
              stroke="#10B981"
              name="Temperature (°C)"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}