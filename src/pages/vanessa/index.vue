<template>
  <view class="page">
    <app-breadcrumb :items="crumbs" />

    <view class="hero-header">
      <text class="hero-role">{{ hero.titleZh }}</text>
      <text class="hero-name">{{ hero.nameZh }}</text>
      <text class="hero-name-en">{{ hero.nameEn }}</text>
      <text class="hero-desc">瓦内莎专属图鉴，支持按中文名、英文名检索。</text>
    </view>

    <view class="toolbar">
      <input
        v-model.trim="keyword"
        class="search-input"
        placeholder="搜索卡牌中文名 / 英文名"
        placeholder-class="search-placeholder"
      />
      <view class="stat-box">
        <text class="stat-number">{{ filteredCards.length }}</text>
        <text class="stat-label">/ {{ hero.count }}</text>
      </view>
    </view>

    <view class="tip-box">
      <text class="tip-text">点击卡牌进入详情页，可同时查看功能介绍和获取来源。</text>
    </view>

    <card-grid :cards="filteredCards" @select="openDetail" />
  </view>
</template>

<script>
import CardGrid from '../../components/card-grid.vue'
import AppBreadcrumb from '../../components/app-breadcrumb.vue'
import vanessaData from '../../data/vanessa-cards.json'

export default {
  components: {
    CardGrid,
    AppBreadcrumb,
  },
  data() {
    return {
      hero: vanessaData.hero,
      cards: vanessaData.cards,
      keyword: '',
      crumbs: [
        { label: '首页', path: '/pages/index/index' },
        { label: '瓦内莎图鉴' },
      ],
    }
  },
  computed: {
    filteredCards() {
      const query = this.keyword.toLowerCase()
      if (!query) {
        return this.cards
      }
      return this.cards.filter((card) => {
        return (
          card.nameZh.toLowerCase().includes(query) ||
          card.nameEn.toLowerCase().includes(query)
        )
      })
    },
  },
  methods: {
    openDetail(card) {
      uni.navigateTo({
        url: `/pages/card-detail/index?slug=${encodeURIComponent(card.slug)}`,
      })
    },
  },
}
</script>

<style>
.hero-header {
  display: flex;
  flex-direction: column;
  gap: 10rpx;
  padding: 32rpx;
  border-radius: 28rpx;
  background: linear-gradient(135deg, #1b2335, #0f131d);
  border: 1rpx solid rgba(255, 255, 255, 0.08);
}

.hero-role {
  font-size: 24rpx;
  color: #d5ae72;
}

.hero-name {
  font-size: 48rpx;
  font-weight: 700;
}

.hero-name-en,
.hero-desc {
  font-size: 24rpx;
  line-height: 1.6;
  color: #a9b4cb;
}

.toolbar {
  display: flex;
  align-items: center;
  gap: 16rpx;
  margin: 24rpx 0 18rpx;
}

.search-input {
  flex: 1;
  height: 84rpx;
  padding: 0 24rpx;
  border-radius: 20rpx;
  background: #1a1d29;
  color: #f8f4e9;
  border: 1rpx solid rgba(255, 255, 255, 0.08);
}

.search-placeholder {
  color: #6f7891;
}

.stat-box {
  min-width: 140rpx;
  padding: 14rpx 20rpx;
  border-radius: 20rpx;
  background: #1a1d29;
  border: 1rpx solid rgba(255, 255, 255, 0.08);
  text-align: center;
}

.stat-number {
  font-size: 32rpx;
  font-weight: 700;
  color: #f5d39a;
}

.stat-label {
  font-size: 22rpx;
  color: #8f9ab3;
}

.tip-box {
  margin-bottom: 20rpx;
  padding: 18rpx 22rpx;
  border-radius: 20rpx;
  background: rgba(245, 188, 89, 0.08);
  border: 1rpx solid rgba(245, 188, 89, 0.18);
}

.tip-text {
  font-size: 22rpx;
  line-height: 1.6;
  color: #d8c3a0;
}
</style>
