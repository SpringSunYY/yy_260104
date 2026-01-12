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
from ruoyi_common.utils.base import ExcelUtil, LogUtil
from ruoyi_common.utils.security_util import get_user_id
from ruoyi_framework.descriptor.log import Log
from ruoyi_framework.descriptor.permission import HasPerm, PreAuthorize
from ruoyi_house.controller import recommend as recommend_bp
from ruoyi_house.domain.entity import Recommend
from ruoyi_house.service.recommend_service import RecommendService

# 使用 controller/__init__.py 中定义的蓝图
gen = recommend_bp

recommend_service = RecommendService()


def _clear_page_context():
    if hasattr(g, "criterian_meta"):
        g.criterian_meta.page = None

@gen.route('/list', methods=["GET"])
@QueryValidator(is_page=True)
@PreAuthorize(HasPerm('house:recommend:list'))
@JsonSerializer()
def recommend_list(dto: Recommend):
    """查询用户推荐列表"""
    recommend_entity = Recommend()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(recommend_entity, attr):
            setattr(recommend_entity, attr, getattr(dto, attr))
    recommends = recommend_service.select_recommend_list(recommend_entity)
    return TableResponse(code=HttpStatus.SUCCESS, msg='查询成功', rows=recommends)


@gen.route('/<int:id>', methods=['GET'])
@PathValidator()
@PreAuthorize(HasPerm('house:recommend:query'))
@JsonSerializer()
def get_recommend(id: int):
    """获取用户推荐详细信息"""
    recommend_entity = recommend_service.select_recommend_by_id(id)
    return AjaxResponse.from_success(data=recommend_entity)


@gen.route('', methods=['POST'])
@BodyValidator()
@PreAuthorize(HasPerm('house:recommend:add'))
@Log(title='用户推荐管理', business_type=BusinessType.INSERT)
@JsonSerializer()
def add_recommend(dto: Recommend):
    """新增用户推荐"""
    recommend_entity = Recommend()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(recommend_entity, attr):
            setattr(recommend_entity, attr, getattr(dto, attr))
    result = recommend_service.insert_recommend(recommend_entity)
    if result > 0:
        return AjaxResponse.from_success(msg='新增成功')
    return AjaxResponse.from_error(msg='新增失败')


@gen.route('', methods=['PUT'])
@BodyValidator()
@PreAuthorize(HasPerm('house:recommend:edit'))
@Log(title='用户推荐管理', business_type=BusinessType.UPDATE)
@JsonSerializer()
def update_recommend(dto: Recommend):
    """修改用户推荐"""
    recommend_entity = Recommend()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(recommend_entity, attr):
            setattr(recommend_entity, attr, getattr(dto, attr))
    result = recommend_service.update_recommend(recommend_entity)
    if result > 0:
        return AjaxResponse.from_success(msg='修改成功')
    return AjaxResponse.from_error(msg='修改失败')



@gen.route('/<ids>', methods=['DELETE'])
@PathValidator()
@PreAuthorize(HasPerm('house:recommend:remove'))
@Log(title='用户推荐管理', business_type=BusinessType.DELETE)
@JsonSerializer()
def delete_recommend(ids: str):
    """删除用户推荐"""
    try:
        id_list = [int(id) for id in ids.split(',')]
        result = recommend_service.delete_recommend_by_ids(id_list)
        if result > 0:
            return AjaxResponse.from_success(msg='删除成功')
        return AjaxResponse.from_error(code=HttpStatus.ERROR, msg='删除失败')
    except Exception as e:
        return AjaxResponse.from_error(msg=f'删除失败: {str(e)}')


@gen.route('/export', methods=['POST'])
@FileDownloadValidator()
@PreAuthorize(HasPerm('house:recommend:export'))
@Log(title='用户推荐管理', business_type=BusinessType.EXPORT)
@BaseSerializer()
def export_recommend(dto: Recommend):
    """导出用户推荐列表"""
    recommend_entity = Recommend()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(recommend_entity, attr):
            setattr(recommend_entity, attr, getattr(dto, attr))
    _clear_page_context()
    recommend_entity.page_num = None
    recommend_entity.page_size = None
    recommends = recommend_service.select_recommend_list(recommend_entity)
    # 使用ExcelUtil导出Excel文件
    excel_util = ExcelUtil(Recommend)
    return excel_util.export_response(recommends, "用户推荐数据")

@gen.route('/importTemplate', methods=['POST'])
@login_required
@BaseSerializer()
def import_template():
    """下载用户推荐导入模板"""
    excel_util = ExcelUtil(Recommend)
    return excel_util.import_template_response(sheetname="用户推荐数据")

@gen.route('/importData', methods=['POST'])
@FileUploadValidator()
@PreAuthorize(HasPerm('house:recommend:import'))
@Log(title='用户推荐管理', business_type=BusinessType.IMPORT)
@JsonSerializer()
def import_data(
    file: List[FileStorage],
    update_support: Annotated[bool, BeforeValidator(lambda x: x != "0")]
):
    """导入用户推荐数据"""
    file = file[0]
    excel_util = ExcelUtil(Recommend)
    recommend_list = excel_util.import_file(file, sheetname="用户推荐数据")
    msg = recommend_service.import_recommend(recommend_list, update_support)
    return AjaxResponse.from_success(msg=msg)


@gen.route('/my-recommendations', methods=['GET'])
@QueryValidator(is_page=True)
@PreAuthorize(HasPerm('house:recommend:list'))
@JsonSerializer()
def get_my_recommendations():
    """获取我的推荐房源列表"""
    try:
        user_id = get_user_id()
        # 直接从请求参数获取分页信息，避免别名转换问题
        from flask import request
        page_num = int(request.args.get('pageNum', 1))
        page_size = int(request.args.get('pageSize', 10))

        LogUtil.logger.info(f"[推荐接口] 用户ID: {user_id}, 请求参数: pageNum={page_num}, pageSize={page_size}")

        if not user_id:
            LogUtil.logger.warning("[推荐接口] 用户未登录")
            return AjaxResponse.from_error(msg='用户未登录')

        # 调用Service层处理所有业务逻辑（包括自动生成推荐）
        houses, total = recommend_service.get_user_recommendations_with_auto_generate(user_id, page_num, page_size)

        if total == 0:
            return TableResponse(code=HttpStatus.SUCCESS, msg='暂无推荐记录', rows=[], total=0)

        LogUtil.logger.info(f"[推荐接口] 用户{user_id}响应数据: 总推荐数={total}, 当前页返回={len(houses)}")

        # 设置分页信息，让TableResponse的computed_field正确返回total
        from ruoyi_common.base.model import PageModel
        page_model = PageModel(page_num=page_num, page_size=page_size, total=total)
        g.criterian_meta.page = page_model

        return TableResponse(
            code=HttpStatus.SUCCESS,
            msg='查询成功',
            rows=houses
        )

    except Exception as e:
        LogUtil.logger.error(f"[推荐接口] 获取用户{user_id}推荐失败: {str(e)}", exc_info=True)
        return AjaxResponse.from_error(msg=f'获取推荐失败: {str(e)}')
