"""
Verify PDF Generation Setup
============================
Checks all dependencies for PDF report generation
"""

import sys
import os

print("\n" + "="*60)
print("🔍 Verifying PDF Generation Setup")
print("="*60 + "\n")

errors = []
warnings = []

# 1. Check Python packages
print("1️⃣  Checking Python packages...")
required_packages = ['reportlab', 'matplotlib', 'pillow', 'jinja2', 'requests', 'dotenv']

for package in required_packages:
    try:
        if package == 'pillow':
            __import__('PIL')
        elif package == 'dotenv':
            __import__('dotenv')
        else:
            __import__(package)
        print(f"   ✅ {package}")
    except ImportError:
        print(f"   ❌ {package} - NOT INSTALLED")
        errors.append(f"Missing package: {package}")

# 2. Check core files
print("\n2️⃣  Checking core files...")
core_files = [
    'gemini/pdf_generation/__init__.py',
    'gemini/pdf_generation/pdf_service.py',
    'gemini/pdf_generation/pdf_routes.py'
]

for file in core_files:
    if os.path.exists(file):
        print(f"   ✅ {file}")
    else:
        print(f"   ❌ {file} - NOT FOUND")
        errors.append(f"Missing file: {file}")

# 3. Check server.py integration
print("\n3️⃣  Checking server.py integration...")
try:
    with open('server.py', 'r') as f:
        content = f.read()
        if 'from gemini.pdf_generation.pdf_routes import pdf_bp' in content:
            print("   ✅ PDF routes imported")
        else:
            print("   ❌ PDF routes NOT imported")
            errors.append("server.py missing: from gemini.pdf_generation.pdf_routes import pdf_bp")
        
        if 'app.register_blueprint(pdf_bp)' in content:
            print("   ✅ PDF blueprint registered")
        else:
            print("   ❌ PDF blueprint NOT registered")
            errors.append("server.py missing: app.register_blueprint(pdf_bp)")
except FileNotFoundError:
    print("   ❌ server.py not found")
    errors.append("server.py not found")

# 4. Check environment variables
print("\n4️⃣  Checking environment variables...")
from dotenv import load_dotenv
load_dotenv()

gemini_key = os.getenv('GEMINI_API_KEY')
if gemini_key:
    print(f"   ✅ GEMINI_API_KEY is set ({gemini_key[:10]}...)")
else:
    print("   ⚠️  GEMINI_API_KEY not set")
    warnings.append("GEMINI_API_KEY not set - will use fallback content")

# 5. Test import
print("\n5️⃣  Testing module import...")
try:
    from gemini.pdf_generation import PDFReportService
    print("   ✅ PDFReportService imports successfully")
    
    service = PDFReportService()
    print(f"   ✅ Service initialized (Gemini available: {service.is_available})")
except Exception as e:
    print(f"   ❌ Import failed: {e}")
    errors.append(f"Import error: {e}")

# Summary
print("\n" + "="*60)
if errors:
    print("❌ SETUP INCOMPLETE")
    print("="*60)
    print("\nErrors found:")
    for error in errors:
        print(f"  • {error}")
    print("\nFix these errors before using PDF generation.")
else:
    print("✅ SETUP COMPLETE")
    print("="*60)
    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"  ⚠️  {warning}")
    print("\n✨ PDF generation is ready to use!")
    print("   Run: python gemini/pdf_generation/test_pdf.py")

print("\n")
sys.exit(0 if not errors else 1)
