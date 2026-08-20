<template>
  <view class="page">
    <app-breadcrumb :items="crumbs" />

    <view class="hero-header">
      <text class="hero-role">{{ hero.titleZh }}</text>
      <text class="hero-name">{{ hero.nameZh }}</text>
      <text class="hero-name-en">{{ hero.nameEn }}</text>
      <text class="hero-desc">支持按中文名、英文名与标签检索，并可筛选尺寸与品级。</text>
    </view>

    <view class="toolbar">
      <input
        v-model.trim="keyword"
        class="search-input"
        placeholder="搜索卡牌名 / 标签（如武器、水生）"
        placeholder-class="search-placeholder"
      />
      <view class="stat-box">
        <text class="stat-number">{{ filteredCards.length }}</text>
        <text class="stat-label">/ {{ hero.count }}</text>
      </view>
    </view>

    <view class="filter-panel">
      <view class="filter-row">
        <text class="filter-label">品级</text>
        <view class="filter-chips">
          <text
            v-for="option in tierOptions"
            :key="option.value"
            class="filter-chip"
            :class="{ active: selectedTier === option.value }"
            @click="selectedTier = option.value"
          >{{ option.label }}</text>
        </view>
      </view>
      <view class="filter-row">
        <text class="filter-label">尺寸</text>
        <view class="filter-chips">
          <text
            v-for="option in sizeOptions"
            :key="option.value"
            class="filter-chip"
            :class="{ active: selectedSize === option.value }"
            @click="selectedSize = option.value"
          >{{ option.label }}</text>
        </view>
      </view>
    </view>

    <view class="tip-box">
      <text class="tip-text">点击卡牌进入详情，可查看效果、商店 / 事件来源与附魔变体。</text>
    </view>

    <card-grid :cards="filteredCards" @select="openDetail" />
  </view>
</template>

<script>
import CardGrid from '../../components/card-grid.vue'
import AppBreadcrumb from '../../components/app-breadcrumb.vue'
import { cardDetailPath, getHeroCards, getHeroMeta } from '../../utils/heroes.js'

const BASE_TIERS = [
  { value: 'all', label: '全部' },
  { value: 'Bronze', label: '青铜' },
  { value: 'Silver', label: '白银' },
  { value: 'Gold', label: '黄金' },
  { value: 'Diamond', label: '钻石' },
]

export default {
  components: {
    CardGrid,
    AppBreadcrumb,
  },
  data() {
    return {
      heroKey: 'vanessa',
      hero: {
        key: 'vanessa',
        nameZh: '',
        nameEn: '',
        titleZh: '',
        count: 0,
      },
      cards: [],
      keyword: '',
      selectedTier: 'all',
      selectedSize: 'all',
      sizeOptions: [
        { value: 'all', label: '全部' },
        { value: '小', label: '小' },
        { value: '中', label: '中' },
        { value: '大', label: '大' },
      ],
    }
  },
  computed: {
    crumbs() {
      return [
        { label: '首页', path: '/pages/index/index' },
        { label: `${this.hero.nameZh || '角色'}图鉴` },
      ]
    },
    tierOptions() {
      const options = [...BASE_TIERS]
      if (this.cards.some((card) => card.tier === 'Legendary')) {
        options.push({ value: 'Legendary', label: '传说' })
      }
      return options
    },
    filteredCards() {
      const query = this.keyword.toLowerCase()
      return this.cards.filter((card) => {
        if (this.selectedTier !== 'all' && card.tier !== this.selectedTier) {
          return false
        }
        if (this.selectedSize !== 'all' && card.sizeZh !== this.selectedSize) {
          return false
        }
        if (!query) {
          return true
        }
        const haystack = [
          card.nameZh,
          card.nameEn,
          card.tierZh,
          card.sizeZh,
          card.dayLabel,
          card.dayZh,
          ...(card.tags || []),
          ...(card.tagsZh || []),
        ]
          .filter(Boolean)
          .join(' ')
          .toLowerCase()
        return haystack.includes(query)
      })
    },
  },
  onLoad(options) {
    const key = decodeURIComponent(options.key || 'vanessa')
    this.loadHero(key)
  },
  methods: {
    loadHero(key) {
      this.heroKey = key
      const meta = getHeroMeta(key)
      this.hero = meta || {
        key,
        nameZh: key,
        nameEn: key,
        titleZh: '',
        count: 0,
      }
      this.cards = getHeroCards(key)
      this.selectedTier = 'all'
      this.selectedSize = 'all'
      this.keyword = ''
      uni.setNavigationBarTitle({
        title: `${this.hero.nameZh}图鉴`,
      })
    },
    openDetail(card) {
      uni.navigateTo({
        url: cardDetailPath(this.heroKey, card.slug),
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

.filter-panel {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
  margin-bottom: 18rpx;
  padding: 20rpx 22rpx;
  border-radius: 22rpx;
  background: #161a24;
  border: 1rpx solid rgba(255, 255, 255, 0.08);
}

.filter-row {
  display: flex;
  align-items: flex-start;
  gap: 16rpx;
}

.filter-label {
  width: 64rpx;
  padding-top: 10rpx;
  font-size: 22rpx;
  color: #9aa6c0;
  flex-shrink: 0;
}

.filter-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
  flex: 1;
}

.filter-chip {
  padding: 10rpx 18rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.06);
  color: #c9d2e6;
  font-size: 22rpx;
  border: 1rpx solid transparent;
}

.filter-chip.active {
  background: rgba(245, 188, 89, 0.16);
  color: #f5d39a;
  border-color: rgba(245, 188, 89, 0.35);
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
