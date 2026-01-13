<template>
  <div v-if="!isStatistics" class="no-statistics">
    您没有权限查看数据分析
  </div>
</template>
<script>
import {checkPermi} from "@/utils/permission";

export default {
  name: "HouseStatistics",
  data() {
    return {
      isStatistics: false
    }
  },
  created() {
    this.isStatistics = checkPermi(['house:house:statistics'])
    //跳转大屏页面
    if (this.isStatistics) {
      // 获取路由地址
      const routeData = this.$router.resolve({name: 'Statistics'});
      // 在新窗口中打开
      window.open(routeData.href, '_blank');
    }
  }
}
</script>


<style scoped lang="scss">
.no-statistics {
  text-align: center;
  font-size: 36px;
}
</style>
