import request from '@/utils/request'

//朝向分析
export function getOrientationStatistics(params) {
  return request({
    url: '/house/statistics/orientation',
    method: 'get',
    params: params
  })
}
