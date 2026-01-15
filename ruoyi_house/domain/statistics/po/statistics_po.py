from typing import Optional

from pydantic import BaseModel

class StatisticsPo(BaseModel):
    """
    统计总数对象
    """
    value: Optional[float] = None
    name: Optional[str] = None
    max: Optional[float] = None
    min: Optional[float] = None

