from typing import List, Optional

from pydantic import BaseModel, Field


class StatisticsVo(BaseModel):
    """
    统计总数对象
    """
    value: Optional[int] = None
    name: Optional[str] = None
    avg: Optional[float] = None
    max: Optional[float] = None
    min: Optional[float] = None
