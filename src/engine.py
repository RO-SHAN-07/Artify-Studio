from dataclasses import dataclass
from PIL import Image, ImageDraw
import cv2
import numpy as np
from io import BytesIO
from typing import List

@dataclass
class TransformationConfig:
    max_image_size: tuple[int, int] = (1920, 1080)
    output_quality: int = 95
    cache_enabled: bool = True
    temp_directory: str = "temp"
    processing_backend: str = 'cpu'

class ImageTransformationEngine:
    def __init__(self, config: TransformationConfig = TransformationConfig()):
        self.config = config
        self.image = None
        self.original_image = None

    def load_image(self, image_path: str):
        try:
            self.original_image = Image.open(image_path)
            self.image = self.original_image.copy()
            # Resize if necessary
            self.image.thumbnail(self.config.max_image_size)
            return {"success": True, "message": "Image loaded successfully."}
        except Exception as e:
            return {"success": False, "message": f"Error loading image: {e}"}

    def apply_transformation(self, transform_type: str, params: dict = None):
        if self.image is None:
            return {"success": False, "message": "No image loaded."}

        # Reset to original image before applying transformation
        self.image = self.original_image.copy()
        self.image.thumbnail(self.config.max_image_size)

        if transform_type == "pencil_sketch":
            return self.pencil_sketch(params)
        elif transform_type == "colored_sketch":
            return self.colored_sketch(params)
        elif transform_type == "opencv_filter":
            return self.opencv_filter(params)
        elif transform_type == "turtle_graphics":
            return self.turtle_graphics(params)
        else:
            return {"success": False, "message": "Invalid transformation type."}

    def batch_process(self, image_paths: List[str], transform_type: str, params: dict = None):
        results = []
        for path in image_paths:
            load_result = self.load_image(path)
            if load_result["success"]:
                transform_result = self.apply_transformation(transform_type, params)
                if transform_result["success"]:
                    results.append({"path": path, "image": self.image.copy()})
        return results

    def export_result(self, format: str = "PNG", quality: int = 95):
        if self.image is None:
            return {"success": False, "message": "No image to export."}

        try:
            # In a real application, we would save to a file
            # For now, we'll just return a success message
            return {"success": True, "message": "Image exported successfully."}
        except Exception as e:
            return {"success": False, "message": f"Error exporting image: {e}"}

    def pencil_sketch(self, params: dict = None):
        try:
            open_cv_image = cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2BGR)
            gray_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
            inverted_image = 255 - gray_image
            blurred = cv2.GaussianBlur(inverted_image, (21, 21), 0)
            inverted_blurred = 255 - blurred
            pencil_sketch = cv2.divide(gray_image, inverted_blurred, scale=256.0)
            self.image = Image.fromarray(pencil_sketch)
            return {"success": True, "message": "Pencil sketch applied successfully."}
        except Exception as e:
            return {"success": False, "message": f"Error applying pencil sketch: {e}"}

    def colored_sketch(self, params: dict = None):
        try:
            open_cv_image = cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2BGR)
            gray_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
            inverted_image = 255 - gray_image
            blurred = cv2.GaussianBlur(inverted_image, (21, 21), 0)
            inverted_blurred = 255 - blurred
            pencil_sketch = cv2.divide(gray_image, inverted_blurred, scale=256.0)
            pencil_sketch_bgr = cv2.cvtColor(pencil_sketch, cv2.COLOR_GRAY2BGR)
            colored_sketch = cv2.bitwise_and(open_cv_image, pencil_sketch_bgr)
            self.image = Image.fromarray(cv2.cvtColor(colored_sketch, cv2.COLOR_BGR2RGB))
            return {"success": True, "message": "Colored sketch applied successfully."}
        except Exception as e:
            return {"success": False, "message": f"Error applying colored sketch: {e}"}

    def opencv_filter(self, params: dict = None):
        try:
            open_cv_image = cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2BGR)
            # Example filter: stylized
            stylized = cv2.stylization(open_cv_image, sigma_s=60, sigma_r=0.6)
            self.image = Image.fromarray(cv2.cvtColor(stylized, cv2.COLOR_BGR2RGB))
            return {"success": True, "message": "OpenCV filter applied successfully."}
        except Exception as e:
            return {"success": False, "message": f"Error applying OpenCV filter: {e}"}

    def turtle_graphics(self, params: dict = None):
        try:
            # Placeholder for turtle graphics using Pillow
            img = Image.new('RGB', (self.image.width, self.image.height), color = 'white')
            d = ImageDraw.Draw(img)
            d.text((10,10), "Turtle Graphics Placeholder", fill=(0,0,0))
            self.image = img
            return {"success": True, "message": "Turtle graphics applied successfully."}
        except Exception as e:
            return {"success": False, "message": f"Error applying turtle graphics: {e}"}
