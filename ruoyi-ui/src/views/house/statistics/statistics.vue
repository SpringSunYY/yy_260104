<template>
  <div class="app-container">
    <div class="content-wrapper">
      <!-- 图表区域 -->
      <el-row :gutter="10">
        <el-col :span="10">
          <div class="chart-wrapper">
            <PieRoseLineCharts/>
          </div>
        </el-col>
        <el-col :span="14">
          <div class="chart-wrapper">

          </div>
        </el-col>
        <el-col :span="14">
          <div class="chart-wrapper">

          </div>
        </el-col>
        <el-col :span="10">
          <div class="chart-wrapper">

          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>


import PieRoseLineCharts from "@/components/Echarts/PieRoseLineCharts.vue";

export default {
  name: "RecommendModel",
  components: {PieRoseLineCharts},
  data() {
    return {};
  },


  methods: {}
};
</script>

<style lang="scss" scoped>
.app-container {
  background-image: url("../../../assets/images/model-bg.png");
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  min-height: 92vh;
  margin-top: -10px;
  padding: 32px;
}

.content-wrapper {
  display: flex;
  flex-direction: column;
  gap: 24px;
  height: 100%;
}


.chart-wrapper {
  height: 38vh;
}

@media (max-width: 768px) {
  .app-container {
    padding: 20px;
  }

  .header-section {
    flex-direction: column;
    gap: 16px;
  }

  .page-title {
    text-align: center;
    margin-bottom: 16px;
  }

  .info-section {
    flex-direction: column;
  }

}
</style>
