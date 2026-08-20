<template>
  <view class="page">
    <text class="tip">正在跳转到凡妮莎图鉴…</text>
  </view>
</template>

<script>
import { heroListPath } from '../../utils/heroes.js'

export default {
  onLoad() {
    uni.redirectTo({
      url: heroListPath('vanessa'),
    })
  },
}
</script>

<style>
.tip {
  display: block;
  padding: 40rpx 32rpx;
  color: #a9b4cb;
  font-size: 26rpx;
}
</style>
