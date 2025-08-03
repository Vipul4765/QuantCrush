from pydantic import BaseModel
from datetime import date
from typing import Literal


from typing import Optional
from pydantic import BaseModel
from datetime import date

class PatternResponse(BaseModel):
    id: Optional[int] = None
    symbol: str
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: float
    prev_close: float
    avg_price: float
    pattern_value: int
    matched_patterns: str


class PatternRankLookup(BaseModel):
    pattern_name: str
    bit_position: int
    pattern_value: int

    class Config:
        orm_mode = True