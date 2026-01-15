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

    @classmethod
    def tags_statistics(cls, statistics_entity) -> List[StatisticsVo]:
        """
        获取标签统计数据
        标签存储格式为分号分割，如："标签1;标签2;标签3"
        """
        pos = HouseStatisticsMapper.tags_statistics(statistics_entity)
        if not pos:
            return []

        # 用于存储每个标签的统计数据
        tag_stats = {}

        for po in pos:
            # 分号分割
            if po.name and isinstance(po.name, str):
                tags = [tag.strip() for tag in po.name.split(';') if tag.strip()]
            else:
                continue

            # 为每个标签累加统计数据
            # value是标签组合的出现次数，avg/max/min是mapper中查询的价格统计
            count_value = int(po.value) if po.value is not None else 1
            for tag in tags:
                if tag not in tag_stats:
                    tag_stats[tag] = {
                        'count': 0,  # 标签出现次数
                        'total_avg': 0,  # 平均价格总和
                        'max_list': [],  # 存储所有最大价格
                        'min_list': []   # 存储所有最小价格
                    }

                tag_stats[tag]['count'] += count_value
                if po.avg is not None:
                    tag_stats[tag]['total_avg'] += float(po.avg)
                if po.max is not None:
                    tag_stats[tag]['max_list'].append(float(po.max))
                if po.min is not None:
                    tag_stats[tag]['min_list'].append(float(po.min))

        # 转换为StatisticsVo对象
        statistics_list = []
        for tag_name, stats in tag_stats.items():
            if stats['count'] > 0:
                # 计算该标签的平均价格
                avg_price = stats['total_avg'] / stats['count'] if stats['total_avg'] > 0 else 0
                # 该标签的最大价格是所有记录中最大的max值
                max_price = max(stats['max_list']) if stats['max_list'] else 0
                # 该标签的最小价格是所有记录中最小的min值
                min_price = min(stats['min_list']) if stats['min_list'] else 0

                statistics_list.append(StatisticsVo(
                    name=tag_name,
                    value=stats['count'],  # 标签出现次数
                    avg=round(avg_price, 2),  # 该标签的平均价格
                    max=round(max_price, 2),  # 该标签的最大价格
                    min=round(min_price, 2)   # 该标签的最小价格
                ))

        # 按出现次数降序排序
        statistics_list.sort(key=lambda x: x.value, reverse=True)
        return statistics_list

    @classmethod
    def house_type_statistics(cls, statistics_entity)-> List[StatisticsVo]:
        """
        获取房屋类型统计数据
        """
        pos = HouseStatisticsMapper.house_type_statistics(statistics_entity)
        if not pos:
            return []
        return [StatisticsVo(
            name=po.name,
            value=po.value,
            avg=po.avg,
            max=po.max,
            min=po.min
        ) for po in pos]
