<template>
  <div class="house-query">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="header-container">
        <h1 class="page-title">
          <i class="el-icon-house"></i>
          东莞市二手房数据查询
        </h1>
        <p class="page-subtitle">专业房源信息查询平台，提供全面准确的房源数据</p>
      </div>
    </div>

    <!-- 搜索区域 -->
    <div class="search-section">
      <div class="search-container">
        <!-- 搜索头部 -->
        <div class="search-header">
          <div class="search-title-section">
            <i class="el-icon-search"></i>
            <span class="search-title">房源筛选</span>
          </div>
          <el-button
            type="text"
            @click="toggleSearch"
            class="toggle-btn"
          >
            {{ showSearch ? '收起筛选' : '展开筛选' }}
            <i :class="showSearch ? 'el-icon-arrow-up' : 'el-icon-arrow-down'"></i>
          </el-button>
        </div>

        <!-- 搜索表单 -->
        <transition name="slide-fade" appear>
          <div v-show="showSearch" class="search-content">
            <!-- 主要搜索 -->
            <div class="main-search-row">
              <el-input
                v-model="queryParams.title"
                placeholder="房源标题"
                size="medium"
                clearable
                @keyup.enter.native="handleQuery"
              />
              <el-input
                v-model="queryParams.community"
                placeholder="小区名称"
                size="medium"
                clearable
                @keyup.enter.native="handleQuery"
              />
              <el-select v-model="queryParams.town" placeholder="镇" size="medium" clearable>
                <el-option
                  v-for="townDict in dict.type.house_town"
                  :key="townDict.value"
                  :label="townDict.label"
                  :value="townDict.value"
                />
              </el-select>
            </div>

            <!-- 扩展搜索 -->
            <div class="extended-search">
              <el-row :gutter="16">
                <el-col :span="4">
                  <el-select v-model="queryParams.houseType" placeholder="户型" size="small" clearable>
                    <el-option
                      v-for="houseTypeDict in dict.type.house_type"
                      :key="houseTypeDict.value"
                      :label="houseTypeDict.label"
                      :value="houseTypeDict.value"
                    />
                  </el-select>
                </el-col>
                <el-col :span="4">
                  <el-select v-model="queryParams.orientation" placeholder="朝向" size="small" clearable>
                    <el-option
                      v-for="orientationDict in dict.type.house_orientation"
                      :key="orientationDict.value"
                      :label="orientationDict.label"
                      :value="orientationDict.value"
                    />
                  </el-select>
                </el-col>
                <el-col :span="4">
                  <el-select v-model="queryParams.floorType" placeholder="楼层" size="small" clearable>
                    <el-option
                      v-for="floorTypeDict in dict.type.house_floor_type"
                      :key="floorTypeDict.value"
                      :label="floorTypeDict.label"
                      :value="floorTypeDict.value"
                    />
                  </el-select>
                </el-col>
                <el-col :span="4">
                  <el-select v-model="queryParams.decorationType" placeholder="装修" size="small" clearable>
                    <el-option
                      v-for="decorationTypeDict in dict.type.house_decoration_type"
                      :key="decorationTypeDict.value"
                      :label="decorationTypeDict.label"
                      :value="decorationTypeDict.value"
                    />
                  </el-select>
                </el-col>
                <el-col :span="4">
                  <el-select v-model="queryParams.propertyRightType" placeholder="产权" size="small" clearable>
                    <el-option
                      v-for="propertyRightTypeDict in dict.type.house_property_right_type"
                      :key="propertyRightTypeDict.value"
                      :label="propertyRightTypeDict.label"
                      :value="propertyRightTypeDict.value"
                    />
                  </el-select>
                </el-col>
                <el-col :span="4">
                  <el-select v-model="queryParams.propertyType" placeholder="物业" size="small" clearable>
                    <el-option
                      v-for="propertyTypeDict in dict.type.house_property_type"
                      :key="propertyTypeDict.value"
                      :label="propertyTypeDict.label"
                      :value="propertyTypeDict.value"
                    />
                  </el-select>
                </el-col>
              </el-row>
            </div>

            <!-- 操作按钮 -->
            <div class="search-actions">
              <el-button type="primary" icon="el-icon-search" @click="handleQuery" size="medium">
                搜索房源
              </el-button>
              <el-button @click="resetQuery" size="medium">
                <i class="el-icon-refresh"></i>
                重置
              </el-button>
            </div>
          </div>
        </transition>
      </div>
    </div>

    <!-- 房源列表 -->
    <div class="house-list-section">
      <div class="container">
        <!-- 结果统计 -->
        <div class="result-stats" v-if="total > 0">
          <div class="stats-content">
            <i class="el-icon-s-home stats-icon"></i>
            <span class="stats-text">共找到 <strong>{{ total }}</strong> 套房源</span>
          </div>
        </div>

        <!-- 房源网格 -->
        <div class="house-grid">
          <div
            v-for="house in houseList"
            :key="house.hoseId"
            class="house-card"
          >
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
                    v-for="tag in getTags(house.tags).slice(0, 3)"
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
                <h3 class="house-title">{{ house.title }}</h3>
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
                    <dict-tag :options="dict.type.house_type" :value="house.houseType" />
                  </div>
                </div>
                <div class="spec-item">
                  <div class="spec-label">面积</div>
                  <div class="spec-value">{{ house.areaSize }}㎡</div>
                </div>
                <div class="spec-item">
                  <div class="spec-label">朝向</div>
                  <div class="spec-value">
                    <dict-tag :options="dict.type.house_orientation" :value="house.orientation" />
                  </div>
                </div>
                <div class="spec-item">
                  <div class="spec-label">楼层</div>
                  <div class="spec-value">{{ house.floorType }}</div>
                </div>
                <div class="spec-item">
                  <div class="spec-label">装修</div>
                  <div class="spec-value">
                    <dict-tag :options="dict.type.house_decoration_type" :value="house.decorationType" />
                  </div>
                </div>
                <div class="spec-item">
                  <div class="spec-label">年代</div>
                  <div class="spec-value">{{ house.buildingYear }}年</div>
                </div>
                <div class="spec-item">
                  <div class="spec-label">产权</div>
                  <div class="spec-value">
                    <dict-tag :options="dict.type.house_property_right_type" :value="house.propertyRightType" />
                  </div>
                </div>
                <div class="spec-item">
                  <div class="spec-label">物业</div>
                  <div class="spec-value">
                    <dict-tag :options="dict.type.house_property_type" :value="house.propertyType" />
                  </div>
                </div>
              </div>


              <!-- 房源编码 -->
              <div class="house-code">
                <span class="code-value">{{ house.hoseId }}</span>
              </div>
            </div>
          </div>

          <!-- 加载状态 -->
          <div v-if="loading && houseList.length > 0" class="loading-more">
            <el-icon class="is-loading">
              <Loading />
            </el-icon>
            <span>正在加载更多...</span>
          </div>

          <!-- 加载触发器 -->
          <div v-if="hasMore" ref="loadTrigger" class="load-trigger"></div>

          <!-- 没有更多数据 -->
          <div v-if="!loading && !hasMore && houseList.length > 0" class="no-more">
            <span>没有更多房源了</span>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-if="!loading && houseList.length === 0" class="empty-state">
          <el-empty description="暂无房源信息" :image-size="80">
            <el-button type="primary" @click="resetQuery">重新搜索</el-button>
          </el-empty>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { listHouse } from "@/api/house/house";

