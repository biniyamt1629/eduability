import cv2
import numpy as np
from typing import Dict
import os

class NDVIAnalyzer:
    """
    NDVI (Normalized Difference Vegetation Index) Analysis
    Analyzes crop health from multispectral imagery
    """
    
    def __init__(self):
        self.ndvi_threshold_good = 0.6
        self.ndvi_threshold_ok = 0.4
    
    def analyze(self, image_path: str) -> Dict:
        """
        Analyze NDVI from image
        """
        if not os.path.exists(image_path):
            raise Exception(f"Image not found: {image_path}")
        
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            raise Exception("Failed to read image")
        
        # Simulate multispectral bands
        # In real scenario, would use actual NIR and Red bands
        b, g, r = cv2.split(image)
        
        # Simulate NIR band (normally from thermal/multispectral camera)
        nir = cv2.addWeighted(g, 0.8, b, 0.2, 0)
        red = r
        
        # Calculate NDVI
        # NDVI = (NIR - RED) / (NIR + RED)
        ndvi = np.divide(
            nir.astype(float) - red.astype(float),
            nir.astype(float) + red.astype(float) + 1e-8
        )
        
        # Normalize to 0-1
        ndvi = (ndvi + 1) / 2
        
        # Calculate statistics
        ndvi_mean = np.nanmean(ndvi)
        ndvi_std = np.nanstd(ndvi)
        ndvi_min = np.nanmin(ndvi)
        ndvi_max = np.nanmax(ndvi)
        
        # Calculate coverage (% of pixels with vegetation)
        vegetation_mask = ndvi > 0.3
        coverage = np.sum(vegetation_mask) / vegetation_mask.size * 100
        
        # Health assessment
        if ndvi_mean > self.ndvi_threshold_good:
            health = "excellent"
        elif ndvi_mean > self.ndvi_threshold_ok:
            health = "good"
        else:
            health = "poor"
        
        return {
            "mean": round(ndvi_mean, 3),
            "std": round(ndvi_std, 3),
            "min": round(ndvi_min, 3),
            "max": round(ndvi_max, 3),
            "coverage": round(coverage, 1),
            "health": health,
            "ndvi_map": ndvi.tolist()  # For visualization
        }
    
    def create_heatmap(self, image_path: str, output_path: str = "heatmap.png"):
        """
        Create NDVI heatmap visualization
        """
        image = cv2.imread(image_path)
        b, g, r = cv2.split(image)
        nir = cv2.addWeighted(g, 0.8, b, 0.2, 0)
        red = r
        
        ndvi = np.divide(
            nir.astype(float) - red.astype(float),
            nir.astype(float) + red.astype(float) + 1e-8
        )
        
        ndvi = (ndvi + 1) / 2
        ndvi_normalized = (ndvi * 255).astype(np.uint8)
        
        # Apply colormap
        heatmap = cv2.applyColorMap(ndvi_normalized, cv2.COLORMAP_JET)
        
        # Save
        cv2.imwrite(output_path, heatmap)
        return output_path
    
    def get_health_recommendations(self, ndvi_mean: float) -> list:
        """
        Get recommendations based on NDVI value
        """
        recommendations = []
        
        if ndvi_mean < 0.3:
            recommendations.append("⚠️  Low vegetation index - check irrigation")
            recommendations.append("⚠️  Consider increasing water supply")
            recommendations.append("⚠️  Monitor for pests/diseases")
        elif ndvi_mean < 0.5:
            recommendations.append("🟡 Moderate vegetation - maintain current schedule")
            recommendations.append("🟡 Check soil moisture levels")
            recommendations.append("🟡 Plan fertilizer application")
        else:
            recommendations.append("✅ Excellent crop health")
            recommendations.append("✅ Continue current maintenance schedule")
            recommendations.append("✅ Monitor for over-watering")
        
        return recommendations