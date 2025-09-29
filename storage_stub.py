"""Simulated file transfer between cloud providers.

This stub mimics the behavior of copying a file from a source to a destination.
"""

def copy_file(source, destination):
    """Simulate copying a file from source to destination.

    Args:
        source (dict): Dictionary with source provider, bucket, and key.
        destination (dict): Dictionary with destination provider, bucket, and key.

    Returns:
        bool: True if simulated copy succeeds.
    """
    print(f"Simulated copy: {source['key']} → {destination['key']}")
    return True  # Always succeed in simulation