export default {
  name: "HouseQuery",
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
      // 显示搜索条件
      showSearch: true,
      // 数据相关
      houseList: [],
      total: 0,
      loading: false,
      loadingMore: false,
      hasMore: true,
      // 无限滚动相关
      observer: null,
      observerActive: false,
      scrollListener: null,
      savedScrollTop: 0,

      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 12,
        hoseId: null,
        houseCode: null,
        title: null,
        community: null,
        city: null,
        town: null,
        houseType: null,
        orientation: null,
        floorHeight: null,
        floorType: null,
        buildingYear: null,
        decorationType: null,
        tags: null,
        propertyRightType: null,
        propertyRightYear: null,
        propertyType: null
      }
    };
  },
  created() {
    this.getHouseList();
  },
  mounted() {
    // 初始化无限滚动
    this.setupIntersectionObserver()
    // 添加滚动监听器
    this.setupScrollListener()
  },
  activated() {
    // keep-alive激活时恢复滚动位置并重新初始化观察器
    this.$nextTick(() => {
      // 恢复滚动位置
      if (this.savedScrollTop > 0) {
        window.scrollTo(0, this.savedScrollTop)

        // 延迟重新初始化观察器，确保滚动位置恢复完成
        setTimeout(() => {
          this.observerActive = false // 重置观察器状态
          this.setupIntersectionObserver()
          this.setupScrollListener()
        }, 100)
      } else {
        // 如果没有保存的位置，正常初始化
        this.observerActive = false // 重置观察器状态
        this.setupIntersectionObserver()
        this.setupScrollListener()
      }
    })
  },
  deactivated() {
    // keep-alive失活时保存滚动位置
    this.savedScrollTop = window.pageYOffset || document.documentElement.scrollTop

    // 断开观察器并清理状态
    if (this.observer) {
      this.observer.disconnect()
      this.observer = null
      this.observerActive = false
    }

    // 移除滚动监听器
    if (this.scrollListener) {
      window.removeEventListener('scroll', this.scrollListener)
      this.scrollListener = null
    }
  },
  beforeDestroy() {
    // 清理资源
    if (this.observer) {
      this.observer.disconnect()
    }
    if (this.scrollListener) {
      window.removeEventListener('scroll', this.scrollListener)
    }
  },
  methods: {
    /** 查询房源列表 */
    getHouseList() {
      if (this.loading && !this.loadingMore) return

      this.loading = !this.loadingMore
      this.loadingMore = this.loadingMore && true

      listHouse(this.queryParams).then(response => {
        if (this.loadingMore) {
          this.houseList = [...this.houseList, ...response.rows]
        } else {
          this.houseList = response.rows
          this.total = response.total || 0
        }

        // 判断是否还有更多数据
        this.hasMore = response.rows.length === this.queryParams.pageSize

        this.loading = false
        this.loadingMore = false
      }).catch(() => {
        this.loading = false
        this.loadingMore = false
      })
    },

    /** 搜索按钮操作 */
    handleQuery() {
      this.queryParams.pageNum = 1
      this.houseList = []
      this.hasMore = true
      this.getHouseList()
    },

    /** 重置按钮操作 */
    resetQuery() {
      // 手动重置所有搜索条件
      this.queryParams = {
        pageNum: 1,
        pageSize: 12,
        hoseId: null,
        houseCode: null,
        title: null,
        community: null,
        city: null,
        town: null,
        houseType: null,
        orientation: null,
        floorHeight: null,
        floorType: null,
        buildingYear: null,
        decorationType: null,
        tags: null,
        propertyRightType: null,
        propertyRightYear: null,
        propertyType: null
      }
      // 重置表单（如果存在的话）
      if (this.$refs.queryForm) {
        this.$refs.queryForm.resetFields()
      }
      // 执行搜索
      this.handleQuery()
    },

    /** 切换搜索表单显示 */
    toggleSearch() {
      this.showSearch = !this.showSearch;
    },

    /** 设置无限滚动观察器 */
    setupIntersectionObserver() {
      if (!window.IntersectionObserver) {
        console.warn('IntersectionObserver not supported')
        return
      }

      // 如果已存在观察器，先断开
      if (this.observer) {
        this.observer.disconnect()
      }

      this.observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting && this.hasMore && !this.loadingMore) {
              this.loadMore()
            }
          })
        },
        {
          root: null,
          rootMargin: '100px',
          threshold: 0.1
        }
      )

      // 延迟开始观察，确保DOM已渲染
      this.$nextTick(() => {
        if (this.$refs.loadTrigger) {
          this.observer.observe(this.$refs.loadTrigger)
        }
      })
    },

    /** 加载更多 */
    loadMore() {
      // 防止重复加载
      if (!this.hasMore || this.loadingMore || this.houseList.length === 0) return

      this.queryParams.pageNum++
      this.loadingMore = true
      this.getHouseList()
    },

    /** 设置滚动监听器 */
    setupScrollListener() {
      this.scrollListener = () => {
        if (this.hasMore && this.houseList.length > 0 && !this.loadingMore) {
          const scrollTop = window.pageYOffset || document.documentElement.scrollTop
          const windowHeight = window.innerHeight
          const documentHeight = document.documentElement.scrollHeight

          // 当滚动到距离底部200px时，连接观察器
          if (scrollTop + windowHeight >= documentHeight - 200) {
            if (this.observer && this.$refs.loadTrigger && !this.observerActive) {
              this.observer.observe(this.$refs.loadTrigger)
              this.observerActive = true
            }
          }
        }
      }

      window.addEventListener('scroll', this.scrollListener, { passive: true })
    },

    /** 处理标签 */
    getTags(tagsStr) {
      if (!tagsStr) return [];
      return tagsStr.split(';').filter(tag => tag.trim() !== '');
    },


    /** 截断文本 */
    truncateText(text, maxLength) {
      if (!text) return '';
      if (text.length <= maxLength) return text;
      return text.substring(0, maxLength) + '...';
    }
  }
};
</script>

