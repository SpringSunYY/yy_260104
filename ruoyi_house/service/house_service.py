# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: house_service.py
# @Time    : 2026-01-10 17:29:50

from typing import List, Optional

from ruoyi_common.exception import ServiceException
from ruoyi_common.utils.base import LogUtil
from ruoyi_house.domain.entity import House
from ruoyi_house.mapper.house_mapper import HouseMapper

class HouseService:
    """房源信息服务类"""
    @classmethod
    def select_house_list(cls, house: House) -> List[House]:
        """
        查询房源信息列表

        Args:
            house (house): 房源信息对象

        Returns:
            List[house]: 房源信息列表
        """
        return HouseMapper.select_house_list(house)

    
    @classmethod
    def select_house_by_id(cls, hose_id: int) -> Optional[House]:
        """
        根据ID查询房源信息

        Args:
            hose_id (int): 房源编号

        Returns:
            house: 房源信息对象
        """
        return HouseMapper.select_house_by_id(hose_id)
    
    @classmethod
    def insert_house(cls, house: House) -> int:
        """
        新增房源信息

        Args:
            house (house): 房源信息对象

        Returns:
            int: 插入的记录数
        """
        return HouseMapper.insert_house(house)

    
    @classmethod
    def update_house(cls, house: House) -> int:
        """
        修改房源信息

        Args:
            house (house): 房源信息对象

        Returns:
            int: 更新的记录数
        """
        return HouseMapper.update_house(house)
    

    
    @classmethod
    def delete_house_by_ids(cls, ids: List[int]) -> int:
        """
        批量删除房源信息

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        return HouseMapper.delete_house_by_ids(ids)
    
    @classmethod
    def import_house(cls, house_list: List[House], is_update: bool = False) -> str:
        """
        导入房源信息数据

        Args:
            house_list (List[house]): 房源信息列表
            is_update (bool): 是否更新已存在的数据

        Returns:
            str: 导入结果消息
        """
        if not house_list:
            raise ServiceException("导入房源信息数据不能为空")

        success_count = 0
        fail_count = 0
        success_msg = ""
        fail_msg = ""

        for house in house_list:
            try:
                display_value = house
                
                display_value = getattr(house, "hose_id", display_value)
                existing = None
                if house.hose_id is not None:
                    existing = HouseMapper.select_house_by_id(house.hose_id)
                if existing:
                    if is_update:
                        result = HouseMapper.update_house(house)
                    else:
                        fail_count += 1
                        fail_msg += f"<br/> 第{fail_count}条数据，已存在：{display_value}"
                        continue
                else:
                    result = HouseMapper.insert_house(house)
                
                if result > 0:
                    success_count += 1
                    success_msg += f"<br/> 第{success_count}条数据，操作成功：{display_value}"
                else:
                    fail_count += 1
                    fail_msg += f"<br/> 第{fail_count}条数据，操作失败：{display_value}"
            except Exception as e:
                fail_count += 1
                fail_msg += f"<br/> 第{fail_count}条数据，导入失败，原因：{e.__class__.__name__}"
                LogUtil.logger.error(f"导入房源信息失败，原因：{e}")

        if fail_count > 0:
            if success_msg:
                fail_msg = f"导入成功{success_count}条，失败{fail_count}条。{success_msg}<br/>" + fail_msg
            else:
                fail_msg = f"导入成功{success_count}条，失败{fail_count}条。{fail_msg}"
            raise ServiceException(fail_msg)
        success_msg = f"恭喜您，数据已全部导入成功！共 {success_count} 条，数据如下：" + success_msg
        return success_msg