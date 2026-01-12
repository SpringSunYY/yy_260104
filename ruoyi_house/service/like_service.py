# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: like_service.py
# @Time    : 2026-01-10 17:29:51

from typing import List, Optional

from ruoyi_common.exception import ServiceException
from ruoyi_common.utils.base import LogUtil
from ruoyi_common.utils.security_util import get_user_id, get_username
from ruoyi_house.domain.entity import Like
from ruoyi_house.mapper import HouseMapper
from ruoyi_house.mapper.like_mapper import LikeMapper
from ruoyi_house.service import HouseService


class LikeService:
    """用户点赞服务类"""

    @classmethod
    def select_like_list(cls, like: Like) -> List[Like]:
        """
        查询用户点赞列表

        Args:
            like (like): 用户点赞对象

        Returns:
            List[like]: 用户点赞列表
        """
        return LikeMapper.select_like_list(like)

    @classmethod
    def select_like_by_id(cls, id: int) -> Optional[Like]:
        """
        根据ID查询用户点赞

        Args:
            id (int): 浏览编号

        Returns:
            like: 用户点赞对象
        """
        return LikeMapper.select_like_by_id(id)

    @classmethod
    def insert_like(cls, like: Like) -> int:
        """
        新增用户点赞

        Args:
            like (like): 用户点赞对象

        Returns:
            int: 插入的记录数
        """
        return LikeMapper.insert_like(like)

    @classmethod
    def like(self, like_entity) -> int:
        """
        点赞

        Args:
            like_entity (Like): 用户点赞对象

        Returns:
            int: 插入的记录数
        """
        # 首先根据房源进行查询
        house = HouseMapper.select_house_by_id(like_entity.house_id)
        if house is None:
            raise ServiceException("用户点赞失败，房源不存在")
        ##其次根据用户和房源进行查询
        user_id = get_user_id()
        like_entity = LikeMapper.select_like_by_user_id_and_house_id(user_id, like_entity.house_id)
        if like_entity is not None and like_entity.id is not None:
            return LikeMapper.delete_like_by_ids([like_entity.id])
        like = Like()
        like.house_id = house.house_id
        like.user_id = user_id
        like.user_name = get_username()
        like.house_title = house.title
        like.cover_image = house.cover_image
        like.house_type = house.house_type
        like.town = house.town
        like.tags = house.tags
        like.orientation = house.orientation
        like.score = 15
        return LikeMapper.insert_like(like)

    @classmethod
    def update_like(cls, like: Like) -> int:
        """
        修改用户点赞

        Args:
            like (like): 用户点赞对象

        Returns:
            int: 更新的记录数
        """
        return LikeMapper.update_like(like)

    @classmethod
    def delete_like_by_ids(cls, ids: List[int]) -> int:
        """
        批量删除用户点赞

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        return LikeMapper.delete_like_by_ids(ids)

    @classmethod
    def import_like(cls, like_list: List[Like], is_update: bool = False) -> str:
        """
        导入用户点赞数据

        Args:
            like_list (List[like]): 用户点赞列表
            is_update (bool): 是否更新已存在的数据

        Returns:
            str: 导入结果消息
        """
        if not like_list:
            raise ServiceException("导入用户点赞数据不能为空")

        success_count = 0
        fail_count = 0
        success_msg = ""
        fail_msg = ""

        for like in like_list:
            try:
                display_value = like

                display_value = getattr(like, "id", display_value)
                existing = None
                if like.id is not None:
                    existing = LikeMapper.select_like_by_id(like.id)
                if existing:
                    if is_update:
                        result = LikeMapper.update_like(like)
                    else:
                        fail_count += 1
                        fail_msg += f"<br/> 第{fail_count}条数据，已存在：{display_value}"
                        continue
                else:
                    result = LikeMapper.insert_like(like)

                if result > 0:
                    success_count += 1
                    success_msg += f"<br/> 第{success_count}条数据，操作成功：{display_value}"
                else:
                    fail_count += 1
                    fail_msg += f"<br/> 第{fail_count}条数据，操作失败：{display_value}"
            except Exception as e:
                fail_count += 1
                fail_msg += f"<br/> 第{fail_count}条数据，导入失败，原因：{e.__class__.__name__}"
                LogUtil.logger.error(f"导入用户点赞失败，原因：{e}")

        if fail_count > 0:
            if success_msg:
                fail_msg = f"导入成功{success_count}条，失败{fail_count}条。{success_msg}<br/>" + fail_msg
            else:
                fail_msg = f"导入成功{success_count}条，失败{fail_count}条。{fail_msg}"
            raise ServiceException(fail_msg)
        success_msg = f"恭喜您，数据已全部导入成功！共 {success_count} 条，数据如下：" + success_msg
        return success_msg
