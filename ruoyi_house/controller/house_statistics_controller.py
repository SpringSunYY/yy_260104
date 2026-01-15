from ruoyi_common.base.model import AjaxResponse
from ruoyi_common.descriptor.serializer import JsonSerializer
from ruoyi_common.descriptor.validator import QueryValidator
from ruoyi_framework.descriptor.permission import HasPerm, PreAuthorize
from ruoyi_house.domain.statistics.dto import HouseStatisticsRequest
from ruoyi_house.controller import house_statistics as house_statistics_bp, house
from ruoyi_house.service.house_statistics_service import HouseStatisticsService

gen = house_statistics_bp
service = HouseStatisticsService()
"""房源信息数据分析统计"""

"""朝向分析"""
@gen.route('/orientation', methods=["GET"])
@QueryValidator(is_page=True)
@PreAuthorize(HasPerm('house:house:statistics'))
@JsonSerializer()
def orientation_statistics(dto: HouseStatisticsRequest):
    statistics_entity = HouseStatisticsRequest()
    # 转换dto到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(statistics_entity, attr):
            setattr(statistics_entity, attr, getattr(dto, attr))
    return AjaxResponse.from_success(data=service.orientation_statistics(statistics_entity))


"""镇分析"""
@gen.route('/town', methods=["GET"])
@QueryValidator(is_page=True)
@PreAuthorize(HasPerm('house:house:statistics'))
@JsonSerializer()
def town_statistics(dto: HouseStatisticsRequest):
    statistics_entity = HouseStatisticsRequest()
    # 转换dto到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(statistics_entity, attr):
            setattr(statistics_entity, attr, getattr(dto, attr))
    return AjaxResponse.from_success(data=service.town_statistics(statistics_entity))


"""房价分析"""
@gen.route('/price', methods=["GET"])
@QueryValidator(is_page=True)
@PreAuthorize(HasPerm('house:house:statistics'))
@JsonSerializer()
def price_statistics(dto: HouseStatisticsRequest):
    statistics_entity = HouseStatisticsRequest()
    # 转换dto到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(statistics_entity, attr):
            setattr(statistics_entity, attr, getattr(dto, attr))
    return AjaxResponse.from_success(data=service.price_statistics(statistics_entity))


"""标签分析"""
@gen.route('/tags', methods=["GET"])
@QueryValidator(is_page=True)
@PreAuthorize(HasPerm('house:house:statistics'))
@JsonSerializer()
def tags_statistics(dto: HouseStatisticsRequest):
    statistics_entity = HouseStatisticsRequest()
    # 转换dto到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(statistics_entity, attr):
            setattr(statistics_entity, attr, getattr(dto, attr))
    return AjaxResponse.from_success(data=service.tags_statistics(statistics_entity))


"""户型分析"""
@gen.route('/house_type', methods=["GET"])
@QueryValidator(is_page=True)
@PreAuthorize(HasPerm('house:house:statistics'))
@JsonSerializer()
def house_type_statistics(dto: HouseStatisticsRequest):
    statistics_entity = HouseStatisticsRequest()
    # 转换dto到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(statistics_entity, attr):
            setattr(statistics_entity, attr, getattr(dto, attr))
    return AjaxResponse.from_success(data=service.house_type_statistics(statistics_entity))


"""楼层"""
@gen.route('/floor_type', methods=["GET"])
@QueryValidator(is_page=True)
@PreAuthorize(HasPerm('house:house:statistics'))
@JsonSerializer()
def floor_type_statistics(dto: HouseStatisticsRequest):
    statistics_entity = HouseStatisticsRequest()
    # 转换dto到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(statistics_entity, attr):
            setattr(statistics_entity, attr, getattr(dto, attr))
    return AjaxResponse.from_success(data=service.floor_type_statistics(statistics_entity))


"""小区"""
@gen.route('/community', methods=["GET"])
@QueryValidator(is_page=True)
@PreAuthorize(HasPerm('house:house:statistics'))
@JsonSerializer()
def community_statistics(dto: HouseStatisticsRequest):
    statistics_entity = HouseStatisticsRequest()
    # 转换dto到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(statistics_entity, attr):
            setattr(statistics_entity, attr, getattr(dto, attr))
    return AjaxResponse.from_success(data=service.community_statistics(statistics_entity))
