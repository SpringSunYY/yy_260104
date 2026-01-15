from typing import List

from sqlalchemy import select, func

from ruoyi_admin.ext import db
from ruoyi_house.domain.po import HousePo
from ruoyi_house.domain.statistics.dto import HouseStatisticsRequest
from ruoyi_house.domain.statistics.po import StatisticsPo


class HouseStatisticsMapper:
    """房源信息数据访问类"""

    @classmethod
    def orientation_statistics(cls, request: HouseStatisticsRequest) -> List[StatisticsPo]:
        """
        朝向分析
        select
            count(*) as value,
            avg(unit_price) as avg,
            max(unit_price) as max,
            min(unit_price) as min,
            orientation as name
        from tb_house
        group by name
        order by value desc;
        """
        try:
            # 构建查询条件
            stmt = select(
                func.count("*").label("value"),
                func.avg(HousePo.unit_price).label("avg"),
                func.max(HousePo.unit_price).label("max"),
                func.min(HousePo.unit_price).label("min"),
                HousePo.orientation.label("name")
            ).select_from(HousePo).group_by("name").order_by(db.desc("value"))
            stmt = cls.builder_where(request, stmt)
            result = db.session.execute(stmt).mappings().all()
            if not result:
                return []
            return [StatisticsPo(**item) for item in result]
        except Exception as e:
            print(f"获取朝向分析数据失败:{e}")
            return []

    @classmethod
    def builder_where(cls, request, stmt):
        # 创建查询条件
        if request.town:
            stmt = stmt.where(HousePo.town == request.town)
        if request.community:
            stmt = stmt.where(HousePo.community == request.community)
        if request.house_type:
            stmt = stmt.where(HousePo.house_type == request.house_type)
        if request.orientation:
            stmt = stmt.where(HousePo.orientation == request.orientation)
        if request.decoration_type:
            stmt = stmt.where(HousePo.decoration_type == request.decoration_type)
        if request.tags:
            stmt = stmt.where(HousePo.tags.like("%" + request.tags + "%"))
        return stmt

    @classmethod
    def town_statistics(cls, statistics_entity)-> List[StatisticsPo]:
        """
        镇分析
        select
            count(*) as value,
            avg(unit_price) as avg,
            max(unit_price) as max,
            min(unit_price) as min,
            town as name
        from tb_house
        group by name
        order by value desc;
        """
        try:
            # 构建查询条件
            stmt = select(
                func.count("*").label("value"),
                func.avg(HousePo.unit_price).label("avg"),
                func.max(HousePo.unit_price).label("max"),
                func.min(HousePo.unit_price).label("min"),
                HousePo.town.label("name")
            ).select_from(HousePo).group_by("name").order_by(db.desc("value"))
            stmt = cls.builder_where(statistics_entity, stmt)
            result = db.session.execute(stmt).mappings().all()
            if not result:
                return []
            return [StatisticsPo(**item) for item in result]
        except Exception as e:
            print(f"获取镇分析数据失败:{e}")
            return []

    @classmethod
    def price_statistics(cls, statistics_entity)-> List[StatisticsPo]:
        """
        价格分析
        select
            count(*) as value,
            price as name
        from tb_house
        group by name
        order by value desc;
        """
        try:
            # 构建查询条件
            stmt = select(
                func.count("*").label("value"),
                HousePo.unit_price.label("name")
            ).select_from(HousePo).group_by("name").order_by(db.desc("value"))
            stmt = cls.builder_where(statistics_entity, stmt)
            result = db.session.execute(stmt).mappings().all()
            if not result:
                return []
            return [StatisticsPo(**item) for item in result]
        except Exception as e:
            print(f"获取价格分析数据失败:{e}")
            return []
