# src/models/data_structures.py

from dataclasses import dataclass, field

@dataclass
class WMItem:
    item_name: str
    matched_data: list = field(default_factory=list)
    is_locked: bool = False