# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: house_service.py
# @Time    : 2026-01-10 17:29:50

import re
from typing import List, Optional

from werkzeug.datastructures.structures import V

from ruoyi_common.exception import ServiceException
from ruoyi_common.utils import DateUtil
from ruoyi_common.utils.base import LogUtil
from ruoyi_common.utils.security_util import get_user_id, get_username
from ruoyi_house.domain.entity import House, View
from ruoyi_house.mapper import LikeMapper, ViewMapper
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
    def select_house_by_id(cls, house_id: int) -> Optional[House]:
        """
        根据ID查询房源信息

        Args:
            house_id (int): 房源编号

        Returns:
            house: 房源信息对象
        """
        return HouseMapper.select_house_by_id(house_id)

    @classmethod
    def select_house_detail_by_id(cls, house_id: str) -> Optional[House]:
        """
        查询房源信息详情

        Args:
            house_id (int): 房源编号

        Returns:
            house: 房源信息对象
        """
        house = HouseMapper.select_house_by_id(house_id)
        if house is None:
            raise ServiceException(f"没有查询到房源信息【{house_id}】")

        # 查询用户有没有点赞
        user_id = get_user_id()
        like = LikeMapper.select_like_by_house_id_and_user_id(house_id, user_id)
        if like is not None:
            house.is_liked = True
        else:
            house.is_liked = False
        # 查询用户今天是否浏览，如果没有需要添加浏览记录
        nowStr = DateUtil.get_date_now()
        view = ViewMapper.select_view_by_house_user_and_date(house_id, user_id, nowStr)
        if view is None:
            view = View()
            view.house_id = house.house_id
            view.user_id = user_id
            view.user_name = get_username()
            view.house_title = house.title
            view.cover_image = house.cover_image
            view.house_type = house.house_type
            view.town = house.town
            view.tags = house.tags
            view.orientation = house.orientation
            view.score = 1
            ViewMapper.insert_view(view)
        return house

    @classmethod
    def insert_house(cls, house: House) -> int:
        """
        新增房源信息

        Args:
            house (house): 房源信息对象

        Returns:
            int: 插入的记录数
        """
        # 首先判断是否已存在
        existing = HouseMapper.select_house_by_id(house.house_id)
        if existing is not None:
            raise ServiceException(f"房源信息【{house.house_id}】已存在")
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
    def delete_house_by_ids(cls, ids: List[str]) -> int:
        """
        批量删除房源信息

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        return HouseMapper.delete_house_by_ids(ids)

    @classmethod
    def import_house(cls, house_list: List[House], update_support: bool = False) -> str:
        """
        导入房源信息数据

        Args:
            house_list (List[House]): 房源信息列表
            update_support (bool): 是否支持更新（保留参数兼容性，实际根据ID自动判断）

        Returns:
            str: 导入结果消息
        """
        if not house_list:
            raise ServiceException("导入房源信息数据不能为空")

        success_count = 0
        fail_count = 0
        success_msg = ""
        fail_msg = ""
        skip_count = 0

        for index, house in enumerate(house_list, 1):
            try:
                # 格式化数据（主要是数据清理）
                house = cls._format_house_data(house)

                # 检查关键字段是否为空，如果任何一个为空则跳过
                key_fields = [
                    house.house_id,  # 房源编号
                    house.house_code,  # 房源编码
                    house.title,  # 房源标题
                    house.community,  # 小区名称
                    house.address,  # 小区地址
                    house.area,  # 所属区域
                    house.house_type,  # 户型
                    house.area_size,  # 建筑面积
                    house.orientation,  # 朝向
                    house.floor  # 楼层
                ]

                if any(field is None or (isinstance(field, str) and field.strip() == "") for field in key_fields):
                    skip_count += 1
                    continue

                display_value = getattr(house, "house_id", f"第{index}条数据")

                # 根据house_id判断是更新还是新增
                existing = None
                if house.house_id is not None:
                    existing = HouseMapper.select_house_by_id(house.house_id)

                if existing:
                    # 更新现有数据
                    result = HouseMapper.update_house(house)
                    operation = "更新"
                else:
                    # 新增数据
                    result = HouseMapper.insert_house(house)
                    operation = "新增"

                if result > 0:
                    success_count += 1
                    success_msg += f"<br/> 第{success_count}条数据，{operation}成功：{display_value}"
                else:
                    fail_count += 1
                    fail_msg += f"<br/> 第{fail_count}条数据，{operation}失败：{display_value}"
            except Exception as e:
                fail_count += 1
                fail_msg += f"<br/> 第{fail_count}条数据，导入失败，原因：{e.__class__.__name__}"
                LogUtil.logger.error(f"导入房源信息失败，原因：{e}")

        # 构建结果消息
        total_processed = success_count + fail_count
        result_msg = f"共处理 {total_processed} 条数据"

        if skip_count > 0:
            result_msg += f"，跳过 {skip_count} 条（关键字段为空）"

        if fail_count > 0:
            if success_msg:
                fail_msg = f"{result_msg}，导入成功{success_count}条，失败{fail_count}条。{success_msg}<br/>" + fail_msg
            else:
                fail_msg = f"{result_msg}，导入成功{success_count}条，失败{fail_count}条。{fail_msg}"
            raise ServiceException(fail_msg)

        success_msg = f"恭喜您，数据已全部导入成功！{result_msg}，数据如下：" + success_msg
        return success_msg

    @staticmethod
    def _clean_dongguan_town(town_name: str) -> str:
        """
        清理东莞镇名称，转换为完整名称

        Args:
            town_name (str): 原始镇名称

        Returns:
            str: 清理后的镇名称
        """
        if not town_name:
            return town_name

        # 东莞镇名称映射表
        town_mapping = {
            "虎门": "虎门港管委会",
            "大岭山": "大岭山镇",
            "南城": "南城街道",
            "东城": "东城街道",
            "莞城": "莞城街道",
            "万江": "万江街道",
            "石碣": "石碣镇",
            "石龙": "石龙镇",
            "茶山": "茶山镇",
            "石排": "石排镇",
            "企石": "企石镇",
            "横沥": "横沥镇",
            "桥头": "桥头镇",
            "谢岗": "谢岗镇",
            "东坑": "东坑镇",
            "常平": "常平镇",
            "寮步": "寮步镇",
            "樟木头": "樟木头镇",
            "大朗": "大朗镇",
            "黄江": "黄江镇",
            "清溪": "清溪镇",
            "塘厦": "塘厦镇",
            "凤岗": "凤岗镇",
            "长安": "长安镇",
            "虎门港": "虎门港管委会",
            "滨海湾": "滨海湾新区",
            "麻涌": "麻涌镇",
            "中堂": "中堂镇",
            "高埗": "高埗镇",
            "厚街": "厚街镇",
            "望牛墩": "望牛墩镇",
            "洪梅": "洪梅镇",
            "道滘": "道滘镇",
            "沙田": "沙田镇",
            "东莞港": "东莞港管委会",
            "松山湖": "松山湖管委会"
        }

        # 移除常见的后缀
        clean_name = town_name.replace("镇", "").replace("街道", "").replace("新区", "").replace("管委会", "").strip()

        # 返回映射后的名称，如果没有映射则返回原名称
        return town_mapping.get(clean_name, town_name)

    @staticmethod
    def _parse_floor_info(floor_str: str) -> tuple:
        """
        解析楼层信息，提取楼层类型和楼层高度

        Args:
            floor_str (str): 楼层字符串，如 "中层(共16层)"

        Returns:
            tuple: (floor_type, floor_height) 楼层类型和楼层高度
        """
        if not floor_str:
            return None, None

        # 使用正则表达式提取楼层信息
        # 匹配模式：楼层类型(共X层)
        pattern = r'(.+?)\(共(\d+)层\)'
        match = re.match(pattern, floor_str.strip())

        if match:
            floor_type = match.group(1).strip()
            floor_height = int(match.group(2))
            return floor_type, floor_height

        return None, None

    @staticmethod
    def _format_house_data(house: House) -> House:
        """
        格式化导入的房源数据，进行数据清理

        Args:
            house (House): 房源对象

        Returns:
            House: 格式化后的房源对象
        """
        # 数据清理和处理
        # 处理城市和镇信息
        if house.area:
            area_parts = house.area.split()
            if len(area_parts) >= 2:
                house.city = area_parts[0]  # 城市
                if len(area_parts) >= 3:
                    house.town = HouseService._clean_dongguan_town(area_parts[1])  # 镇（取中间的区域名）
                else:
                    house.town = HouseService._clean_dongguan_town(area_parts[1])  # 镇

        # 处理楼层信息
        if house.floor:
            floor_type, floor_height = HouseService._parse_floor_info(house.floor)
            if floor_type:
                house.floor_type = floor_type
            if floor_height:
                house.floor_height = floor_height

        return house
