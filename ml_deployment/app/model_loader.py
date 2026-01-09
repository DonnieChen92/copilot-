"""Model loading utilities supporting multiple formats."""
import os
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional, Union

import numpy as np

logger = logging.getLogger(__name__)


class BaseModelLoader(ABC):
    """Abstract base class for model loaders."""

    def __init__(self, model_path: str):
        self.model_path = Path(model_path)
        self.model = None
        self._metadata: Dict[str, Any] = {}

    @abstractmethod
    def load(self) -> None:
        """Load the model from disk."""
        pass

    @abstractmethod
    def predict(self, input_data: np.ndarray) -> np.ndarray:
        """Run inference on the model."""
        pass

    @property
    def metadata(self) -> Dict[str, Any]:
        """Return model metadata."""
        return self._metadata

    def is_loaded(self) -> bool:
        """Check if model is loaded."""
        return self.model is not None


class ONNXModelLoader(BaseModelLoader):
    """Loader for ONNX format models."""

    def load(self) -> None:
        """Load ONNX model using ONNX Runtime."""
        try:
            import onnxruntime as ort

            logger.info(f"Loading ONNX model from {self.model_path}")

            # Configure session options for optimal performance
            sess_options = ort.SessionOptions()
            sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL

            # Try GPU first, fallback to CPU
            providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
            self.model = ort.InferenceSession(
                str(self.model_path),
                sess_options=sess_options,
                providers=providers
            )

            # Extract metadata
            self._metadata = {
                "format": "onnx",
                "inputs": [{"name": i.name, "shape": i.shape, "type": i.type}
                          for i in self.model.get_inputs()],
                "outputs": [{"name": o.name, "shape": o.shape, "type": o.type}
                           for o in self.model.get_outputs()],
                "providers": self.model.get_providers()
            }

            logger.info(f"ONNX model loaded successfully with providers: {self._metadata['providers']}")

        except ImportError:
            raise ImportError("onnxruntime is required for ONNX models. Install with: pip install onnxruntime")

    def predict(self, input_data: np.ndarray) -> np.ndarray:
        """Run inference on ONNX model."""
        if not self.is_loaded():
            raise RuntimeError("Model not loaded. Call load() first.")

        input_name = self.model.get_inputs()[0].name
        output_name = self.model.get_outputs()[0].name

        result = self.model.run([output_name], {input_name: input_data})
        return result[0]


class TensorFlowModelLoader(BaseModelLoader):
    """Loader for TensorFlow SavedModel format."""

    def load(self) -> None:
        """Load TensorFlow SavedModel."""
        try:
            import tensorflow as tf

            logger.info(f"Loading TensorFlow model from {self.model_path}")

            self.model = tf.saved_model.load(str(self.model_path))

            # Get the serving signature
            if hasattr(self.model, 'signatures'):
                self._infer = self.model.signatures.get('serving_default')
            else:
                self._infer = self.model

            self._metadata = {
                "format": "tensorflow_savedmodel",
                "path": str(self.model_path),
                "has_signatures": hasattr(self.model, 'signatures')
            }

            logger.info("TensorFlow model loaded successfully")

        except ImportError:
            raise ImportError("tensorflow is required. Install with: pip install tensorflow")

    def predict(self, input_data: np.ndarray) -> np.ndarray:
        """Run inference on TensorFlow model."""
        if not self.is_loaded():
            raise RuntimeError("Model not loaded. Call load() first.")

        import tensorflow as tf

        tensor_input = tf.constant(input_data)
        result = self._infer(tensor_input)

        # Handle different output formats
        if isinstance(result, dict):
            # Get the first output
            key = list(result.keys())[0]
            return result[key].numpy()
        return result.numpy()


class PyTorchModelLoader(BaseModelLoader):
    """Loader for PyTorch models (.pt, .pth)."""

    def __init__(self, model_path: str, model_class: Optional[Any] = None):
        super().__init__(model_path)
        self.model_class = model_class
        self.device = None

    def load(self) -> None:
        """Load PyTorch model."""
        try:
            import torch

            logger.info(f"Loading PyTorch model from {self.model_path}")

            # Determine device
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

            # Load model
            if self.model_class is not None:
                # Load state dict into model class
                self.model = self.model_class()
                state_dict = torch.load(str(self.model_path), map_location=self.device)
                self.model.load_state_dict(state_dict)
            else:
                # Load entire model (TorchScript or pickled)
                self.model = torch.load(str(self.model_path), map_location=self.device)

            self.model.to(self.device)
            self.model.eval()

            self._metadata = {
                "format": "pytorch",
                "device": str(self.device),
                "path": str(self.model_path)
            }

            logger.info(f"PyTorch model loaded on {self.device}")

        except ImportError:
            raise ImportError("torch is required. Install with: pip install torch")

    def predict(self, input_data: np.ndarray) -> np.ndarray:
        """Run inference on PyTorch model."""
        if not self.is_loaded():
            raise RuntimeError("Model not loaded. Call load() first.")

        import torch

        with torch.no_grad():
            tensor_input = torch.from_numpy(input_data).to(self.device)
            result = self.model(tensor_input)
            return result.cpu().numpy()


class TFLiteModelLoader(BaseModelLoader):
    """Loader for TensorFlow Lite models (for edge/mobile deployment)."""

    def load(self) -> None:
        """Load TFLite model."""
        try:
            import tensorflow as tf

            logger.info(f"Loading TFLite model from {self.model_path}")

            self.model = tf.lite.Interpreter(model_path=str(self.model_path))
            self.model.allocate_tensors()

            input_details = self.model.get_input_details()
            output_details = self.model.get_output_details()

            self._metadata = {
                "format": "tflite",
                "inputs": [{"name": d["name"], "shape": d["shape"].tolist(),
                           "dtype": str(d["dtype"])} for d in input_details],
                "outputs": [{"name": d["name"], "shape": d["shape"].tolist(),
                            "dtype": str(d["dtype"])} for d in output_details]
            }

            logger.info("TFLite model loaded successfully")

        except ImportError:
            raise ImportError("tensorflow is required. Install with: pip install tensorflow")

    def predict(self, input_data: np.ndarray) -> np.ndarray:
        """Run inference on TFLite model."""
        if not self.is_loaded():
            raise RuntimeError("Model not loaded. Call load() first.")

        input_details = self.model.get_input_details()
        output_details = self.model.get_output_details()

        self.model.set_tensor(input_details[0]['index'], input_data)
        self.model.invoke()

        return self.model.get_tensor(output_details[0]['index'])


def get_model_loader(model_path: str) -> BaseModelLoader:
    """Factory function to get appropriate model loader based on file extension."""
    path = Path(model_path)
    extension = path.suffix.lower()

    loaders = {
        ".onnx": ONNXModelLoader,
        ".pt": PyTorchModelLoader,
        ".pth": PyTorchModelLoader,
        ".tflite": TFLiteModelLoader,
    }

    # Check for TensorFlow SavedModel (directory)
    if path.is_dir() and (path / "saved_model.pb").exists():
        return TensorFlowModelLoader(model_path)

    loader_class = loaders.get(extension)
    if loader_class is None:
        raise ValueError(f"Unsupported model format: {extension}. "
                        f"Supported formats: {list(loaders.keys())}")

    return loader_class(model_path)
