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
@PreAuthorize(HasPerm('house:like:list'))
@JsonSerializer()
def orientation_statistics(dto: HouseStatisticsRequest):
    statistics_entity = HouseStatisticsRequest()
    # 转换dto到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(statistics_entity, attr):
            setattr(statistics_entity, attr, getattr(dto, attr))
    return AjaxResponse.from_success(data=service.orientation_statistics(statistics_entity))
