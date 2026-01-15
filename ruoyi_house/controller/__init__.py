# -*- coding: utf-8 -*-
# @Module: ruoyi_house/controller

from flask import Blueprint

view = Blueprint('view', __name__, url_prefix='/house/view')
house = Blueprint('house', __name__, url_prefix='/house/house')
recommend = Blueprint('recommend', __name__, url_prefix='/house/recommend')
like = Blueprint('like', __name__, url_prefix='/house/like')
house_statistics = Blueprint('house_statistics', __name__, url_prefix='/house/statistics')


from . import view_controller
from . import house_controller
from . import recommend_controller
from . import like_controller
from . import house_statistics_controller
