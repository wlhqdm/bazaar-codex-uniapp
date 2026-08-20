<template>
  <view class="page">
    <app-breadcrumb :items="crumbs" />

    <view v-if="card" class="header-card">
      <view class="header-main">
        <view class="cover-wrap">
          <image class="cover" :src="coverUrl" mode="aspectFit"></image>
        </view>
        <view class="header-copy">
          <text class="role">{{ hero.titleZh }} · {{ hero.nameZh }}</text>
          <text class="name">{{ card.nameZh }}</text>
          <text class="name-en">{{ card.nameEn }}</text>

          <view class="meta-line">
            <text class="meta-strong">{{ card.tierZh }}</text>
            <text class="meta-dot">·</text>
            <text class="meta-text">尺寸：{{ card.sizeZh }}</text>
            <text v-if="card.dayZh || card.dayLabel" class="meta-dot">·</text>
            <text v-if="card.dayZh" class="meta-day">{{ card.dayZh }}</text>
            <text v-else-if="card.dayLabel" class="meta-day">{{ card.dayLabel }}</text>
          </view>

          <view class="chip-row">
            <text v-for="tag in displayTags" :key="tag" class="chip">{{ tag }}</text>
            <text v-if="card.dayLabel" class="chip day">{{ card.dayLabel }}</text>
          </view>

          <text v-if="card.imageStatus === 'placeholder'" class="warning">
            当前封面为占位图，源站缺失原始图片。
          </text>
        </view>
      </view>
    </view>

    <view v-else class="section-card">
      <text class="empty-text">未找到对应卡牌。</text>
    </view>

    <view v-if="card" class="section-grid">
      <view class="section-card">
        <text class="section-title">各品级效果</text>
        <view v-if="effectList.length" class="effects-list">
          <view v-for="effect in effectList" :key="effect.tier" class="effect-block">
            <text class="effect-tier">{{ effect.tierZh }}</text>
            <text
              v-for="(line, lineIndex) in effect.lines"
              :key="`${effect.tier}-${lineIndex}`"
              class="effect-line"
            >{{ line }}</text>
          </view>
        </view>
        <text v-else class="empty-text">{{ card.detailNoticeZh || card.detailNotice || '暂无可展示的效果说明。' }}</text>
      </view>

      <view class="section-card">
        <view class="section-title-row">
          <text class="section-title">获取来源</text>
          <text class="section-sub">商店 / 事件</text>
        </view>

        <view v-if="shopList.length" class="source-group">
          <text class="group-title">商店</text>
          <view class="source-list">
            <view v-for="source in shopList" :key="`shop-${source.name}`" class="source-item">
              <text class="source-name">{{ source.nameZh || source.name }}</text>
              <text v-if="source.nameZh && source.nameZh !== source.name" class="source-en">{{ source.name }}</text>
              <text class="source-desc">{{ source.description }}</text>
            </view>
          </view>
        </view>

        <view v-if="eventList.length" class="source-group">
          <text class="group-title">出现于战斗事件</text>
          <view class="source-list">
            <view v-for="event in eventList" :key="`event-${event.name}`" class="source-item event">
              <text class="source-name">{{ event.nameZh || event.name }}</text>
              <text v-if="event.nameZh && event.nameZh !== event.name" class="source-en">{{ event.name }}</text>
              <text class="source-desc">{{ event.description || '出现于战斗事件' }}</text>
            </view>
          </view>
        </view>

        <text v-if="!shopList.length && !eventList.length" class="empty-text">暂无来源数据。</text>
      </view>
    </view>

    <view v-if="card" class="section-card enchant-section">
      <text class="section-title">附魔变体</text>
      <view v-if="enchantList.length" class="enchant-grid">
        <view v-for="enchant in enchantList" :key="enchant.name" class="enchant-item">
          <view class="enchant-head">
            <text class="enchant-name">{{ enchant.nameZh || enchant.name }}</text>
            <text v-if="enchant.nameZh && enchant.nameZh !== enchant.name" class="enchant-en">{{ enchant.name }}</text>
          </view>
          <text
            v-for="(line, lineIndex) in enchant.lines"
            :key="`${enchant.name}-${lineIndex}`"
            class="enchant-line"
          >{{ line }}</text>
        </view>
      </view>
      <text v-else class="empty-text">暂无附魔变体数据。</text>
    </view>
  </view>
