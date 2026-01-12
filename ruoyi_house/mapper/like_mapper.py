# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: like_mapper.py
# @Time    : 2026-01-10 17:29:51

from typing import List, Optional
from datetime import datetime

from flask import g
from sqlalchemy import select, update, delete

from ruoyi_admin.ext import db
from ruoyi_house.domain.entity import Like
from ruoyi_house.domain.po import LikePo


class LikeMapper:
    """用户点赞Mapper"""

    @classmethod
    def select_like_list(cls, like: Like) -> List[Like]:
        """
        查询用户点赞列表

        Args:
            like (like): 用户点赞对象

        Returns:
            List[like]: 用户点赞列表
        """
        try:
            # 构建查询条件
            stmt = select(LikePo)

            if like.id is not None:
                stmt = stmt.where(LikePo.id == like.id)

            if like.user_name:
                stmt = stmt.where(LikePo.user_name.like("%" + str(like.user_name) + "%"))

            if like.house_title:
                stmt = stmt.where(LikePo.house_title.like("%" + str(like.house_title) + "%"))

            if like.score is not None:
                stmt = stmt.where(LikePo.score == like.score)

            _params = getattr(like, "params", {}) or {}
            begin_val = _params.get("beginCreateTime")
            end_val = _params.get("endCreateTime")
            if begin_val is not None:
                stmt = stmt.where(LikePo.create_time >= begin_val)
            if end_val is not None:
                stmt = stmt.where(LikePo.create_time <= end_val)
            if "criterian_meta" in g and g.criterian_meta.page:
                g.criterian_meta.page.stmt = stmt
            stmt = stmt.order_by(LikePo.create_time.desc())
            result = db.session.execute(stmt).scalars().all()
            return [Like.model_validate(item) for item in result] if result else []
        except Exception as e:
            print(f"查询用户点赞列表出错: {e}")
            return []

    @classmethod
    def select_like_by_id(cls, id: int) -> Optional[Like]:
        """
        根据ID查询用户点赞

        Args:
            id (int): 浏览编号

        Returns:
            like: 用户点赞对象
        """
        try:
            result = db.session.get(LikePo, id)
            return Like.model_validate(result) if result else None
        except Exception as e:
            print(f"根据ID查询用户点赞出错: {e}")
            return None

    @classmethod
    def insert_like(cls, like: Like) -> int:
        """
        新增用户点赞

        Args:
            like (like): 用户点赞对象

        Returns:
            int: 插入的记录数
        """
        try:
            now = datetime.now()
            new_po = LikePo()
            new_po.id = like.id
            new_po.user_id = like.user_id
            new_po.user_name = like.user_name
            new_po.house_id = like.house_id
            new_po.house_title = like.house_title
            new_po.cover_image = like.cover_image
            new_po.town = like.town
            new_po.house_type = like.house_type
            new_po.orientation = like.orientation
            new_po.tags = like.tags
            new_po.score = like.score
            new_po.create_time = like.create_time or now
            db.session.add(new_po)
            db.session.commit()
            like.id = new_po.id
            return 1
        except Exception as e:
            db.session.rollback()
            print(f"新增用户点赞出错: {e}")
            return 0


    @classmethod
    def select_like_by_user_id_and_house_id(cls, user_id, house_id)-> Optional[Like]:
        """
        根据用户查询是否点赞
        """
        try:
            result = db.session.execute(
                select(LikePo).where(LikePo.user_id == user_id, LikePo.house_id == house_id)
            ).scalars().first()
            return Like.model_validate(result) if result else None
        except Exception as e:
            print(f"根据用户查询是否点赞出错: {e}")
            return None

    @classmethod
    def update_like(cls, like: Like) -> int:
        """
        修改用户点赞

        Args:
            like (like): 用户点赞对象

        Returns:
            int: 更新的记录数
        """
        try:

            existing = db.session.get(LikePo, like.id)
            if not existing:
                return 0
            now = datetime.now()
            # 主键不参与更新
            existing.user_id = like.user_id
            existing.user_name = like.user_name
            existing.house_id = like.house_id
            existing.house_title = like.house_title
            existing.cover_image = like.cover_image
            existing.town = like.town
            existing.house_type = like.house_type
            existing.orientation = like.orientation
            existing.tags = like.tags
            existing.score = like.score
            existing.create_time = like.create_time
            db.session.commit()
            return 1

        except Exception as e:
            db.session.rollback()
            print(f"修改用户点赞出错: {e}")
            return 0

    @classmethod
    def delete_like_by_ids(cls, ids: List[int]) -> int:
        """
        批量删除用户点赞

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        try:
            stmt = delete(LikePo).where(LikePo.id.in_(ids))
            result = db.session.execute(stmt)
            db.session.commit()
            return result.rowcount
        except Exception as e:
            db.session.rollback()
            print(f"批量删除用户点赞出错: {e}")
            return 0

    @classmethod
    def select_like_by_house_id_and_user_id(cls, house_id, user_id) -> Optional[Like]:
        """
        根据 house_id 和 user_id 查询用户点赞

        Args:
            house_id (int): 房源ID
            user_id (int): 用户ID

        Returns:
            like: 用户点赞对象
        """
        try:
            result = db.session.execute(
                select(LikePo).where(LikePo.house_id == house_id, LikePo.user_id == user_id)
            ).scalars().first()
            return Like.model_validate(result) if result else None
        except Exception as e:
            print(f"根据 house_id 和 user_id 查询用户点赞出错: {e}")
            return None

    @classmethod
    def select_likes_after_time(cls, user_id: int, after_time: datetime) -> List[Like]:
        """
        查询指定时间之后用户的点赞记录

        Args:
            user_id (int): 用户ID
            after_time (datetime): 时间点

        Returns:
            List[Like]: 点赞记录列表
        """
        try:
            stmt = select(LikePo).where(
                LikePo.user_id == user_id,
                LikePo.create_time > after_time
            )
            result = db.session.execute(stmt)
            like_pos = result.scalars().all()

            likes = []
            for like_po in like_pos:
                like = Like()
                # 转换PO到Entity
                for attr in like.model_fields.keys():
                    if hasattr(like_po, attr):
                        setattr(like, attr, getattr(like_po, attr))
                likes.append(like)

            return likes
        except Exception as e:
            print(f"查询用户{user_id}在{after_time}之后的点赞记录失败: {str(e)}")
            return []
