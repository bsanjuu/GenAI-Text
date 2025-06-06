import os
import logging
from typing import Dict, Any, Optional
import pickle
import json
from pathlib import Path

logger = logging.getLogger(__name__)

class ModelLoader:
    """
    Model loading and management utilities
    """

    def __init__(self, models_dir: str = "models"):
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(exist_ok=True)
        self._loaded_models = {}
        self._model_configs = {}

    def load_model_config(self, model_name: str) -> Dict[str, Any]:
        """
        Load model configuration from JSON file

        Args:
            model_name: Name of the model

        Returns:
            Model configuration dictionary
        """
        config_path = self.models_dir / f"{model_name}_config.json"

        try:
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self._model_configs[model_name] = config
                    logger.info(f"Loaded config for model: {model_name}")
                    return config
            else:
                logger.warning(f"Config file not found for model: {model_name}")
                return {}
        except Exception as e:
            logger.error(f"Failed to load config for {model_name}: {str(e)}")
            return {}

    def save_model_config(self, model_name: str, config: Dict[str, Any]) -> bool:
        """
        Save model configuration to JSON file

        Args:
            model_name: Name of the model
            config: Configuration dictionary

        Returns:
            True if saved successfully, False otherwise
        """
        config_path = self.models_dir / f"{model_name}_config.json"

        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

            self._model_configs[model_name] = config
            logger.info(f"Saved config for model: {model_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to save config for {model_name}: {str(e)}")
            return False

    def load_model(self, model_name: str, model_path: Optional[str] = None) -> Any:
        """
        Load a model from file

        Args:
            model_name: Name of the model
            model_path: Optional custom path to model file

        Returns:
            Loaded model object
        """
        if model_name in self._loaded_models:
            logger.info(f"Returning cached model: {model_name}")
            return self._loaded_models[model_name]

        if model_path is None:
            model_path = self.models_dir / f"{model_name}.pkl"
        else:
            model_path = Path(model_path)

        try:
            if model_path.exists():
                with open(model_path, 'rb') as f:
                    model = pickle.load(f)
                    self._loaded_models[model_name] = model
                    logger.info(f"Loaded model: {model_name}")
                    return model
            else:
                logger.warning(f"Model file not found: {model_path}")
                return None
        except Exception as e:
            logger.error(f"Failed to load model {model_name}: {str(e)}")
            return None

    def save_model(self, model_name: str, model: Any, model_path: Optional[str] = None) -> bool:
        """
        Save a model to file

        Args:
            model_name: Name of the model
            model: Model object to save
            model_path: Optional custom path to save model

        Returns:
            True if saved successfully, False otherwise
        """
        if model_path is None:
            model_path = self.models_dir / f"{model_name}.pkl"
        else:
            model_path = Path(model_path)

        try:
            model_path.parent.mkdir(parents=True, exist_ok=True)

            with open(model_path, 'wb') as f:
                pickle.dump(model, f)

            self._loaded_models[model_name] = model
            logger.info(f"Saved model: {model_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to save model {model_name}: {str(e)}")
            return False

    def list_available_models(self) -> Dict[str, Dict[str, Any]]:
        """
        List all available models with their metadata

        Returns:
            Dictionary of model names and their metadata
        """
        models = {}

        for model_file in self.models_dir.glob("*.pkl"):
            model_name = model_file.stem
            config = self.load_model_config(model_name)

            models[model_name] = {
                'path': str(model_file),
                'size_mb': round(model_file.stat().st_size / (1024 * 1024), 2),
                'config': config,
                'loaded': model_name in self._loaded_models
            }

        return models

    def unload_model(self, model_name: str) -> bool:
        """
        Unload a model from memory

        Args:
            model_name: Name of the model to unload

        Returns:
            True if unloaded successfully, False otherwise
        """
        if model_name in self._loaded_models:
            del self._loaded_models[model_name]
            logger.info(f"Unloaded model: {model_name}")
            return True
        else:
            logger.warning(f"Model not loaded: {model_name}")
            return False

    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """
        Get information about a specific model

        Args:
            model_name: Name of the model

        Returns:
            Model information dictionary
        """
        model_path = self.models_dir / f"{model_name}.pkl"
        config = self.load_model_config(model_name)

        info = {
            'name': model_name,
            'exists': model_path.exists(),
            'loaded': model_name in self._loaded_models,
            'config': config
        }

        if model_path.exists():
            stat = model_path.stat()
            info.update({
                'size_mb': round(stat.st_size / (1024 * 1024), 2),
                'modified_time': stat.st_mtime,
                'path': str(model_path)
            })

        return info

    def validate_model(self, model_name: str) -> Dict[str, Any]:
        """
        Validate a model's integrity and compatibility

        Args:
            model_name: Name of the model to validate

        Returns:
            Validation results
        """
        validation_result = {
            'valid': False,
            'errors': [],
            'warnings': []
        }

        try:
            # Check if model file exists
            model_path = self.models_dir / f"{model_name}.pkl"
            if not model_path.exists():
                validation_result['errors'].append(f"Model file not found: {model_path}")
                return validation_result

            # Try to load the model
            model = self.load_model(model_name)
            if model is None:
                validation_result['errors'].append("Failed to load model")
                return validation_result

            # Check model configuration
            config = self.load_model_config(model_name)
            if not config:
                validation_result['warnings'].append("No configuration file found")

            # Check if model has required methods (if it's a custom model)
            if hasattr(model, '__dict__'):
                required_methods = ['predict', 'fit'] if hasattr(model, 'predict') else []
                missing_methods = [method for method in required_methods if not hasattr(model, method)]
                if missing_methods:
                    validation_result['warnings'].append(f"Missing methods: {missing_methods}")

            # Additional validation for model attributes
            if hasattr(model, 'metadata'):
                if not isinstance(model.metadata, dict):
                    validation_result['warnings'].append("Model metadata is not a dictionary")
                elif 'version' not in model.metadata:
                    validation_result['warnings'].append("Model metadata missing 'version' key")

            validation_result['valid'] = len(validation_result['errors']) == 0

        except Exception as e:
            validation_result['errors'].append(f"Validation error: {str(e)}")

        return validation_result

# Create a global model loader instance
model_loader = ModelLoader()

