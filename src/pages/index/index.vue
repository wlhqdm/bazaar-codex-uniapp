<template>
  <view class="page">
    <app-breadcrumb :items="crumbs" />

    <view class="hero-block">
      <text class="eyebrow">The Bazaar 中文图鉴</text>
      <text class="title">大巴扎中文图鉴</text>
      <text class="desc">
        第一阶段先收录海盗瓦内莎专属卡牌，当前已整理 139 张卡牌中文名与封面资源。
      </text>
    </view>

    <view class="section">
      <text class="section-title">角色入口</text>
      <view class="hero-card" @click="goVanessa">
        <view class="hero-copy">
          <text class="hero-role">海盗</text>
          <text class="hero-name">瓦内莎</text>
          <text class="hero-name-en">Vanessa</text>
        </view>
        <view class="hero-count">
          <text class="hero-count-number">139</text>
          <text class="hero-count-label">张卡牌</text>
        </view>
      </view>
    </view>

    <view class="section info-card">
      <text class="section-title">数据说明</text>
      <text class="info-text">中文名基于 BazaarWinner 标注的官方简体中文页面整理。</text>
      <text class="info-text">当前版本聚焦图鉴浏览，后续可继续补充效果、来源、商店与出现天数。</text>
    </view>
  </view>
</template>

<script>
import AppBreadcrumb from '../../components/app-breadcrumb.vue'

export default {
  components: {
    AppBreadcrumb,
  },
  data() {
    return {
      crumbs: [{ label: '首页' }],
    }
  },
  methods: {
    goVanessa() {
      uni.navigateTo({
        url: '/pages/vanessa/index',
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

.section-title {
  display: block;
  margin-bottom: 18rpx;
  font-size: 30rpx;
  font-weight: 600;
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
