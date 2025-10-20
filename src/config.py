import json
from typing import Any, Dict

class Config:
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._create_default_config()

    def _create_default_config(self) -> Dict[str, Any]:
        default_config = {
            "feature_flags": {
                "batch_processing": False,
                "cloud_sync": False
            },
            "platform_settings": {
                "web": {
                    "max_upload_size_mb": 10
                },
                "android": {
                    "use_gpu_acceleration": True
                },
                "ios": {
                    "use_metal_acceleration": True
                }
            }
        }
        self.save_config(default_config)
        return default_config

    def save_config(self, config: Dict[str, Any]):
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=4)
        self.config = config

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

    def is_feature_enabled(self, feature_name: str) -> bool:
        return self.config.get("feature_flags", {}).get(feature_name, False)

config = Config()