<style scoped lang="scss">
.house-query {
  background: #f8f9fa;
  min-height: 100vh;
}

/* 页面标题 */
.page-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 40px 0 60px;
  text-align: center;
  position: relative;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 100" fill="rgba(255,255,255,0.1)"><polygon points="0,0 1000,0 1000,60 0,100"/></svg>') no-repeat center bottom;
    background-size: cover;
    opacity: 0.5;
  }

  .header-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 24px;
    position: relative;
    z-index: 2;

    .page-title {
      margin: 0 0 12px 0;
      font-size: 36px;
      font-weight: 700;
      color: #ffffff;
      display: flex;
      align-items: center;
      justify-content: center;
      text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);

      i {
        margin-right: 16px;
        font-size: 40px;
        filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.3));
      }
    }

    .page-subtitle {
      margin: 0;
      font-size: 16px;
      color: rgba(255, 255, 255, 0.9);
      font-weight: 400;
    }
  }
}

/* 搜索区域 */
.search-section {
  background: #ffffff;
  border-bottom: 1px solid #e4e7ed;
  padding: 32px 0;
  margin-top: -30px;
  position: relative;
  z-index: 3;

  .search-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 24px;

    .search-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
      padding-bottom: 16px;
      border-bottom: 2px solid #f0f2f5;

      .search-title-section {
        display: flex;
        align-items: center;

        i {
          font-size: 20px;
          color: #409eff;
          margin-right: 8px;
        }

        .search-title {
          font-size: 18px;
          font-weight: 600;
          color: #303133;
        }
      }

      .toggle-btn {
        color: #606266;
        font-weight: 500;

        &:hover {
          color: #409eff;
        }
      }
    }

    .search-content {
      .main-search-row {
        display: grid;
        grid-template-columns: 2fr 2fr 1fr;
        gap: 16px;
        margin-bottom: 16px;

        .el-input__inner,
        .el-select {
          width: 100%;
          border-radius: 8px;
          border: 2px solid #e1e8ed;
          transition: all 0.3s ease;

          &:focus,
          &:hover {
            border-color: #409eff;
            box-shadow: 0 0 0 3px rgba(64, 158, 255, 0.1);
          }
        }
      }

      .extended-search {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #e9ecef;

        .el-input__inner,
        .el-select {
          width: 100%;
          border-radius: 6px;
          border: 1px solid #ced4da;
          font-size: 13px;
          transition: all 0.2s ease;

          &:focus {
            border-color: #409eff;
            box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.1);
          }
        }
      }

      .search-actions {
        display: flex;
        justify-content: center;
        gap: 12px;

        .el-button {
          padding: 10px 24px;
          border-radius: 8px;
          font-weight: 600;
          transition: all 0.3s ease;

          &.el-button--primary {
            background: linear-gradient(135deg, #409eff 0%, #5cadff 100%);
            border: none;
            box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);

            &:hover {
              transform: translateY(-2px);
              box-shadow: 0 6px 16px rgba(64, 158, 255, 0.4);
            }

            i {
              margin-right: 6px;
            }
          }

          &.el-button--default {
            border-color: #d9d9d9;
            color: #606266;

            &:hover {
              border-color: #409eff;
              color: #409eff;
              transform: translateY(-1px);
            }
          }
        }
      }
    }

    /* 滑动动画 */
    .slide-fade-enter-active,
    .slide-fade-leave-active {
      transition: all 0.3s ease;
    }

    .slide-fade-enter,
    .slide-fade-leave-to {
      opacity: 0;
      transform: translateY(-10px);
    }
  }
}

