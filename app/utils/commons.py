from datetime import datetime


def convert_to_strftime(dt: datetime):
    """Convert datetime data to strftime format"""
    
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')