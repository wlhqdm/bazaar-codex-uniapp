<script>
export default {
  onLaunch: function () {
    console.log('App Launch')
  },
  onShow: function () {
    console.log('App Show')
  },
  onHide: function () {
    console.log('App Hide')
  },
}
</script>

<style>
/*每个页面公共css */
page {
  background: #0f1118;
  color: #f8f4e9;
  font-family: Arial, "PingFang SC", "Microsoft YaHei", sans-serif;
}

view,
text,
input,
button {
  box-sizing: border-box;
}

.page {
  min-height: 100vh;
  padding: 24rpx;
  background: #0f1118;
  color: #f8f4e9;
}

/* #ifdef H5 */
.page {
  max-width: 1100px;
  margin: 0 auto;
  padding: 24px 20px 48px;
}
/* #endif */
</style>
