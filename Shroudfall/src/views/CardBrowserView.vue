<script setup>
import { ref, computed, onMounted } from 'vue'
import CardComponent from '@/components/CardComponent.vue'
import { loadCards, getCardsSync } from '@/services/databaseService'

const cards = ref([])
const searchQuery = ref('')
const filterType = ref('')
const filterAttribute = ref('')
const selectedCard = ref(null)

onMounted(async () => {
  cards.value = await loadCards()
})

const types = computed(() => {
  const set = new Set(getCardsSync().map((c) => c.type))
  return [...set]
})
const attributes = computed(() => {
  const set = new Set(getCardsSync().flatMap((c) => c.attributes || []))
  return [...set]
})

const filteredCards = computed(() => {
  let list = cards.value
  const q = searchQuery.value.trim().toLowerCase()
  if (q) {
    list = list.filter(
      (c) =>
        c.name.toLowerCase().includes(q) ||
        (c.attributes && c.attributes.some((a) => a.toLowerCase().includes(q)))
    )
  }
  if (filterType.value) list = list.filter((c) => c.type === filterType.value)
  if (filterAttribute.value) {
    list = list.filter(
      (c) => c.attributes && c.attributes.includes(filterAttribute.value)
    )
  }
  return list
})

function openDetail(card) {
  selectedCard.value = card
}
function closeDetail() {
  selectedCard.value = null
}
</script>

<template>
  <div class="card-browser-view">
    <h1 class="page-title">Kartenbrowser</h1>

    <div class="toolbar">
      <input
        v-model="searchQuery"
        type="search"
        placeholder="Name oder Attribut suchen…"
        class="search-input"
        aria-label="Suche"
      />
      <div class="filters">
        <select v-model="filterType" class="filter-select" aria-label="Typ">
          <option value="">Alle Typen</option>
          <option v-for="t in types" :key="t" :value="t">{{ t }}</option>
        </select>
        <select v-model="filterAttribute" class="filter-select" aria-label="Attribut">
          <option value="">Alle Attribute</option>
          <option v-for="a in attributes" :key="a" :value="a">{{ a }}</option>
        </select>
      </div>
    </div>

    <div class="gallery">
      <CardComponent
        v-for="card in filteredCards"
        :key="card.id"
        :card="card"
        :compact="false"
        @click="openDetail(card)"
      />
    </div>

    <div v-if="selectedCard" class="modal-overlay" @click.self="closeDetail">
      <div class="modal-card">
        <button type="button" class="modal-close" aria-label="Schließen" @click="closeDetail">
          ×
        </button>
        <CardComponent :card="selectedCard" :compact="false" :show-description="true" />
        <router-link
          :to="{ name: 'army-editor', query: { addCard: selectedCard.id } }"
          class="btn btn-primary"
        >
          Zur Armee hinzufügen
        </router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card-browser-view {
  padding: 1rem;
  max-width: 900px;
  margin: 0 auto;
}
.page-title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}
.toolbar {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}
.search-input {
  width: 100%;
  padding: 0.6rem 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  font-size: 1rem;
  background: var(--color-background);
  color: var(--color-text);
}
.filters {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}
.filter-select {
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  background: var(--color-background);
  color: var(--color-text);
  min-width: 120px;
}
.gallery {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 1rem;
}
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  padding: 1rem;
}
.modal-card {
  background: var(--color-background);
  border-radius: 12px;
  padding: 1.5rem;
  max-width: 360px;
  width: 100%;
  position: relative;
}
.modal-close {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  width: 2rem;
  height: 2rem;
  border: none;
  background: transparent;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--color-text);
  line-height: 1;
}
.btn {
  display: inline-block;
  margin-top: 1rem;
  padding: 0.6rem 1rem;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 500;
  text-align: center;
}
.btn-primary {
  background: var(--color-accent);
  color: #fff;
  border: none;
  width: 100%;
}
.btn-primary:hover {
  opacity: 0.9;
}
</style>
