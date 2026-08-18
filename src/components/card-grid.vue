<template>
  <view class="card-grid">
    <view
      v-for="card in cards"
      :key="card.id"
      class="card-item"
      @click="$emit('select', card)"
    >
      <image class="card-cover" :src="coverOf(card)" mode="aspectFit"></image>
      <view class="card-body">
        <text class="card-name">{{ card.nameZh }}</text>
        <text class="card-name-en">{{ card.nameEn }}</text>
        <view class="card-meta">
          <text class="card-chip tier">{{ card.tierZh }}</text>
          <text class="card-chip">{{ card.sizeZh }}</text>
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

.card-cover {
  width: 100%;
  height: 250rpx;
  background: #2b3245;
  display: block;
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

.tier {
  color: #f8d08f;
}

.warn {
  color: #ffcf88;
}
</style>
