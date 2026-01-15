from typing import List

from ruoyi_common.constant import ConfigConstants
from ruoyi_house.domain.statistics.dto import HouseStatisticsRequest
from ruoyi_house.domain.statistics.vo import StatisticsVo
from ruoyi_house.mapper.house_statistics_mapper import HouseStatisticsMapper
from ruoyi_system.service import SysConfigService


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
        return [StatisticsVo(
            name=po.name,
            value=po.value,
            avg=po.avg,
            max=po.max,
            min=po.min
        ) for po in pos]

    @classmethod
    def town_statistics(cls, statistics_entity) -> List[StatisticsVo]:
        """
        获取房源信息统计数据
        """
        pos = HouseStatisticsMapper.town_statistics(statistics_entity)
        if not pos:
            return []
        return [StatisticsVo(
            name=po.name,
            value=po.value,
            avg=po.avg,
            max=po.max,
            min=po.min
        ) for po in pos]

    @classmethod
    def price_statistics(cls, statistics_entity) -> List[StatisticsVo]:
        """
        获取房源信息统计数据
        """
        pos = HouseStatisticsMapper.price_statistics(statistics_entity)
        if not pos:
            return []
        # 价格范围
        price_range = [8000, 12000, 20000, 30000, 40000]
        price_range_str = SysConfigService.select_config_by_key(ConfigConstants.STATISTICS_PRICE_RANGE)
        if price_range_str:
            try:
                # 配置格式为 "8000,12000,20000,30000,40000"
                price_range = [int(x.strip()) for x in price_range_str.split(',')]
            except ValueError:
                # 如果配置格式错误，使用默认值
                price_range = [8000, 12000, 20000, 30000, 40000]
        result = {}

        for po in pos:
            # name 是价格，value 是数量
            price = float(po.name)
            count = int(po.value)

            # 根据价格确定范围标签
            price_label = cls._get_price_range_label(price, price_range)

            # 累加数量
            if price_label not in result:
                result[price_label] = 0
            result[price_label] += count

        # 格式化结果
        statistics_list = []
        for price_label, total_count in result.items():
            statistics_list.append(StatisticsVo(
                name=price_label,
                value=total_count
            ))

        # 按价格范围排序
        def sort_key(vo):
            if '以下' in vo.name:
                return 0
            elif '以上' in vo.name:
                return float('inf')
            else:
                # 提取价格数字
                import re
                match = re.search(r'(\d+)', vo.name.replace('K', '000').replace('W', '0000'))
                return int(match.group(1)) if match else 0

        statistics_list.sort(key=sort_key)
        return statistics_list

    @staticmethod
    def _get_price_range_label(price: float, price_range: List[int]) -> str:
        """
        根据价格获取范围标签
        """
        if price < price_range[0]:
            return f"{HouseStatisticsService._format_price(price_range[0])}以下"
        elif price >= price_range[-1]:
            return f"{HouseStatisticsService._format_price(price_range[-1])}以上"
        else:
            for i in range(len(price_range) - 1):
                if price_range[i] <= price < price_range[i + 1]:
                    return f"{HouseStatisticsService._format_price(price_range[i])}-{HouseStatisticsService._format_price(price_range[i + 1])}"
        return f"{HouseStatisticsService._format_price(price_range[-1])}以上"

    @staticmethod
    def _format_price(price: float) -> str:
        """
        格式化价格显示
        小于10000显示为K，大于等于10000显示为W
        """
        if price < 10000:
            return f"{int(price / 1000)}K"
        else:
            # 计算万为单位，保留一位小数
            w_value = price / 10000
            if w_value == int(w_value):
                return f"{int(w_value)}W"
            else:
                return f"{w_value:.1f}W"
