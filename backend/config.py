"""
Configuration Module for Student Dropout Prediction System
==========================================================

This module contains configuration settings for the application.
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Database configuration
DATABASE_PATH = BASE_DIR / 'database' / 'students_data.json'

# ML Model configuration
ML_MODELS_PATH = BASE_DIR / 'ml' / 'saved_models'
MODEL_FILE = ML_MODELS_PATH / 'dropout_model.pkl'
SCALER_FILE = ML_MODELS_PATH / 'scaler.pkl'
FEATURE_NAMES_FILE = ML_MODELS_PATH / 'feature_names.pkl'
LABEL_ENCODERS_FILE = ML_MODELS_PATH / 'label_encoders.pkl'
METADATA_FILE = ML_MODELS_PATH / 'training_metadata.pkl'

# Server configuration
HOST = '0.0.0.0'
PORT = 8000
DEBUG = True

# CORS configuration
CORS_ORIGINS = ['http://localhost:5173', 'http://localhost:3000']

# Risk thresholds
HIGH_RISK_THRESHOLD = 70
MEDIUM_RISK_THRESHOLD = 40

# API configuration
API_PREFIX = '/api'
