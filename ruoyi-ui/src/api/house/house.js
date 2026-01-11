import request from '@/utils/request'





// 查询房源信息列表
export function listHouse(query) {
  return request({
    url: '/house/house/list',
    method: 'get',
    params: query
  })
}

// 查询房源信息详细
export function getHouse(hoseId) {
  return request({
    url: '/house/house/' +hoseId,
    method: 'get'
  })
}

//查询房源详细信息
export function getHouseDetail(hoseId) {
  return request({
    url: '/house/house/detail/' +hoseId,
    method: 'get'
  })
}

// 新增房源信息
export function addHouse(data) {
  return request({
    url: '/house/house',
    method: 'post',
    data: data
  })
}

// 修改房源信息
export function updateHouse(data) {
  return request({
    // 后端 Flask 控制器使用的是不带主键的 PUT '' 路径，这里保持一致
    url: '/house/house',
    method: 'put',
    data: data
  })
}

// 删除房源信息
export function delHouse(hoseId) {
  return request({
    url: '/house/house/' +hoseId,
    method: 'delete'
  })
}
