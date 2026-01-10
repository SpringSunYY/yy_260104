from typing import List

from flask import g
from flask_login import login_required
from pydantic import BeforeValidator
from typing_extensions import Annotated
from werkzeug.datastructures import FileStorage

from ruoyi_common.base.model import AjaxResponse, TableResponse
from ruoyi_common.constant import HttpStatus
from ruoyi_common.descriptor.serializer import BaseSerializer, JsonSerializer
from ruoyi_common.descriptor.validator import QueryValidator, BodyValidator, PathValidator, FileDownloadValidator, \
    FileUploadValidator
from ruoyi_common.domain.enum import BusinessType
from ruoyi_common.utils.base import ExcelUtil
from ruoyi_framework.descriptor.log import Log
from ruoyi_framework.descriptor.permission import HasPerm, PreAuthorize
from ruoyi_house.controller import house as house_bp
from ruoyi_house.domain.entity import House
from ruoyi_house.service.house_service import HouseService

# 使用 controller/__init__.py 中定义的蓝图
gen = house_bp

house_service = HouseService()


def _clear_page_context():
    if hasattr(g, "criterian_meta"):
        g.criterian_meta.page = None


@gen.route('/list', methods=["GET"])
@QueryValidator(is_page=True)
@PreAuthorize(HasPerm('house:house:list'))
@JsonSerializer()
def house_list(dto: House):
    """查询房源信息列表"""
    house_entity = House()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(house_entity, attr):
            setattr(house_entity, attr, getattr(dto, attr))
    houses = house_service.select_house_list(house_entity)
    return TableResponse(code=HttpStatus.SUCCESS, msg='查询成功', rows=houses)


@gen.route('/<string:hoseId>', methods=['GET'])
@PathValidator()
@PreAuthorize(HasPerm('house:house:query'))
@JsonSerializer()
def get_house(hose_id: str):
    """获取房源信息详细信息"""
    house_entity = house_service.select_house_by_id(hose_id)
    return AjaxResponse.from_success(data=house_entity)


@gen.route('', methods=['POST'])
@BodyValidator()
@PreAuthorize(HasPerm('house:house:add'))
@Log(title='房源信息管理', business_type=BusinessType.INSERT)
@JsonSerializer()
def add_house(dto: House):
    """新增房源信息"""
    house_entity = House()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(house_entity, attr):
            setattr(house_entity, attr, getattr(dto, attr))
    result = house_service.insert_house(house_entity)
    if result > 0:
        return AjaxResponse.from_success(msg='新增成功')
    return AjaxResponse.from_error(msg='新增失败')


@gen.route('', methods=['PUT'])
@BodyValidator()
@PreAuthorize(HasPerm('house:house:edit'))
@Log(title='房源信息管理', business_type=BusinessType.UPDATE)
@JsonSerializer()
def update_house(dto: House):
    """修改房源信息"""
    house_entity = House()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(house_entity, attr):
            setattr(house_entity, attr, getattr(dto, attr))
    result = house_service.update_house(house_entity)
    if result > 0:
        return AjaxResponse.from_success(msg='修改成功')
    return AjaxResponse.from_error(msg='修改失败')


@gen.route('/<ids>', methods=['DELETE'])
@PathValidator()
@PreAuthorize(HasPerm('house:house:remove'))
@Log(title='房源信息管理', business_type=BusinessType.DELETE)
@JsonSerializer()
def delete_house(ids: str):
    """删除房源信息"""
    try:
        id_list = [int(id) for id in ids.split(',')]
        result = house_service.delete_house_by_ids(id_list)
        if result > 0:
            return AjaxResponse.from_success(msg='删除成功')
        return AjaxResponse.from_error(code=HttpStatus.ERROR, msg='删除失败')
    except Exception as e:
        return AjaxResponse.from_error(msg=f'删除失败: {str(e)}')


@gen.route('/export', methods=['POST'])
@FileDownloadValidator()
@PreAuthorize(HasPerm('house:house:export'))
@Log(title='房源信息管理', business_type=BusinessType.EXPORT)
@BaseSerializer()
def export_house(dto: House):
    """导出房源信息列表"""
    house_entity = House()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(house_entity, attr):
            setattr(house_entity, attr, getattr(dto, attr))
    _clear_page_context()
    house_entity.page_num = None
    house_entity.page_size = None
    houses = house_service.select_house_list(house_entity)
    # 使用ExcelUtil导出Excel文件
    excel_util = ExcelUtil(House)
    return excel_util.export_response(houses, "房源信息数据")


@gen.route('/importTemplate', methods=['POST'])
@login_required
@BaseSerializer()
def import_template():
    """下载房源信息导入模板"""
    excel_util = ExcelUtil(House)
    return excel_util.import_template_response(sheetname="房源信息数据")


@gen.route('/importData', methods=['POST'])
@FileUploadValidator()
@PreAuthorize(HasPerm('house:house:import'))
@Log(title='房源信息管理', business_type=BusinessType.IMPORT)
@JsonSerializer()
def import_data(
        file: List[FileStorage]
):
    """导入房源信息数据"""
    file = file[0]
    excel_util = ExcelUtil(House)
    house_list = excel_util.import_file(file, sheetname="房源信息数据")
    msg = house_service.import_house(house_list)
    return AjaxResponse.from_success(msg=msg)
