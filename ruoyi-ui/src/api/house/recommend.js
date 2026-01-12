import request from '@/utils/request'





// 查询用户推荐列表
export function listRecommend(query) {
  return request({
    url: '/house/recommend/list',
    method: 'get',
    params: query
  })
}

// 查询用户推荐详细
export function getRecommend(id) {
  return request({
    url: '/house/recommend/' +id,
    method: 'get'
  })
}

// 新增用户推荐
export function addRecommend(data) {
  return request({
    url: '/house/recommend',
    method: 'post',
    data: data
  })
}

// 修改用户推荐
export function updateRecommend(data) {
  return request({
    // 后端 Flask 控制器使用的是不带主键的 PUT '' 路径，这里保持一致
    url: '/house/recommend',
    method: 'put',
    data: data
  })
}

// 删除用户推荐
export function delRecommend(id) {
  return request({
    url: '/house/recommend/' +id,
    method: 'delete'
  })
}

// 查询我的推荐房源列表
export function listMyRecommendations(query) {
  return request({
    url: '/house/recommend/my-recommendations',
    method: 'get',
    params: query
  })
}