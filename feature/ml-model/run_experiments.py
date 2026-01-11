"""
Run MLflow experiments with different hyperparameters
Branch: feature/ml-model
"""

import os
import sys
import argparse
from recommendation_model import train_with_mlflow, CollaborativeFilteringModel
import pandas as pd
from sklearn.model_selection import train_test_split
import mlflow
import mlflow.sklearn
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_hyperparameter_experiments(data_path: str, experiment_name: str = "hyperparameter_tuning"):
    """Run multiple experiments with different hyperparameters"""
    
    # Set up MLflow
    mlflow.set_experiment(experiment_name)
    
    # Load data
    logger.info(f"Loading data from {data_path}")
    df = pd.read_csv(data_path)
    
    # Split data once for all experiments
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
    
    # Define hyperparameter grid
    hyperparameters = [
        {"n_recommendations": 5, "min_interactions": 1, "alpha": 0.3},
        {"n_recommendations": 10, "min_interactions": 2, "alpha": 0.5},
        {"n_recommendations": 15, "min_interactions": 2, "alpha": 0.7},
        {"n_recommendations": 10, "min_interactions": 3, "alpha": 0.5},
        {"n_recommendations": 20, "min_interactions": 1, "alpha": 0.5},
    ]
    
    best_metrics = None
    best_run_id = None
    best_params = None
    
    for i, params in enumerate(hyperparameters):
        logger.info(f"\n=== Experiment {i+1}/{len(hyperparameters)} ===")
        logger.info(f"Parameters: {params}")
        
        with mlflow.start_run():
            # Log hyperparameters
            mlflow.log_params({
                "n_recommendations": params["n_recommendations"],
                "min_interactions": params["min_interactions"],
                "alpha": params["alpha"],
                "train_size": len(train_df),
                "test_size": len(test_df),
                "n_users": df["user_id"].nunique(),
                "n_products": df["product_id"].nunique(),
            })
            
            # Train model
            model = CollaborativeFilteringModel(
                n_recommendations=params["n_recommendations"],
                min_interactions=params["min_interactions"]
            )
            
            model.create_interaction_matrix(train_df)
            model.compute_user_similarity()
            model.compute_item_similarity()
            
            # Evaluate
            metrics = model.evaluate(test_df)
            mlflow.log_metrics(metrics)
            
            # Log model
            mlflow.sklearn.log_model(
                sk_model=model,
                artifact_path="model",
                registered_model_name="recommendation_model"
            )
            
            # Track best model
            if best_metrics is None or metrics.get("rmse", float('inf')) < best_metrics.get("rmse", float('inf')):
                best_metrics = metrics
                best_run_id = mlflow.active_run().info.run_id
                best_params = params
            
            logger.info(f"Metrics: {metrics}")
    
    logger.info(f"\n=== Best Model ===")
    logger.info(f"Run ID: {best_run_id}")
    logger.info(f"Parameters: {best_params}")
    logger.info(f"Metrics: {best_metrics}")
    
    return best_run_id, best_params, best_metrics


def register_best_model(run_id: str, model_name: str = "recommendation_model"):
    """Register the best model to MLflow Model Registry"""
    
    client = mlflow.tracking.MlflowClient()
    
    # Get the model from the run
    model_uri = f"runs:/{run_id}/model"
    
    # Register model
    mv = client.create_model_version(
        name=model_name,
        source=model_uri,
        run_id=run_id
    )
    
    logger.info(f"Registered model version: {mv.version}")
    logger.info(f"Model URI: {model_uri}")
    
    # Transition to Production if it's the best
    client.transition_model_version_stage(
        name=model_name,
        version=mv.version,
        stage="Production"
    )
    
    logger.info(f"Model version {mv.version} transitioned to Production")
    
    return mv


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run MLflow hyperparameter experiments")
    parser.add_argument("--data-path", type=str, default="data/cleaned_data.csv",
                        help="Path to cleaned data CSV")
    parser.add_argument("--experiment-name", type=str, default="hyperparameter_tuning",
                        help="MLflow experiment name")
    parser.add_argument("--register-best", action="store_true",
                        help="Register best model to Model Registry")
    
    args = parser.parse_args()
    
    # Check MLflow tracking URI
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
    mlflow.set_tracking_uri(tracking_uri)
    logger.info(f"MLflow Tracking URI: {tracking_uri}")
    
    # Run experiments
    best_run_id, best_params, best_metrics = run_hyperparameter_experiments(
        args.data_path,
        args.experiment_name
    )
    
    # Register best model if requested
    if args.register_best:
        register_best_model(best_run_id)

