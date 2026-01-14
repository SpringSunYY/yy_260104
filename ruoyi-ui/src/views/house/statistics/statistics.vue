<template>
  <div class="app-container">
    <div class="content-wrapper">
      <!-- 图表区域 -->
      <el-row :gutter="0">
        <el-col :span="6">
          <div class="chart-wrapper">
            <PieRoseLineCharts
              :chart-title="tagStatisticsName"
            />
          </div>
          <div class="chart-wrapper">
            <ScatterGradientCharts
              :chart-title="decorationStatisticsName"
            />
          </div>
          <div class="chart-wrapper">
            <ScatterGradientZoomCharts
              :chart-title="communityStatisticsName"
            />
          </div>
        </el-col>
        <el-col :span="12">
          <div class="chart-map-wrapper">
            <DongGuanMapCharts
              :chart-name="townStatisticsName"
              @mapClick="mapClick"/>
          </div>
          <div class="chart-trend-wrapper">
            <BarTrendCharts
              :chart-title="pricePredictionName"
            />
          </div>
        </el-col>
        <el-col :span="6">
          <div class="chart-wrapper">
            <PieRoseHollowCharts
              :chart-title="priceStatisticsName"/>
          </div>
          <div class="chart-wrapper">
            <ScatterRippleCharts
              :chart-title="houseTypeStatisticsName"
            />
          </div>
          <div class="chart-wrapper">
            <PieRoundCharts
              :chart-title="decorationStatisticsName"/>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>


import PieRoseLineCharts from "@/components/Echarts/PieRoseLineCharts.vue";
import PieRoseHollowCharts from "@/components/Echarts/PieRoseHollowCharts.vue";
import ScatterGradientZoomCharts from "@/components/Echarts/ScatterGradientZoomCharts.vue";
import DongGuanMapCharts from "@/components/Echarts/DongGuan/DongGuanMapCharts.vue";
import BarTrendCharts from "@/components/Echarts/BarTrendCharts.vue";
import PieGhostingCharts from "@/components/Echarts/PieGhostingCharts.vue";
import PieRoundCharts from "@/components/Echarts/PieRoundCharts.vue";
import ScatterGradientCharts from "@/components/Echarts/ScatterGradientCharts.vue";
import ScatterRippleCharts from "@/components/Echarts/ScatterRippleCharts.vue";

export default {
  name: "RecommendModel",
  components: {
    ScatterRippleCharts,
    ScatterGradientCharts,
    PieRoundCharts,
    PieGhostingCharts,
    BarTrendCharts, DongGuanMapCharts, ScatterGradientZoomCharts, PieRoseHollowCharts, PieRoseLineCharts
  },
  data() {
    return {
      //标签
      tagStatisticsData: [],
      tagStatisticsName: '标签分析',
      //装饰类型
      decorationStatisticsData: [],
      decorationStatisticsName: '装修分析',
      //价格
      priceStatisticsData: [],
      priceStatisticsName: '价格分析',

      //镇
      townStatisticsData: [],
      townStatisticsName: '东莞市二手房数据分析',
      //价格预测
      pricePredictionData: [],
      pricePredictionName: '价格预测',
      //户型
      houseTypeStatisticsData: [],
      houseTypeStatisticsName: '户型分析',
      //朝向
      directionStatisticsData: [],
      directionStatisticsName: '朝向分析',
      //小区
      communityStatisticsData: [],
      communityStatisticsName: '小区分析',
    };
  },


  methods: {
    mapClick(locationName) {
      console.log(locationName);
    }
  }
};
</script>

<style lang="scss" scoped>
.app-container {
  background-image: url("../../../assets/images/statistics-bg.png");
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  max-height: 100vh;
  overflow-y: auto;
}



.chart-wrapper {
  height: 33vh;
}

.chart-map-wrapper {
  height: 55vh;
}

.chart-trend-wrapper {
  height: 35vh;
}

</style>
