"""
Lightweight error pattern matching for Python and pandas errors.

This is NOT a full bug-fixer, it just scans error messages
to extract useful labels (error types) and entities (like column names).

Used to help the assistant identify topics for retrieval and tiering.
"""

import re
import logging
from typing import Dict, List

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Common error patterns
# Each regex below tries to capture error details like missing keys, attributes, etc.
COMMON_PATTERNS = [
    r"KeyError: '([^']+)'",  # e.g., KeyError: 'age'
    r"AttributeError: '([^']+)' object has no attribute '([^']+)'",  # e.g., 'DataFrame' object has no attribute 'groupbyy'
    r"IndexError: list index out of range",  # no match groups
    r"TypeError: unsupported operand type\(s\) for",  # math between incompatible types
    r"ValueError:.*",  # general ValueErrors
    r"NameError: name '([^']+)' is not defined",  # undefined variables
    r"SettingWithCopyWarning",  # pandas-specific warning
    r"ZeroDivisionError: division by zero",  # dividing by 0
]

def parse_error(trace_or_msg: str) -> Dict[str, List[str]]:
    """
    Parse a traceback or error message and extract helpful labels and keywords.

    Args:
        trace_or_msg (str): The full error message or traceback.

    Returns:
        dict: {
            "labels": List of detected error types (e.g. 'KeyError', 'NameError'),
            "entities": List of relevant variable names or values from the error
        }
    """
    logger.info("🧩 Parsing error message...")
    info = {"labels": [], "entities": []}

    try:
        for pattern in COMMON_PATTERNS:
            match = re.search(pattern, trace_or_msg, re.IGNORECASE | re.DOTALL)
            if match:
                error_type = pattern.split(":")[0]  # Get the name like 'KeyError'
                if error_type not in info["labels"]:
                    info["labels"].append(error_type)

                # Capture all matched pieces (like variable names)
                info["entities"].extend([g for g in match.groups() if g])

        # De-duplicate entities
        info["entities"] = list(dict.fromkeys(info["entities"]))

        logger.info(f"✅ Parsed: {info}")
        return info

    except Exception as e:
        logger.error(f"❌ Failed to parse error: {e}")
        return {"labels": [], "entities": []}
