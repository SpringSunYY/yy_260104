from typing import Optional, Annotated, List

from pydantic import Field

from ruoyi_common.base.model import BaseEntity
from ruoyi_common.base.schema_excel import ExcelField
from ruoyi_common.base.schema_vo import VoField


class HouseStatisticsRequest(BaseEntity):
    """
     房源信息对象
     """
    # 小区名称
    community: Annotated[
        Optional[str],
        Field(default=None, description="小区名称"),
        VoField(query=True),
        ExcelField(name="小区名称")
    ]
    # 镇
    town: Annotated[
        Optional[str],
        Field(default=None, description="镇"),
        VoField(query=True),
        ExcelField(name="镇", action='export')
    ]
    # 户型
    house_type: Annotated[
        Optional[str],
        Field(default=None, description="户型"),
        VoField(query=True),
        ExcelField(name="户型")
    ]
    # 朝向
    orientation: Annotated[
        Optional[str],
        Field(default=None, description="朝向"),
        VoField(query=True),
        ExcelField(name="朝向")
    ]

    # 装修类型
    decoration_type: Annotated[
        Optional[str],
        Field(default=None, description="装修类型"),
        VoField(query=True),
        ExcelField(name="装修类型")
    ]
    # 房源标签
    tags: Annotated[
        Optional[str],
        Field(default=None, description="房源标签"),
        VoField(query=True),
        ExcelField(name="房源标签")
    ]
