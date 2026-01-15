# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: view_mapper.py
# @Time    : 2026-01-10 17:29:50

from typing import List, Optional
from datetime import datetime

from flask import g
from sqlalchemy import select, update, delete
from sqlalchemy.sql.functions import func

from ruoyi_admin.ext import db
from ruoyi_house.domain.entity import View
from ruoyi_house.domain.po import ViewPo


class ViewMapper:
    """用户浏览Mapper"""

    @classmethod
    def select_view_list(cls, view: View) -> List[View]:
        """
        查询用户浏览列表

        Args:
            view (view): 用户浏览对象

        Returns:
            List[view]: 用户浏览列表
        """
        try:
            # 构建查询条件
            stmt = select(ViewPo)

            if view.id is not None:
                stmt = stmt.where(ViewPo.id == view.id)

            if view.user_name:
                stmt = stmt.where(ViewPo.user_name.like("%" + str(view.user_name) + "%"))
            if view.user_id is not None:
                stmt = stmt.where(ViewPo.user_id == view.user_id)
            if view.house_title:
                stmt = stmt.where(ViewPo.house_title.like("%" + str(view.house_title) + "%"))

            if view.score is not None:
                stmt = stmt.where(ViewPo.score == view.score)

            _params = getattr(view, "params", {}) or {}
            begin_val = _params.get("beginCreateTime")
            end_val = _params.get("endCreateTime")
            if begin_val is not None:
                stmt = stmt.where(ViewPo.create_time >= begin_val)
            if end_val is not None:
                stmt = stmt.where(ViewPo.create_time <= end_val)
            if "criterian_meta" in g and g.criterian_meta.page:
                g.criterian_meta.page.stmt = stmt
                # 应用数据范围过滤（如果 DataScope 设置了有效的过滤条件）
            if ("criterian_meta" in g and
                    g.criterian_meta.scope is not None and
                    g.criterian_meta.scope != [] and
                    g.criterian_meta.scope != ()):
                stmt = stmt.where(g.criterian_meta.scope)
            stmt = stmt.order_by(ViewPo.create_time.desc())
            result = db.session.execute(stmt).scalars().all()
            return [View.model_validate(item) for item in result] if result else []
        except Exception as e:
            print(f"查询用户浏览列表出错: {e}")
            return []

    @classmethod
    def select_view_by_id(cls, id: int) -> Optional[View]:
        """
        根据ID查询用户浏览

        Args:
            id (int): 浏览编号

        Returns:
            view: 用户浏览对象
        """
        try:
            result = db.session.get(ViewPo, id)
            return View.model_validate(result) if result else None
        except Exception as e:
            print(f"根据ID查询用户浏览出错: {e}")
            return None

    @classmethod
    def insert_view(cls, view: View) -> int:
        """
        新增用户浏览

        Args:
            view (view): 用户浏览对象

        Returns:
            int: 插入的记录数
        """
        try:
            now = datetime.now()
            new_po = ViewPo()
            new_po.id = view.id
            new_po.user_id = view.user_id
            new_po.user_name = view.user_name
            new_po.house_id = view.house_id
            new_po.house_title = view.house_title
            new_po.cover_image = view.cover_image
            new_po.town = view.town
            new_po.house_type = view.house_type
            new_po.orientation = view.orientation
            new_po.tags = view.tags
            new_po.score = view.score
            new_po.create_time = view.create_time or now
            db.session.add(new_po)
            db.session.commit()
            view.id = new_po.id
            return 1
        except Exception as e:
            db.session.rollback()
            print(f"新增用户浏览出错: {e}")
            return 0

    @classmethod
    def update_view(cls, view: View) -> int:
        """
        修改用户浏览

        Args:
            view (view): 用户浏览对象

        Returns:
            int: 更新的记录数
        """
        try:

            existing = db.session.get(ViewPo, view.id)
            if not existing:
                return 0
            now = datetime.now()
            # 主键不参与更新
            existing.user_id = view.user_id
            existing.user_name = view.user_name
            existing.house_id = view.house_id
            existing.house_title = view.house_title
            existing.cover_image = view.cover_image
            existing.town = view.town
            existing.house_type = view.house_type
            existing.orientation = view.orientation
            existing.tags = view.tags
            existing.score = view.score
            existing.create_time = view.create_time
            db.session.commit()
            return 1

        except Exception as e:
            db.session.rollback()
            print(f"修改用户浏览出错: {e}")
            return 0

    @classmethod
    def delete_view_by_ids(cls, ids: List[int]) -> int:
        """
        批量删除用户浏览

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        try:
            stmt = delete(ViewPo).where(ViewPo.id.in_(ids))
            result = db.session.execute(stmt)
            db.session.commit()
            return result.rowcount
        except Exception as e:
            db.session.rollback()
            print(f"批量删除用户浏览出错: {e}")
            return 0

    @classmethod
    def select_view_by_house_user_and_date(cls, house_id: str, user_id: int, target_date: str) -> Optional[View]:
        """
        根据 house_id 和 user_id、时间 查询用户浏览，时间格式化为年月日

        Args:
            house_id (int): 房源编号
            user_id (int): 用户编号
            target_date (str): 日期时间对象

        Returns:
            view: 用户浏览对象
        """
        try:
            # 提取创建时间的日期部分并与传入日期的日期部分比较
            stmt = select(ViewPo).where(
                ViewPo.house_id == house_id,
                ViewPo.user_id == user_id,
                func.DATE(ViewPo.create_time) == target_date
            )

            result = db.session.execute(stmt).scalars().first()
            return View.model_validate(result) if result else None
        except Exception as e:
            print(f"根据房源ID、用户ID和时间查询用户浏览出错: {e}")
            return None

    @classmethod
    def select_views_after_time(cls, user_id: int, after_time: datetime) -> List[View]:
        """
        查询指定时间之后用户的浏览记录

        Args:
            user_id (int): 用户ID
            after_time (datetime): 时间点

        Returns:
            List[View]: 浏览记录列表
        """
        try:
            stmt = select(ViewPo).where(
                ViewPo.user_id == user_id,
                ViewPo.create_time > after_time
            )
            result = db.session.execute(stmt)
            view_pos = result.scalars().all()

            views = []
            for view_po in view_pos:
                view = View()
                # 转换PO到Entity
                for attr in view.model_fields.keys():
                    if hasattr(view_po, attr):
                        setattr(view, attr, getattr(view_po, attr))
                views.append(view)

            return views
        except Exception as e:
            print(f"查询用户{user_id}在{after_time}之后的浏览记录失败: {str(e)}")
            return []