</template>

<script>
import AppBreadcrumb from '../../components/app-breadcrumb.vue'
import { assetUrl } from '../../utils/asset.js'
import { findCard, getHeroMeta, heroListPath } from '../../utils/heroes.js'

export default {
  components: {
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
        {
          label: `${this.hero.nameZh || '角色'}图鉴`,
          path: heroListPath(this.heroKey),
        },
        { label: this.card ? this.card.nameZh : '卡牌详情' },
      ]
    },
    displayTags() {
      if (!this.card) {
        return []
      }
      return this.card.tagsZh && this.card.tagsZh.length ? this.card.tagsZh : this.card.tags || []
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
    shopList() {
      if (!this.card || !this.card.sources) {
        return []
      }
      return this.card.sources.map((source) => ({
        ...source,
        nameZh: source.nameZh || source.name,
        description: source.descriptionZh || source.description || '',
      }))
    },
    eventList() {
      if (!this.card || !this.card.events) {
        return []
      }
      return this.card.events
    },
    enchantList() {
      if (!this.card || !this.card.enchantments) {
        return []
      }
      return this.card.enchantments.map((enchant) => ({
        ...enchant,
        lines: enchant.linesZh && enchant.linesZh.length ? enchant.linesZh : enchant.lines || [],
      }))
    },
  },
  onLoad(options) {
    this.heroKey = decodeURIComponent(options.hero || 'vanessa')
    const slug = decodeURIComponent(options.slug || '')
    this.hero = getHeroMeta(this.heroKey) || {
      key: this.heroKey,
      nameZh: this.heroKey,
      nameEn: this.heroKey,
      titleZh: '',
      count: 0,
    }
    this.card = findCard(this.heroKey, slug)

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

.header-main {
  display: flex;
  flex-direction: column;
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
.source-en,
.enchant-line,
.enchant-en,
.empty-text,
.meta-text,
.section-sub {
  font-size: 24rpx;
  line-height: 1.7;
  color: #bac4da;
}

.source-en,
.enchant-en {
  font-size: 22rpx;
  color: #8f9ab3;
}

.meta-line {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8rpx;
}

.meta-strong {
  font-size: 26rpx;
  font-weight: 600;
  color: #f3cf92;
}

.meta-dot {
  color: #6f7891;
  font-size: 22rpx;
}

.meta-day {
  font-size: 24rpx;
  color: #f5d39a;
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

.chip.day {
  background: rgba(245, 188, 89, 0.14);
  color: #f5d39a;
}

.section-grid {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
  margin-top: 24rpx;
}

.section-card {
  padding: 28rpx;
}

.enchant-section {
  margin-top: 24rpx;
}

.section-title-row {
  display: flex;
  align-items: baseline;
  gap: 12rpx;
  margin-bottom: 18rpx;
}

.section-title {
  display: block;
  margin-bottom: 18rpx;
  font-size: 30rpx;
  font-weight: 700;
}

.section-title-row .section-title {
  margin-bottom: 0;
}

.source-group + .source-group {
  margin-top: 24rpx;
}

.group-title {
  display: block;
  margin-bottom: 14rpx;
  font-size: 24rpx;
  color: #9aa6c0;
}

.effects-list,
.source-list {
  display: flex;
  flex-direction: column;
  gap: 18rpx;
}

.effect-block,
.source-item,
.enchant-item {
  display: flex;
  flex-direction: column;
  gap: 8rpx;
  padding: 20rpx;
  border-radius: 22rpx;
  background: #1c2230;
}

.source-item.event {
  border: 1rpx solid rgba(245, 188, 89, 0.18);
}

.effect-tier,
.source-name,
.enchant-name {
  font-size: 26rpx;
  font-weight: 600;
  color: #f3cf92;
}

.enchant-head {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 10rpx;
}

.enchant-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280rpx, 1fr));
  gap: 16rpx;
}

/* #ifdef H5 */
.cover {
  max-width: 220px;
  height: 160px;
}

@media (min-width: 900px) {
  .header-main {
    flex-direction: row;
    align-items: stretch;
  }

  .cover-wrap {
    width: 240px;
    flex-shrink: 0;
    padding: 24px;
    align-items: flex-start;
  }

  .cover {
    max-width: 100%;
    height: 180px;
  }

  .section-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24rpx;
  }
}
/* #endif */
</style>
