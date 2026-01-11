# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: view.py
# @Time    : 2026-01-10 17:29:50

from typing import Optional, Annotated
from datetime import datetime
from pydantic import Field, BeforeValidator
from ruoyi_common.base.model import BaseEntity
from ruoyi_common.base.transformer import to_datetime, str_to_int
from ruoyi_common.base.schema_excel import ExcelField
from ruoyi_common.base.schema_vo import VoField


class View(BaseEntity):
    """
    用户浏览对象
    """
    # 浏览编号
    id: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="浏览编号"),
        VoField(query=True),
        ExcelField(name="浏览编号")
    ]
    # 用户
    user_id: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="用户"),
        ExcelField(name="用户")
    ]
    # 用户名
    user_name: Annotated[
        Optional[str],
        Field(default=None, description="用户名"),
        VoField(query=True),
        ExcelField(name="用户名")
    ]
    # 房源编号
    house_id: Annotated[
        Optional[str],
        Field(default=None, description="房源编号"),
        ExcelField(name="房源编号")
    ]
    # 名称
    house_title: Annotated[
        Optional[str],
        Field(default=None, description="名称"),
        VoField(query=True),
        ExcelField(name="名称")
    ]
    # 封面
    cover_image: Annotated[
        Optional[str],
        Field(default=None, description="封面"),
        ExcelField(name="封面")
    ]
    # 镇
    town: Annotated[
        Optional[str],
        Field(default=None, description="镇"),
        ExcelField(name="镇")
    ]
    # 户型
    house_type: Annotated[
        Optional[str],
        Field(default=None, description="户型"),
        ExcelField(name="户型")
    ]
    # 朝向
    orientation: Annotated[
        Optional[str],
        Field(default=None, description="朝向"),
        ExcelField(name="朝向")
    ]
    # 房源标签
    tags: Annotated[
        Optional[str],
        Field(default=None, description="房源标签"),
        ExcelField(name="房源标签")
    ]
    # 分数
    score: Annotated[
        Optional[float],
        Field(default=None, description="分数"),
        VoField(query=True),
        ExcelField(name="分数")
    ]
    # 创建时间
    create_time: Annotated[
        Optional[datetime],
        BeforeValidator(to_datetime()),
        Field(default=None, description="创建时间"),
        VoField(query=True),
        ExcelField(name="创建时间")
    ]

    # 页码
    page_num: Optional[int] = Field(default=1, description="页码")
    # 每页数量
    page_size: Optional[int] = Field(default=10, description="每页数量")
