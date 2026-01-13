<template>
  <div class="app-container">
    <div class="content-wrapper">
      <!-- 标题和信息左右布局 -->
      <div class="header-section">
        <!-- 标题在左 -->
        <h1 class="page-title">推荐模型详情</h1>

        <!-- 重新设计信息卡片，使用标签和数值分离的方式，更清晰美观 -->
        <div class="info-section">
          <div class="info-card">
            <div class="info-items">
              <div class="info-item">
                <span class="label">镇</span>
                <span class="value">{{ weights.town }}</span>
              </div>
              <div class="info-item">
                <span class="label">房型</span>
                <span class="value">{{ weights.houseType }}</span>
              </div>
              <div class="info-item">
                <span class="label">朝向</span>
                <span class="value">{{ weights.orientation }}</span>
              </div>
              <div class="info-item">
                <span class="label">标签</span>
                <span class="value">{{ weights.tags }}</span>
              </div>
              <div class="info-item">
                <span class="label">推荐数</span>
                <span class="value">{{ modelInfo.total }}</span>
              </div>
              <div class="info-item">
                <span class="label">时间衰减</span>
                <span class="value">{{ modelInfo.timeDecayFactor }}</span>
              </div>
              <div class="info-item">
                <span class="label">推荐算法</span>
                <span class="value">多维协作过滤</span>
              </div>

              <div class="info-item">
                <span class="label">创建时间</span>
                <span class="value">{{ modelInfo.createTime }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 图表区域 -->
      <el-row :gutter="30">
        <el-col :span="14">
          <div class="chart-wrapper">
            <PieGhostingCharts
              :chart-title="orientationModelName"
              :chart-data="orientationModelData"/>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>

import {getRecommend} from "@/api/house/recommend";
import PieGhostingCharts from "@/components/Echarts/PieGhostingCharts.vue";


export default {
  name: "RecommendModel",
  components: {PieGhostingCharts},
  data() {
    return {
      recommend: {},
      recommendId: null,

      modelInfo: {},
      weights: {},
      //房屋朝向
      orientationModelData: [],
      orientationModelName: '房屋朝向'
    };
  },
  created() {
    this.recommendId = this.$route.query && this.$route.query.recommendId;
    this.getRecommend();
  },
  watch: {
    // 监听路由
    $route(to, from) {
      this.recommendId = to.query.recommendId;
      if (this.recommendId) {
        console.log(this.recommendId);
        this.getRecommend();
      }
    }
  },
  methods: {
    getRecommend() {
      getRecommend(this.recommendId).then((response) => {
        this.recommend = response.data;
        let modelInfo = {}
        if (this.recommend.modelInfo) {
          modelInfo = JSON.parse(this.recommend.modelInfo)
          this.modelInfo = modelInfo.modelInfo
          this.weights = modelInfo.weights
        }
        let model = {}
        if (modelInfo.modelInfo) {
          model = modelInfo.modelInfo
        }
        if (model.orientationModel) {
          this.orientationModelData = model.orientationModel
        }
      });
    },
  }
};
</script>

<style lang="scss" scoped>
.app-container {
  background-image: url("../../../assets/images/model-bg.png");
  background-repeat: no-repeat;
  background-size: 100%;
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

.header-section {
  display: flex;
  align-items: flex-start;
  gap: 24px;
  margin-bottom: 24px;
}

/* 标题居中，简洁大方 */
.page-title {
  flex: 3;
  font-size: 42px;
  font-weight: 700;
  color: #ffffff;
  padding-top: 10px;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  margin: 0;
  text-align: center;
}

.info-section {
  flex: 4;
  display: flex;
  gap: 24px;
}

/* 重新设计卡片样式，使用清晰的标签和数值分离布局 */
.info-card {
  flex: 1;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  padding: 0;
  overflow: hidden;
}

.card-header {
  font-size: 18px;
  font-weight: 600;
  color: #ffffff;
  padding: 16px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.info-items {
  display: flex;
  padding: 20px 24px;
  gap: 32px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: center;
}

.label {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.6);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.value {
  font-size: 20px;
  color: #ffffff;
  font-weight: 600;
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
