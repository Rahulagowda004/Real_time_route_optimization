---
# Real-Time Route Optimization 🚚

A cutting-edge system designed to revolutionize delivery operations by optimizing routes in real-time, accounting for traffic, delivery constraints, and dynamic conditions.
---

## 🌟 Features

- **Real-Time Route Optimization**  
  Continuously calculates the most efficient routes based on current conditions.

- **Multi-Vehicle Support**  
  Seamlessly handles fleet routing to maximize efficiency.

- **Dynamic Traffic Integration**  
  Adapts to real-time traffic and weather changes to ensure timely deliveries.

- **Delivery Time Windows**  
  Guarantees adherence to customer delivery schedules.

- **Load Balancing**  
  Optimizes vehicle capacity utilization for cost efficiency.

- **Live Order Tracking**  
  Provides real-time updates and order tracking.

---

## 🚀 Quick Start

### 🛠 Backend Setup

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/rahulagowda004/real_time_route_optimization.git
   cd real_time_route_optimization
   ```

2. **Create a Virtual Environment**:

   ```bash
   python3.11 -m venv .venv
   source .venv/bin/activate  # For Windows, use .venv\Scripts\activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Backend Server**:
   ```bash
   python app.py
   ```

### 🖼 Frontend Setup

1. **Navigate to the Frontend Directory** (if applicable):

   ```bash
   cd frontend
   ```

2. **Install Node.js Dependencies**:

   ```bash
   npm install
   ```

3. **Start the Frontend Server**:
   ```bash
   npm run dev
   ```

---

## 🛠 Configuration

All customizable settings are located in `config/config.yaml`. Adjust as necessary:

- **Vehicle Specifications**: Speed, capacity, and number of vehicles.
- **Delivery Constraints**: Time windows and maximum route durations.
- **Optimization Algorithms**: Choose from algorithms like Dijkstra, A\*, or custom methods.
- **Mapping API Keys**: Integrate third-party mapping services for precise navigation.

---

## 📂 Directory Structure

```
real_time_route_optimization/
├── README.md             # Project Documentation
├── LICENSE               # Licensing Information
├── app.py                # Backend Application
├── requirements.txt      # Python Dependencies
├── config/               # Configuration Files
│   └── config.yaml
├── artifacts/            # Model & Preprocessing Outputs
│   ├── Data/             # Training & Testing Datasets
│   │   ├── dataset.csv
│   │   ├── test.csv
│   │   └── train.csv
│   ├── model/            # Trained Models
│   │   └── best_model.pkl
│   └── preprocessor/     # Preprocessing Tools
│       ├── preprocessor.pkl
│       └── traffic_weather_impact.pkl
├── src/                  # Core Source Code
│   ├── components/       # React Components
│   │   ├── Map.tsx
│   │   ├── Metrics.tsx
│   │   ├── OrderForm.tsx
│   │   └── TrendChart.tsx
│   ├── services/         # API Services
│   │   └── api.ts
│   ├── utils/            # Utility Scripts
│       ├── logger.py
│       ├── exception.py
│       └── utils.py
└── research/             # Research & Analysis Notebooks
    ├── data_analysis.ipynb
    ├── data_cleaning.ipynb
    ├── feature_engineering.ipynb
    └── model_training.ipynb
```

---

## 📊 Model Insights

Utilizing the [Food Delivery Dataset](https://www.kaggle.com/datasets/gauravmalik26/food-delivery-dataset/code), various regression models were trained and evaluated:

| Model                  | Training Time | R² Score  |
| ---------------------- | ------------- | --------- |
| **Random Forest**      | 41.12 sec     | **0.906** |
| **Decision Tree**      | 0.64 sec      | 0.745     |
| **Gradient Boosting**  | 11.99 sec     | 0.885     |
| **Linear Regression**  | 0.02 sec      | 0.695     |
| **XGBRegressor**       | 0.92 sec      | 0.874     |
| **CatBoost Regressor** | 3.57 sec      | 0.864     |
| **AdaBoost Regressor** | 14.05 sec     | 0.832     |

**Winner**: Random Forest with an R² Score of **0.906**!

---

## 🧑‍💻 Contributing

We welcome contributions! Here's how you can get involved:

1. **Fork the Repository**:

   ```bash
   git fork https://github.com/rahulagowda004/real_time_route_optimization
   ```

2. **Create a Feature Branch**:

   ```bash
   git checkout -b feature/my-awesome-feature
   ```

3. **Commit Changes**:

   ```bash
   git commit -m "Add my awesome feature"
   ```

4. **Submit a Pull Request**:  
   Navigate to the repository on GitHub and open a pull request.

---

## 📄 License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---

## 📬 Contact

For any questions, issues, or suggestions:  
**Rahul A Gowda**

- GitHub: [rahulagowda004](https://github.com/rahulagowda004)
- Email: [rahulagowda004@example.com](mailto:rahulagowda004@example.com)

Happy optimizing! 🚀

---
