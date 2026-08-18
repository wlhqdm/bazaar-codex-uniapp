# 大巴扎中文图鉴

The Bazaar（大巴扎）中文图鉴，基于 uni-app Vue3。一期已收录海盗**瓦内莎** 139 张专属卡牌。

## 在线访问

GitHub Pages：

https://wlhqdm.github.io/bazaar-codex-uniapp/

## 本地开发

```bash
npm install
npm run dev:h5
```

## 打包 H5

```bash
npm run build:h5
```

产物在 `dist/build/h5`。

## 说明

- 中文名参考公开图鉴站标注的官方简体中文
- 效果说明为初版中文，可在 `src/data/vanessa-cards.json` 中继续校对
- 支持 H5 与微信小程序端；H5 使用面包屑导航并限制内容最大宽度
