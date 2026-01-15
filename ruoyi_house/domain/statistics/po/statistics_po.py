from typing import Optional, Union
from decimal import Decimal

from pydantic import BaseModel

class StatisticsPo(BaseModel):
    """
    统计总数对象
    """
    value: Optional[Union[int, float, str]] = None
    name: Optional[Union[str, int, float, Decimal]] = None
    avg: Optional[Union[float, int, str]] = None
    max: Optional[Union[float, int, str]] = None
    min: Optional[Union[float, int, str]] = None

