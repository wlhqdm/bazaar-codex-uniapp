/**
 * 兼容 GitHub Pages 子路径与小程序本地静态资源。
 * H5 使用 Vite BASE_URL；小程序仍走 /static。
 */
export function assetUrl(path = '') {
  const clean = String(path || '').replace(/^\//, '')
  // #ifdef H5
  const base = import.meta.env.BASE_URL || '/'
  return `${base}${clean}`
  // #endif
  // #ifndef H5
  return `/${clean}`
  // #endif
}
