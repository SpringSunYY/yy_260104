import datetime
from typing import List

from ruoyi_common.constant import ConfigConstants
from ruoyi_house.domain.statistics.dto import HouseStatisticsRequest
from ruoyi_house.domain.statistics.po import StatisticsPo
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
                        'min_list': []  # 存储所有最小价格
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
                    min=round(min_price, 2)  # 该标签的最小价格
                ))

        # 按出现次数降序排序
        statistics_list.sort(key=lambda x: x.value, reverse=True)
        return statistics_list

    @classmethod
    def house_type_statistics(cls, statistics_entity) -> List[StatisticsVo]:
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

    @classmethod
    def floor_type_statistics(cls, statistics_entity) -> List[StatisticsVo]:
        """
        获取楼层分析
        """
        pos = HouseStatisticsMapper.floor_type_statistics(statistics_entity)
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
    def community_statistics(cls, statistics_entity) -> List[StatisticsVo]:
        """
        获取小区分析
        """
        limit = 100
        limit_str = SysConfigService.select_config_by_key(ConfigConstants.STATISTICS_COMMITY_LIMIT)
        try:
            if limit_str:
                limit = int(limit_str)
        except ValueError:
            limit = 100
        pos = HouseStatisticsMapper.community_statistics(statistics_entity, limit)
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
    def decoration_type_statistics(cls, statistics_entity)-> List[StatisticsVo]:
        """
        获取装修类型分析
        """
        pos = HouseStatisticsMapper.decoration_type_statistics(statistics_entity)
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
    def price_predict_detailed(cls, statistics_entity)-> List[StatisticsVo]:
        """
        基于详细数据分析的价格预测 加权线性回归 + 周期扰动

        核心思路：
        1. 获取每个房子的详细信息
        2. 按建筑年代分组，但考虑更多影响因素
        3. 使用多维度分析进行更准确的预测
        4. 考虑市场成熟度、位置因素、房屋品质等
        """
        try:
            predict_year_str = SysConfigService.select_config_by_key(ConfigConstants.STATISTICS_PRICE_PREDICT_YEAR)
            start_year_str = SysConfigService.select_config_by_key(ConfigConstants.STATISTICS_PRICE_START_YEAR)

            predict_year = 10
            start_year = 2010

            try:
                if predict_year_str:
                    predict_year = int(predict_year_str)
                if start_year_str:
                    start_year = int(start_year_str)
            except ValueError:
                predict_year = 10
                start_year = 2010

            # 获取详细房源数据
            detailed_data = HouseStatisticsMapper.get_detailed_house_data(statistics_entity, start_year)

            if not detailed_data:
                print("没有获取到详细房源数据")
                return []

            print(f"获取到 {len(detailed_data)} 条详细房源数据")

            # 按建筑年代聚合，但保留更多维度信息
            yearly_stats = cls._analyze_yearly_detailed_data(detailed_data)

            # 确保包含所有年份，即使某些年份没有数据
            complete_yearly_stats = cls._ensure_complete_years(yearly_stats, start_year)

            pos = []
            for year, stats in complete_yearly_stats.items():
                pos.append(StatisticsPo(
                    value=stats['count'],
                    name=str(year),
                    avg=stats['avg_price'],
                    max=stats['max_price'],
                    min=stats['min_price']
                ))

            # 按年份排序
            pos.sort(key=lambda x: int(x.name))

            # 生成预测
            predictions = cls._predict_future_statistics_detailed(pos, predict_year)

            # 合并历史数据和预测数据
            result = []
            for po in pos:
                result.append(StatisticsVo(
                    value=int(po.value),
                    name=po.name,
                    avg=round(float(po.avg), 2),
                    max=round(float(po.max), 2),
                    min=round(float(po.min), 2)
                ))

            # 添加预测数据
            result.extend(predictions)

            return result

        except Exception as e:
            print(f"详细价格预测失败: {e}")
            return []

    @classmethod
    def price_predict(cls, statistics_entity)-> List[StatisticsVo]:
        """
        价格预测
        """
        #从哪一年开始
        start_year=2010
        #预测年数
        predict_year=10
        start_year_str = SysConfigService.select_config_by_key(ConfigConstants.STATISTICS_PRICE_START_YEAR)
        predict_year_str = SysConfigService.select_config_by_key(ConfigConstants.STATISTICS_PRICE_PREDICT_YEAR)
        try:
            if start_year_str:
                start_year = int(start_year_str)
            if predict_year_str:
                predict_year = int(predict_year_str)
        except ValueError:
            start_year = 10
            predict_year = 10
        pos = HouseStatisticsMapper.price_predict(statistics_entity,start_year)
        if not pos:
            return []

        # 转换历史数据为VO格式并按年份升序排序
        historical_data = []
        for po in pos:
            vo = StatisticsVo(
                name=str(po.name) if po.name is not None else None,
                value=int(po.value) if po.value is not None else 0,
                avg=float(po.avg) if po.avg is not None else 0.0,
                max=float(po.max) if po.max is not None else 0.0,
                min=float(po.min) if po.min is not None else 0.0
            )
            historical_data.append(vo)

        # 按年份升序排序历史数据
        def sort_key(item):
            try:
                return int(float(item.name)) if item.name else 0
            except (ValueError, TypeError):
                return 0

        historical_data.sort(key=sort_key)

        # 根据年预测数量以及价格
        predictions = cls._predict_future_statistics(pos, predict_year)

        # 返回历史数据 + 预测数据（都已经按年份排序）
        return historical_data + predictions

    @classmethod
    def _predict_future_statistics(cls, historical_data: List[StatisticsPo], predict_years: int) -> List[StatisticsVo]:
        """
        二手房市场预测：考虑新房vs成熟二手房的区别

        Args:
            historical_data: 历史统计数据
            predict_years: 预测年数

        Returns:
            预测结果列表
        """
        if not historical_data:
            return []

        # 提取年份和对应的统计指标
        years = []
        values = []  # 数量
        avgs = []    # 平均价
        maxs = []    # 最大价
        mins = []    # 最小价

        for data in historical_data:
            try:
                year = int(float(data.name)) if data.name is not None else None
                if year is None:
                    continue

                years.append(year)
                values.append(float(data.value) if data.value is not None else 0)
                avgs.append(float(data.avg) if data.avg is not None else 0)
                maxs.append(float(data.max) if data.max is not None else 0)
                mins.append(float(data.min) if data.min is not None else 0)
            except (ValueError, TypeError):
                continue

        if len(years) < 5:  # 需要足够的历史数据
            return []

        # 对数据按年份排序
        sorted_indices = sorted(range(len(years)), key=lambda i: years[i])
        years = [years[i] for i in sorted_indices]
        values = [values[i] for i in sorted_indices]
        avgs = [avgs[i] for i in sorted_indices]
        maxs = [maxs[i] for i in sorted_indices]
        mins = [mins[i] for i in sorted_indices]

        # 综合预测：各维度独立但相互影响
        # 数量预测独立进行
        predicted_values = cls._predict_volume_independently(values, years, predict_years)

        # 价格预测考虑数量权重（新房数据少，数量权重影响价格预测）
        predicted_avgs = cls._predict_price_with_volume_weight(avgs, values, years, predict_years)
        predicted_maxs = cls._predict_max_price_independently(maxs, years, predict_years)
        predicted_mins = cls._predict_min_price_independently(mins, years, predict_years)

        # 生成连续的预测结果
        predictions = []
        start_year = max(years) + 1  # 从下一年开始预测

        # 确保预测年份连续
        for i in range(predict_years):
            year = start_year + i
            prediction = StatisticsVo(
                name=str(year),
                value=int(predicted_values[i]),
                avg=round(predicted_avgs[i], 2),
                max=round(predicted_maxs[i], 2),
                min=round(predicted_mins[i], 2)
            )
            predictions.append(prediction)

        return predictions

    @classmethod
    def _mature_second_hand_predict(cls, values: List[float], years: List[int], predict_years: int) -> List[float]:
        """
        成熟二手房数量预测：基于多维度权重和趋势分析

        权重因子：
        1. 时间权重：越近的年份权重越大
        2. 数据量权重：数据越多的年份权重越大
        3. 周期权重：考虑市场周期影响
        4. 季节性调整：考虑经济周期

        Args:
            values: 成熟二手房历史数量数据
            years: 年份数据
            predict_years: 预测年数

        Returns:
            预测数量列表
        """
        if not values or not years or len(values) != len(years):
            return [0.0] * predict_years

        current_year = max(years)

        # 1. 计算基础权重（修正：年份越近权重越大，新建筑更重要）
        weights = []
        print(f"预测数量数据权重计算 (当前年份: {current_year}):")

        for i, (year, value) in enumerate(zip(years, values)):
            # 时间权重：年份越近权重越低（新房需要时间进入二手市场，数据可靠性低）
            time_weight = 1 / (1 + (current_year - year) * 0.3)  # 年份越近权重越低

            # 数据量权重：数据越多权重越大，但设置上限
            data_weight = min(value / 300.0, 2.0)  # 降低门槛，提高权重

            # 建筑年代权重：新建筑权重更高
            age = current_year - year
            if age <= 2:
                # 2年内的建筑：权重最高（最新建筑）
                age_weight = 3.0
            elif age <= 5:
                # 2-5年的建筑：权重较高
                age_weight = 2.5 - (age - 2) * 0.2
            elif age <= 10:
                # 5-10年的建筑：权重中等
                age_weight = 2.0 - (age - 5) * 0.1
            else:
                # 10年以上的建筑：权重递减但仍重要
                age_weight = max(0.8, 1.5 - (age - 10) * 0.05)

            # 周期权重：考虑建筑市场周期
            cycle_position = (year % 6) / 6.0  # 6年建筑周期
            cycle_weight = 1 + 0.25 * (0.5 - abs(cycle_position - 0.5)) * 2

            # 异常值调整：异常值降低权重
            mean_value = sum(values) / len(values)
            deviation = abs(value - mean_value) / mean_value
            outlier_penalty = max(0.1, 1 - deviation * 3)  # 更严格的异常值惩罚

            total_weight = time_weight * (1 + data_weight) * age_weight * cycle_weight * outlier_penalty

            # 调试日志
            print(f"建筑年份 {year} (房龄{age}年): 时间权重={time_weight:.2f}, "
                  f"数据权重={data_weight:.2f}, 房龄权重={age_weight:.2f}, "
                  f"周期权重={cycle_weight:.2f}, 异常惩罚={outlier_penalty:.2f}, "
                  f"总权重={total_weight:.2f}")

            weights.append(total_weight)

        # 2. 计算加权统计
        total_weight = sum(weights)
        if total_weight == 0:
            return [sum(values)/len(values)] * predict_years

        weighted_mean = sum(v * w for v, w in zip(values, weights)) / total_weight

        # 3. 计算趋势因子（加权线性回归）
        if len(years) >= 3:
            # 使用加权最小二乘法计算趋势
            weighted_trend = cls._calculate_weighted_trend(years, values, weights)
        else:
            # 计算简单趋势（最近几年变化率）
            if len(values) >= 2:
                recent_trend = (values[-1] - values[0]) / len(values)
                weighted_trend = recent_trend * 0.1  # 保守趋势因子
            else:
                weighted_trend = 0

        # 4. 预测未来值
        predictions = []
        base_value = weighted_mean

        print(f"开始生成{predict_years}年预测 (基础值: {base_value:.2f}, 趋势: {weighted_trend:.4f})")

        for i in range(predict_years):
            future_year = current_year + i + 1

            # 趋势预测
            trend_prediction = base_value + weighted_trend * (i + 1)

            # 周期调整 - 增强波动性
            cycle_position = (future_year % 7) / 7.0
            cycle_adjustment = 1 + 0.25 * (0.5 - abs(cycle_position - 0.5)) * 2  # ±25%周期波动

            # 建筑市场周期 - 新增
            building_cycle = (future_year % 5) / 5.0  # 5年建筑周期
            building_adjustment = 1 + 0.2 * (0.5 - abs(building_cycle - 0.5)) * 2  # ±20%建筑周期

            # 长期衰减（考虑二手房市场饱和）
            long_term_decay = (0.975) ** i  # 每年2.5%的自然衰减

            # 短期波动（模拟市场随机性和政策影响）
            short_term_noise = 1 + 0.15 * ((i % 4) - 1.5) * 0.8  # ±12%波动

            # 季节性调整（考虑一年中的销售高峰）
            seasonal_factor = 1 + 0.08 * ((future_year % 4) - 1.5) * 0.6  # ±4.8%季节性

            prediction = (trend_prediction * cycle_adjustment * building_adjustment *
                         long_term_decay * short_term_noise * seasonal_factor)

            # 约束预测值在合理范围内 - 放宽约束
            min_reasonable = weighted_mean * 0.4  # 不低于加权均值的40%
            max_reasonable = weighted_mean * 2.5  # 不高于加权均值的250%
            prediction = max(min_reasonable, min(prediction, max_reasonable))

            print(f"预测年份 {future_year}: 趋势={trend_prediction:.2f}, 周期={cycle_adjustment:.3f}, "
                  f"建筑周期={building_adjustment:.3f}, 衰减={long_term_decay:.3f}, "
                  f"噪声={short_term_noise:.3f}, 季节性={seasonal_factor:.3f}, "
                  f"最终预测={prediction:.2f}")

            predictions.append(prediction)

        return predictions

    @classmethod
    def _mature_second_hand_price_predict(cls, prices: List[float], years: List[int], predict_years: int) -> List[float]:
        """
        成熟二手房平均价格预测：考虑多重市场因素的独立预测

        影响因子：
        1. 通胀因素：房价通常随通胀上涨
        2. 市场周期：经济周期对房价的影响
        3. 供需关系：区域发展对房价的影响
        4. 政策因素：房地产政策的影响

        Args:
            prices: 成熟二手房历史平均价格数据
            years: 年份数据
            predict_years: 预测年数

        Returns:
            预测价格列表
        """
        if not prices or not years:
            return [0.0] * predict_years

        current_year = max(years)

        # 1. 计算基础统计
        historical_avg = sum(prices) / len(prices)
        recent_count = min(4, len(prices))
        recent_prices = prices[-recent_count:]
        recent_avg = sum(recent_prices) / len(recent_prices)

        # 2. 计算价格趋势（使用指数平滑）
        alpha = 0.3  # 价格变化相对平滑
        smoothed_prices = [prices[0]]
        for i in range(1, len(prices)):
            smoothed_val = alpha * prices[i] + (1 - alpha) * smoothed_prices[-1]
            smoothed_prices.append(smoothed_val)

        # 计算长期趋势
        if len(prices) >= 5:
            # 使用最近5年的数据计算趋势
            trend_prices = prices[-5:]
            trend_years = years[-5:]
            if len(trend_prices) >= 2:
                # 简单线性趋势
                n = len(trend_prices)
                sum_xy = sum(y * p for y, p in zip(trend_years, trend_prices))
                sum_x = sum(trend_years)
                sum_y = sum(trend_prices)
                sum_xx = sum(y * y for y in trend_years)

                denominator = n * sum_xx - sum_x * sum_x
                if denominator != 0:
                    slope = (n * sum_xy - sum_x * sum_y) / denominator
                    trend_rate = slope / recent_avg  # 相对增长率
                else:
                    trend_rate = 0.02  # 默认2%的年增长率
            else:
                trend_rate = 0.02
        else:
            trend_rate = 0.015  # 数据不足时使用保守的1.5%增长率

        # 3. 预测未来价格
        predictions = []
        base_price = recent_avg

        for i in range(predict_years):
            future_year = current_year + i + 1

            # 基础趋势预测
            trend_prediction = base_price * (1 + trend_rate) ** (i + 1)

            # 经济周期调整（假设5-7年周期）
            cycle_position = (future_year % 6) / 6.0  # 6年经济周期
            cycle_factor = 1 + 0.08 * (0.5 - abs(cycle_position - 0.5)) * 2

            # 通胀调整（房价通常略高于通胀）
            inflation_factor = (1.03) ** i  # 假设3%年通胀率，房价增长略高

            # 政策影响因子（模拟房地产调控）
            policy_factor = 1 + 0.05 * (0.5 - abs((i % 5) / 5.0 - 0.5)) * 2

            prediction = trend_prediction * cycle_factor * inflation_factor * policy_factor

            # 约束在合理范围内，避免过度波动
            min_reasonable = historical_avg * 0.8  # 不低于历史均值的80%
            max_reasonable = historical_avg * 1.5  # 不高于历史均值的150%
            prediction = max(min_reasonable, min(prediction, max_reasonable))

            predictions.append(prediction)

        return predictions

    @classmethod
    def _predict_volume_independently(cls, values: List[float], years: List[int], predict_years: int) -> List[float]:
        """
        数量独立预测：基于市场活跃度、人口变化、供应规律

        影响因子：
        1. 人口增长：城市人口增加带动住房需求
        2. 市场饱和：长期来看市场会达到平衡
        3. 经济周期：经济波动影响购房能力
        4. 政策调控：限购限贷影响交易量
        """
        if not values or not years:
            return [0.0] * predict_years

        current_year = max(years)
        print(f"数量独立预测 (当前年: {current_year})")

        # 1. 整体市场趋势分析（考虑新老建筑的市场成熟度差异）
        # 计算各年份的成熟度权重
        volume_weights = []
        for i, (year, value) in enumerate(zip(years, values)):
            # 时间权重：越近权重越低（新房数据不完整）
            time_weight = 1 / (1 + (current_year - year) * 0.2)

            # 数据量权重：数据越多越可靠
            volume_weight = min(value / 300.0, 2.5)

            # 建筑成熟度：新建筑进入市场需要时间
            age = current_year - year
            if age <= 2:
                maturity_weight = 1.5  # 新建筑，数据可能不完整
            elif age <= 5:
                maturity_weight = 2.0  # 逐渐成熟
            elif age <= 10:
                maturity_weight = 2.5  # 成熟期
            else:
                maturity_weight = 2.0  # 老建筑，可靠但市场可能饱和

            total_weight = time_weight * (1 + volume_weight) * maturity_weight
            volume_weights.append(total_weight)

        # 加权计算基准数量
        total_weight = sum(volume_weights)
        if total_weight > 0:
            base_volume = sum(v * w for v, w in zip(values, volume_weights)) / total_weight
        else:
            base_volume = sum(values[-3:]) / min(3, len(values)) if values else 1000

        print(f"整体数量趋势分析: 基准数量={base_volume:.0f}, 平均权重={total_weight/len(volume_weights):.2f}")

        # 2. 整体趋势预测（平滑波动）
        predictions = []

        # 计算整体市场的长期趋势
        if len(values) >= 5:
            # 计算长期趋势变化率
            long_term_trend = (values[-1] - values[0]) / len(values)
            trend_rate = long_term_trend / base_volume if base_volume > 0 else 0
            # 限制在合理范围内
            trend_rate = max(min(trend_rate, 0.02), -0.03)  # -3% 到 2%
        else:
            trend_rate = -0.01  # 默认轻微下降

        for i in range(predict_years):
            future_year = current_year + i + 1

            # 基础趋势预测
            trend_prediction = base_volume * (1 + trend_rate) ** (i + 1)

            # 人口增长调整（温和）
            population_factor = (1.008) ** (i + 1)  # 0.8%年增长

            # 经济周期（平滑波动）
            economic_cycle = 1 + 0.08 * (0.5 - abs((future_year % 7) / 7.0 - 0.5)) * 2

            # 政策影响（温和）
            policy_phase = future_year % 5
            if policy_phase <= 1:
                policy_factor = 1.03  # 温和放松
            elif policy_phase <= 3:
                policy_factor = 0.98  # 温和收紧
            else:
                policy_factor = 1.00  # 稳定

            # 市场饱和度（随着时间推移逐渐稳定）
            saturation_factor = max(0.85, 1 - i * 0.015)  # 每年减少1.5%，最低85%

            prediction = (trend_prediction * population_factor * economic_cycle *
                         policy_factor * saturation_factor)

            # 约束在合理范围内（保守约束）
            min_volume = base_volume * 0.6
            max_volume = base_volume * 1.6
            prediction = max(min_volume, min(prediction, max_volume))

            print(f"整体数量预测年 {future_year}: 基准={base_volume:.0f}, 趋势={trend_prediction:.0f}, "
                  f"人口={population_factor:.3f}, 经济周期={economic_cycle:.3f}, "
                  f"政策={policy_factor:.3f}, 饱和度={saturation_factor:.3f}, "
                  f"最终预测={prediction:.0f}")

            predictions.append(prediction)

        return predictions

    @classmethod
    def _analyze_yearly_detailed_data(cls, detailed_data):
        """
        分析按年份分组的详细数据

        过滤掉大于当前年份的脏数据（未来数据）
        """
        current_year = datetime.datetime.now().year

        yearly_stats = {}

        # 按年份分组数据，过滤掉未来年份的脏数据
        from collections import defaultdict
        yearly_groups = defaultdict(list)

        for house in detailed_data:
            year = house['building_year']
            if year and year <= current_year and house['unit_price'] and house['unit_price'] > 0:  # 只保留有效数据
                yearly_groups[year].append(house)

        print(f"数据过滤: 保留 {len(yearly_groups)} 个有效年份，过滤掉未来年份数据")

        for year, houses in yearly_groups.items():
            prices = []
            areas = []
            house_types = []
            floors = []
            orientations = []
            communities = []

            for house in houses:
                if house['unit_price'] and house['unit_price'] > 0:
                    prices.append(float(house['unit_price']))

                if house['area_size']:
                    areas.append(house['area_size'])

                if house['house_type']:
                    house_types.append(house['house_type'])

                if house['floor']:
                    floors.append(house['floor'])

                if house['orientation']:
                    orientations.append(house['orientation'])

                if house['community']:
                    communities.append(house['community'])

            if prices:
                # 基础价格统计
                avg_price = sum(prices) / len(prices)
                max_price = max(prices)
                min_price = min(prices)

                # 价格分布分析
                sorted_prices = sorted(prices)
                median_price = sorted_prices[len(sorted_prices) // 2]

                # 面积调整因子
                avg_area = sum(areas) / len(areas) if areas else 80

                # 户型多样性（户型越多，市场越成熟）
                unique_house_types = len(set(house_types)) if house_types else 1

                # 位置多样性（小区越多，覆盖范围越广）
                unique_communities = len(set(communities)) if communities else 1

                yearly_stats[year] = {
                    'count': len(prices),
                    'avg_price': avg_price,
                    'median_price': median_price,
                    'max_price': max_price,
                    'min_price': min_price,
                    'avg_area': avg_area,
                    'house_type_diversity': unique_house_types,
                    'location_diversity': unique_communities,
                    'price_volatility': max_price / min_price if min_price > 0 else 1
                }

                print(f"年份 {year}: {len(prices)} 套房源, 平均价格 {avg_price:.0f}, "
                      f"中位数 {median_price:.0f}, 面积 {avg_area:.0f}, "
                      f"户型多样性 {unique_house_types}, 位置多样性 {unique_communities}")

        # 最后再次过滤掉数据量太少的年份
        MIN_HOUSE_COUNT = 5  # 最少5套房源
        filtered_stats = {}
        for year, stats in yearly_stats.items():
            if stats['count'] >= MIN_HOUSE_COUNT:
                filtered_stats[year] = stats
            else:
                print(f"最终过滤: 年份 {year} 房源数 {stats['count']} 太少，排除")

        print(f"最终筛选: 保留 {len(filtered_stats)} 个年份数据")
        return filtered_stats

    @classmethod
    def _ensure_complete_years(cls, yearly_stats, start_year):
        """
        确保所有年份都有数据，包括没有房源数据的年份和预测年份

        Args:
            yearly_stats: 实际查询到的年份统计数据
            start_year: 开始年份

        Returns:
            包含所有年份的完整统计数据
        """
        current_year = max(yearly_stats.keys()) if yearly_stats else start_year

        # 计算有效数据的平均水平，用于推断缺失年份
        valid_counts = [stats['count'] for stats in yearly_stats.values() if stats['count'] > 0]
        valid_prices = [stats['avg_price'] for stats in yearly_stats.values() if stats['avg_price']]

        avg_count = sum(valid_counts) / len(valid_counts) if valid_counts else 1000
        avg_price = sum(valid_prices) / len(valid_prices) if valid_prices else 15000

        # 创建连续的年份列表（包括预测年份）
        complete_stats = {}

        # 历史年份（包括缺失的年份）
        for year in range(start_year, current_year + 1):
            if year in yearly_stats and yearly_stats[year]['count'] > 0:
                complete_stats[year] = yearly_stats[year]
            else:
                # 对于没有数据的年份，基于整体水平推断合理值
                inferred_count = int(avg_count * 0.8)  # 假设缺失年份成交量稍低
                complete_stats[year] = {
                    'count': inferred_count,
                    'avg_price': avg_price,
                    'median_price': avg_price,
                    'max_price': avg_price * 1.5,
                    'min_price': avg_price * 0.5,
                    'avg_area': 85,  # 平均面积
                    'house_type_diversity': 5,
                    'location_diversity': 20,
                    'price_volatility': 0.8
                }
                print(f"补充缺失年份 {year}: 推断 {inferred_count} 套房源，平均价 {avg_price:.0f}")

        return complete_stats

    @classmethod
    def _predict_future_statistics_detailed(cls, historical_data: List[StatisticsPo], predict_years: int) -> List[StatisticsVo]:
        """
        基于详细分析的未来预测

        使用多维度分析：
        1. 价格趋势分析（考虑通胀、经济发展）
        2. 市场成熟度分析（新房vs老房的市场表现）
        3. 供给需求分析（数量变化趋势）
        4. 质量因素分析（房屋品质对价格的影响）
        """
        if not historical_data:
            return []

        # 提取数据
        years = [int(po.name) for po in historical_data]
        values = [int(po.value) for po in historical_data]  # 数量
        avgs = [float(po.avg) for po in historical_data]    # 平均价格
        maxs = [float(po.max) for po in historical_data]    # 最大价格
        mins = [float(po.min) for po in historical_data]    # 最小价格

        print(f"详细预测分析: {len(years)} 个年份的数据, 预测 {predict_years} 年")

        # 使用更精细的预测方法
        predicted_values = cls._predict_volume_detailed(values, years, predict_years)
        predicted_avgs = cls._predict_price_detailed(avgs, values, years, predict_years)
        predicted_maxs = cls._predict_max_price_detailed(maxs, values, years, predict_years)
        predicted_mins = cls._predict_min_price_detailed(mins, values, years, predict_years)

        # 生成预测结果
        predictions = []
        # 从历史数据的最后一个年份开始预测
        last_historical_year = max(years)

        for i in range(predict_years):
            future_year = last_historical_year + i + 1

            predictions.append(StatisticsVo(
                value=int(predicted_values[i]),
                name=str(future_year),
                avg=round(predicted_avgs[i], 2),
                max=round(predicted_maxs[i], 2),
                min=round(predicted_mins[i], 2)
            ))

            print(f"详细预测年 {future_year}: 数量={predicted_values[i]:.0f}, "
                  f"平均价={predicted_avgs[i]:.0f}, 最高价={predicted_maxs[i]:.0f}, "
                  f"最低价={predicted_mins[i]:.0f}")

        return predictions

    @classmethod
    def _predict_volume_detailed(cls, values: List[float], years: List[int], predict_years: int) -> List[float]:
        """基于整体市场趋势的数量预测"""
        current_year = max(years)

        # 从整体市场趋势分析 - 重新设计权重逻辑
        # 核心思想：建筑年代权重优先，数据质量优先，舍弃数据不足的年份
        volume_weights = []
        valid_years = []
        valid_values = []

        # 首先筛选出数据充足的年份（数据量太少的年份不参与权重计算）
        MIN_DATA_THRESHOLD = 10  # 最小数据量阈值

        for i, (year, value) in enumerate(zip(years, values)):
            if value >= MIN_DATA_THRESHOLD:
                valid_years.append(year)
                valid_values.append(value)
            else:
                print(f"年份 {year}: 数据量 {value} 太少，舍弃不参与权重计算")

        print(f"筛选后有效年份: {len(valid_years)} 个 (总共 {len(years)} 个)")

        # 计算整体统计，用于比例权重
        total_data_volume = sum(valid_values)
        max_age = max(current_year - year for year in valid_years)
        min_age = min(current_year - year for year in valid_years)
        age_range = max_age - min_age if max_age > min_age else 1

        # 对有效年份计算权重
        for i, (year, value) in enumerate(zip(valid_years, valid_values)):
            # 建筑年龄：距离现在的年数
            age = current_year - year

            # 建筑年代权重：年龄越大权重越高（老房数据更可靠）
            # 使用比例：年龄占年龄跨度的比例，归一化到1-2倍权重
            age_ratio = (age - min_age) / age_range
            age_weight = 1.0 + age_ratio * 1.0  # 1.0 到 2.0 之间

            # 数据量权重：数量越大权重越高（代表性越强）
            # 使用比例：数据量占总数据量的比例，归一化到1-2倍权重
            data_ratio = value / total_data_volume if total_data_volume > 0 else 0
            data_weight = 1.0 + data_ratio * 10.0  # 根据数据量比例放大权重

            # 时间位置权重：越近的年份在趋势预测中权重略高
            recency_weight = 1 + 0.2 * (1 - 1/(1 + (current_year - year) * 0.5))

            total_weight = age_weight * data_weight * recency_weight
            volume_weights.append(total_weight)

            print(f"年份 {year} (房龄{age}年, 数据{value}): 年代权重={age_weight:.3f}, "
                  f"数据权重={data_weight:.3f}, 位置权重={recency_weight:.2f}, "
                  f"总权重={total_weight:.3f}")

        # 使用整体加权平均作为基准（基于可靠数据）
        if volume_weights:
            total_weight = sum(volume_weights)
            base_volume = sum(v * w for v, w in zip(valid_values, volume_weights)) / total_weight
            print(f"整体数量基准: 基于{len(valid_values)}个有效年份，加权平均 {base_volume:.0f}")
        else:
            # 如果没有有效数据，使用所有数据的简单平均
            base_volume = sum(values) / len(values)
            print(f"整体数量基准: 无有效数据，使用简单平均 {base_volume:.0f}")

        # 识别数据空白年份，包括2027年
        min_year = min(years) if years else current_year
        max_year = max(years) if years else current_year
        missing_years = []
        for y in range(min_year, max_year + 1):
            if y not in years:
                missing_years.append(y)

        if missing_years:
            print(f"数据空白年份: {missing_years}，基于整体趋势推断")
            # 空白年份应该有正常的成交量，不应该被假设为0

        # 计算整体市场长期趋势（使用全部数据）
        if len(values) >= 5:
            # 使用线性回归计算长期趋势
            n = len(years)
            sum_x = sum(years)
            sum_y = sum(values)
            sum_xy = sum(x * y for x, y in zip(years, values))
            sum_xx = sum(x * x for x in years)

            denominator = n * sum_xx - sum_x * sum_x
            if denominator != 0:
                slope = (n * sum_xy - sum_x * sum_y) / denominator
                trend_rate = slope / base_volume if base_volume > 0 else 0
                # 限制在合理范围内
                trend_rate = max(min(trend_rate, 0.05), -0.08)  # -8% 到 5%
            else:
                trend_rate = 0
        else:
            trend_rate = 0

        print(f"整体市场趋势: 每年变化 {trend_rate:.1%}")

        predictions = []
        for i in range(predict_years):
            future_year = current_year + i + 1

            # 基于整体趋势的预测
            trend_prediction = base_volume * (1 + trend_rate) ** (i + 1)

            # 建筑年代成熟度调整（重新设计）
            # 核心思想：新房进入二手市场有一个自然过程，但不应该过度压低预测
            years_since_build = i + 1
            if years_since_build <= 1:
                maturity_factor = 0.5  # 第一年进入较慢
            elif years_since_build <= 3:
                maturity_factor = 0.7 + (years_since_build - 1) * 0.15  # 逐渐加速
            elif years_since_build <= 8:
                maturity_factor = 0.9 + (years_since_build - 3) * 0.025  # 相对稳定
            else:
                maturity_factor = 1.0  # 完全成熟

            # 市场周期调整（温和调整，不要过度波动）
            cycle_factor = 1 + 0.05 * (0.5 - abs((future_year % 7) / 7.0 - 0.5)) * 2

            prediction = trend_prediction * maturity_factor * cycle_factor

            # 更宽松的约束范围，不要被当前数据少而压低预测
            min_volume = max(100, base_volume * 0.3)  # 最低100套或基准的30%
            max_volume = base_volume * 2.0  # 最高2倍基准
            prediction = max(min_volume, min(prediction, max_volume))

            print(f"整体数量预测年 {future_year}: 趋势={trend_prediction:.0f}, "
                  f"成熟度={maturity_factor:.2f}, 周期={cycle_factor:.2f}, 最终={prediction:.0f}")

            predictions.append(prediction)

        return predictions

    @classmethod
    def _predict_price_detailed(cls, prices: List[float], volumes: List[float], years: List[int], predict_years: int) -> List[float]:
        """基于通胀和市场趋势的价格预测（总体上涨）"""
        current_year = max(years)

        # 计算加权平均价格（数量越多权重越大）
        total_volume = sum(volumes)
        weighted_price = sum(p * v for p, v in zip(prices, volumes)) / total_volume if total_volume > 0 else prices[-1]

        # 计算长期通胀调整的价格增长率
        # 房价应该随通胀稳步上涨，不会有太大波动
        if len(prices) >= 3:
            # 计算历史平均增长率，但限制在合理范围内
            growth_rates = []
            for i in range(1, len(prices)):
                if prices[i-1] > 0:
                    growth = (prices[i] - prices[i-1]) / prices[i-1]
                    growth_rates.append(growth)

            if growth_rates:
                avg_growth = sum(growth_rates) / len(growth_rates)
                # 限制在0.5%-5%之间（通胀水平）
                cagr = max(min(avg_growth, 0.05), -0.005)
            else:
                cagr = 0.025  # 默认2.5%增长（通胀水平）
        else:
            cagr = 0.025

        print(f"价格预测基准: {weighted_price:.0f}, 长期增长率: {cagr:.1%}")

        predictions = []
        for i in range(predict_years):
            future_year = current_year + i + 1

            # 基础通胀驱动的价格上涨
            inflation_adjusted_price = weighted_price * (1 + cagr) ** (i + 1)

            # 轻微的经济周期调整（房价不会像数量一样大起大落）
            economic_cycle = 1 + 0.02 * (0.5 - abs((future_year % 8) / 8.0 - 0.5)) * 2

            # 长期趋势保持上涨
            prediction = inflation_adjusted_price * economic_cycle

            print(f"价格预测年 {future_year}: 基准={weighted_price:.0f}, 通胀调整={inflation_adjusted_price:.0f}, "
                  f"经济周期={economic_cycle:.3f}, 最终={prediction:.0f}")

            predictions.append(prediction)

        return predictions

    @classmethod
    def _predict_max_price_detailed(cls, max_prices: List[float], volumes: List[float], years: List[int], predict_years: int) -> List[float]:
        """基于通胀趋势的最大价格预测（总体上涨）"""
        current_year = max(years)

        # 使用加权平均计算基准最高价
        total_volume = sum(volumes)
        weighted_max = sum(p * v for p, v in zip(max_prices, volumes)) / total_volume if total_volume > 0 else max_prices[-1]

        # 计算长期增长率（略高于平均水平，但保持上涨）
        if len(max_prices) >= 3:
            growth_rates = []
            for i in range(1, len(max_prices)):
                if max_prices[i-1] > 0:
                    growth = (max_prices[i] - max_prices[i-1]) / max_prices[i-1]
                    growth_rates.append(growth)

            if growth_rates:
                avg_growth = sum(growth_rates) / len(growth_rates)
                # 限制在0.5%-6%之间（略高于通胀）
                cagr = max(min(avg_growth, 0.06), 0.005)
            else:
                cagr = 0.035  # 默认3.5%增长
        else:
            cagr = 0.035

        print(f"最高价预测基准: {weighted_max:.0f}, 增长率: {cagr:.1%}")

        predictions = []
        for i in range(predict_years):
            future_year = current_year + i + 1

            # 基础通胀上涨
            trend_price = weighted_max * (1 + cagr) ** (i + 1)

            # 轻微的市场波动（高端市场相对稳定）
            market_cycle = 1 + 0.03 * (0.5 - abs((future_year % 10) / 10.0 - 0.5)) * 2

            prediction = trend_price * market_cycle

            print(f"最高价预测年 {future_year}: 趋势={trend_price:.0f}, 周期={market_cycle:.3f}, 最终={prediction:.0f}")

            predictions.append(prediction)

        return predictions

    @classmethod
    def _predict_min_price_detailed(cls, min_prices: List[float], volumes: List[float], years: List[int], predict_years: int) -> List[float]:
        """基于通胀趋势的最小价格预测（总体上涨）"""
        current_year = max(years)

        # 使用加权平均计算基准最低价
        total_volume = sum(volumes)
        weighted_min = sum(p * v for p, v in zip(min_prices, volumes)) / total_volume if total_volume > 0 else min_prices[-1]

        # 计算长期增长率（与通胀保持同步）
        if len(min_prices) >= 3:
            growth_rates = []
            for i in range(1, len(min_prices)):
                if min_prices[i-1] > 0:
                    growth = (min_prices[i] - min_prices[i-1]) / min_prices[i-1]
                    growth_rates.append(growth)

            if growth_rates:
                avg_growth = sum(growth_rates) / len(growth_rates)
                # 限制在0%-4%之间（跟随通胀但略低）
                cagr = max(min(avg_growth, 0.04), -0.01)
            else:
                cagr = 0.02  # 默认2%增长
        else:
            cagr = 0.02

        print(f"最低价预测基准: {weighted_min:.0f}, 增长率: {cagr:.1%}")

        predictions = []
        for i in range(predict_years):
            future_year = current_year + i + 1

            # 基础通胀上涨
            trend_price = weighted_min * (1 + cagr) ** (i + 1)

            # 政策稳定因素（最低价相对稳定）
            policy_stability = 1 + 0.01 * (0.5 - abs((future_year % 5) / 5.0 - 0.5)) * 2

            prediction = trend_price * policy_stability

            print(f"最低价预测年 {future_year}: 趋势={trend_price:.0f}, 政策={policy_stability:.3f}, 最终={prediction:.0f}")

            predictions.append(prediction)

        return predictions

    @classmethod
    def _predict_price_with_volume_weight(cls, prices: List[float], volumes: List[float], years: List[int], predict_years: int) -> List[float]:
        """
        价格预测：基于整体市场趋势和数量置信度

        核心思想：
        1. 整体市场趋势分析：使用全部历史数据建立长期趋势
        2. 数量置信度调节：数据量影响预测的稳定性
        3. 市场成熟度考虑：新老建筑的市场表现差异
        4. 平滑波动：避免过度激进的预测变化

        方法：
        1. 计算整体市场趋势（长期视角）
        2. 应用数量置信度调节（短期数据质量）
        3. 考虑建筑年代成熟度（市场生命周期）
        4. 生成平滑的预测曲线
        """
        if not prices or not volumes or not years:
            return [0.0] * predict_years

        current_year = max(years)
        print(f"价格预测（整体趋势+数量权重）(当前年: {current_year})")

        # 1. 整体市场趋势分析（使用全部数据建立长期视角）
        # 计算整体市场的长期复合增长率
        if len(prices) >= 5:
            # 使用前80%数据计算长期趋势，后20%作为验证
            trend_data_length = int(len(prices) * 0.8)
            trend_prices = prices[:trend_data_length]
            trend_years = years[:trend_data_length]

            if len(trend_prices) >= 3:
                # 计算长期CAGR
                initial_price = trend_prices[0]
                final_price = trend_prices[-1]
                years_diff = trend_years[-1] - trend_years[0]

                if years_diff > 0 and initial_price > 0:
                    long_term_cagr = (final_price / initial_price) ** (1 / years_diff) - 1
                    # 限制在合理范围内
                    long_term_cagr = max(min(long_term_cagr, 0.05), -0.02)  # -2% 到 5%
                else:
                    long_term_cagr = 0.015  # 默认1.5%增长
            else:
                long_term_cagr = 0.015
        else:
            long_term_cagr = 0.015

        # 2. 数量置信度分析（数据质量评估）
        # 计算各年份的数据成熟度权重
        volume_weights = []
        for i, (year, volume) in enumerate(zip(years, volumes)):
            # 时间权重：越近权重越低（新房数据可靠性低）
            time_weight = 1 / (1 + (current_year - year) * 0.25)

            # 数据量权重：数据越多越可靠
            volume_weight = min(volume / 500.0, 3.0)  # 标准化到0-3范围

            # 建筑成熟度：考虑市场生命周期
            age = current_year - year
            if age <= 3:
                maturity_weight = 2.0  # 新建筑，权重较高但数据可能不稳定
            elif age <= 8:
                maturity_weight = 2.5  # 成熟期，权重最高
            elif age <= 15:
                maturity_weight = 2.0  # 衰退初期
            else:
                maturity_weight = 1.5  # 老建筑，可靠性递减

            total_weight = time_weight * (1 + volume_weight) * maturity_weight
            volume_weights.append(total_weight)

        # 计算整体置信度
        total_weight_sum = sum(volume_weights)
        if total_weight_sum > 0:
            avg_weight = total_weight_sum / len(volume_weights)
            confidence_level = min(avg_weight / 10.0, 1.0)  # 标准化到0-1
        else:
            confidence_level = 0.5

        # 3. 综合趋势计算
        # 结合长期趋势和置信度调节
        adjusted_cagr = long_term_cagr * (0.7 + 0.3 * confidence_level)  # 置信度调节范围0.7-1.0

        # 基准价格：使用加权平均，考虑数据质量
        weighted_price_sum = sum(p * w for p, w in zip(prices, volume_weights))
        if total_weight_sum > 0:
            base_price = weighted_price_sum / total_weight_sum
        else:
            base_price = sum(prices[-3:]) / min(3, len(prices)) if prices else 0

        print(f"整体趋势分析: 长期CAGR={long_term_cagr:.1%}, 置信度={confidence_level:.2f}, "
              f"调整后CAGR={adjusted_cagr:.1%}, 基准价格={base_price:.0f}")

        # 4. 生成平滑预测曲线
        predictions = []

        for i in range(predict_years):
            future_year = current_year + i + 1

            # 基础趋势预测
            trend_prediction = base_price * (1 + adjusted_cagr) ** (i + 1)

            # 经济周期调整（平滑波动）
            economic_cycle = 1 + 0.08 * (0.5 - abs((future_year % 7) / 7.0 - 0.5)) * 2

            # 通胀调整
            inflation_adjustment = (1.025) ** (i + 1)  # 保守的2.5%通胀

            # 政策因子（平滑调整）
            policy_phase = future_year % 5
            if policy_phase <= 1:
                policy_factor = 1.04  # 温和放松
            elif policy_phase <= 3:
                policy_factor = 0.98  # 温和收紧
            else:
                policy_factor = 1.01  # 稳定

            # 置信度波动抑制（高置信度允许更多波动）
            volatility_factor = 1 + (confidence_level - 0.5) * 0.05 * ((i % 3) - 1)

            prediction = (trend_prediction * economic_cycle * inflation_adjustment *
                         policy_factor * volatility_factor)

            # 约束范围（基于置信度调整）
            min_bound = base_price * (0.8 - confidence_level * 0.1)  # 置信度高时下限相对宽松
            max_bound = base_price * (2.5 + confidence_level * 0.5)  # 置信度高时上限相对宽松
            prediction = max(min_bound, min(prediction, max_bound))

            print(f"整体价格预测年 {future_year}: 基准={base_price:.0f}, 趋势={trend_prediction:.0f}, "
                  f"经济周期={economic_cycle:.3f}, 通胀={inflation_adjustment:.3f}, "
                  f"政策={policy_factor:.3f}, 波动={volatility_factor:.3f}, "
                  f"最终预测={prediction:.0f}")

            predictions.append(prediction)

        return predictions

    @classmethod
    def _predict_price_independently_with_adjustment(cls, prices: List[float], years: List[int], predict_years: int, growth_multiplier: float = 1.0) -> List[float]:
        """
        二手房平均价格预测：基于学术研究的专业方法

        基于房价预测研究的发现：
        1. 时间序列分析：ARIMA/SARIMA模型
        2. 房龄衰减效应：hedonic价格模型
        3. 宏观经济因子：GDP、通胀、利率
        4. 供需平衡：人口增长vs住房供应

        核心公式：P_t = P_0 * (1 + r)^t * Age_decay * Economic_factors
        """
        if not prices or not years:
            return [0.0] * predict_years

        current_year = max(years)
        print(f"二手房平均价格专业预测 (当前年: {current_year})")

        # 1. 计算历史价格趋势（基于近期数据，避免长期波动影响）
        # 使用最近7年的数据计算趋势，避免历史数据跨度过长导致的异常CAGR
        if len(prices) >= 7:
            # 使用最近7年数据计算趋势
            recent_prices_for_trend = prices[-7:]
            recent_years_for_trend = years[-7:]
            if len(recent_prices_for_trend) >= 2:
                initial_price = recent_prices_for_trend[0]
                final_price = recent_prices_for_trend[-1]
                years_diff = recent_years_for_trend[-1] - recent_years_for_trend[0]
                if years_diff > 0 and initial_price > 0:
                    cagr = (final_price / initial_price) ** (1 / years_diff) - 1
                    # 确保CAGR在合理范围内，至少1%的年增长率
                    cagr = max(cagr, 0.01)  # 最低1%年增长率
                else:
                    cagr = 0.03  # 默认3%年增长率
            else:
                cagr = 0.03
        else:
            cagr = 0.025  # 默认2.5%年增长率

        # 当前基准价格（最近2年平均，避免异常值影响）
        recent_prices = prices[-2:] if len(prices) >= 2 else prices
        current_base_price = sum(recent_prices) / len(recent_prices)

        print(f"平均价趋势分析: 使用最近{len(recent_prices_for_trend) if 'recent_prices_for_trend' in locals() else 'N/A'}年数据, CAGR={cagr:.1%}")

        # 2. 基于研究的预测因子
        predictions = []

        for i in range(predict_years):
            future_year = current_year + i + 1

            # 基础增长趋势（基于历史CAGR）
            trend_growth = (1 + cagr) ** (i + 1)

            # 经济周期调整（基于研究：房价与经济周期相关）
            # 假设经济周期为7年，房价在周期高峰时上涨更快
            economic_cycle_position = (future_year % 7) / 7.0
            economic_multiplier = 1 + 0.12 * (0.5 - abs(economic_cycle_position - 0.5)) * 2

            # 通胀调整（基于央行数据，房价通常领先通胀）
            inflation_adjustment = (1.028) ** (i + 1)  # 房价领先通胀约0.8%

            # 人口增长对房价的影响（城市化驱动）
            population_effect = (1.012) ** (i + 1)  # 1.2%年人口增长影响

            # 政策调控因子（基于中国房地产调控周期）
            policy_cycle = future_year % 5  # 5年调控周期
            if policy_cycle <= 1:  # 调控放松期
                policy_factor = 1.08
            elif policy_cycle <= 3:  # 调控收紧期
                policy_factor = 0.95
            else:  # 调控稳定期
                policy_factor = 1.02

            # 利率影响（房贷利率对房价的影响）
            interest_rate_effect = 1 - 0.05 * ((future_year % 6) / 6.0)  # 利率周期影响

            # 综合预测（基于hedonic价格模型原理）
            prediction = (current_base_price * trend_growth * economic_multiplier *
                         inflation_adjustment * population_effect * policy_factor *
                         interest_rate_effect)

            # 约束在合理范围内（放宽限制，允许更多波动性）
            min_price = current_base_price * (0.7 - 0.03 * i)   # 从0.85放宽到0.7，随着时间进一步放宽
            max_price = current_base_price * (3.0 + 0.1 * i)    # 从2.2放宽到3.0，随着时间进一步放宽
            prediction = max(min_price, min(prediction, max_price))

            print(f"专业房价预测年 {future_year}: 基准价={current_base_price:.0f}, CAGR={cagr:.1%}, "
                  f"经济周期={economic_multiplier:.3f}, 通胀调整={inflation_adjustment:.3f}, "
                  f"人口效应={population_effect:.3f}, 政策={policy_factor:.3f}, "
                  f"利率影响={interest_rate_effect:.3f}, 最终预测={prediction:.0f}")

            predictions.append(prediction)

        return predictions

    @classmethod
    def _predict_max_price_independently(cls, max_prices: List[float], years: List[int], predict_years: int) -> List[float]:
        """
        高端房价预测：基于学术研究的投资组合模型

        基于房地产投资研究的发现：
        1. 高端物业作为投资标的：资本化率模型
        2. 资本流动效应：国际资本偏好
        3. 稀缺性溢价：供应限制驱动价格
        4. 地段品牌价值：位置稀缺性

        核心模型：高端房价 = 基础价值 × 投资回报率 × 资本溢价 × 稀缺性系数
        """
        if not max_prices or not years:
            return [0.0] * predict_years

        current_year = max(years)
        print(f"高端房价专业预测 (当前年: {current_year})")

        # 1. 计算高端市场历史表现
        recent_max_prices = max_prices[-4:] if len(max_prices) >= 4 else max_prices
        current_max_price = recent_max_prices[-1]

        # 计算高端市场的波动性和增长率
        if len(recent_max_prices) >= 2:
            # 计算年均增长率
            growth_rates = []
            for j in range(1, len(recent_max_prices)):
                if recent_max_prices[j-1] > 0:
                    rate = (recent_max_prices[j] - recent_max_prices[j-1]) / recent_max_prices[j-1]
                    growth_rates.append(rate)
            avg_growth_rate = sum(growth_rates) / len(growth_rates) if growth_rates else 0.05
            # 确保高端市场有合理的增长预期
            avg_growth_rate = max(avg_growth_rate, 0.02)  # 最低2%年增长率
        else:
            avg_growth_rate = 0.05  # 默认5%增长率

        # 2. 基于研究的预测因子
        predictions = []

        for i in range(predict_years):
            future_year = current_year + i + 1

            # 投资回报率模型（资本化率倒数）
            # 高端物业通常有更高的资本化率（6-8%），对应较低的资本化率倍数
            cap_rate = 0.07 - 0.005 * ((future_year % 8) / 8.0)  # 7%基础资本化率，略有波动
            investment_multiplier = 1 / cap_rate  # 资本化率倍数

            # 资本流动效应（基于国际资本流动周期）
            capital_flow_cycle = (future_year % 11) / 11.0  # 11年国际资本周期
            capital_premium = 1 + 0.3 * (0.5 - abs(capital_flow_cycle - 0.5)) * 2

            # 稀缺性溢价（基于供应限制）
            # 高端物业供应通常受限，价格随需求增长更快
            scarcity_premium = (1.04) ** (i + 1)  # 4%年稀缺性溢价

            # 地段品牌价值（基于位置经济学）
            location_premium = 1 + 0.08 * ((future_year % 9) / 9.0)  # 9年地段周期

            # 市场情绪因子（高端市场对经济信心更敏感）
            sentiment_factor = 1 + 0.2 * (0.5 - abs((future_year % 6) / 6.0 - 0.5)) * 2

            # 综合预测（基于投资组合理论）
            prediction = (current_max_price * (1 + avg_growth_rate) ** (i + 1) *
                         investment_multiplier * capital_premium * scarcity_premium *
                         location_premium * sentiment_factor)

            # 约束在合理范围内（高端市场波动更大）
            min_price = current_max_price * (0.75 - 0.02 * i)  # 随时间放宽下限
            max_price = current_max_price * (3.5 + 0.1 * i)   # 放宽上限
            prediction = max(min_price, min(prediction, max_price))

            print(f"高端房价预测年 {future_year}: 当前价={current_max_price:.0f}, 投资倍数={investment_multiplier:.2f}, "
                  f"资本溢价={capital_premium:.3f}, 稀缺溢价={scarcity_premium:.3f}, "
                  f"地段溢价={location_premium:.3f}, 情绪因子={sentiment_factor:.3f}, "
                  f"最终预测={prediction:.0f}")

            predictions.append(prediction)

        return predictions

    @classmethod
    def _predict_min_price_independently(cls, min_prices: List[float], years: List[int], predict_years: int) -> List[float]:
        """
        刚需房价预测：基于房地产经济学和政策研究

        基于刚需住房市场研究的发现：
        1. 收入价格比模型：房价收入比稳定在合理区间
        2. 政策干预效应：政府调控对刚需房价格影响显著
        3. 保障性住房供给：公租房、廉租房影响市场价格
        4. 城市化进程：人口流入对刚需房需求的影响

        核心模型：刚需房价 = 收入基础 × 政策调节 × 供给影响 × 通胀调整
        """
        if not min_prices or not years:
            return [0.0] * predict_years

        current_year = max(years)
        print(f"刚需房价专业预测 (当前年: {current_year})")

        # 1. 计算刚需市场历史特征
        recent_min_prices = min_prices[-4:] if len(min_prices) >= 4 else min_prices
        current_min_price = recent_min_prices[-1]

        # 计算价格稳定性（刚需市场波动较小）
        if len(recent_min_prices) >= 2:
            price_volatility = sum(abs(recent_min_prices[i] - recent_min_prices[i-1])
                                 for i in range(1, len(recent_min_prices))) / len(recent_min_prices)
            stability_index = price_volatility / current_min_price  # 价格波动率
        else:
            stability_index = 0.05  # 默认5%波动率

        # 2. 基于研究的预测因子
        predictions = []

        for i in range(predict_years):
            future_year = current_year + i + 1

            # 收入基础（基于居民可支配收入增长）
            # 刚需房价格通常与中等收入家庭购买力相关
            income_base = (1.045) ** (i + 1)  # 4.5%年收入增长

            # 政策调节因子（基于中国房地产调控周期）
            policy_phase = future_year % 6  # 6年政策周期
            if policy_phase <= 1:  # 宽松期
                policy_regulation = 1.06  # 政策放宽，价格略涨
            elif policy_phase <= 4:  # 收紧期
                policy_regulation = 0.96  # 政策收紧，价格受抑
            else:  # 稳定期
                policy_regulation = 0.99  # 政策稳定，价格微跌

            # 保障性住房供给效应
            # 公租房、廉租房等保障性住房会影响市场价格
            affordable_supply_cycle = (future_year % 7) / 7.0  # 7年保障房建设周期
            supply_effect = 1 - 0.08 * (0.5 - abs(affordable_supply_cycle - 0.5)) * 2

            # 城市化进程对刚需房需求的影响
            urbanization_effect = 1 + 0.06 * (0.5 - abs((future_year % 13) / 13.0 - 0.5)) * 2

            # 通胀调整（刚需市场对通胀敏感度较低）
            inflation_adjustment = (1.015) ** (i + 1)  # 1.5%通胀调整

            # 市场周期（刚需市场相对稳定）
            market_stability = 1 + 0.04 * (0.5 - abs((future_year % 10) / 10.0 - 0.5)) * 2

            # 综合预测（基于房地产经济学模型）
            prediction = (current_min_price * income_base * policy_regulation *
                         supply_effect * urbanization_effect * inflation_adjustment *
                         market_stability)

            # 约束在合理范围内（放宽限制，允许合理波动）
            min_price = current_min_price * (0.75 - 0.02 * i)  # 从0.82放宽到0.75，随时间进一步放宽
            max_price = current_min_price * (2.0 + 0.05 * i)   # 从1.45放宽到2.0，随时间进一步放宽
            prediction = max(min_price, min(prediction, max_price))

            print(f"刚需房价预测年 {future_year}: 当前价={current_min_price:.0f}, 收入基础={income_base:.3f}, "
                  f"政策调节={policy_regulation:.3f}, 供给效应={supply_effect:.3f}, "
                  f"城市化={urbanization_effect:.3f}, 通胀调整={inflation_adjustment:.3f}, "
                  f"市场稳定={market_stability:.3f}, 最终预测={prediction:.0f}")

            predictions.append(prediction)

        return predictions

    @classmethod
    def _comprehensive_trend_predict(cls, data: List[float], years: List[int], predict_years: int, data_type: str) -> List[float]:
        """
        基于整体数据趋势的综合预测

        Args:
            data: 历史数据
            years: 年份数据
            predict_years: 预测年数
            data_type: 数据类型 ("volume", "price", "max_price", "min_price")

        Returns:
            预测结果列表
        """
        if not data or not years or len(data) != len(years):
            return [0.0] * predict_years

        current_year = max(years)

        # 1. 计算整体趋势（使用全部数据）
        if len(data) >= 3:
            # 多项式趋势拟合（2次多项式）
            trend_coefficients = cls._polynomial_trend_fit(years, data, degree=2)
        else:
            # 简单线性趋势
            trend_coefficients = cls._linear_trend_fit(years, data)

        # 2. 根据数据类型调整预测策略
        if data_type == "volume":
            # 数量预测：考虑市场周期和季节性
            base_predictions = cls._predict_with_polynomial(years, trend_coefficients, predict_years, current_year)
            predictions = cls._apply_market_cycles(base_predictions, current_year, predict_years)

        elif data_type == "price":
            # 平均价预测：考虑通胀和经济周期
            base_predictions = cls._predict_with_polynomial(years, trend_coefficients, predict_years, current_year)
            predictions = cls._apply_economic_factors(base_predictions, current_year, predict_years)

        elif data_type == "max_price":
            # 最大价预测：考虑高端市场波动
            base_predictions = cls._predict_with_polynomial(years, trend_coefficients, predict_years, current_year)
            predictions = cls._apply_luxury_market_factors(base_predictions, current_year, predict_years)

        elif data_type == "min_price":
            # 最小价预测：考虑刚需市场稳定性和政策影响
            base_predictions = cls._predict_with_polynomial(years, trend_coefficients, predict_years, current_year)
            predictions = cls._apply_affordable_market_factors(base_predictions, current_year, predict_years)

        else:
            # 默认预测
            predictions = cls._predict_with_polynomial(years, trend_coefficients, predict_years, current_year)

        # 3. 约束预测结果在合理范围内
        predictions = cls._constrain_predictions(predictions, data, data_type)

        return predictions

    @classmethod
    def _polynomial_trend_fit(cls, years: List[int], values: List[float], degree: int = 2) -> List[float]:
        """
        多项式趋势拟合

        Args:
            years: 年份数据
            values: 数值数据
            degree: 多项式次数

        Returns:
            多项式系数 [a2, a1, a0] for degree=2
        """
        if len(years) < degree + 1:
            return cls._linear_trend_fit(years, values)

        # 使用最小二乘法拟合多项式
        n = len(years)
        if degree == 2:
            # 2次多项式: y = a2*x^2 + a1*x + a0
            sum_x = sum(years)
            sum_x2 = sum(x**2 for x in years)
            sum_x3 = sum(x**3 for x in years)
            sum_x4 = sum(x**4 for x in years)
            sum_y = sum(values)
            sum_xy = sum(x * y for x, y in zip(years, values))
            sum_x2y = sum(x**2 * y for x, y in zip(years, values))

            # 解线性方程组
            A = [[sum_x4, sum_x3, sum_x2],
                 [sum_x3, sum_x2, sum_x],
                 [sum_x2, sum_x, n]]

            B = [sum_x2y, sum_xy, sum_y]

            try:
                coeffs = cls._solve_linear_system(A, B)
                return coeffs  # [a2, a1, a0]
            except:
                return cls._linear_trend_fit(years, values)

        return cls._linear_trend_fit(years, values)

    @classmethod
    def _linear_trend_fit(cls, years: List[int], values: List[float]) -> List[float]:
        """
        线性趋势拟合

        Returns:
            [slope, intercept] for y = slope*x + intercept
        """
        if len(years) < 2:
            return [0.0, float(values[0]) if values else 0.0]

        n = len(years)
        sum_x = sum(years)
        sum_y = sum(values)
        sum_xy = sum(x * y for x, y in zip(years, values))
        sum_xx = sum(x * x for x in years)

        denominator = n * sum_xx - sum_x * sum_x
        if denominator == 0:
            return [0.0, sum_y / n]

        slope = (n * sum_xy - sum_x * sum_y) / denominator
        intercept = (sum_y - slope * sum_x) / n

        return [slope, intercept]  # [a1, a0] for y = a1*x + a0

    @classmethod
    def _predict_with_polynomial(cls, years: List[int], coeffs: List[float], predict_years: int, current_year: int) -> List[float]:
        """
        使用多项式系数进行预测
        """
        predictions = []
        for i in range(predict_years):
            future_year = current_year + i + 1
            if len(coeffs) == 3:  # 2次多项式
                prediction = coeffs[0] * future_year**2 + coeffs[1] * future_year + coeffs[2]
            elif len(coeffs) == 2:  # 线性
                prediction = coeffs[0] * future_year + coeffs[1]
            else:
                prediction = coeffs[0] if coeffs else 0.0
            predictions.append(prediction)
        return predictions

    @classmethod
    def _apply_market_cycles(cls, predictions: List[float], current_year: int, predict_years: int) -> List[float]:
        """
        应用市场周期调整（针对数量预测）- 增强波动性
        """
        adjusted = []
        for i, pred in enumerate(predictions):
            future_year = current_year + i + 1
            # 3-5年市场周期 - 增强波动幅度
            cycle_factor = 1 + 0.25 * (0.5 - abs((future_year % 5) / 5.0 - 0.5)) * 2
            # 年度季节性调整 - 增加季节性影响
            seasonal_factor = 1 + 0.08 * ((i % 4) - 1.5) * 0.8  # 考虑季度影响
            # 随机市场波动 - 添加不可预测的市场因素
            market_noise = 1 + 0.12 * ((i % 7) - 3) * 0.3  # ±12%的市场噪声
            adjusted_pred = pred * cycle_factor * seasonal_factor * market_noise
            adjusted.append(adjusted_pred)
        return adjusted

    @classmethod
    def _apply_economic_factors(cls, predictions: List[float], current_year: int, predict_years: int) -> List[float]:
        """
        应用经济因素调整（针对价格预测）- 增强波动性
        """
        adjusted = []
        print(f"价格预测经济因子调整 (起始年: {current_year})")

        for i, pred in enumerate(predictions):
            future_year = current_year + i + 1
            # 通胀调整（3%年通胀）
            inflation_factor = (1.03) ** (i + 1)
            # 经济周期调整 - 增强周期影响
            economic_cycle = 1 + 0.25 * (0.5 - abs((future_year % 7) / 7.0 - 0.5)) * 2  # ±25%经济周期
            # 利率影响 - 央行政策对房价的影响
            interest_rate_effect = 1 + 0.2 * ((future_year % 5) - 2) * 0.5  # ±10%利率影响
            # 政策冲击 - 房地产调控影响
            policy_shock = 1 + 0.25 * (0.5 - abs((future_year % 6) / 6.0 - 0.5)) * 2  # ±12.5%政策冲击
            # 建筑成本影响 - 新建筑成本上升
            construction_cost = 1 + 0.08 * ((i % 3) - 1) * 0.6  # ±4.8%建筑成本

            adjusted_pred = (pred * inflation_factor * economic_cycle * interest_rate_effect *
                           policy_shock * construction_cost)

            print(f"价格预测年份 {future_year}: 基础={pred:.2f}, 通胀={inflation_factor:.3f}, "
                  f"经济周期={economic_cycle:.3f}, 利率={interest_rate_effect:.3f}, "
                  f"政策={policy_shock:.3f}, 建筑成本={construction_cost:.3f}, "
                  f"最终={adjusted_pred:.2f}")

            adjusted.append(adjusted_pred)
        return adjusted

    @classmethod
    def _apply_luxury_market_factors(cls, predictions: List[float], current_year: int, predict_years: int) -> List[float]:
        """
        应用高端市场因素（针对最大价预测）- 增强波动性
        """
        adjusted = []
        print(f"高端市场最大价预测调整 (起始年: {current_year})")

        for i, pred in enumerate(predictions):
            future_year = current_year + i + 1
            # 高端市场更易受周期影响 - 增强周期强度
            luxury_cycle = 1 + 0.35 * (0.5 - abs((future_year % 4) / 4.0 - 0.5)) * 2  # ±35%豪宅周期
            # 投资属性影响 - 增强投资波动
            investment_factor = 1 + 0.15 * ((future_year % 3) - 1) * 1.0  # ±15%投资影响
            # 国际资本流动影响 - 外资对高端物业的影响
            capital_flow = 1 + 0.25 * (0.5 - abs((future_year % 8) / 8.0 - 0.5)) * 2  # ±12.5%资本流动
            # 豪宅供应稀缺性 - 供应变化带来的价格波动
            supply_scarcity = 1 + 0.18 * ((future_year % 6) - 2.5) * 0.7  # ±6.3%供应影响
            # 品牌溢价 - 高端物业的品牌价值
            brand_premium = 1 + 0.1 * ((i % 5) - 2) * 0.4  # ±4%品牌溢价

            adjusted_pred = (pred * luxury_cycle * investment_factor * capital_flow *
                           supply_scarcity * brand_premium)

            print(f"最大价预测年份 {future_year}: 基础={pred:.2f}, 豪宅周期={luxury_cycle:.3f}, "
                  f"投资={investment_factor:.3f}, 资本={capital_flow:.3f}, "
                  f"供应={supply_scarcity:.3f}, 品牌={brand_premium:.3f}, "
                  f"最终={adjusted_pred:.2f}")

            adjusted.append(adjusted_pred)
        return adjusted

    @classmethod
    def _apply_affordable_market_factors(cls, predictions: List[float], current_year: int, predict_years: int) -> List[float]:
        """
        应用刚需市场因素（针对最小价预测）- 增强波动性
        """
        adjusted = []
        print(f"刚需市场最小价预测调整 (起始年: {current_year})")

        for i, pred in enumerate(predictions):
            future_year = current_year + i + 1
            # 刚需市场相对稳定但仍有波动 - 增强波动幅度
            stability_factor = 1 + 0.08 * ((future_year % 6) - 2.5) * 0.8  # ±6.4%稳定性波动
            # 政策保障因素 - 增强政策影响
            policy_factor = 1 + 0.12 * (0.5 - abs((future_year % 5) / 5.0 - 0.5)) * 2  # ±12%政策影响
            # 人口结构变化 - 适婚人口变化对刚需房的影响
            demographic_factor = 1 + 0.08 * ((future_year % 7) - 3) * 0.6  # ±4.8%人口影响
            # 城市化进程 - 新市民购房需求
            urbanization_factor = 1 + 0.06 * (0.5 - abs((future_year % 10) / 10.0 - 0.5)) * 2  # ±6%城市化影响
            # 收入增长 - 居民收入对刚需房价格的影响
            income_growth = 1 + 0.04 * ((i % 4) - 1.5) * 0.5  # ±2%收入增长

            adjusted_pred = (pred * stability_factor * policy_factor * demographic_factor *
                           urbanization_factor * income_growth)

            print(f"最小价预测年份 {future_year}: 基础={pred:.2f}, 稳定性={stability_factor:.3f}, "
                  f"政策={policy_factor:.3f}, 人口={demographic_factor:.3f}, "
                  f"城市化={urbanization_factor:.3f}, 收入={income_growth:.3f}, "
                  f"最终={adjusted_pred:.2f}")

            adjusted.append(adjusted_pred)
        return adjusted

    @classmethod
    def _constrain_predictions(cls, predictions: List[float], historical_data: List[float], data_type: str) -> List[float]:
        """
        约束预测结果在合理范围内
        """
        if not historical_data:
            return predictions

        # 计算历史数据的统计特征
        hist_min = min(historical_data)
        hist_max = max(historical_data)
        hist_avg = sum(historical_data) / len(historical_data)

        # 根据数据类型设置不同的约束范围 - 放宽约束以允许更多波动
        if data_type == "volume":
            # 数量约束：不能低于历史最小值的30%，不能高于历史最大值的200% - 放宽范围
            min_bound = hist_min * 0.3
            max_bound = hist_max * 2.0
        elif data_type == "price":
            # 价格约束：不能低于历史平均值的60%，不能高于历史平均值的160% - 放宽范围
            min_bound = hist_avg * 0.6
            max_bound = hist_avg * 1.6
        elif data_type == "max_price":
            # 最大价约束：不能低于历史最大值的60%，不能高于历史最大值的400% - 大幅放宽范围
            min_bound = hist_max * 0.6
            max_bound = hist_max * 4.0
        elif data_type == "min_price":
            # 最小价约束：不能低于历史最小值的70%，不能高于历史平均值的180% - 大幅放宽范围
            min_bound = hist_min * 0.7
            max_bound = hist_avg * 1.8
        else:
            min_bound = hist_min * 0.7
            max_bound = hist_max * 1.5

        # 应用约束
        constrained = []
        for pred in predictions:
            constrained_pred = max(min_bound, min(pred, max_bound))
            constrained.append(constrained_pred)

        return constrained

    @classmethod
    def _solve_linear_system(cls, A: List[List[float]], B: List[float]) -> List[float]:
        """
        解线性方程组 Ax = B（用于多项式拟合）
        使用简单的高斯消元法
        """
        n = len(A)
        if n != len(B):
            raise ValueError("Matrix dimensions don't match")

        # 创建增广矩阵
        augmented = [row[:] + [B[i]] for i, row in enumerate(A)]

        # 高斯消元
        for i in range(n):
            # 找到主元
            max_row = i
            for k in range(i + 1, n):
                if abs(augmented[k][i]) > abs(augmented[max_row][i]):
                    max_row = k

            # 交换行
            augmented[i], augmented[max_row] = augmented[max_row], augmented[i]

            # 检查主元是否为零
            if abs(augmented[i][i]) < 1e-10:
                raise ValueError("Matrix is singular")

            # 消元
            for k in range(i + 1, n):
                factor = augmented[k][i] / augmented[i][i]
                for j in range(i, n + 1):
                    augmented[k][j] -= factor * augmented[i][j]

        # 回代
        x = [0.0] * n
        for i in range(n - 1, -1, -1):
            x[i] = augmented[i][n]
            for j in range(i + 1, n):
                x[i] -= augmented[i][j] * x[j]
            x[i] /= augmented[i][i]

        return x

    @classmethod
    def _calculate_weighted_trend(cls, years: List[int], values: List[float], weights: List[float]) -> float:
        """
        计算加权线性趋势

        Args:
            years: 年份数据
            values: 数值数据
            weights: 对应的权重

        Returns:
            趋势斜率（每年变化量）
        """
        if len(years) < 2 or len(values) != len(years) or len(weights) != len(years):
            return 0.0

        # 计算加权平均
        total_weight = sum(weights)
        if total_weight == 0:
            return 0.0

        weighted_years = sum(y * w for y, w in zip(years, weights)) / total_weight
        weighted_values = sum(v * w for v, w in zip(values, weights)) / total_weight

        # 计算加权协方差和方差
        numerator = sum(w * (y - weighted_years) * (v - weighted_values)
                       for y, v, w in zip(years, values, weights))
        denominator = sum(w * (y - weighted_years) ** 2 for y, w in zip(years, weights))

        if denominator == 0:
            return 0.0

        # 返回趋势斜率（每年变化量）
        return numerator / denominator

    @classmethod
    def _mature_second_hand_extreme_predict(cls, extreme_prices: List[float], years: List[int], price_type: str, predict_years: int) -> List[float]:
        """
        成熟二手房极值价格预测：最大价和最小价的独立预测

        Args:
            extreme_prices: 极值价格数据（最大价或最小价）
            years: 年份数据
            price_type: "max" 或 "min"
            predict_years: 预测年数

        Returns:
            预测价格列表
        """
        if not extreme_prices or not years:
            return [0.0] * predict_years

        current_year = max(years)

        # 为最大价和最小价分别设计不同的预测策略

        if price_type == "max":
            # 最大价预测：通常受豪宅市场影响，更易波动
            # 使用指数平滑 + 趋势调整
            if len(extreme_prices) >= 3:
                # 计算趋势（最近3年的变化率）
                recent_prices = extreme_prices[-3:]
                trend_rate = (recent_prices[-1] - recent_prices[0]) / recent_prices[0]

                # 指数平滑预测
                alpha = 0.4  # 较高平滑系数，反映市场波动
                smoothed = [extreme_prices[0]]
                for i in range(1, len(extreme_prices)):
                    smoothed_val = alpha * extreme_prices[i] + (1 - alpha) * smoothed[-1]
                    smoothed.append(smoothed_val)

                base_price = smoothed[-1]
            else:
                base_price = sum(extreme_prices) / len(extreme_prices)
                trend_rate = 0.02  # 默认2%的年增长率

        else:  # price_type == "min"
            # 最小价预测：通常受刚需市场影响，相对稳定
            # 使用保守的移动平均
            recent_count = min(4, len(extreme_prices))
            recent_prices = extreme_prices[-recent_count:]
            base_price = sum(recent_prices) / len(recent_prices)

            # 最小价通常变化较慢
            trend_rate = 0.01  # 默认1%的年增长率

        # 生成预测
        predictions = []
        for i in range(predict_years):
            if price_type == "max":
                # 最大价：考虑市场周期，每3-4年有一个高峰
                cycle_factor = 1 + 0.1 * (0.5 - abs((i % 4) / 4.0 - 0.5)) * 2
                prediction = base_price * (1 + trend_rate) ** (i + 1) * cycle_factor
            else:
                # 最小价：稳定增长，偶尔小幅调整
                stability_factor = 1 + 0.005 * ((i % 2) * 2 - 1)  # ±0.5%的微调
                prediction = base_price * (1 + trend_rate) ** (i + 1) * stability_factor

            # 约束在合理范围内
            if price_type == "max":
                min_bound = base_price * 0.8
                max_bound = base_price * 2.0
            else:
                min_bound = base_price * 0.9
                max_bound = base_price * 1.5

            prediction = max(min_bound, min(prediction, max_bound))
            predictions.append(prediction)

        return predictions

    @classmethod
    def _second_hand_count_predict(cls, values: List[float], years: List[int], predict_years: int) -> List[float]:
        """
        二手房数量预测：考虑数据稀疏性和市场成熟度

        Args:
            values: 历史数量数据
            years: 年份数据
            predict_years: 预测年数

        Returns:
            预测数量列表
        """
        if not values or not years:
            return [0.0] * predict_years

        # 计算各年份的数据权重（基于数据量和时间距离）
        current_year = max(years)
        weights = []
        for i, (year, value) in enumerate(zip(years, values)):
            # 时间权重：越近的年份权重越低（新房数据不成熟）
            time_weight = 1 / (1 + (current_year - year) * 0.3)
            # 数据量权重：数据越多的年份权重越大
            data_weight = min(value / 1000, 2.0)  # 数据量权重上限为2
            total_weight = time_weight * (1 + data_weight)
            weights.append(total_weight)

        # 加权平均作为预测基础
        total_weight = sum(weights)
        if total_weight == 0:
            return [sum(values)/len(values)] * predict_years

        weighted_avg = sum(v * w for v, w in zip(values, weights)) / total_weight

        # 二手房数量预测：考虑市场逐渐成熟，数量会逐步稳定
        predictions = []
        for i in range(predict_years):
            # 随着时间推移，预测值逐渐趋于稳定
            stability_factor = min(i * 0.1, 0.5)  # 稳定性因子
            prediction = weighted_avg * (1 - stability_factor) + (weighted_avg * 0.8) * stability_factor
            predictions.append(max(prediction, 1))  # 确保至少为1

        return predictions

    @classmethod
    def _second_hand_price_predict(cls, prices: List[float], years: List[int], predict_years: int) -> List[float]:
        """
        二手房价格预测：考虑房龄效应和市场周期

        Args:
            prices: 历史价格数据
            years: 年份数据
            predict_years: 预测年数

        Returns:
            预测价格列表
        """
        if not prices or not years:
            return [0.0] * predict_years

        current_year = max(years)

        # 计算房龄效应：新房价格更高
        age_adjusted_prices = []
        for i, (price, year) in enumerate(zip(prices, years)):
            age = current_year - year
            # 房龄调整：假设新房价格比实际高20%，每增加1年房龄下降2%
            age_factor = 1.2 * (0.98 ** age) if age <= 10 else 0.8  # 房龄超过10年按80%计算
            adjusted_price = price / age_factor
            age_adjusted_prices.append(adjusted_price)

        # 使用调整后的价格进行趋势预测
        if len(age_adjusted_prices) >= 3:
            # 计算趋势
            recent_prices = age_adjusted_prices[-3:]
            trend = (recent_prices[-1] - recent_prices[0]) / len(recent_prices)

            # 预测未来价格
            last_price = recent_prices[-1]
            predictions = []
            for i in range(predict_years):
                future_price = last_price + trend * (i + 1)
                # 确保价格在合理范围内
                future_price = max(future_price, min(recent_prices) * 0.8)
                future_price = min(future_price, max(recent_prices) * 1.5)
                predictions.append(future_price)
        else:
            # 数据不足，使用简单平均
            avg_price = sum(age_adjusted_prices) / len(age_adjusted_prices)
            predictions = [avg_price] * predict_years

        return predictions

    @classmethod
    def _second_hand_conservative_predict(cls, prices: List[float], values: List[float], predict_years: int) -> List[float]:
        """
        二手房保守预测：基于数据量加权的平均值

        Args:
            prices: 价格数据
            values: 对应数量数据（作为权重）
            predict_years: 预测年数

        Returns:
            预测价格列表
        """
        if not prices or not values:
            return [0.0] * predict_years

        # 使用数据量作为权重计算加权平均
        total_weight = sum(values)
        if total_weight == 0:
            return [sum(prices)/len(prices)] * predict_years

        weighted_avg = sum(p * v for p, v in zip(prices, values)) / total_weight

        # 对于波动较大的价格数据，使用更保守的预测
        # 预测值为加权平均值，略微考虑趋势
        predictions = []
        for i in range(predict_years):
            # 轻微的趋势调整（±5%）
            trend_factor = 1 + (i * 0.01)  # 每年上涨1%
            prediction = weighted_avg * trend_factor
            predictions.append(prediction)

        return predictions

    @classmethod
    def _exponential_smoothing_predict(cls, data: List[float], predict_years: int, alpha: float = 0.3) -> List[float]:
        """
        使用指数平滑预测波动性数据

        Args:
            data: 历史数据列表
            predict_years: 预测年数
            alpha: 平滑系数 (0-1之间，越小越保守)

        Returns:
            预测值列表
        """
        if not data:
            return [0.0] * predict_years

        # 计算指数平滑值
        smoothed = [data[0]]  # 初始值
        for i in range(1, len(data)):
            smoothed_value = alpha * data[i] + (1 - alpha) * smoothed[-1]
            smoothed.append(smoothed_value)

        # 使用最后一个平滑值作为预测起点
        last_smoothed = smoothed[-1]

        # 对于未来预测，考虑轻微趋势衰减
        predictions = []
        for i in range(predict_years):
            # 每次预测略微衰减，模拟下降趋势
            decay_factor = 0.95 ** i  # 每次衰减5%
            prediction = max(last_smoothed * decay_factor, 1)  # 确保不小于1
            predictions.append(prediction)

        return predictions

    @classmethod
    def _conservative_predict(cls, data: List[float], predict_years: int) -> List[float]:
        """
        对于波动性大的数据使用保守预测策略
        从整体历史数据计算平均值，而不是最近几年

        Args:
            data: 历史数据列表
            predict_years: 预测年数

        Returns:
            预测值列表
        """
        if not data:
            return [0.0] * predict_years

        # 计算全部历史数据的平均值作为预测值
        avg_value = sum(data) / len(data)

        # 对于所有预测年份，使用整体平均值
        return [avg_value] * predict_years
