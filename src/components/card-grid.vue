<template>
  <view class="card-grid">
    <view
      v-for="card in cards"
      :key="card.id"
      class="card-item"
      @click="$emit('select', card)"
    >
      <view class="cover-wrap">
        <image class="card-cover" :src="coverOf(card)" mode="aspectFit"></image>
        <text class="badge tier" :class="'tier-' + (card.tier || '')">{{ card.tierZh }}</text>
        <text v-if="card.dayLabel" class="badge day" :class="{ community: card.dayStatus === 'community' }">
          {{ card.dayLabel }}
        </text>
      </view>
      <view class="card-body">
        <text class="card-name">{{ card.nameZh }}</text>
        <text class="card-name-en">{{ card.nameEn }}</text>
        <view class="card-meta">
          <text v-if="card.sizeZh" class="card-chip">{{ card.sizeZh }}</text>
          <text v-for="tag in displayTags(card)" :key="tag" class="card-chip">{{ tag }}</text>
          <text v-if="card.imageStatus === 'placeholder'" class="card-chip warn">待补封面</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import { assetUrl } from '../utils/asset.js'

export default {
  name: 'CardGrid',
  props: {
    cards: {
      type: Array,
      default() {
        return []
      },
    },
  },
  emits: ['select'],
  methods: {
    coverOf(card) {
      return assetUrl(card.image)
    },
    displayTags(card) {
      const tags = card.tagsZh && card.tagsZh.length ? card.tagsZh : card.tags || []
      return tags
    },
  },
}
</script>

<style scoped>
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220rpx, 1fr));
  gap: 20rpx;
}

.card-item {
  overflow: hidden;
  border-radius: 24rpx;
  background: #1a1d29;
  border: 1rpx solid rgba(255, 255, 255, 0.08);
}

.cover-wrap {
  position: relative;
  background: #2b3245;
}

.card-cover {
  width: 100%;
  height: 250rpx;
  display: block;
}

.badge {
  position: absolute;
  top: 12rpx;
  padding: 6rpx 12rpx;
  border-radius: 999rpx;
  background: rgba(0, 0, 0, 0.62);
  font-size: 18rpx;
  line-height: 1.2;
}

.badge.tier {
  left: 12rpx;
  color: #f8d08f;
}

.badge.tier.tier-Bronze {
  color: #d4a574;
}

.badge.tier.tier-Silver {
  color: #d7dde8;
}

.badge.tier.tier-Gold {
  color: #f5d39a;
}

.badge.tier.tier-Diamond {
  color: #9fd8ff;
}

.badge.day {
  right: 12rpx;
  color: #e8eefc;
}

.badge.day.community {
  background: rgba(245, 188, 89, 0.88);
  color: #1a1408;
}

.card-body {
  display: flex;
  flex-direction: column;
  gap: 10rpx;
  padding: 18rpx;
}

.card-name {
  font-size: 28rpx;
  color: #f8f4e9;
  font-weight: 600;
  line-height: 1.35;
}

.card-name-en {
  font-size: 22rpx;
  color: #8f9ab3;
  line-height: 1.35;
}

.card-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 10rpx;
}

.card-chip {
  padding: 6rpx 12rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.08);
  color: #d7dded;
  font-size: 20rpx;
}

.warn {
  color: #ffcf88;
}
</style>
