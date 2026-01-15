from typing import List

from ruoyi_house.domain.statistics.dto import HouseStatisticsRequest
from ruoyi_house.domain.statistics.vo import StatisticsVo
from ruoyi_house.mapper.house_statistics_mapper import HouseStatisticsMapper


class HouseStatisticsService:
    """房源统计服务类"""

    @classmethod
    def orientation_statistics(cls, statistics_entity: HouseStatisticsRequest) -> List[StatisticsVo]:
        """
        获取房源信息统计数据
        """
        pos = HouseStatisticsMapper.orientation_statistics(statistics_entity)
        if not pos:
            return []
        return [StatisticsVo(name=po.name, value=po.value, avg=po.avg, max=po.max, min=po.min) for po in pos]

    @classmethod
    def town_statistics(cls, statistics_entity) -> List[StatisticsVo]:
        """
        获取房源信息统计数据
        """
        pos = HouseStatisticsMapper.town_statistics(statistics_entity)
        if not pos:
            return []
        return [StatisticsVo(name=po.name, value=po.value, avg=po.avg, max=po.max, min=po.min) for po in pos]
