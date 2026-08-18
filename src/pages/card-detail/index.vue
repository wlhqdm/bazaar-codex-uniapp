<template>
  <view class="page">
    <app-breadcrumb :items="crumbs" />

    <view class="header-card" v-if="card">
      <view class="cover-wrap">
        <image class="cover" :src="coverUrl" mode="aspectFit"></image>
      </view>
      <view class="header-copy">
        <text class="role">{{ hero.titleZh }}</text>
        <text class="name">{{ card.nameZh }}</text>
        <text class="name-en">{{ card.nameEn }}</text>

        <view class="chip-row">
          <text class="chip">{{ card.tierZh }}</text>
          <text class="chip">{{ card.sizeZh }}</text>
          <text class="chip">瓦内莎</text>
        </view>

        <view class="chip-row">
          <text v-for="tag in displayTags" :key="tag" class="chip subtle">{{ tag }}</text>
        </view>

        <text v-if="card.imageStatus === 'placeholder'" class="warning">
          当前封面为占位图，源站缺失原始图片。
        </text>
      </view>
    </view>

    <view class="section-card" v-if="card">
      <text class="section-title">卡牌功能介绍</text>
      <view v-if="effectList.length" class="effects-list">
        <view v-for="effect in effectList" :key="effect.tier" class="effect-block">
          <text class="effect-tier">{{ effect.tierZh }}</text>
          <text v-for="(line, lineIndex) in effect.lines" :key="`${effect.tier}-${lineIndex}`" class="effect-line">{{ line }}</text>
        </view>
      </view>
      <text v-else class="empty-text">{{ card.detailNoticeZh || card.detailNotice || '暂无可展示的效果说明。' }}</text>
    </view>

    <view class="section-card" v-if="card">
      <text class="section-title">获取来源</text>
      <view v-if="sourceList.length" class="source-list">
        <view v-for="source in sourceList" :key="`${source.name}-${source.description}`" class="source-item">
          <text class="source-name">{{ source.name }}</text>
          <text class="source-desc">{{ source.description }}</text>
        </view>
      </view>
      <text v-else class="empty-text">暂无来源数据。</text>
    </view>
  </view>
</template>

<script>
import AppBreadcrumb from '../../components/app-breadcrumb.vue'
import vanessaData from '../../data/vanessa-cards.json'
import { assetUrl } from '../../utils/asset.js'

export default {
  components: {
    AppBreadcrumb,
  },
  data() {
    return {
      hero: vanessaData.hero,
      card: null,
    }
  },
  computed: {
    coverUrl() {
      return this.card ? assetUrl(this.card.image) : ''
    },
    crumbs() {
      return [
        { label: '首页', path: '/pages/index/index' },
        { label: '瓦内莎图鉴', path: '/pages/vanessa/index' },
        { label: this.card ? this.card.nameZh : '卡牌详情' },
      ]
    },
    displayTags() {
      if (!this.card) {
        return []
      }
      return this.card.tagsZh && this.card.tagsZh.length ? this.card.tagsZh : this.card.tags
    },
    effectList() {
      if (!this.card || !this.card.effects) {
        return []
      }
      return this.card.effects.map((effect) => ({
        ...effect,
        lines: effect.linesZh && effect.linesZh.length ? effect.linesZh : effect.lines || [],
      }))
    },
    sourceList() {
      if (!this.card || !this.card.sources) {
        return []
      }
      return this.card.sources.map((source) => ({
        ...source,
        description: source.descriptionZh || source.description || '',
      }))
    },
  },
  onLoad(options) {
    const slug = decodeURIComponent(options.slug || '')
    this.card = vanessaData.cards.find((item) => item.slug === slug) || null

    if (this.card) {
      uni.setNavigationBarTitle({
        title: this.card.nameZh,
      })
    }
  },
}
</script>

<style>
.header-card,
.section-card {
  border-radius: 28rpx;
  background: #161a24;
  border: 1rpx solid rgba(255, 255, 255, 0.08);
}

.header-card {
  overflow: hidden;
}

.cover-wrap {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  padding: 24rpx 24rpx 0;
  background: #121722;
}

.cover {
  width: 100%;
  max-width: 640rpx;
  height: 420rpx;
}

.header-copy {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
  padding: 28rpx;
}

.role {
  font-size: 24rpx;
  color: #d5ae72;
}

.name {
  font-size: 44rpx;
  font-weight: 700;
}

.name-en,
.warning,
.effect-line,
.source-desc,
.empty-text {
  font-size: 24rpx;
  line-height: 1.7;
  color: #bac4da;
}

.warning {
  color: #ffc977;
}

.chip-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.chip {
  padding: 8rpx 16rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.08);
  color: #e2e7f5;
  font-size: 22rpx;
}

.subtle {
  color: #cfd6e8;
}

.section-card {
  margin-top: 24rpx;
  padding: 28rpx;
}

.section-title {
  display: block;
  margin-bottom: 18rpx;
  font-size: 30rpx;
  font-weight: 700;
}

.effects-list,
.source-list {
  display: flex;
  flex-direction: column;
  gap: 18rpx;
}

.effect-block,
.source-item {
  display: flex;
  flex-direction: column;
  gap: 8rpx;
  padding: 20rpx;
  border-radius: 22rpx;
  background: #1c2230;
}

.effect-tier,
.source-name {
  font-size: 26rpx;
  font-weight: 600;
  color: #f3cf92;
}

/* #ifdef H5 */
.cover {
  max-width: 360px;
  height: 240px;
}
/* #endif */
</style>