/* 房源列表区域 */
.house-list-section {
  padding: 40px 0;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);

  .container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 24px;

    .result-stats {
      margin-bottom: 24px;
      text-align: center;

      .stats-content {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border: 1px solid #0ea5e9;
        border-radius: 20px;
        padding: 8px 16px;
        box-shadow: 0 2px 8px rgba(14, 165, 233, 0.1);

        .stats-icon {
          color: #0ea5e9;
          font-size: 16px;
        }

        .stats-text {
          font-size: 14px;
          color: #0c4a6e;
          font-weight: 500;

          strong {
            color: #0ea5e9;
            font-size: 16px;
            font-weight: 700;
          }
        }
      }
    }

    .house-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 24px;
      margin-bottom: 32px;

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
    }

    .loading-more, .no-more {
      grid-column: 1 / -1;
      text-align: center;
      padding: 32px;
      color: #909399;

      .el-icon {
        margin-right: 8px;
      }
    }

    .load-trigger {
      height: 20px;
      margin: 20px 0;
    }

    .no-more {
      color: #c0c4cc;
    }

    .empty-state {
      grid-column: 1 / -1;
      padding: 64px 0;
    }
  }
}

/* 响应式设计 */
@media (max-width: 1400px) {
  .house-query .house-list-section .container .house-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 1024px) {
  .house-query .house-list-section .container .house-grid {
    grid-template-columns: repeat(1, 1fr);
    gap: 16px;
  }
}

@media (max-width: 768px) {
  .house-query {
    .search-section {
      padding: 16px 0;

      .search-container {
        padding: 0 16px;

        .search-header {
          flex-direction: column;
          align-items: flex-start;
          gap: 12px;

          .search-title {
            font-size: 18px;
          }
        }

        .search-form .form-row {
          .el-col {
            width: 100%;
            margin-bottom: 12px;
          }
        }
      }
    }

    .house-list-section {
      padding: 20px 0;

      .container {
        padding: 0 16px;

        .house-grid {
          grid-template-columns: 1fr;
          gap: 12px;

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
      }
    }
  }
}

@media (max-width: 480px) {
  .house-query {
    .search-section .search-container {
      .search-form .form-row .el-form-item .el-form-item__label {
        width: 100px !important;
      }
    }

    .house-list-section .container .house-grid .house-card {
      .house-info-section {
        .specs-grid {
          grid-template-columns: 1fr;
        }

        .address-info {
          font-size: 12px;
        }
      }
    }
  }
}
</style>
