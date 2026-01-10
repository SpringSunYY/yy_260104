# -*- coding: utf-8 -*-
# @Module: house
# @Author: YY

def init_app(app):
    """
    初始化模块，注册蓝图
    
    Args:
        app: Flask应用实例
    """
    # 导入 controller 模块，自动注册所有蓝图
    # 使用 pythonModelName 生成 Python 导入路径
    from ruoyi_house.controller import view
    app.register_blueprint(view)
    # 使用 pythonModelName 生成 Python 导入路径
    from ruoyi_house.controller import house
    app.register_blueprint(house)
    # 使用 pythonModelName 生成 Python 导入路径
    from ruoyi_house.controller import recommend
    app.register_blueprint(recommend)
    # 使用 pythonModelName 生成 Python 导入路径
    from ruoyi_house.controller import like
    app.register_blueprint(like)