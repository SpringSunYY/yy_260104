<template>
  <div class="house-card">
    <!-- 房源图片区域 -->
    <div class="house-image-section">
      <div class="house-image">
        <img
          :src="house.coverImage"
          alt="房源图片"
          class="house-img"
        />
        <div class="image-overlay"></div>

        <!-- 价格标签 - 右上角 -->
        <div class="price-badge">
          <span class="price">{{ house.totalPrice }}万</span>
        </div>

        <!-- 房源标签 - 左下角 -->
        <div class="tags-overlay" v-if="house.tags">
          <el-tag
            v-for="tag in getTags(house.tags).slice(0, 5)"
            :key="tag"
            size="mini"
            type="warning"
            class="tag"
          >
            {{ tag }}
          </el-tag>
        </div>
      </div>
    </div>

    <!-- 房源信息区域 -->
    <div class="house-info-section">
      <!-- 标题 -->
      <div class="title-section">
        <router-link
          :to="'/house/detail/index/' + house.houseId" class="house-title">
          {{ house.title }}
        </router-link>
      </div>

      <!-- 地址信息 -->
      <div class="address-info">
        <i class="el-icon-location-outline"></i>
        <span class="community">{{ house.community }}</span>
        <span class="separator">·</span>
        <span class="area">{{ house.address }}</span>
      </div>

      <!-- 规格信息 -->
      <div class="specs-grid">
        <div class="spec-item">
          <div class="spec-label">户型</div>
          <div class="spec-value">
            <dict-tag :options="dict.type.house_type" :value="house.houseType"/>
          </div>
        </div>
        <div class="spec-item">
          <div class="spec-label">面积</div>
          <div class="spec-value">{{ house.areaSize }}㎡</div>
        </div>
        <div class="spec-item">
          <div class="spec-label">朝向</div>
          <div class="spec-value">
            <dict-tag :options="dict.type.house_orientation" :value="house.orientation"/>
          </div>
        </div>
        <div class="spec-item">
          <div class="spec-label">楼层</div>
          <div class="spec-value">{{ house.floorType }}</div>
        </div>
        <div class="spec-item">
          <div class="spec-label">装修</div>
          <div class="spec-value">
            <dict-tag :options="dict.type.house_decoration_type" :value="house.decorationType"/>
          </div>
        </div>
        <div class="spec-item">
          <div class="spec-label">年代</div>
          <div class="spec-value">{{ house.buildingYear }}年</div>
        </div>
        <div class="spec-item">
          <div class="spec-label">产权</div>
          <div class="spec-value">
            <dict-tag :options="dict.type.house_property_right_type" :value="house.propertyRightType"/>
          </div>
        </div>
        <div class="spec-item">
          <div class="spec-label">物业</div>
          <div class="spec-value">
            <dict-tag :options="dict.type.house_property_type" :value="house.propertyType"/>
          </div>
        </div>
      </div>


      <!-- 房源编码 -->
      <div class="house-code">
        <span class="code-value">{{ house.houseId }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "HouseCard",
  dicts: [
    'house_type',
    'house_orientation',
    'house_decoration_type',
    'house_property_right_type',
    'house_property_type'
  ],
  props: {
    house: {
      type: Object,
      required: true
    }
  },
  methods: {
    /** 处理标签 */
    getTags(tagsStr) {
      if (!tagsStr) return [];
      return tagsStr.split(';').filter(tag => tag.trim() !== '');
    }
  }
};
</script>

<style scoped lang="scss">
.house-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  border: 1px solid rgba(64, 158, 255, 0.1);

  &:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 12px 40px rgba(64, 158, 255, 0.15);
    border-color: rgba(64, 158, 255, 0.2);
  }

  .house-image-section {
    position: relative;

    .house-image {
      position: relative;
      width: 100%;
      height: 300px;
      overflow: hidden;
      border-radius: 12px 12px 0 0;

      .house-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
      }

      .image-overlay {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 60px;
        background: linear-gradient(transparent, rgba(0, 0, 0, 0.2));
      }

      .price-badge {
        position: absolute;
        top: 16px;
        right: 16px;
        color: #e74c3c;
        font-size: 36px;
        font-weight: 800;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
      }

      .tags-overlay {
        position: absolute;
        bottom: 16px;
        left: 16px;
        right: 16px;
        display: flex;
        flex-wrap: wrap;
        gap: 6px;

        .tag {
          background: rgba(255, 193, 7, 0.95);
          color: #fff;
          border: none;
          font-size: 11px;
          padding: 4px 8px;
          font-weight: 500;
          border-radius: 12px;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
          display: inline-flex;
          align-items: center;
          justify-content: center;
          text-align: center;
        }
      }
    }
  }

  .house-info-section {
    padding: 24px;

    .title-section {
      margin-bottom: 12px;

      .house-title {
        margin: 0;
        font-size: 26px;
        font-weight: 700;
        color: #2c3e50;
        line-height: 1.4;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        line-clamp: 2;
        overflow: hidden;
        transition: color 0.3s ease;
        cursor: pointer;

        &:hover {
          color: #409eff;
        }
      }
    }

    .address-info {
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 4px;
      font-size: 14px;
      color: #606266;
      margin-bottom: 16px;
      padding: 8px 12px;
      background: rgba(64, 158, 255, 0.05);
      border-radius: 8px;
      border-left: 3px solid #409eff;

      i {
        color: #409eff;
        margin-right: 6px;
      }

      .community {
        color: #409eff;
        font-weight: 600;
      }

      .separator {
        color: #909399;
        margin: 0 6px;
      }

      .area, .address {
        color: #7f8c8d;
      }
    }

    .specs-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
      margin-bottom: 16px;

      .spec-item {
        text-align: center;
        padding: 12px 8px;
        background: linear-gradient(135deg, #f8f9fa 0%, #e8f4f8 100%);
        border-radius: 8px;
        border: 1px solid rgba(64, 158, 255, 0.1);
        transition: all 0.3s ease;

        &:hover {
          background: linear-gradient(135deg, #e8f4f8 0%, #d1ecf1 100%);
          transform: translateY(-1px);
          box-shadow: 0 2px 8px rgba(64, 158, 255, 0.1);
        }

        .spec-label {
          font-size: 11px;
          color: #7f8c8d;
          margin-bottom: 4px;
          line-height: 1.2;
          font-weight: 500;
        }

        .spec-value {
          font-size: 13px;
          font-weight: 600;
          color: #2c3e50;
          line-height: 1.2;
        }
      }
    }


    .house-code {
      padding-top: 12px;
      border-top: 1px solid rgba(64, 158, 255, 0.1);

      .code-label {
        font-size: 12px;
        color: #909399;
        margin-right: 8px;
      }

      .code-value {
        font-size: 12px;
        color: #7f8c8d;
        font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
        background: rgba(0, 0, 0, 0.05);
        padding: 2px 6px;
        border-radius: 4px;
      }
    }
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .house-card .house-info-section {
    padding: 16px;

    .specs-grid {
      grid-template-columns: repeat(2, 1fr);
      gap: 6px;
    }

    .house-title {
      font-size: 14px;
    }
  }
}

@media (max-width: 480px) {
  .house-card .house-info-section {
    .specs-grid {
      grid-template-columns: 1fr;
    }

    .address-info {
      font-size: 12px;
    }
  }
}
</style>
