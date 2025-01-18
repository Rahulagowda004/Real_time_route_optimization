import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor,Pool
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.utils.exception import CustomException
from src.utils.logger import logging
from src.utils.utils import save_object,evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path=os.path.join("artifacts","model.pkl")
    

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()
        
    def initiate_model_trainer(self,train_array,test_array):
        try:
            
            print("**********Initialized Model Trainer***************")
            
            logging.info("Split training and test input data")
            X_train,y_train,X_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            # Define models and hyperparameters
            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "XGBRegressor": XGBRegressor(),
                "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                "AdaBoost Regressor": AdaBoostRegressor(),
            }

            params = {
                "Decision Tree": {
                    'criterion': ['squared_error', 'friedman_mse'],
                },
                "Random Forest": {
                    'n_estimators': [50, 100, 150],
                    'max_depth': [10, 20, None],
                },
                "Gradient Boosting": {
                    'learning_rate': [0.01, 0.1],
                    'n_estimators': [50, 100],
                },
                "XGBRegressor": {
                    'learning_rate': [0.01, 0.1],
                    'n_estimators': [50, 100],
                },
                "CatBoosting Regressor": {
                    'depth': [6, 8],
                    'iterations': [50, 100],
                },
                "AdaBoost Regressor": {
                    'learning_rate': [0.01, 0.1],
                    'n_estimators': [50, 100],
                },
            }

            # Evaluate models
            model_report = evaluate_models(X_train, y_train, X_test, y_test, models, params)

            # Get the best model
            best_model_name = max(model_report, key=model_report.get)
            best_model_score = model_report[best_model_name]
            best_model = models[best_model_name]

            print(f"Best Model: {best_model_name} with R2 Score: {best_model_score}")

            # Ensure the best model is trained
            if hasattr(best_model, "is_fitted") and not best_model.is_fitted():
                print(f"{best_model_name} was not properly trained. Training now...")
                if isinstance(best_model, CatBoostRegressor):
                    train_pool = Pool(data=X_train, label=y_train)
                    best_model.fit(train_pool)
                else:
                    best_model.fit(X_train, y_train)

            # Predictions and final R2 score
            if isinstance(best_model, CatBoostRegressor):
                test_pool = Pool(data=X_test, label=y_test)
                predicted = best_model.predict(test_pool)
            else:
                predicted = best_model.predict(X_test)

            r2_square = r2_score(y_test, predicted)

            if best_model_score<0.6:
                raise CustomException("No best model found")
            logging.info(f"Best found model on both training and testing dataset")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted=best_model.predict(X_test)

            r2_square = r2_score(y_test, predicted)
            
            print("*************Ended Model Trainer******************")
            
            return r2_square
              
        except Exception as e:
            raise CustomException(e,sys)