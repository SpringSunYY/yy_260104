# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: house_po.py
# @Time    : 2026-01-10 17:29:50

from typing import Optional
from datetime import datetime

from sqlalchemy import BigInteger, Boolean, Date, DateTime, Float, Integer, JSON, LargeBinary, Numeric, String, Text, Time
from sqlalchemy.orm import Mapped, mapped_column

from ruoyi_admin.ext import db

class HousePo(db.Model):
    """
    房源信息PO对象
    """
    __tablename__ = 'tb_house'
    __table_args__ = {'comment': '房源信息'}
    hose_id: Mapped[int] = mapped_column(
        'hose_id',
        String(255),
        primary_key=True,
        autoincrement=False,
        nullable=False,
        comment='房源编号'
    )
    house_code: Mapped[Optional[str]] = mapped_column(
        'house_code',
        String(255),
        nullable=False,
        comment='房源编码'
    )
    cover_image: Mapped[Optional[str]] = mapped_column(
        'cover_image',
        String(255),
        nullable=True,
        comment='封面图片'
    )
    title: Mapped[Optional[str]] = mapped_column(
        'title',
        String(255),
        nullable=True,
        comment='房源标题'
    )
    community: Mapped[Optional[str]] = mapped_column(
        'community',
        String(255),
        nullable=True,
        comment='小区名称'
    )
    address: Mapped[Optional[str]] = mapped_column(
        'address',
        String(255),
        nullable=True,
        comment='小区地址'
    )
    area: Mapped[Optional[str]] = mapped_column(
        'area',
        String(255),
        nullable=True,
        comment='所属区域'
    )
    city: Mapped[Optional[str]] = mapped_column(
        'city',
        String(255),
        nullable=True,
        comment='城市'
    )
    town: Mapped[Optional[str]] = mapped_column(
        'town',
        String(255),
        nullable=True,
        comment='镇'
    )
    total_price: Mapped[Optional[str]] = mapped_column(
        'total_price',
        Numeric(10, 0),
        nullable=True,
        comment='总价'
    )
    unit_price: Mapped[Optional[str]] = mapped_column(
        'unit_price',
        Numeric(10, 0),
        nullable=True,
        comment='单价'
    )
    house_type: Mapped[Optional[str]] = mapped_column(
        'house_type',
        String(255),
        nullable=True,
        comment='户型'
    )
    area_size: Mapped[Optional[int]] = mapped_column(
        'area_size',
        Integer,
        nullable=True,
        comment='建筑面积'
    )
    orientation: Mapped[Optional[str]] = mapped_column(
        'orientation',
        String(255),
        nullable=True,
        comment='朝向'
    )
    floor: Mapped[Optional[str]] = mapped_column(
        'floor',
        String(255),
        nullable=True,
        comment='楼层'
    )
    floor_height: Mapped[Optional[int]] = mapped_column(
        'floor_height',
        Integer,
        nullable=True,
        comment='楼层高度'
    )
    decoration_area: Mapped[Optional[str]] = mapped_column(
        'decoration_area',
        Numeric(10, 0),
        nullable=True,
        comment='装修面积单价'
    )
    floor_type: Mapped[Optional[str]] = mapped_column(
        'floor_type',
        String(255),
        nullable=True,
        comment='楼层类型'
    )
    building_year: Mapped[Optional[int]] = mapped_column(
        'building_year',
        Integer,
        nullable=True,
        comment='建筑年代'
    )
    decoration_type: Mapped[Optional[str]] = mapped_column(
        'decoration_type',
        String(255),
        nullable=True,
        comment='装修类型'
    )
    tags: Mapped[Optional[str]] = mapped_column(
        'tags',
        String(255),
        nullable=True,
        comment='房源标签'
    )
    property_right_type: Mapped[Optional[str]] = mapped_column(
        'property_right_type',
        String(255),
        nullable=True,
        comment='产权性质'
    )
    property_right_year: Mapped[Optional[str]] = mapped_column(
        'property_right_year',
        String(255),
        nullable=True,
        comment='产权年限'
    )
    house_intro: Mapped[Optional[str]] = mapped_column(
        'house_intro',
        Text,
        nullable=True,
        comment='房源介绍'
    )
    image_urls: Mapped[Optional[str]] = mapped_column(
        'image_urls',
        Text,
        nullable=True,
        comment='房源图片'
    )
    property_type: Mapped[Optional[str]] = mapped_column(
        'property_type',
        String(255),
        nullable=True,
        comment='物业类型'
    )