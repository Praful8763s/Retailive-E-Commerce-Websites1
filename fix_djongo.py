"""
Fix for djongo database connection issues
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'retailhive.settings')
django.setup()

def fix_djongo_connection():
    """Fix djongo connection issues by patching the problematic methods"""
    try:
        from djongo.base import DatabaseWrapper
        
        # Patch the _close method to handle the connection properly
        original_close = DatabaseWrapper._close
        
        def patched_close(self):
            try:
                if hasattr(self, 'connection') and self.connection is not None:
                    self.connection.close()
                    self.connection = None
            except Exception:
                pass
        
        DatabaseWrapper._close = patched_close
        print("✅ Djongo connection patched successfully")
        return True
    except Exception as e:
        print(f"⚠️ Could not patch djongo: {e}")
        return False

if __name__ == "__main__":
    fix_djongo_connection()