<template>
  <!-- #ifdef H5 -->
  <view class="breadcrumb" v-if="items && items.length > 1">
    <text
      v-for="(item, index) in items"
      :key="`${item.label}-${index}`"
      class="crumb"
    >
      <text
        v-if="item.path && index < items.length - 1"
        class="link"
        @click="go(item.path)"
      >{{ item.label }}</text>
      <text v-else class="current">{{ item.label }}</text>
      <text v-if="index < items.length - 1" class="sep">/</text>
    </text>
  </view>
  <!-- #endif -->
</template>

<script>
export default {
  name: 'AppBreadcrumb',
  props: {
    items: {
      type: Array,
      default() {
        return []
      },
    },
  },
  methods: {
    go(path) {
      if (path === '/pages/index/index') {
        uni.reLaunch({ url: path })
        return
      }
      uni.redirectTo({ url: path })
    },
  },
}
</script>

<style scoped>
.breadcrumb {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  margin-bottom: 20rpx;
  font-size: 24rpx;
  color: #8f9ab3;
}

.crumb {
  display: flex;
  align-items: center;
}

.link {
  color: #d5ae72;
}

.sep {
  margin: 0 12rpx;
  color: #6f7891;
}

.current {
  color: #f8f4e9;
}
</style>
