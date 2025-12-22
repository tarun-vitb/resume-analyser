"""Quick test script to check if main.py can be imported"""
import sys

try:
    print("Testing main.py import...")
    import main
    print("✅ main.py imported successfully!")
    print(f"✅ App object: {main.app}")
    print(f"✅ App title: {main.app.title}")
except SyntaxError as e:
    print(f"❌ Syntax Error: {e}")
    sys.exit(1)
except ImportError as e:
    print(f"❌ Import Error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

