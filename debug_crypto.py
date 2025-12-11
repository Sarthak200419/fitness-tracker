import sys
print(f"Python Executable: {sys.executable}")
print(f"Python Version: {sys.version}")

try:
    import cryptography
    print(f"SUCCESS: cryptography {cryptography.__version__} imported from {cryptography.__file__}")
except ImportError as e:
    print(f"FAILURE: cryptography import failed: {e}")
except Exception as e:
    print(f"FAILURE: cryptography broke: {e}")

try:
    import OpenSSL
    print(f"SUCCESS: OpenSSL {OpenSSL.__version__} imported from {OpenSSL.__file__}")
except ImportError as e:
    print(f"FAILURE: OpenSSL import failed: {e}")
