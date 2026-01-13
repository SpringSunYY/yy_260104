<template>
  <div :class="className" :style="{ height, width }" ref="chartRef"/>
</template>

<script>
import * as echarts from 'echarts';
import {generateRandomColor} from "@/utils/ruoyi";

export default {
  name: 'ScatterRippleCharts',
  props: {
    className: {
      type: String,
      default: 'chart'
    },
    width: {
      type: String,
      default: '100%'
    },
    height: {
      type: String,
      default: '100%'
    },
    chartTitle: {
      type: String,
      default: '人员构成分布'
    },
    chartData: {
      type: Array,
      default: () => [
        {name: "电力热力", value: 130, tooltipText: "电力供应与热力生产"},
        {name: "管理员", value: 80, tooltipText: "系统后台管理"},
        {name: "医生", value: 110, tooltipText: "医疗诊断专家"},
        {name: "护工", value: 600, tooltipText: "专业生活护理"},
        {name: "护士", value: 95, tooltipText: "医疗护理服务"},
        {name: "技师", value: 70, tooltipText: "技术支持"},
        {name: "志愿者", value: 50, tooltipText: "社区服务"}
      ]
    },
    backgroundColor: {
      type: String,
      default: 'transparent'
    },
    defaultColor: {
      type: Array,
      default: () => [
        '#002FA7', '#1F6AE1', '#3F8EFC', '#88D9FF', // 克莱因蓝系（理性 / 科技 / 主视觉）
        '#0B3C5D', '#1C5D99', '#3A7CA5', '#7FB7D9', // 深海蓝系（秩序 / 稳定 / 后台）
        '#5AC8FA', '#6BC4FF', '#88D9FF', '#BEE9FF', // 天空蓝系（清爽 / 数据可视化）
        '#5B7CFA', '#6A6FF2', '#8A7CF6', '#A184F3', // 紫蓝过渡系（理性 + 情绪）
        '#5F4B8B', '#7A6C9D', '#9C89B8', '#C1B2D6', // 高级紫系（创造 / 想象）
        '#8C1D18', '#B22222', '#C80000', '#EB5757', // 中国红系（权威 / 关键状态）
        '#9E2A2B', '#B23A48', '#C8553D', '#E07A5F', // 胭脂红系（人文 / 温度）
        '#D4A017', '#EB9C10', '#F2C94C', '#FFE08A', // 金黄系（价值 / 成就）
        '#2E7D32', '#43A047', '#66BB6A', '#A5D6A7', // 东方绿系（生命 / 成长）
        '#1F7A7A', '#2FA4A9', '#6ADBCF', '#BFEFEF', // 青绿系（治愈 / 正反馈）
        '#4ED6E6', '#6FE7F0', '#9FF3F5', '#D6FBFB', // 薄荷青系（轻盈 / 呼吸感）
        '#F48FB1', '#F58AD9', '#E38CEB', '#FFD1E8'  // 樱粉系（情绪点缀）
      ]
    },
    minBubbleSize: {
      type: Number,
      default: 70
    },
    maxBubbleSize: {
      type: Number,
      default: 130
    }
  }
  ,
  data() {
    return {
      chart: null,
      totalSum: 0
    };
  }
  ,
  watch: {
    chartData: {
      handler() {
        this.setOptions();
      },
      deep: true
    }
  }
  ,
  mounted() {
    this.$nextTick(() => {
      this.initChart();
      window.addEventListener('resize', this.handleResize);
    });
  }
  ,
  beforeDestroy() {
    if (this.chart) {
      this.chart.dispose();
      this.chart = null;
    }
    window.removeEventListener('resize', this.handleResize);
  }
  ,
  methods: {
    /**
     * 带碰撞检测的随机位置生成
     */
    generateBubbleData() {
      const datas = [];
      const maxVal = Math.max(...this.chartData.map(d => d.value));

      this.chartData.forEach((item, index) => {
        const currentSize = this.minBubbleSize + (item.value / maxVal) * (this.maxBubbleSize - this.minBubbleSize);

        let x, y, isOverlap;
        let attempts = 0;

        // 为每个气泡寻找一个不重叠的随机位置
        do {
          isOverlap = false;
          // 随机坐标 (20% - 80% 之间，留出边缘避免切边)
          x = Math.floor(Math.random() * 60) + 20;
          y = Math.floor(Math.random() * 60) + 20;
          attempts++;

          // 碰撞检测：遍历已生成的点，确保圆心距离 > 两圆半径之和
          for (let i = 0; i < datas.length; i++) {
            const prev = datas[i];
            const dx = x - prev.value[0];
            const dy = y - prev.value[1];
            const distance = Math.sqrt(dx * dx + dy * dy);

            // 映射到坐标系，给一个安全间距系数
            const minDistance = (currentSize + prev.symbolSize) / 10;
            if (distance < minDistance) {
              isOverlap = true;
              break;
            }
          }
        } while (isOverlap && attempts < 100);

        datas.push({
          name: item.name,
          value: [x, y],
          symbolSize: currentSize,
          tooltipText: item.tooltipText || item.name,
          rawValue: item.value,
          itemStyle: {
            normal: {
              color: generateRandomColor(this.defaultColor),
              opacity: 0.9,
              shadowBlur: 15,
              shadowColor: 'rgba(0,0,0,0.2)'
            }
          }
        });
      });

      return datas;
    }
    ,

    /**
     * 初始化图表
     */
    initChart() {
      if (!this.$refs.chartRef) return;

      if (this.chart) {
        this.chart.dispose();
      }
      this.chart = echarts.init(this.$refs.chartRef);
      this.setOptions();
    },
    setOptions() {
      // 计算总计
      this.totalSum = this.chartData.reduce((sum, item) => sum + (item.value || 0), 0);

      const processedData = this.generateBubbleData();

      const option = {
        backgroundColor: this.backgroundColor,
        title: {
          text: this.chartTitle,
          left: 'center',
          top: 20,
          textStyle: {color: '#fff', fontSize: 20}
        },
        dataZoom: [
          { type: 'inside', xAxisIndex: 0, minSpan: 60 },
          { type: 'inside', yAxisIndex: 0, minSpan: 60 }
        ],
        tooltip: {
          show: true,
          backgroundColor: 'rgba(0,0,0,0.8)',
          borderColor: '#555',
          textStyle: {color: '#fff'},
          formatter: (params) => {
            const d = params.data;
            console.log(d)
            const percentage = ((d.rawValue / this.totalSum) * 100).toFixed(2);
            console.log(percentage)
            let res = `<div style="line-height:22px;">
                        <b style="color:#FFD700">总计: ${this.totalSum}</b><br/>
                        ${d.name}: ${d.rawValue} (${percentage}%)`;
            if (d.tooltipText) {
              res += `<br/><span style="color:#00FFFF">${d.tooltipText}</span>`;
            }
            res += `</div>`;
            return res;
          }
        },
        grid: {
          left: 0,
          right: 0,
          top: 0,
          bottom: 0
        },
        xAxis: {
          type: 'value',
          show: false,
          min: 0,
          max: 100
        },
        yAxis: {
          type: 'value',
          show: false,
          min: 0,
          max: 100
        },
        series: [{
          type: 'effectScatter',
          symbol: 'circle',
          symbolSize: 120,
          label: {
            normal: {
              show: true,
              formatter: '{b}',
              color: '#fff',
              textStyle: {
                fontSize: '20'
              }
            }
          },
          data: processedData
        }]
      };

      this.chart.setOption(option);
    },

    handleResize() {
      if (this.chart) {
        this.chart.resize();
      }
    }
  }
};
</script>

<style scoped>
.chart {
  min-height: 400px;
}
</style>
