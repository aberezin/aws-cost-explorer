import json
from datetime import datetime

# Define a custom function to serialize datetime objects
def serialize_datetime(obj):
    """

    Args:
        obj:

    Returns:

    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")


def json_from_py(obj)->str:
    """
    Rules: DataTimes are serialized as isoformat

    Args:
        obj:

    Returns:

    """

    return json.dumps(obj, default=serialize_datetime)

