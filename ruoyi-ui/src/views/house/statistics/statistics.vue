<template>
  <div class="app-container">
    <div class="content-wrapper">
      <!-- 图表区域 -->
      <el-row :gutter="0">
        <el-col :span="6">
          <div class="chart-wrapper">
            <PieRoseLineCharts
              :chart-title="orientationStatisticsName"
              :chart-data="orientationStatisticsData"
            />
          </div>
          <div class="chart-wrapper">
            <ScatterGradientCharts
              :chart-title="tagStatisticsName"
              :chart-data="tagStatisticsData"
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
              :chart-data="townStatisticsData"
              :default-index-name="defaultIndexName"
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
              :chart-title="priceStatisticsName"
              :chart-data="priceStatisticsData"/>
          </div>
          <div class="chart-wrapper">
            <ScatterRippleCharts
              :chart-title="floorTypeStatisticsName"
              :chart-data="floorTypeStatisticsData"
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
import {
  getFloorTypeStatistics,
  getHouseTypeStatistics,
  getOrientationStatistics,
  getPriceStatistics,
  getTagsStatistics,
  getTownStatistics
} from "@/api/house/statistics";

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
      defaultIndexName: '总房源数',
      //价格预测
      pricePredictionData: [],
      pricePredictionName: '价格预测',
      //户型
      houseTypeStatisticsData: [],
      houseTypeStatisticsName: '户型分析',
      //楼层
      floorTypeStatisticsData: [],
      floorTypeStatisticsName: '楼层分析',
      //朝向
      orientationStatisticsData: [],
      orientationStatisticsName: '朝向分析',
      //小区
      communityStatisticsData: [],
      communityStatisticsName: '小区分析',

      statisticsParams: {}
    };
  },

  created() {
    this.getTownStatisticsData()
    this.getStatisticsData();
  },
  methods: {
    mapClick(locationName) {
      console.log(locationName);
      this.statisticsParams.town = locationName
      this.getStatisticsData()
    },
    //获取统计
    getStatisticsData() {
      this.getOrientationStatisticsData()
      this.getPriceStatisticsData()
      this.getTagsStatisticsData()
      this.getHouseTypeStatisticsData()
      this.getFloorTypeStatisticsData()
    },
    //获取朝向
    getOrientationStatisticsData() {
      getOrientationStatistics(this.statisticsParams).then(res => {
        this.orientationStatisticsData = res.data;
      });
    },
    //价格
    getPriceStatisticsData() {
      getPriceStatistics(this.statisticsParams).then(res => {
        this.priceStatisticsData = res.data;
      });
    },
    //标签
    getTagsStatisticsData() {
      getTagsStatistics(this.statisticsParams).then(res => {
        this.tagStatisticsData = res.data;
      });
    },
    //户型
    getHouseTypeStatisticsData() {
      getHouseTypeStatistics(this.statisticsParams).then(res => {
        this.houseTypeStatisticsData = res.data;
      });
    },
    //楼层
    getFloorTypeStatisticsData() {
      getFloorTypeStatistics(this.statisticsParams).then(res => {
        this.floorTypeStatisticsData = res.data;
      });
    },
    //获取镇
    getTownStatisticsData() {
      getTownStatistics(this.statisticsParams).then(res => {
        const data = res.data;
        let valueValues = []
        let avgValues = []
        let maxValues = []
        let minValues = []
        for (let i = 0; i < data.length; i++) {
          let name = data[i].name
          valueValues.push({location: name, value: data[i].value})
          avgValues.push({location: name, value: data[i].avg.toFixed(2)})
          maxValues.push({location: name, value: data[i].max})
          minValues.push({location: name, value: data[i].min})
        }
        this.townStatisticsData = []
        this.townStatisticsData.push({
          name: "总房源数",
          value: valueValues
        })
        this.townStatisticsData.push({
          name: "平均价格",
          value: avgValues
        })
        this.townStatisticsData.push({
          name: "最高价格",
          value: maxValues
        })
        this.townStatisticsData.push({
          name: "最低价格",
          value: minValues
        })
        console.log(this.townStatisticsData)
      });
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
