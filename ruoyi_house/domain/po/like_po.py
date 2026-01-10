# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: like_po.py
# @Time    : 2026-01-10 17:29:51

from typing import Optional
from datetime import datetime

from sqlalchemy import BigInteger, Boolean, Date, DateTime, Float, Integer, JSON, LargeBinary, Numeric, String, Text, Time
from sqlalchemy.orm import Mapped, mapped_column

from ruoyi_admin.ext import db

class LikePo(db.Model):
    """
    用户点赞PO对象
    """
    __tablename__ = 'tb_like'
    __table_args__ = {'comment': '用户点赞'}
    id: Mapped[int] = mapped_column(
        'id',
        BigInteger,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment='浏览编号'
    )
    user_id: Mapped[Optional[int]] = mapped_column(
        'user_id',
        BigInteger,
        nullable=False,
        comment='用户'
    )
    user_name: Mapped[Optional[str]] = mapped_column(
        'user_name',
        String(255),
        nullable=False,
        comment='用户名'
    )
    house_id: Mapped[Optional[int]] = mapped_column(
        'house_id',
        BigInteger,
        nullable=False,
        comment='房源编号'
    )
    house_title: Mapped[Optional[str]] = mapped_column(
        'house_title',
        String(255),
        nullable=True,
        comment='名称'
    )
    cover_image: Mapped[Optional[str]] = mapped_column(
        'cover_image',
        String(255),
        nullable=True,
        comment='封面'
    )
    town: Mapped[Optional[str]] = mapped_column(
        'town',
        String(255),
        nullable=True,
        comment='镇'
    )
    house_type: Mapped[Optional[str]] = mapped_column(
        'house_type',
        String(255),
        nullable=True,
        comment='户型'
    )
    orientation: Mapped[Optional[str]] = mapped_column(
        'orientation',
        String(255),
        nullable=True,
        comment='朝向'
    )
    tags: Mapped[Optional[str]] = mapped_column(
        'tags',
        String(255),
        nullable=True,
        comment='房源标签'
    )
    score: Mapped[Optional[str]] = mapped_column(
        'score',
        Numeric(10, 0),
        nullable=False,
        comment='分数'
    )
    create_time: Mapped[Optional[datetime]] = mapped_column(
        'create_time',
        DateTime,
        nullable=False,
        comment='创建时间'
    )