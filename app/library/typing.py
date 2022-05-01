from typing import Dict, List, Any

from sqlalchemy.orm import Session


JSON = Dict[str, Any]
JSON_ARRAY = List[Dict[str, Any]]
DB_SESSION = Session
