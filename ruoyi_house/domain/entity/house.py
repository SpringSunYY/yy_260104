# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: house.py
# @Time    : 2026-01-10 17:29:50

from typing import Optional, Annotated
from pydantic import Field, BeforeValidator
from ruoyi_common.base.model import BaseEntity
from ruoyi_common.base.transformer import str_to_int
from ruoyi_common.base.schema_excel import ExcelField
from ruoyi_common.base.schema_vo import VoField


class House(BaseEntity):
    """
    房源信息对象
    """
    # 房源编号
    hose_id: Annotated[
        Optional[str],
        Field(default=None, description="房源编号"),
        VoField(query=True),
        ExcelField(name="房源编号")
    ]
    # 房源编码
    house_code: Annotated[
        Optional[str],
        Field(default=None, description="房源编码"),
        VoField(query=True),
        ExcelField(name="房源编码")
    ]
    # 封面图片
    cover_image: Annotated[
        Optional[str],
        Field(default=None, description="封面图片"),
        ExcelField(name="封面图片")
    ]
    # 房源标题
    title: Annotated[
        Optional[str],
        Field(default=None, description="房源标题"),
        VoField(query=True),
        ExcelField(name="房源标题")
    ]
    # 小区名称
    community: Annotated[
        Optional[str],
        Field(default=None, description="小区名称"),
        VoField(query=True),
        ExcelField(name="小区名称")
    ]
    # 小区地址
    address: Annotated[
        Optional[str],
        Field(default=None, description="小区地址"),
        ExcelField(name="小区地址")
    ]
    # 所属区域
    area: Annotated[
        Optional[str],
        Field(default=None, description="所属区域"),
        ExcelField(name="所属区域")
    ]
    # 城市
    city: Annotated[
        Optional[str],
        Field(default=None, description="城市"),
        VoField(query=True),
        ExcelField(name="城市")
    ]
    # 镇
    town: Annotated[
        Optional[str],
        Field(default=None, description="镇"),
        VoField(query=True),
        ExcelField(name="镇")
    ]
    # 总价
    total_price: Annotated[
        Optional[float],
        Field(default=None, description="总价"),
        ExcelField(name="总价")
    ]
    # 单价
    unit_price: Annotated[
        Optional[float],
        Field(default=None, description="单价"),
        ExcelField(name="单价")
    ]
    # 户型
    house_type: Annotated[
        Optional[str],
        Field(default=None, description="户型"),
        VoField(query=True),
        ExcelField(name="户型")
    ]
    # 建筑面积
    area_size: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="建筑面积"),
        ExcelField(name="建筑面积")
    ]
    # 朝向
    orientation: Annotated[
        Optional[str],
        Field(default=None, description="朝向"),
        VoField(query=True),
        ExcelField(name="朝向")
    ]
    # 楼层
    floor: Annotated[
        Optional[str],
        Field(default=None, description="楼层"),
        ExcelField(name="楼层")
    ]
    # 楼层高度
    floor_height: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="楼层高度"),
        VoField(query=True),
        ExcelField(name="楼层高度")
    ]
    # 装修面积单价
    decoration_area: Annotated[
        Optional[float],
        Field(default=None, description="装修面积单价"),
        ExcelField(name="装修面积单价")
    ]
    # 楼层类型
    floor_type: Annotated[
        Optional[str],
        Field(default=None, description="楼层类型"),
        VoField(query=True),
        ExcelField(name="楼层类型")
    ]
    # 建筑年代
    building_year: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="建筑年代"),
        VoField(query=True),
        ExcelField(name="建筑年代")
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
    # 产权性质
    property_right_type: Annotated[
        Optional[str],
        Field(default=None, description="产权性质"),
        VoField(query=True),
        ExcelField(name="产权性质")
    ]
    # 产权年限
    property_right_year: Annotated[
        Optional[str],
        Field(default=None, description="产权年限"),
        VoField(query=True),
        ExcelField(name="产权年限")
    ]
    # 房源介绍
    house_intro: Annotated[
        Optional[str],
        Field(default=None, description="房源介绍"),
        ExcelField(name="房源介绍")
    ]
    # 房源图片
    image_urls: Annotated[
        Optional[str],
        Field(default=None, description="房源图片"),
        ExcelField(name="房源图片")
    ]
    # 物业类型
    property_type: Annotated[
        Optional[str],
        Field(default=None, description="物业类型"),
        VoField(query=True),
        ExcelField(name="物业类型")
    ]

    # 页码
    page_num: Optional[int] = Field(default=1, description="页码")
    # 每页数量
    page_size: Optional[int] = Field(default=10, description="每页数量")