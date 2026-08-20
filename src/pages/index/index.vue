<template>
  <view class="page">
    <app-breadcrumb :items="crumbs" />

    <view class="hero-block">
      <text class="eyebrow">The Bazaar 中文图鉴</text>
      <text class="title">大巴扎中文图鉴</text>
      <text class="desc">
        收录官网全部角色与中立卡牌，支持按角色浏览列表与详情（效果、来源、附魔）。
      </text>
    </view>

    <view class="section">
      <view class="section-head">
        <text class="section-title">角色入口</text>
        <text class="section-count">共 {{ totalCards }} 张</text>
      </view>
      <view class="hero-list">
        <view
          v-for="item in heroes"
          :key="item.key"
          class="hero-card"
          @click="goHero(item.key)"
        >
          <view class="hero-copy">
            <text class="hero-role">{{ item.titleZh }}</text>
            <text class="hero-name">{{ item.nameZh }}</text>
            <text class="hero-name-en">{{ item.nameEn }}</text>
          </view>
          <view class="hero-count">
            <text class="hero-count-number">{{ item.count }}</text>
            <text class="hero-count-label">张卡牌</text>
          </view>
        </view>
      </view>
    </view>

    <view class="section info-card">
      <text class="section-title">数据说明</text>
      <text class="info-text">中文名基于 BazaarWinner 标注的官方简体中文页面整理。</text>
      <text class="info-text">效果与来源说明为本站初版中文，可继续校对完善。</text>
    </view>
  </view>
</template>

<script>
import AppBreadcrumb from '../../components/app-breadcrumb.vue'
import { heroListPath, listHeroes } from '../../utils/heroes.js'

export default {
  components: {
    AppBreadcrumb,
  },
  data() {
    return {
      crumbs: [{ label: '首页' }],
      heroes: listHeroes(),
    }
  },
  computed: {
    totalCards() {
      return this.heroes.reduce((sum, item) => sum + (item.count || 0), 0)
    },
  },
  methods: {
    goHero(key) {
      uni.navigateTo({
        url: heroListPath(key),
      })
    },
  },
}
</script>

<style>
.hero-block {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
  padding: 40rpx 32rpx;
  border-radius: 28rpx;
  background: linear-gradient(135deg, #1c2231, #10141d);
  border: 1rpx solid rgba(255, 255, 255, 0.08);
}

.eyebrow {
  font-size: 24rpx;
  color: #c9a86a;
}

.title {
  font-size: 52rpx;
  font-weight: 700;
}

.desc {
  font-size: 26rpx;
  line-height: 1.7;
  color: #cad1e3;
}

.section {
  margin-top: 32rpx;
}

.section-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 18rpx;
}

.section-title {
  display: block;
  font-size: 30rpx;
  font-weight: 600;
}

.section-count {
  font-size: 22rpx;
  color: #8f9ab3;
}

.hero-list {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.hero-card {
  display: flex;
  justify-content: space-between;
  gap: 24rpx;
  padding: 28rpx;
  border-radius: 28rpx;
  background: #1a1d29;
  border: 1rpx solid rgba(255, 255, 255, 0.08);
}

.hero-copy {
  display: flex;
  flex-direction: column;
  gap: 12rpx;
}

.hero-role {
  font-size: 24rpx;
  color: #c9a86a;
}

.hero-name {
  font-size: 40rpx;
  font-weight: 700;
}

.hero-name-en {
  font-size: 24rpx;
  color: #8f9ab3;
}

.hero-count {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-end;
}

.hero-count-number {
  font-size: 54rpx;
  font-weight: 700;
  color: #f6d59b;
}

.hero-count-label {
  font-size: 24rpx;
  color: #8f9ab3;
}

.info-card {
  padding: 28rpx;
  border-radius: 28rpx;
  background: #161a24;
  border: 1rpx solid rgba(255, 255, 255, 0.06);
}

.info-card .section-title {
  margin-bottom: 18rpx;
}

.info-text {
  display: block;
  font-size: 24rpx;
  line-height: 1.7;
  color: #cad1e3;
}

.info-text + .info-text {
  margin-top: 10rpx;
}
</style>
