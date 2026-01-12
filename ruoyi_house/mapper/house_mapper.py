# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: house_mapper.py
# @Time    : 2026-01-10 17:29:50

from typing import List, Optional
from datetime import datetime

from flask import g
from sqlalchemy import select, update, delete

from ruoyi_admin.ext import db
from ruoyi_house.domain.entity import House
from ruoyi_house.domain.po import HousePo

class HouseMapper:
    """房源信息Mapper"""

    @classmethod
    def select_house_list(cls, house: House) -> List[House]:
        """
        查询房源信息列表

        Args:
            house (house): 房源信息对象

        Returns:
            List[house]: 房源信息列表
        """
        try:
            # 构建查询条件
            stmt = select(HousePo)


            if house.house_id:
                stmt = stmt.where(HousePo.house_id.like("%" + str(house.house_id) + "%"))

            if house.house_code:
                stmt = stmt.where(HousePo.house_code.like("%" + str(house.house_code) + "%"))


            if house.title:
                stmt = stmt.where(HousePo.title.like("%" + str(house.title) + "%"))

            if house.community:
                stmt = stmt.where(HousePo.community.like("%" + str(house.community) + "%"))



            if house.city:
                stmt = stmt.where(HousePo.city.like("%" + str(house.city) + "%"))

            if house.town:
                stmt = stmt.where(HousePo.town.like("%" + str(house.town) + "%"))



            if house.house_type:
                stmt = stmt.where(HousePo.house_type.like("%" + str(house.house_type) + "%"))


            if house.orientation is not None:
                stmt = stmt.where(HousePo.orientation == house.orientation)


            if house.floor_height is not None:
                stmt = stmt.where(HousePo.floor_height == house.floor_height)


            if house.floor_type:
                stmt = stmt.where(HousePo.floor_type.like("%" + str(house.floor_type) + "%"))

            if house.building_year:
                stmt = stmt.where(HousePo.building_year.like("%" + str(house.building_year) + "%"))

            if house.decoration_type:
                stmt = stmt.where(HousePo.decoration_type.like("%" + str(house.decoration_type) + "%"))

            if house.tags:
                stmt = stmt.where(HousePo.tags.like("%" + str(house.tags) + "%"))

            if house.property_right_type:
                stmt = stmt.where(HousePo.property_right_type.like("%" + str(house.property_right_type) + "%"))

            if house.property_right_year:
                stmt = stmt.where(HousePo.property_right_year.like("%" + str(house.property_right_year) + "%"))



            if house.property_type is not None:
                stmt = stmt.where(HousePo.property_type == house.property_type)
            if "criterian_meta" in g and g.criterian_meta.page:
                g.criterian_meta.page.stmt = stmt
            result = db.session.execute(stmt).scalars().all()
            return [House.model_validate(item) for item in result] if result else []
        except Exception as e:
            print(f"查询房源信息列表出错: {e}")
            return []


    @classmethod
    def select_house_by_id(cls, house_id: str) -> Optional[House]:
        """
        根据ID查询房源信息

        Args:
            house_id (int): 房源编号

        Returns:
            house: 房源信息对象
        """
        try:
            result = db.session.get(HousePo, house_id)
            return House.model_validate(result) if result else None
        except Exception as e:
            print(f"根据ID查询房源信息出错: {e}")
            return None


    @classmethod
    def insert_house(cls, house: House) -> int:
        """
        新增房源信息

        Args:
            house (house): 房源信息对象

        Returns:
            int: 插入的记录数
        """
        try:
            now = datetime.now()
            new_po = HousePo()
            new_po.house_id = house.house_id
            new_po.house_code = house.house_code
            new_po.cover_image = house.cover_image
            new_po.title = house.title
            new_po.community = house.community
            new_po.address = house.address
            new_po.area = house.area
            new_po.city = house.city
            new_po.town = house.town
            new_po.total_price = house.total_price
            new_po.unit_price = house.unit_price
            new_po.house_type = house.house_type
            new_po.area_size = house.area_size
            new_po.orientation = house.orientation
            new_po.floor = house.floor
            new_po.floor_height = house.floor_height
            new_po.decoration_area = house.decoration_area
            new_po.floor_type = house.floor_type
            new_po.building_year = house.building_year
            new_po.decoration_type = house.decoration_type
            new_po.tags = house.tags
            new_po.property_right_type = house.property_right_type
            new_po.property_right_year = house.property_right_year
            new_po.house_intro = house.house_intro
            new_po.image_urls = house.image_urls
            new_po.property_type = house.property_type
            db.session.add(new_po)
            db.session.commit()
            house.house_id = new_po.house_id
            return 1
        except Exception as e:
            db.session.rollback()
            print(f"新增房源信息出错: {e}")
            return 0


    @classmethod
    def update_house(cls, house: House) -> int:
        """
        修改房源信息

        Args:
            house (house): 房源信息对象

        Returns:
            int: 更新的记录数
        """
        try:

            existing = db.session.get(HousePo, house.house_id)
            if not existing:
                return 0
            now = datetime.now()
            # 主键不参与更新
            existing.house_code = house.house_code
            existing.cover_image = house.cover_image
            existing.title = house.title
            existing.community = house.community
            existing.address = house.address
            existing.area = house.area
            existing.city = house.city
            existing.town = house.town
            existing.total_price = house.total_price
            existing.unit_price = house.unit_price
            existing.house_type = house.house_type
            existing.area_size = house.area_size
            existing.orientation = house.orientation
            existing.floor = house.floor
            existing.floor_height = house.floor_height
            existing.decoration_area = house.decoration_area
            existing.floor_type = house.floor_type
            existing.building_year = house.building_year
            existing.decoration_type = house.decoration_type
            existing.tags = house.tags
            existing.property_right_type = house.property_right_type
            existing.property_right_year = house.property_right_year
            existing.house_intro = house.house_intro
            existing.image_urls = house.image_urls
            existing.property_type = house.property_type
            db.session.commit()
            return 1

        except Exception as e:
            db.session.rollback()
            print(f"修改房源信息出错: {e}")
            return 0

    @classmethod
    def delete_house_by_ids(cls, ids: List[str]) -> int:
        """
        批量删除房源信息

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        try:
            stmt = delete(HousePo).where(HousePo.house_id.in_(ids))
            result = db.session.execute(stmt)
            db.session.commit()
            return result.rowcount
        except Exception as e:
            db.session.rollback()
            print(f"批量删除房源信息出错: {e}")
            return 0
