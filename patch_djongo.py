"""
Patch djongo to fix connection issues
"""
import djongo.base

# Store the original _close method
original_close = djongo.base.DatabaseWrapper._close

def patched_close(self):
    """Patched version of _close that handles connection properly"""
    try:
        if hasattr(self, 'connection') and self.connection is not None:
            self.connection.close()
            self.connection = None
    except Exception:
        # Ignore any errors during close
        pass

# Apply the patch
djongo.base.DatabaseWrapper._close = patched_close

print("✅ Djongo connection patch applied")