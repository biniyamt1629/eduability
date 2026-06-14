import cv2
import numpy as np
from typing import Dict
import random
import os

class DiseaseDetector:
    """
    Crop Disease Detection using Image Analysis
    Identifies common crop diseases from aerial imagery
    """
    
    def __init__(self):
        self.diseases = {
            "powdery_mildew": {"color_range": [(0, 0, 200), (100, 100, 255)], "confidence_mult": 1.2},
            "leaf_spot": {"color_range": [(50, 50, 50), (100, 100, 100)], "confidence_mult": 1.0},
            "rust": {"color_range": [(0, 100, 200), (100, 150, 255)], "confidence_mult": 1.1},
            "blight": {"color_range": [(0, 0, 100), (50, 50, 150)], "confidence_mult": 0.9},
            "mosaic_virus": {"color_range": [(150, 150, 0), (255, 255, 100)], "confidence_mult": 1.3},
        }
        self.health_threshold = 0.15
    
    def detect(self, image_path: str) -> Dict:
        """
        Detect diseases in drone image
        """
        if not os.path.exists(image_path):
            raise Exception(f"Image not found: {image_path}")
        
        image = cv2.imread(image_path)
        if image is None:
            raise Exception("Failed to read image")
        
        # Analyze color distribution
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Detect unhealthy colors
        disease_pixels = self._detect_disease_colors(hsv)
        
        # Calculate disease coverage
        total_pixels = hsv.shape[0] * hsv.shape[1]
        disease_coverage = np.sum(disease_pixels) / total_pixels
        
        # Determine if disease is present
        detected = disease_coverage > self.health_threshold
        
        # Identify disease type
        disease_type = None
        confidence = 0
        
        if detected:
            disease_type, confidence = self._identify_disease(hsv, disease_pixels)
        
        return {
            "detected": detected,
            "type": disease_type,
            "coverage": round(disease_coverage * 100, 1),
            "confidence": round(confidence, 3),
            "recommendation": self._get_recommendation(disease_type, disease_coverage)
        }
    
    def _detect_disease_colors(self, hsv_image: np.ndarray) -> np.ndarray:
        """
        Detect unhealthy crop colors
        """
        # Define unhealthy color ranges (brown, yellow, black spots)
        lower_brown = np.array([10, 50, 50])
        upper_brown = np.array([25, 200, 200])
        
        lower_yellow = np.array([25, 50, 50])
        upper_yellow = np.array([35, 200, 200])
        
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([180, 100, 100])
        
        # Create masks
        mask_brown = cv2.inRange(hsv_image, lower_brown, upper_brown)
        mask_yellow = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
        mask_black = cv2.inRange(hsv_image, lower_black, upper_black)
        
        # Combine masks
        combined_mask = cv2.bitwise_or(mask_brown, mask_yellow)
        combined_mask = cv2.bitwise_or(combined_mask, mask_black)
        
        return combined_mask
    
    def _identify_disease(self, hsv_image: np.ndarray, disease_pixels: np.ndarray) -> tuple:
        """
        Identify specific disease type
        """
        # Analyze disease pixel distribution
        h_values = hsv_image[:, :, 0][disease_pixels > 0]
        
        if len(h_values) == 0:
            return None, 0
        
        h_mean = np.mean(h_values)
        
        # Map hue to disease type
        if h_mean < 30:
            disease_type = "rust"
            confidence = 0.85
        elif h_mean < 60:
            disease_type = "mosaic_virus"
            confidence = 0.78
        elif h_mean < 90:
            disease_type = "leaf_spot"
            confidence = 0.82
        else:
            disease_type = "powdery_mildew"
            confidence = 0.80
        
        return disease_type, confidence
    
    def _get_recommendation(self, disease_type: str, coverage: float) -> str:
        """
        Get treatment recommendation for identified disease
        """
        if disease_type is None:
            return "No disease detected - maintain current crop management"
        
        recommendations = {
            "powdery_mildew": "Apply sulfur-based fungicide. Improve air circulation.",
            "leaf_spot": "Remove affected leaves. Apply copper fungicide.",
            "rust": "Apply phosphorous-based fungicide. Reduce humidity.",
            "blight": "Apply systemic fungicide immediately. Isolate affected area.",
            "mosaic_virus": "Remove infected plants. Control vectors (insects)."
        }
        
        rec = recommendations.get(disease_type, "Consult agricultural expert")
        
        if coverage > 50:
            rec = "🚨 CRITICAL: " + rec
        elif coverage > 20:
            rec = "⚠️  WARNING: " + rec
        else:
            rec = "📋 MONITOR: " + rec
        
        return rec
    
    def segment_diseased_areas(self, image_path: str) -> np.ndarray:
        """
        Create segmentation map of diseased areas
        """
        image = cv2.imread(image_path)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        disease_pixels = self._detect_disease_colors(hsv)
        
        # Morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        disease_pixels = cv2.morphologyEx(disease_pixels, cv2.MORPH_CLOSE, kernel)
        
        return disease_pixels