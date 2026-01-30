"""
Smoothed Model Class
====================

Model wrapper that applies temperature scaling and beta calibration
for smooth probability distributions.
"""

import numpy as np
from scipy.special import expit
from scipy.stats import beta as beta_dist


class SmoothedModel:
    """Model with temperature scaling and beta calibration"""
    
    def __init__(self, base_model, temperature=2.5, beta_a=1.5, beta_b=1.5):
        self.base_model = base_model
        self.temperature = temperature
        self.beta_a = beta_a
        self.beta_b = beta_b
    
    def _logit(self, p):
        """Convert probability to logit"""
        p = np.clip(p, 1e-7, 1 - 1e-7)
        return np.log(p / (1 - p))
    
    def _beta_calibrate(self, proba):
        """Apply beta calibration"""
        return beta_dist.cdf(proba, self.beta_a, self.beta_b)
    
    def predict(self, X):
        """Predict class labels"""
        proba = self.predict_proba(X)
        return (proba[:, 1] >= 0.5).astype(int)
    
    def predict_proba(self, X):
        """Predict class probabilities with smoothing"""
        # Get base probabilities
        base_proba = self.base_model.predict_proba(X)[:, 1]
        
        # Apply temperature scaling
        logits = self._logit(base_proba) / self.temperature
        temp_proba = expit(logits)
        
        # Apply beta calibration
        smooth_proba = self._beta_calibrate(temp_proba)
        
        return np.column_stack([1 - smooth_proba, smooth_proba])
