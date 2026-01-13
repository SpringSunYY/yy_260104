# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: recommend_service.py
# @Time    : 2026-01-10 17:29:50

import json
from datetime import datetime
from typing import List, Optional, Dict, Tuple

from ruoyi_common.exception import ServiceException
from ruoyi_common.utils.base import LogUtil
from ruoyi_common.utils.security_util import get_username
from ruoyi_house.domain.entity import Recommend, House, Like, View
from ruoyi_house.mapper import LikeMapper, ViewMapper
from ruoyi_house.mapper.house_mapper import HouseMapper
from ruoyi_house.mapper.recommend_mapper import RecommendMapper


class RecommendService:
    """用户推荐服务类"""

    # 推荐算法配置
    WEIGHTS = {
        'town': 6,  # 镇权重
        'house_type': 15,  # 户型权重
        'orientation': 10,  # 朝向权重
        'tags': 3  # 标签权重
    }

    # 时间衰减配置 - 基于最新行为记录的指数衰减
    TIME_DECAY_FACTOR = 0.95  # 每天衰减0.05（即前一天权重为0.95）
    VIEW_RECORDS_COUNT = 30  # 最新浏览记录数量
    VIEW_NEW_RECORDS_COUNT = 5  # 创建模型后最新浏览记录数量
    LIKE_RECORDS_COUNT = 5  # 最新点赞记录数量
    LIKE_NEW_RECORDS_COUNT = 1  # 创建模型后最新点赞记录数量
    # 推荐配置
    MAX_RECOMMENDATIONS = 1000  # 最大推荐数量
    TAG_COMBINATION_BONUS = 1.5  # 标签组合奖励倍数

    @classmethod
    def generate_recommendations(cls, user_id: int, top_n: int = 10) -> List[str]:
        """
        生成用户推荐房源列表（优化版本，避免全表查询）

        Args:
            user_id (int): 用户ID
            top_n (int): 返回推荐房源数量

        Returns:
            List[str]: 推荐房源ID列表
        """
        try:
            # 1. 获取用户的喜欢和浏览记录
            user_behaviors = cls._get_user_behaviors(user_id)
            if not user_behaviors:
                LogUtil.logger.info(f"用户{user_id}没有行为记录，无法生成推荐")
                return []

            # 2. 计算用户偏好向量
            user_preferences = cls._calculate_user_preferences(user_behaviors)

            # 3. 智能采样房源进行评分（避免全表查询）
            sampled_houses = cls._sample_houses_for_scoring(user_preferences, top_n * 10)  # 采样更多用于排序
            LogUtil.logger.info(f"[推荐算法] 对{len(sampled_houses)}个采样房源进行评分计算")

            house_scores = cls._calculate_house_scores(sampled_houses, user_preferences, user_behaviors)
            LogUtil.logger.info(f"[推荐算法] 计算出{len(house_scores)}个房源得分")

            # 4. 直接排序并返回Top N（不过滤已交互房源）
            recommended_houses = cls._sort_houses_by_score(house_scores, top_n)
            LogUtil.logger.info(f"[推荐算法] 最终生成{len(recommended_houses)}个推荐房源")

            return recommended_houses

        except Exception as e:
            LogUtil.logger.error(f"生成用户{user_id}推荐失败: {str(e)}")
            raise ServiceException(f"生成推荐失败: {str(e)}")

    @classmethod
    def save_user_recommendations(cls, user_id: int, recommendations: List[str], model_info: Dict) -> int:
        """
        保存用户推荐结果

        Args:
            user_id (int): 用户ID
            recommendations (List[str]): 推荐房源ID列表
            model_info (Dict): 推荐模型信息

        Returns:
            int: 保存的记录数
        """
        try:
            # 验证数据
            if not recommendations:
                raise ValueError("推荐内容不能为空")

            # 序列化并验证JSON格式
            model_info_json = json.dumps(model_info, ensure_ascii=False)
            content_json = json.dumps(recommendations, ensure_ascii=False)

            # 验证JSON可以正确反序列化
            try:
                json.loads(model_info_json)
                json.loads(content_json)
            except json.JSONDecodeError as e:
                LogUtil.logger.error(f"JSON序列化验证失败: {str(e)}")
                raise ValueError(f"JSON格式错误: {str(e)}")

            recommend = Recommend()
            recommend.user_id = user_id
            recommend.user_name = get_username()
            recommend.model_info = model_info_json
            recommend.content = content_json
            recommend.create_time = datetime.now()

            result = RecommendMapper.insert_recommend(recommend)
            LogUtil.logger.info(
                f"成功保存用户{user_id}推荐，模型信息长度: {len(model_info_json)}, 内容长度: {len(content_json)}")
            return result
        except Exception as e:
            LogUtil.logger.error(f"保存用户{user_id}推荐失败: {str(e)}")
            raise ServiceException(f"保存推荐失败: {str(e)}")

    @classmethod
    def should_generate_recommendations(cls, user_id: int) -> bool:
        """
        判断是否需要生成推荐

        Args:
            user_id (int): 用户ID

        Returns:
            bool: 是否需要生成推荐
        """
        try:
            # 查询用户的推荐记录
            recommend = RecommendMapper.select_latest_recommend_by_user_id(user_id)

            # 如果没有推荐记录，需要生成
            if not recommend:
                LogUtil.logger.info(f"[判断推荐] 用户{user_id}没有推荐记录，需要生成")
                return True

            # 获取最新的推荐记录
            recommend_create_time = recommend.create_time

            if not recommend_create_time:
                LogUtil.logger.info(f"[判断推荐] 用户{user_id}推荐记录没有创建时间，需要重新生成")
                return True

            LogUtil.logger.info(f"[判断推荐] 用户{user_id}最新推荐创建时间: {recommend_create_time}")

            # 检查从推荐创建时间之后的新行为

            # 检查浏览记录：5条浏览
            new_views = ViewMapper.select_views_after_time(user_id, recommend_create_time)
            view_count = len(new_views) if new_views else 0
            LogUtil.logger.info(f"[判断推荐] 用户{user_id}推荐创建后新增浏览数: {view_count}")

            # 检查点赞记录：1条点赞
            new_likes = LikeMapper.select_likes_after_time(user_id, recommend_create_time)
            like_count = len(new_likes) if new_likes else 0
            LogUtil.logger.info(f"[判断推荐] 用户{user_id}推荐创建后新增点赞数: {like_count}")

            # 如果同时满足浏览了n条且点赞了n条，才需要重新生成推荐
            should_generate = view_count >= cls.VIEW_NEW_RECORDS_COUNT or like_count >= cls.LIKE_NEW_RECORDS_COUNT
            LogUtil.logger.info(
                f"[判断推荐] 用户{user_id}是否需要重新生成推荐: {should_generate} (浏览{view_count}>={cls.VIEW_NEW_RECORDS_COUNT} 且 点赞{like_count}>={cls.LIKE_NEW_RECORDS_COUNT})")

            return should_generate

        except Exception as e:
            LogUtil.logger.error(f"[判断推荐] 检查用户{user_id}是否需要生成推荐失败: {str(e)}")
            # 出错时保守处理，返回True重新生成
            return True

    @classmethod
    def get_user_recommendations_with_auto_generate(cls, user_id: int, page_num: int = 1, page_size: int = 10) -> Tuple[
        List[House], int]:
        """
        获取用户推荐房源列表，自动生成推荐逻辑

        Args:
            user_id (int): 用户ID
            page_num (int): 页码
            page_size (int): 每页大小

        Returns:
            Tuple[List[House], int]: (房源列表, 总数)
        """
        # 只有第一页才检查是否需要生成推荐
        if page_num != 1:
            return cls._get_user_recommendations(user_id, page_num, page_size)

        # 检查是否需要生成推荐
        should_generate = cls.should_generate_recommendations(user_id)
        LogUtil.logger.info(f"[推荐服务] 用户{user_id}是否需要生成推荐: {should_generate}")

        if not should_generate:
            return cls._get_user_recommendations(user_id, page_num, page_size)

        # 生成推荐
        try:
            LogUtil.logger.info(f"[推荐服务] 用户{user_id}开始生成推荐")
            recommendations = cls.generate_recommendations(user_id, top_n=cls.MAX_RECOMMENDATIONS)
            LogUtil.logger.info(f"[推荐服务] 用户{user_id}生成了{len(recommendations)}个推荐")

            if not recommendations:
                LogUtil.logger.warning(f"[推荐服务] 用户{user_id}没有生成到推荐内容")
                return cls._get_user_recommendations(user_id, page_num, page_size)

            # 构建并保存推荐模型
            model_info = cls._build_model_info(user_id, recommendations)
            result = cls.save_user_recommendations(user_id, recommendations, model_info)
            LogUtil.logger.info(f"[推荐服务] 用户{user_id}推荐保存结果: {result}")

        except Exception as e:
            LogUtil.logger.error(f"[推荐服务] 用户{user_id}自动生成推荐失败: {str(e)}")

        return cls._get_user_recommendations(user_id, page_num, page_size)

    @classmethod
    def _build_model_info(cls, user_id: int, recommendations: List[str]) -> Dict:
        """
        构建推荐模型信息

        Args:
            user_id (int): 用户ID
            recommendations (List[str]): 推荐房源ID列表

        Returns:
            Dict: 模型信息
        """
        # 获取用户偏好数据
        user_behaviors = cls._get_user_behaviors(user_id)
        user_preferences = cls._calculate_user_preferences(user_behaviors)

        # 构建分类的维度评分模型
        town_model = []
        house_type_model = []
        orientation_model = []
        tags_model = []

        if user_preferences.get('town'):
            town_model = [{'name': name, 'value': round(score, 2)} for name, score in user_preferences['town'].items()]
        if user_preferences.get('house_type'):
            house_type_model = [{'name': name, 'value': round(score, 2)} for name, score in
                                user_preferences['house_type'].items()]
        if user_preferences.get('orientation'):
            orientation_model = [{'name': name, 'value': round(score, 2)} for name, score in
                                 user_preferences['orientation'].items()]
        if user_preferences.get('tags'):
            tags_model = [{'name': name, 'value': round(score, 2)} for name, score in user_preferences['tags'].items()]

        return {
            'algorithm': 'multiDimensionCollaborativeFiltering',
            'weights': {
                'town': float(cls.WEIGHTS['town']),
                'houseType': float(cls.WEIGHTS['house_type']),
                'orientation': float(cls.WEIGHTS['orientation']),
                'tags': float(cls.WEIGHTS['tags'])
            },
            'timeDecayFactor': float(cls.TIME_DECAY_FACTOR),
            'viewRecordsCount': cls.VIEW_RECORDS_COUNT,
            'likeRecordsCount': cls.LIKE_RECORDS_COUNT,
            'viewNewRecordsCount': cls.VIEW_NEW_RECORDS_COUNT,
            'likeNewRecordsCount': cls.LIKE_NEW_RECORDS_COUNT,
            'tagCombinationBonus': float(cls.TAG_COMBINATION_BONUS),
            'total': float(cls.MAX_RECOMMENDATIONS),
            'createTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'autoGenerated': True,
            'totalRecommended': float(len(recommendations)),
            'modelInfo': {
                'townModel': town_model,
                'houseTypeModel': house_type_model,
                'orientationModel': orientation_model,
                'tagsModel': tags_model
            }
        }

    @classmethod
    def _get_user_recommendations(cls, user_id: int, page_num: int = 1, page_size: int = 10) -> Tuple[List[House], int]:
        """
        获取用户推荐房源列表

        Args:
            user_id (int): 用户ID
            page_num (int): 页码
            page_size (int): 每页大小

        Returns:
            Tuple[List[House], int]: (房源列表, 总数)
        """
        from ruoyi_house.service.house_service import HouseService

        # 直接查询用户的最新推荐记录
        latest_recommend = RecommendMapper.select_latest_recommend_by_user_id(user_id)

        if not latest_recommend:
            LogUtil.logger.info(f"[推荐服务] 用户{user_id}没有推荐记录")
            return [], 0

        LogUtil.logger.info(
            f"[推荐服务] 用户{user_id}最新推荐记录ID: {latest_recommend.id}, 创建时间: {latest_recommend.create_time}")

        # 解析推荐的房源ID列表
        try:
            if not latest_recommend.content or not latest_recommend.content.strip():
                LogUtil.logger.warning(f"[推荐服务] 用户{user_id}推荐内容为空")
                return [], 0

            recommended_house_ids = json.loads(latest_recommend.content)
            if not isinstance(recommended_house_ids, list):
                LogUtil.logger.error(
                    f"[推荐服务] 用户{user_id}推荐数据格式错误: 期望列表类型，实际为{type(recommended_house_ids)}")
                return [], 0

            LogUtil.logger.info(
                f"[推荐服务] 用户{user_id}推荐房源总数: {len(recommended_house_ids)}, 房源ID列表: {recommended_house_ids[:10]}...")
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            LogUtil.logger.error(f"[推荐服务] 用户{user_id}推荐数据格式错误: {str(e)}")
            # 尝试清理损坏的推荐记录
            try:
                RecommendMapper.delete_recommend_by_ids([latest_recommend.id])
                LogUtil.logger.info(f"[推荐服务] 已清理损坏的推荐记录 ID: {latest_recommend.id}")
            except Exception as clean_e:
                LogUtil.logger.error(f"[推荐服务] 清理损坏记录失败: {str(clean_e)}")
            return [], 0

        if not recommended_house_ids:
            LogUtil.logger.info(f"[推荐服务] 用户{user_id}推荐房源列表为空")
            return [], 0

        # 分页处理推荐房源ID
        start_idx = (page_num - 1) * page_size
        end_idx = start_idx + page_size
        page_house_ids = recommended_house_ids[start_idx:end_idx]

        LogUtil.logger.info(
            f"[推荐服务] 用户{user_id}分页参数: page_num={page_num}, page_size={page_size}, 返回房源数: {len(page_house_ids)}")

        # 查询对应的房源信息
        houses = []
        success_count = 0
        fail_count = 0

        for house_id in page_house_ids:
            try:
                house = HouseService.select_house_by_id(str(house_id))
                if house:
                    houses.append(house)
                    success_count += 1
                else:
                    fail_count += 1
                    LogUtil.logger.warning(f"[推荐服务] 用户{user_id}房源{house_id}查询结果为空")
            except Exception as e:
                fail_count += 1
                LogUtil.logger.error(f"[推荐服务] 用户{user_id}房源{house_id}查询失败: {str(e)}")
                continue

        LogUtil.logger.info(
            f"[推荐服务] 用户{user_id}房源查询完成: 成功{success_count}个, 失败{fail_count}个, 总共返回{len(houses)}个房源")

        return houses, len(recommended_house_ids)

    @classmethod
    def _get_user_behaviors(cls, user_id: int) -> List[Dict]:
        """
        获取用户最新的行为记录

        Args:
            user_id (int): 用户ID

        Returns:
            List[Dict]: 用户行为记录列表
        """

        behaviors = []

        # 获取最新点赞记录（5条）- 按时间倒序
        like_entity = Like()
        like_entity.user_id = user_id
        like_entity.page_size = cls.LIKE_RECORDS_COUNT
        likes = LikeMapper.select_like_list(like_entity)
        # 确保按时间倒序排序
        likes = sorted(likes, key=lambda x: x.create_time, reverse=True)[:cls.LIKE_RECORDS_COUNT]

        for like in likes:
            behaviors.append({
                'house_id': like.house_id,
                'town': like.town,
                'house_type': like.house_type,
                'orientation': like.orientation,
                'tags': like.tags,
                'score': float(like.score) if like.score else 1.0,
                'create_time': like.create_time,
                'behavior_type': 'like'
            })

        # 获取最新浏览记录- 按时间倒序
        view_entity = View()
        view_entity.user_id = user_id
        view_entity.page_size = cls.VIEW_RECORDS_COUNT
        views = ViewMapper.select_view_list(view_entity)
        # 确保按时间倒序排序
        views = sorted(views, key=lambda x: x.create_time, reverse=True)[:cls.VIEW_RECORDS_COUNT]

        for view in views:
            behaviors.append({
                'house_id': view.house_id,
                'town': view.town,
                'house_type': view.house_type,
                'orientation': view.orientation,
                'tags': view.tags,
                'score': float(view.score) if view.score else 1.0,
                'create_time': view.create_time,
                'behavior_type': 'view'
            })

        LogUtil.logger.info(f"[推荐算法] 获取到用户{user_id}的{len(likes)}条点赞记录和{len(views)}条浏览记录")
        return behaviors

    @classmethod
    def _calculate_time_weight(cls, create_time: datetime, base_time: datetime = None) -> float:
        """
        计算时间权重（基于最新行为记录的指数衰减）

        Args:
            create_time (datetime): 行为记录创建时间
            base_time (datetime): 基准时间（通常是最新的行为记录时间）

        Returns:
            float: 时间权重
        """
        if not create_time:
            return 0.5  # 默认权重

        if base_time is None:
            base_time = datetime.now()

        days_diff = (base_time - create_time).days
        if days_diff <= 0:
            return 1.0  # 最新行为权重最高

        # 指数衰减：昨天0.95，前天0.95^2 ≈ 0.9025，以此类推
        time_weight = cls.TIME_DECAY_FACTOR ** days_diff

        return max(time_weight, 0.1)  # 确保最低权重为0.1

    @classmethod
    def _calculate_user_preferences(cls, behaviors: List[Dict]) -> Dict:
        """
        计算用户偏好向量（基于最新行为记录时间作为基准）

        Args:
            behaviors (List[Dict]): 用户行为记录

        Returns:
            Dict: 用户偏好向量
        """
        if not behaviors:
            return {
                'town': {},
                'house_type': {},
                'orientation': {},
                'tags': {}
            }

        preferences = {
            'town': {},
            'house_type': {},
            'orientation': {},
            'tags': {}
        }

        # 找到最新行为记录的时间作为基准时间
        latest_time = max(behavior['create_time'] for behavior in behaviors)

        for behavior in behaviors:
            time_weight = cls._calculate_time_weight(behavior['create_time'], latest_time)
            score = behavior['score'] * time_weight

            # 处理镇偏好
            if behavior['town']:
                preferences['town'][behavior['town']] = preferences['town'].get(behavior['town'], 0) + score

            # 处理户型偏好
            if behavior['house_type']:
                preferences['house_type'][behavior['house_type']] = preferences['house_type'].get(
                    behavior['house_type'], 0) + score

            # 处理朝向偏好
            if behavior['orientation']:
                preferences['orientation'][behavior['orientation']] = preferences['orientation'].get(
                    behavior['orientation'], 0) + score

            # 处理标签偏好
            if behavior['tags']:
                tags = behavior['tags'].split(';') if behavior['tags'] else []
                for tag in tags:
                    tag = tag.strip()
                    if tag:
                        preferences['tags'][tag] = preferences['tags'].get(tag, 0) + score

        LogUtil.logger.info(f"[推荐算法] 计算用户偏好完成，基准时间: {latest_time}")
        return preferences

    @classmethod
    def _sample_houses_for_scoring(cls, user_preferences: Dict, sample_size: int = 100) -> List[House]:
        """
        智能采样房源用于评分计算（基于相似性而非精确匹配）

        Args:
            user_preferences (Dict): 用户偏好向量
            sample_size (int): 采样数量

        Returns:
            List[House]: 采样房源列表
        """
        try:
            sampled_houses = []
            seen_ids = set()

            # 1. 基于相似性采样（而非精确匹配）
            similar_houses = cls._sample_similar_houses(user_preferences, sample_size)
            for house in similar_houses:
                if house.house_id not in seen_ids:
                    sampled_houses.append(house)
                    seen_ids.add(house.house_id)

            # 2. 补充热门/最新房源，确保有足够的候选房源
            remaining = sample_size - len(sampled_houses)
            if remaining > 0:
                recent_houses = cls._query_recent_houses(remaining * 2)  # 多取一些用于去重
                for house in recent_houses:
                    if house.house_id not in seen_ids:
                        sampled_houses.append(house)
                        seen_ids.add(house.house_id)
                        if len(sampled_houses) >= sample_size:
                            break

            LogUtil.logger.info(f"[推荐算法] 采样到{len(sampled_houses)}个房源用于评分计算")
            return sampled_houses[:sample_size]

        except Exception as e:
            LogUtil.logger.error(f"[推荐算法] 采样房源失败: {str(e)}")
            return []

    @classmethod
    def _sample_similar_houses(cls, user_preferences: Dict, limit: int) -> List[House]:
        """
        基于相似性采样房源（而非精确匹配）

        Args:
            user_preferences (Dict): 用户偏好
            limit (int): 限制数量

        Returns:
            List[House]: 相似房源列表
        """
        similar_houses = []
        seen_ids = set()

        # 1. 基于镇的相似性采样（相同城市或其他相关镇）
        if user_preferences.get('town'):
            town_houses = cls._sample_similar_by_town(user_preferences['town'], limit // 4)
            for house in town_houses:
                if house.house_id not in seen_ids:
                    similar_houses.append(house)
                    seen_ids.add(house.house_id)

        # 2. 基于户型的相似性采样（面积相近的户型）
        if user_preferences.get('house_type'):
            type_houses = cls._sample_similar_by_house_type(user_preferences['house_type'], limit // 4)
            for house in type_houses:
                if house.house_id not in seen_ids:
                    similar_houses.append(house)
                    seen_ids.add(house.house_id)

        # 3. 基于朝向的相似性采样（相近朝向）
        if user_preferences.get('orientation'):
            orientation_houses = cls._sample_similar_by_orientation(user_preferences['orientation'], limit // 4)
            for house in orientation_houses:
                if house.house_id not in seen_ids:
                    similar_houses.append(house)
                    seen_ids.add(house.house_id)

        # 4. 基于标签的相似性采样（包含相似标签）
        if user_preferences.get('tags'):
            tag_houses = cls._sample_similar_by_tags(user_preferences['tags'], limit // 4)
            for house in tag_houses:
                if house.house_id not in seen_ids:
                    similar_houses.append(house)
                    seen_ids.add(house.house_id)

        LogUtil.logger.info(f"[相似性采样] 采样到{len(similar_houses)}个相似房源")
        return similar_houses[:limit]

    @classmethod
    def _sample_similar_by_town(cls, town_preferences: Dict, limit: int) -> List[House]:
        """
        基于镇的相似性采样（优先相同镇，然后是同一城市的其他镇）

        Args:
            town_preferences (Dict): 镇偏好 {'镇名': 权重}
            limit (int): 限制数量

        Returns:
            List[House]: 相似房源
        """
        houses = []
        seen_ids = set()

        # 按偏好排序
        sorted_towns = sorted(town_preferences.items(), key=lambda x: x[1], reverse=True)

        for town, _ in sorted_towns:
            # 1. 先采样完全匹配的镇
            exact_houses = cls._query_houses_by_condition({'town': town}, limit // 2)
            for house in exact_houses:
                if house.house_id not in seen_ids:
                    houses.append(house)
                    seen_ids.add(house.house_id)
                    if len(houses) >= limit:
                        return houses

        return houses

    @classmethod
    def _sample_similar_by_house_type(cls, type_preferences: Dict, limit: int) -> List[House]:
        """
        基于户型的相似性采样（只考虑完全匹配）

        Args:
            type_preferences (Dict): 户型偏好 {'户型': 权重}
            limit (int): 限制数量

        Returns:
            List[House]: 相似房源
        """
        houses = []
        seen_ids = set()

        # 按偏好排序
        sorted_types = sorted(type_preferences.items(), key=lambda x: x[1], reverse=True)

        for house_type, _ in sorted_types:
            # 只采样完全匹配的户型
            exact_houses = cls._query_houses_by_condition({'house_type': house_type}, limit)
            for house in exact_houses:
                if house.house_id not in seen_ids:
                    houses.append(house)
                    seen_ids.add(house.house_id)
                    if len(houses) >= limit:
                        return houses

        return houses

    @classmethod
    def _sample_similar_by_orientation(cls, orientation_preferences: Dict, limit: int) -> List[House]:
        """
        基于朝向的相似性采样（相近朝向）

        Args:
            orientation_preferences (Dict): 朝向偏好 {'朝向': 权重}
            limit (int): 限制数量

        Returns:
            List[House]: 相似房源
        """
        houses = []
        seen_ids = set()

        # 定义朝向相似度映射
        orientation_similarity = {
            '南': ['东南', '西南', '南北'],
            '北': ['东北', '西北', '南北'],
            '东': ['东南', '东北', '东西'],
            '西': ['西南', '西北', '东西'],
            '东南': ['南', '东', '西南'],
            '西南': ['南', '西', '西北'],
            '东北': ['北', '东', '西北'],
            '西北': ['北', '西', '西南'],
            '南北': ['南', '北', '东南', '西南'],
            '东西': ['东', '西', '东南', '西北'],
        }

        # 按偏好排序
        sorted_orientations = sorted(orientation_preferences.items(), key=lambda x: x[1], reverse=True)

        for orientation, _ in sorted_orientations:
            # 1. 先采样完全匹配的朝向
            exact_houses = cls._query_houses_by_condition({'orientation': orientation}, limit // 3)
            for house in exact_houses:
                if house.house_id not in seen_ids:
                    houses.append(house)
                    seen_ids.add(house.house_id)
                    if len(houses) >= limit:
                        return houses

            # 2. 采样相似朝向
            similar_orientations = orientation_similarity.get(orientation, [])
            for similar_orientation in similar_orientations:
                similar_houses = cls._query_houses_by_condition({'orientation': similar_orientation}, limit // 6)
                for house in similar_houses:
                    if house.house_id not in seen_ids:
                        houses.append(house)
                        seen_ids.add(house.house_id)
                        if len(houses) >= limit:
                            return houses

        return houses

    @classmethod
    def _sample_similar_by_tags(cls, tag_preferences: Dict, limit: int) -> List[House]:
        """
        基于标签的相似性采样（包含相似标签的房源）

        Args:
            tag_preferences (Dict): 标签偏好 {'标签': 权重}
            limit (int): 限制数量

        Returns:
            List[House]: 相似房源
        """
        houses = []
        seen_ids = set()

        # 按偏好排序
        sorted_tags = sorted(tag_preferences.items(), key=lambda x: x[1], reverse=True)

        for tag, _ in sorted_tags[:3]:  # 只取前3个最喜欢的标签
            # 使用标签模糊匹配查询（需要在mapper中实现）
            tag_houses = cls._query_houses_by_condition({'tags': tag}, limit // 3)
            for house in tag_houses:
                if house.house_id not in seen_ids:
                    houses.append(house)
                    seen_ids.add(house.house_id)
                    if len(houses) >= limit:
                        return houses

        return houses

    @classmethod
    def _sample_random_houses(cls, limit: int) -> List[House]:
        """
        随机采样房源

        Args:
            limit (int): 限制数量

        Returns:
            List[House]: 随机房源
        """
        return cls._query_recent_houses(limit)

    @classmethod
    def _query_houses_by_condition(cls, conditions: Dict, limit: int = 50) -> List[House]:
        """
        根据条件查询房源（调用Mapper层方法）

        Args:
            conditions (Dict): 查询条件
            limit (int): 限制数量

        Returns:
            List[House]: 房源列表
        """
        try:
            # 根据条件调用对应的Mapper方法
            if 'town' in conditions and conditions['town']:
                houses = HouseMapper.select_houses_by_town(conditions['town'], limit)
                LogUtil.logger.info(f"[条件查询] 按镇查询 '{conditions['town']}' 得到{len(houses)}个房源")
                return houses

            elif 'house_type' in conditions and conditions['house_type']:
                houses = HouseMapper.select_houses_by_house_type(conditions['house_type'], limit)
                LogUtil.logger.info(f"[条件查询] 按户型查询 '{conditions['house_type']}' 得到{len(houses)}个房源")
                return houses

            elif 'orientation' in conditions and conditions['orientation']:
                houses = HouseMapper.select_houses_by_orientation(conditions['orientation'], limit)
                LogUtil.logger.info(f"[条件查询] 按朝向查询 '{conditions['orientation']}' 得到{len(houses)}个房源")
                return houses

            elif 'tags' in conditions and conditions['tags']:
                houses = HouseMapper.select_houses_by_tag_like(conditions['tags'], limit)
                LogUtil.logger.info(f"[条件查询] 按标签模糊查询 '{conditions['tags']}' 得到{len(houses)}个房源")
                return houses

            else:
                # 没有有效条件，返回空列表
                LogUtil.logger.warning(f"[条件查询] 无效查询条件: {conditions}")
                return []

        except Exception as e:
            LogUtil.logger.error(f"[条件查询] 查询条件{conditions}失败: {str(e)}")
            return []

    @classmethod
    def _query_recent_houses(cls, limit: int = 50) -> List[House]:
        """
        查询最近的房源（调用Mapper层方法）

        Args:
            limit (int): 限制数量

        Returns:
            List[House]: 房源列表
        """
        try:
            houses = HouseMapper.select_recent_houses(limit)
            LogUtil.logger.info(f"[查询房源] 查询到{len(houses)}个最近房源")
            return houses
        except Exception as e:
            LogUtil.logger.error(f"[查询房源] 查询房源失败: {str(e)}")
            return []

    @classmethod
    def _calculate_house_scores(cls, houses: List[House], user_preferences: Dict, user_behaviors: List[Dict]) -> Dict[
        str, float]:
        """
        计算房源的推荐得分

        Args:
            houses (List[House]): 房源列表
            user_preferences (Dict): 用户偏好向量
            user_behaviors (List[Dict]): 用户行为记录

        Returns:
            Dict[str, float]: 房源ID -> 得分映射
        """
        house_scores = {}

        for house in houses:
            total_score = 0

            # 计算镇相似度得分
            if house.town and house.town in user_preferences['town']:
                town_score = user_preferences['town'][house.town] * cls.WEIGHTS['town']
                total_score += town_score

            # 计算户型相似度得分
            if house.house_type and house.house_type in user_preferences['house_type']:
                house_type_score = user_preferences['house_type'][house.house_type] * cls.WEIGHTS['house_type']
                total_score += house_type_score

            # 计算朝向相似度得分
            if house.orientation and house.orientation in user_preferences['orientation']:
                orientation_score = user_preferences['orientation'][house.orientation] * cls.WEIGHTS['orientation']
                total_score += orientation_score

            # 计算标签相似度得分 - 考虑标签组合奖励
            if house.tags:
                house_tags = set(tag.strip() for tag in house.tags.split(';') if tag.strip())
                matched_tags = []
                tag_score = 0

                # 计算匹配的标签权重总和
                for tag in house_tags:
                    if tag in user_preferences['tags']:
                        tag_score += user_preferences['tags'][tag]
                        matched_tags.append(tag)

                # 如果匹配的标签数量超过1个，给予组合奖励
                if len(matched_tags) > 1:
                    # 组合奖励：每个额外匹配的标签给予固定奖励分
                    combination_bonus = (len(matched_tags) - 1) * cls.TAG_COMBINATION_BONUS
                    tag_score += combination_bonus

                total_score += tag_score * cls.WEIGHTS['tags']

            # 即使得分很低也保留，至少给每个房源一个基础得分用于多样性
            house_scores[house.house_id] = max(total_score, 0.1)

        return house_scores

    @classmethod
    def auto_update_recommendations(cls, user_id: int) -> None:
        """
        自动更新用户推荐（在用户浏览房源时调用）

        Args:
            user_id (int): 用户ID
        """
        try:
            # 直接生成推荐，不需要判断是否应该更新
            recommendations = cls.generate_recommendations(user_id, top_n=cls.MAX_RECOMMENDATIONS)

            if recommendations:
                # 构建模型信息
                model_info = cls._build_model_info(user_id, recommendations)

                # 保存推荐结果
                cls.save_user_recommendations(user_id, recommendations, model_info)

                LogUtil.logger.info(f"自动更新用户{user_id}推荐成功，共{len(recommendations)}条")

        except Exception as e:
            LogUtil.logger.error(f"自动更新用户{user_id}推荐失败: {str(e)}")
            # 不抛出异常，避免影响正常业务流程

    @classmethod
    def _sort_houses_by_score(cls, house_scores: Dict[str, float], top_n: int) -> List[str]:
        """
        按得分排序房源

        Args:
            house_scores (Dict[str, float]): 房源得分
            top_n (int): 返回数量

        Returns:
            List[str]: 排序后的房源ID列表
        """
        # 按得分降序排序
        sorted_houses = sorted(house_scores.items(), key=lambda x: x[1], reverse=True)

        # 返回Top N，如果不够则返回所有有得分的房源
        result = [house_id for house_id, score in sorted_houses if score > 0]
        return result[:top_n]

    @classmethod
    def select_recommend_list(cls, recommend: Recommend) -> List[Recommend]:
        """
        查询用户推荐列表

        Args:
            recommend (recommend): 用户推荐对象

        Returns:
            List[recommend]: 用户推荐列表
        """
        return RecommendMapper.select_recommend_list(recommend)

    @classmethod
    def select_recommend_by_id(cls, id: int) -> Optional[Recommend]:
        """
        根据ID查询用户推荐

        Args:
            id (int): 推荐编号

        Returns:
            recommend: 用户推荐对象
        """
        return RecommendMapper.select_recommend_by_id(id)

    @classmethod
    def insert_recommend(cls, recommend: Recommend) -> int:
        """
        新增用户推荐

        Args:
            recommend (recommend): 用户推荐对象

        Returns:
            int: 插入的记录数
        """
        return RecommendMapper.insert_recommend(recommend)

    @classmethod
    def update_recommend(cls, recommend: Recommend) -> int:
        """
        修改用户推荐

        Args:
            recommend (recommend): 用户推荐对象

        Returns:
            int: 更新的记录数
        """
        return RecommendMapper.update_recommend(recommend)

    @classmethod
    def delete_recommend_by_ids(cls, ids: List[int]) -> int:
        """
        批量删除用户推荐

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        return RecommendMapper.delete_recommend_by_ids(ids)

    @classmethod
    def import_recommend(cls, recommend_list: List[Recommend], is_update: bool = False) -> str:
        """
        导入用户推荐数据

        Args:
            recommend_list (List[recommend]): 用户推荐列表
            is_update (bool): 是否更新已存在的数据

        Returns:
            str: 导入结果消息
        """
        if not recommend_list:
            raise ServiceException("导入用户推荐数据不能为空")

        success_count = 0
        fail_count = 0
        success_msg = ""
        fail_msg = ""

        for recommend in recommend_list:
            try:
                display_value = recommend

                display_value = getattr(recommend, "id", display_value)
                existing = None
                if recommend.id is not None:
                    existing = RecommendMapper.select_recommend_by_id(recommend.id)
                if existing:
                    if is_update:
                        result = RecommendMapper.update_recommend(recommend)
                    else:
                        fail_count += 1
                        fail_msg += f"<br/> 第{fail_count}条数据，已存在：{display_value}"
                        continue
                else:
                    result = RecommendMapper.insert_recommend(recommend)

                if result > 0:
                    success_count += 1
                    success_msg += f"<br/> 第{success_count}条数据，操作成功：{display_value}"
                else:
                    fail_count += 1
                    fail_msg += f"<br/> 第{fail_count}条数据，操作失败：{display_value}"
            except Exception as e:
                fail_count += 1
                fail_msg += f"<br/> 第{fail_count}条数据，导入失败，原因：{e.__class__.__name__}"
                LogUtil.logger.error(f"导入用户推荐失败，原因：{e}")

        if fail_count > 0:
            if success_msg:
                fail_msg = f"导入成功{success_count}条，失败{fail_count}条。{success_msg}<br/>" + fail_msg
            else:
                fail_msg = f"导入成功{success_count}条，失败{fail_count}条。{fail_msg}"
            raise ServiceException(fail_msg)
        success_msg = f"恭喜您，数据已全部导入成功！共 {success_count} 条，数据如下：" + success_msg
        return success_msg
