from typing import List, Optional

from pydantic import BaseModel, Field


class StatisticsVo(BaseModel):
    """
    统计总数对象
    """
    value: Optional[float] = None
    name: Optional[str] = None
    max: Optional[float] = None
    min: Optional[float] = None
