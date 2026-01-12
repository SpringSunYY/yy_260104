<template>
  <div class="home-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="header-container">
        <h1 class="page-title">
          <i class="el-icon-house"></i>
          欢迎使用东莞市二手房平台
        </h1>
        <p class="page-subtitle">发现您的理想家园，我们为您推荐最适合的房源</p>
      </div>
    </div>

    <!-- 推荐房源区域 -->
    <div class="recommendations-section">
      <div class="container">
        <!-- 推荐标题 -->
        <div class="recommendations-header">
          <div class="header-content">
            <i class="el-icon-star-on"></i>
            <span class="recommendations-title">为您推荐</span>
            <span class="recommendations-subtitle">基于您的喜好智能推荐</span>
          </div>
          <router-link to="/house/query" class="view-more">
            查看更多
            <i class="el-icon-arrow-right"></i>
          </router-link>
        </div>

        <!-- 结果统计 -->
        <div class="result-stats" v-if="total > 0">
          <div class="stats-content">
            <i class="el-icon-s-home stats-icon"></i>
            <span class="stats-text">为您推荐 <strong>{{ total }}</strong> 套优质房源</span>
          </div>
        </div>

        <!-- 推荐房源网格 -->
        <div class="recommendations-grid">
          <house-card
            v-for="house in houseList"
            :key="house.houseId"
            :house="house"
          />

          <!-- 加载状态 -->
          <div v-if="loading && houseList.length > 0" class="loading-more">
            <el-icon class="is-loading">
              <Loading/>
            </el-icon>
            <span>正在加载更多...</span>
          </div>

          <!-- 加载触发器 -->
          <div v-if="hasMore" ref="loadTrigger" class="load-trigger"></div>

          <!-- 没有更多数据 -->
          <div v-if="!loading && !hasMore && houseList.length > 0" class="no-more">
            <span>没有更多推荐了</span>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-if="!loading && houseList.length === 0" class="empty-state">
          <el-empty description="暂无推荐房源，浏览一些房源后系统会为您推荐" :image-size="80">
            <router-link to="/house/query">
              <el-button type="primary">去浏览房源</el-button>
            </router-link>
          </el-empty>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import HouseCard from '@/components/HouseCard'
import { listMyRecommendations } from "@/api/house/recommend";

export default {
  name: "Index",
  components: {
    HouseCard
  },
  data() {
    return {
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
        pageSize: 12
      }
    };
  },
  created() {
    this.getRecommendations();
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
    /** 查询推荐房源列表 */
    getRecommendations() {
      if (this.loading && !this.loadingMore) return

      this.loading = !this.loadingMore
      this.loadingMore = this.loadingMore && true

      listMyRecommendations(this.queryParams).then(response => {
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

    /** 加载更多 */
    loadMore() {
      // 防止重复加载
      if (!this.hasMore || this.loadingMore || this.houseList.length === 0) return

      this.queryParams.pageNum++
      this.loadingMore = true
      this.getRecommendations()
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

      window.addEventListener('scroll', this.scrollListener, {passive: true})
    }
  }
};
</script>

<style scoped lang="scss">
.home-page {
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

/* 推荐房源区域 */
.recommendations-section {
  padding: 40px 0;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);

  .container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 24px;

    .recommendations-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
      padding-bottom: 16px;
      border-bottom: 2px solid #e4e7ed;

      .header-content {
        display: flex;
        align-items: center;

        i {
          font-size: 24px;
          color: #e6a23c;
          margin-right: 12px;
        }

        .recommendations-title {
          font-size: 24px;
          font-weight: 700;
          color: #303133;
          margin-right: 12px;
        }

        .recommendations-subtitle {
          font-size: 14px;
          color: #909399;
        }
      }

      .view-more {
        display: flex;
        align-items: center;
        color: #409eff;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.3s ease;

        &:hover {
          color: #66b1ff;

          i {
            transform: translateX(4px);
          }
        }

        i {
          margin-left: 6px;
          transition: transform 0.3s ease;
        }
      }
    }

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

    .recommendations-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 24px;
      margin-bottom: 32px;

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
    }

    .empty-state {
      grid-column: 1 / -1;
      padding: 64px 0;
    }
  }
}


/* 响应式设计 */
@media (max-width: 1400px) {
  .home-page .recommendations-section .container .recommendations-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 1024px) {
  .home-page .recommendations-section .container .recommendations-grid {
    grid-template-columns: repeat(1, 1fr);
    gap: 16px;
  }
}

@media (max-width: 768px) {
  .home-page {
    .page-header {
      padding: 20px 0 40px;

      .header-container {
        padding: 0 16px;

        .page-title {
          font-size: 24px;

          i {
            font-size: 28px;
          }
        }

        .page-subtitle {
          font-size: 14px;
        }
      }
    }

    .recommendations-section {
      padding: 20px 0;

      .container {
        padding: 0 16px;

        .recommendations-header {
          flex-direction: column;
          align-items: flex-start;
          gap: 12px;

          .header-content {
            .recommendations-title {
              font-size: 18px;
            }
          }
        }

        .recommendations-grid {
          grid-template-columns: 1fr;
          gap: 12px;
        }
      }
    }

  }
}
</style>
