import heroesRegistry from '../data/heroes.json'
import vanessaData from '../data/vanessa-cards.json'
import dooleyData from '../data/dooley-cards.json'
import pygmalienData from '../data/pygmalien-cards.json'
import makData from '../data/mak-cards.json'
import julesData from '../data/jules-cards.json'
import stelleData from '../data/stelle-cards.json'
import karnokData from '../data/karnok-cards.json'
import commonData from '../data/common-cards.json'

const DATA_BY_KEY = {
  vanessa: vanessaData,
  dooley: dooleyData,
  pygmalien: pygmalienData,
  mak: makData,
  jules: julesData,
  stelle: stelleData,
  karnok: karnokData,
  common: commonData,
}

export function listHeroes() {
  return (heroesRegistry.heroes || []).map((meta) => {
    const payload = DATA_BY_KEY[meta.key]
    const count = payload && payload.cards ? payload.cards.length : meta.count || meta.expectedCount || 0
    return {
      ...meta,
      count,
    }
  })
}

export function getHeroPayload(key) {
  return DATA_BY_KEY[key] || null
}

export function getHeroMeta(key) {
  const payload = getHeroPayload(key)
  if (payload && payload.hero) {
    return {
      ...payload.hero,
      count: (payload.cards || []).length,
    }
  }
  const fromRegistry = (heroesRegistry.heroes || []).find((item) => item.key === key)
  return fromRegistry || null
}

export function getHeroCards(key) {
  const payload = getHeroPayload(key)
  return payload && payload.cards ? payload.cards : []
}

export function findCard(heroKey, slug) {
  return getHeroCards(heroKey).find((card) => card.slug === slug) || null
}

export function heroListPath(key) {
  return `/pages/hero/index?key=${encodeURIComponent(key)}`
}

export function cardDetailPath(heroKey, slug) {
  return `/pages/card-detail/index?hero=${encodeURIComponent(heroKey)}&slug=${encodeURIComponent(slug)}`
}
