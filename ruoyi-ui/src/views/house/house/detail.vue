<template>
  <div class="house-detail">
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-section">
      <el-skeleton animated>
        <template slot="template">
          <el-skeleton-item variant="image" style="width: 100%; height: 400px;"/>
          <el-row :gutter="20" style="margin-top: 20px;">
            <el-col :span="16">
              <el-skeleton-item variant="h1" style="width: 50%;"/>
              <el-skeleton-item variant="text" style="width: 100%; margin: 10px 0;"/>
              <el-skeleton-item variant="text" style="width: 80%;"/>
              <el-skeleton-item variant="text" style="width: 60%;"/>
            </el-col>
            <el-col :span="8">
              <el-skeleton-item variant="text" style="width: 100%;"/>
              <el-skeleton-item variant="text" style="width: 100%; margin: 10px 0;"/>
              <el-skeleton-item variant="text" style="width: 80%;"/>
            </el-col>
          </el-row>
        </template>
      </el-skeleton>
    </div>

    <!-- 房源详情 -->
    <div v-else-if="houseData" class="detail-content">
      <!-- 清除浮动 -->
      <div class="clearfix"></div>
      <div class="container">
        <!-- 房源图片区域 -->
        <div class="image-gallery-section">
          <div class="image-gallery">
            <div v-if="imageList.length > 0" class="main-image">
              <el-carousel :autoplay="false" height="700px" arrow="always">
                <el-carousel-item v-for="(image, index) in imageList" :key="index">
                  <img :src="image" alt="房源图片" class="carousel-image"/>
                </el-carousel-item>
              </el-carousel>
            </div>
            <div v-else class="no-image">
              <el-empty description="暂无图片" :image-size="120"></el-empty>
            </div>
          </div>
        </div>

        <!-- 房源信息区域 -->
        <div class="info-section">
          <!-- 标题和价格 -->
          <div class="header-info">
            <div class="title-section">
              <div class="title-row">
                <h1 class="house-title">{{ houseData.title }}</h1>
                <div class="action-buttons">
                  <el-button
                    type="primary"
                    size="small"
                    @click="viewExternalDetail"
                    icon="el-icon-view"
                  >
                    查看详情
                  </el-button>
                  <el-button
                    :type="isLiked ? 'warning' : 'default'"
                    size="small"
                    @click="toggleLike"
                    :icon="isLiked ? 'el-icon-star-on' : 'el-icon-star-off'"
                  >
                    {{ isLiked ? '已收藏' : '收藏' }}
                  </el-button>
                </div>
              </div>
              <div class="price-info">
                <div class="total-price">
                  <span class="price">{{ houseData.totalPrice }}万</span>
                  <span class="unit">总价</span>
                </div>
                <div class="unit-price">
                  <span class="price">{{ houseData.unitPrice }}元/㎡</span>
                  <span class="unit">单价</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 基本信息 -->
          <div class="basic-info">
            <div class="info-row">
              <div class="info-item">
                <i class="el-icon-house"></i>
                <span class="label">户型：</span>
                <span class="value">
                  <dict-tag :options="dict.type.house_type" :value="houseData.houseType"/>
                </span>
              </div>
              <div class="info-item">
                <i class="el-icon-s-home"></i>
                <span class="label">面积：</span>
                <span class="value">{{ houseData.areaSize }}㎡</span>
              </div>
              <div class="info-item">
                <i class="el-icon-location-outline"></i>
                <span class="label">朝向：</span>
                <span class="value">
                  <dict-tag :options="dict.type.house_orientation" :value="houseData.orientation"/>
                </span>
              </div>
              <div class="info-item">
                <i class="el-icon-office-building"></i>
                <span class="label">楼层：</span>
                <span class="value">{{ houseData.floorType }}</span>
              </div>
              <div class="info-item">
                <i class="el-icon-brush"></i>
                <span class="label">装修：</span>
                <span class="value">
                  <dict-tag :options="dict.type.house_decoration_type" :value="houseData.decorationType"/>
                </span>
              </div>
              <div class="info-item">
                <i class="el-icon-brush"></i>
                <span class="label">装修价格：</span>
                <span class="value">
                  <span class="value">{{ houseData.decorationArea }}元/㎡</span>
                </span>
              </div>
              <div class="info-item">
                <i class="el-icon-time"></i>
                <span class="label">年代：</span>
                <span class="value">{{ houseData.buildingYear }}年</span>
              </div>
            </div>
          </div>

          <!-- 地址信息 -->
          <div class="address-info">
            <h3 class="section-title">
              <i class="el-icon-map-location"></i>
              房源地址
            </h3>
            <div class="address-content">
              <div class="address-item">
                <span class="label">详细地址：</span>
                <span class="value">
                  {{ houseData.address }}  {{ houseData.community }}
                </span>
              </div>
            </div>
          </div>

          <!-- 房源标签 -->
          <div v-if="houseData.tags" class="tags-info">
            <h3 class="section-title">
              <i class="el-icon-price-tag"></i>
              房源标签
            </h3>
            <div class="tags-content">
              <el-tag
                v-for="tag in getTags(houseData.tags)"
                :key="tag"
                size="medium"
                type="warning"
                class="tag"
              >
                {{ tag }}
              </el-tag>
            </div>
          </div>

          <!-- 产权信息 -->
          <div class="property-info">
            <h3 class="section-title">
              <i class="el-icon-document-copy"></i>
              产权信息
            </h3>
            <div class="property-content">
              <div class="property-item">
                <span class="label">产权信息：</span>
                <span class="value">
                  <dict-tag :options="dict.type.house_property_right_type" :value="houseData.propertyRightType"/>
                  <dict-tag :options="dict.type.house_property_right_year" :value="houseData.propertyRightYear"/>
                  <dict-tag :options="dict.type.house_property_type" :value="houseData.propertyType"/>
                </span>
              </div>
            </div>
          </div>

          <!-- 房源介绍 -->
          <div v-if="houseData.houseIntro" class="intro-info">
            <h3 class="section-title">
              <i class="el-icon-document"></i>
              房源介绍
            </h3>
            <div class="intro-content">
              <div class="intro-text">
                {{ houseData.houseIntro }}
              </div>
            </div>
          </div>

          <!-- 房源编码 -->
          <div class="code-info">
            <div class="code-item">
              <span class="label">房源编号：</span>
              <span class="value">{{ houseData.hoseId }}</span>
              <span class="separator">|</span>
              <span class="label">房源编码：</span>
              <span class="value">{{ houseData.houseCode }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 错误状态 -->
    <div v-else class="error-section">
      <el-empty description="房源信息不存在或已删除">
        <el-button @click="goBack">返回列表</el-button>
      </el-empty>
    </div>
  </div>
</template>

<script>
import {getHouseDetail} from "@/api/house/house";
import {likeLike} from "@/api/house/like";

export default {
  name: "HouseDetail",
  dicts: [
    'house_city',
    'house_town',
    'house_type',
    'house_orientation',
    'house_floor_type',
    'house_decoration_type',
    'house_property_right_type',
    'house_property_right_year',
    'house_property_type'
  ],
  data() {
    return {
      loading: true,
      houseData: null,
      imageList: [],
      isLiked: false,
      hoseId: null,
    };
  },
  created() {
    this.hoseId = this.$route.params.hoseId;
    this.getHouseDetail();
  },
  methods: {
    /** 获取房源详情 */
    getHouseDetail() {
      if (!this.hoseId) {
        this.$message.error("房源ID不能为空");
        this.loading = false;
        return;
      }

      getHouseDetail(this.hoseId).then(response => {
        this.houseData = response.data;
        this.isLiked = response.data.isLiked;
        // 处理图片列表
        this.processImages();
        this.loading = false;
      }).catch(() => {
        this.loading = false;
        this.$message.error("获取房源详情失败");
      });
    },

    /** 处理图片列表 */
    processImages() {
      this.imageList = [];
      if (this.houseData.coverImage) {
        this.imageList.push(this.houseData.coverImage);
      }
      if (this.houseData.imageUrls) {
        const otherImages = this.houseData.imageUrls.split(';').filter(img => img.trim());
        this.imageList = [...this.imageList, ...otherImages];
      }
    },

    /** 处理标签 */
    getTags(tagsStr) {
      if (!tagsStr) return [];
      return tagsStr.split(';').filter(tag => tag.trim() !== '');
    },

    /** 查看外部详情 */
    viewExternalDetail() {
      const url = `https://dg.anjuke.com/prop/view/${this.houseData.hoseId}`;
      window.open(url, '_blank');
    },

    /** 切换点赞状态 */
    toggleLike() {
      this.isLiked = !this.isLiked;
      likeLike({houseId: this.hoseId}).then(res => {
        this.$message.success(this.isLiked ? '已收藏' : '已取消收藏');
      })
    },

    /** 返回列表 */
    goBack() {
      this.$router.go(-1);
    }
  }
};
</script>

<style scoped lang="scss">
.house-detail {
  background: #f8f9fa;
  min-height: 100vh;
}

.clearfix {
  clear: both;
}

.loading-section, .error-section {
  padding: 60px 0;
  text-align: center;

  .container {
    max-width: 100%;
    margin: 0 auto;
    padding: 0 24px;
  }
}

.detail-content {
  padding: 24px 0;

  .container {
    max-width: 100%;
    margin: 0 auto;
    padding: 0 24px;
  }

  .image-gallery-section {
    margin-bottom: 32px;

    .image-gallery {
      background: #ffffff;
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);

      .main-image {
        .carousel-image {
          width: 100%;
          height: 700px;
          object-fit: cover;
          display: block;
        }
      }

      .no-image {
        padding: 80px 0;
      }
    }
  }

  .info-section {
    background: #ffffff;
    border-radius: 12px;
    padding: 32px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);

    .header-info {
      margin-bottom: 32px;
      padding-bottom: 24px;
      border-bottom: 2px solid #f0f2f5;

      .title-section {
        .title-row {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          margin-bottom: 16px;

          .house-title {
            margin: 0;
            font-size: 32px;
            font-weight: 700;
            color: #2c3e50;
            flex: 1;
            margin-right: 16px;
          }

          .action-buttons {
            display: flex;
            gap: 12px;

            .el-button {
              border-radius: 6px;
            }
          }
        }

        .price-info {
          display: flex;
          gap: 32px;

          .total-price, .unit-price {
            .price {
              font-size: 28px;
              font-weight: 700;
              color: #e74c3c;
            }

            .unit {
              font-size: 14px;
              color: #909399;
              margin-left: 8px;
            }
          }
        }
      }
    }

    .basic-info {
      margin-bottom: 32px;

      .info-row {
        display: flex;
        gap: 32px;
        margin-bottom: 16px;

        .info-item {
          display: flex;
          align-items: center;
          font-size: 16px;

          i {
            color: #409eff;
            margin-right: 8px;
            font-size: 18px;
          }

          .label {
            color: #606266;
            margin-right: 4px;
          }

          .value {
            color: #2c3e50;
            font-weight: 500;
          }
        }
      }
    }

    .section-title {
      font-size: 20px;
      font-weight: 600;
      color: #2c3e50;
      margin: 0 0 16px 0;
      display: flex;
      align-items: center;

      i {
        color: #409eff;
        margin-right: 8px;
      }
    }

    .address-info, .property-info, .tags-info, .intro-info {
      margin-bottom: 32px;

      .address-content, .property-content {
        .address-item, .property-item {
          display: flex;
          margin-bottom: 12px;
          font-size: 15px;

          .label {
            color: #606266;
            min-width: 80px;
            margin-right: 16px;
          }

          .value {
            color: #2c3e50;
            font-weight: 500;
          }
        }
      }

      .tags-content {
        .tag {
          margin-right: 12px;
          margin-bottom: 8px;
        }
      }

      .intro-content {
        p {
          color: #606266;
          line-height: 1.6;
          font-size: 15px;
          margin: 0;
        }
      }
    }

    .code-info {
      background: #f8f9fa;
      border-radius: 8px;
      padding: 20px;
      border: 1px solid #e9ecef;

      .code-item {
        display: flex;
        align-items: center;
        font-size: 14px;

        .label {
          color: #909399;
          margin-right: 8px;
        }

        .value {
          color: #7f8c8d;
          font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
          background: rgba(0, 0, 0, 0.05);
          padding: 2px 6px;
          border-radius: 4px;
        }

        .separator {
          color: #909399;
          margin: 0 12px;
        }
      }
    }
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .house-detail {
    .detail-content .container {
      padding: 0 16px;
    }

    .detail-content .info-section {
      padding: 20px 16px;

      .header-info {
        flex-direction: column;
        gap: 16px;

        .house-title {
          font-size: 24px;
          margin-right: 0;
        }

        .price-info {
          text-align: left;
        }
      }

      .basic-info .info-row {
        flex-direction: column;
        gap: 12px;
      }
    }
  }
}
</style>
