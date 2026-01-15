import request from '@/utils/request'

//朝向分析
export function getOrientationStatistics(params) {
  return request({
    url: '/house/statistics/orientation',
    method: 'get',
    params: params
  })
}

//镇
export function getTownStatistics(params) {
  return request({
    url: '/house/statistics/town',
    method: 'get',
    params: params
  })
}

//价格
export function getPriceStatistics(params) {
  return request({
    url: '/house/statistics/price',
    method: 'get',
    params: params
  })
}

//标签
export function getTagsStatistics(params) {
  return request({
    url: '/house/statistics/tags',
    method: 'get',
    params: params
  })
}

//户型
export function getHouseTypeStatistics(params) {
  return request({
    url: '/house/statistics/house_type',
    method: 'get',
    params: params
  })
}


//楼层
export function getFloorTypeStatistics(params) {
  return request({
    url: '/house/statistics/floor_type',
    method: 'get',
    params: params
  })
}

//小区
export function getCommunityStatistics(params) {
  return request({
    url: '/house/statistics/community',
    method: 'get',
    params: params
  })
}
