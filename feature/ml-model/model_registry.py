"""
MLflow Model Registry Management
Branch: feature/ml-model
"""

import mlflow
from mlflow.tracking import MlflowClient
import argparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def list_models(model_name: str = "recommendation_model"):
    """List all versions of a registered model"""
    client = MlflowClient()
    
    try:
        versions = client.search_model_versions(f"name='{model_name}'")
        
        if not versions:
            logger.info(f"No versions found for model '{model_name}'")
            return
        
        logger.info(f"\n=== Model Versions for '{model_name}' ===")
        for version in versions:
            logger.info(f"Version {version.version}:")
            logger.info(f"  Stage: {version.current_stage}")
            logger.info(f"  Run ID: {version.run_id}")
            logger.info(f"  Status: {version.status}")
            logger.info(f"  Created: {version.creation_timestamp}")
            logger.info("")
    except Exception as e:
        logger.error(f"Error listing models: {e}")


def get_latest_model(model_name: str = "recommendation_model", stage: str = "Production"):
    """Get the latest model version in a specific stage"""
    client = MlflowClient()
    
    try:
        latest = client.get_latest_versions(model_name, stages=[stage])
        
        if not latest:
            logger.warning(f"No model found in stage '{stage}'")
            return None
        
        model_version = latest[0]
        logger.info(f"Latest model in '{stage}':")
        logger.info(f"  Version: {model_version.version}")
        logger.info(f"  Run ID: {model_version.run_id}")
        logger.info(f"  Model URI: models:/{model_name}/{stage}")
        
        return model_version
    except Exception as e:
        logger.error(f"Error getting latest model: {e}")
        return None


def transition_model(model_name: str, version: int, stage: str):
    """Transition a model version to a new stage"""
    client = MlflowClient()
    
    try:
        client.transition_model_version_stage(
            name=model_name,
            version=version,
            stage=stage
        )
        logger.info(f"Model {model_name} version {version} transitioned to '{stage}'")
    except Exception as e:
        logger.error(f"Error transitioning model: {e}")


def promote_to_production(model_name: str, version: int):
    """Promote a model version to Production"""
    transition_model(model_name, version, "Production")


def archive_model(model_name: str, version: int):
    """Archive a model version"""
    transition_model(model_name, version, "Archived")


def compare_models(model_name: str, version1: int, version2: int):
    """Compare two model versions"""
    client = MlflowClient()
    
    try:
        v1 = client.get_model_version(model_name, version1)
        v2 = client.get_model_version(model_name, version2)
        
        # Get run details
        run1 = client.get_run(v1.run_id)
        run2 = client.get_run(v2.run_id)
        
        logger.info(f"\n=== Comparing Model Versions ===")
        logger.info(f"\nVersion {version1} (Run {v1.run_id}):")
        logger.info(f"  Parameters: {run1.data.params}")
        logger.info(f"  Metrics: {run1.data.metrics}")
        
        logger.info(f"\nVersion {version2} (Run {v2.run_id}):")
        logger.info(f"  Parameters: {run2.data.params}")
        logger.info(f"  Metrics: {run2.data.metrics}")
        
    except Exception as e:
        logger.error(f"Error comparing models: {e}")


if __name__ == "__main__":
    import os
    
    parser = argparse.ArgumentParser(description="MLflow Model Registry Management")
    parser.add_argument("--tracking-uri", type=str, default=None,
                        help="MLflow tracking URI (default: from MLFLOW_TRACKING_URI env var or http://localhost:5000)")
    parser.add_argument("--model-name", type=str, default="recommendation_model",
                        help="Model name in registry")
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # List models
    subparsers.add_parser("list", help="List all model versions")
    
    # Get latest
    latest_parser = subparsers.add_parser("latest", help="Get latest model version")
    latest_parser.add_argument("--stage", type=str, default="Production",
                               help="Stage to get latest from")
    
    # Promote
    promote_parser = subparsers.add_parser("promote", help="Promote model to Production")
    promote_parser.add_argument("--version", type=int, required=True,
                                help="Model version to promote")
    
    # Archive
    archive_parser = subparsers.add_parser("archive", help="Archive a model version")
    archive_parser.add_argument("--version", type=int, required=True,
                                help="Model version to archive")
    
    # Compare
    compare_parser = subparsers.add_parser("compare", help="Compare two model versions")
    compare_parser.add_argument("--version1", type=int, required=True,
                                help="First model version")
    compare_parser.add_argument("--version2", type=int, required=True,
                                help="Second model version")
    
    args = parser.parse_args()
    
    # Set tracking URI
    tracking_uri = args.tracking_uri or os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
    mlflow.set_tracking_uri(tracking_uri)
    logger.info(f"MLflow Tracking URI: {tracking_uri}")
    
    # Execute command
    if args.command == "list":
        list_models(args.model_name)
    elif args.command == "latest":
        get_latest_model(args.model_name, args.stage)
    elif args.command == "promote":
        promote_to_production(args.model_name, args.version)
    elif args.command == "archive":
        archive_model(args.model_name, args.version)
    elif args.command == "compare":
        compare_models(args.model_name, args.version1, args.version2)
    else:
        parser.print_help()

