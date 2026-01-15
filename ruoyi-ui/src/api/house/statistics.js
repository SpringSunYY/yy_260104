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
