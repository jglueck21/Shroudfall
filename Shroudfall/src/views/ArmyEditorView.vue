<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import ArmyList from '@/components/ArmyList.vue'
import CardComponent from '@/components/CardComponent.vue'
import {
  getArmyLists,
  saveArmyLists,
  getSettings,
  setLastEditedArmyId,
} from '@/services/storageService'
import { loadCards, getCardsSync } from '@/services/databaseService'
import { getArmyValidationMessage, isArmyValid } from '@/services/validationService'

const route = useRoute()
const armyLists = ref([])
const currentListId = ref(null)
const budgetMax = ref(200)
const cards = ref([])
const showCardPicker = ref(false)
const searchCard = ref('')
const saveNotice = ref('')

onMounted(async () => {
  const settings = getSettings()
  budgetMax.value = settings.defaultBudget ?? 200
  armyLists.value = getArmyLists()
  cards.value = await loadCards()

  const listId = route.query.listId
  if (listId) {
    const list = armyLists.value.find((l) => l.id === listId)
    if (list) {
      currentListId.value = listId
      budgetMax.value = list.budgetMax ?? budgetMax.value
    }
  }
  if (!currentListId.value) {
    if (armyLists.value.length) currentListId.value = armyLists.value[0].id
    else createNewList()
  }
  if (currentList.value) budgetMax.value = currentList.value.budgetMax ?? budgetMax.value

  const addCardId = route.query.addCard
  if (addCardId) {
    const card = getCardsSync().find((c) => c.id === addCardId)
    if (card) addUnit(card)
  }
})

const currentList = computed(() =>
  armyLists.value.find((l) => l.id === currentListId.value)
)
const currentUnits = computed(() => currentList.value?.units ?? [])
const totalCost = computed(() =>
  currentUnits.value.reduce((sum, u) => sum + (u.cost ?? u.card?.cost ?? 0), 0)
)
const remainingPoints = computed(() => Math.max(0, budgetMax.value - totalCost.value))
const canAdd = computed(() => remainingPoints.value > 0)
const validationWarning = computed(() => getArmyValidationMessage(currentUnits.value))
const armyValid = computed(() => isArmyValid(currentUnits.value))

watch(currentListId, (id) => {
  const list = armyLists.value.find((l) => l.id === id)
  if (list) budgetMax.value = list.budgetMax ?? budgetMax.value
})

const filteredCardsForPicker = computed(() => {
  let list = cards.value
  const q = searchCard.value.trim().toLowerCase()
  if (q) list = list.filter((c) => c.name.toLowerCase().includes(q))
  return list
})

function createNewList() {
  const name = prompt('Name der neuen Armeeliste:', 'Neue Armee')
  if (name == null) return
  const id = 'list_' + Date.now()
  armyLists.value.push({
    id,
    name: name.trim() || 'Neue Armee',
    budgetMax: budgetMax.value,
    units: [],
  })
  currentListId.value = id
  save()
}

function addUnit(card) {
  const list = currentList.value
  if (!list || !canAdd.value) return
  const cost = card.cost ?? 0
  if (totalCost.value + cost > budgetMax.value) return
  list.units = list.units || []
  list.units.push({ card, name: card.name, cost })
  save()
}

function removeUnit(index) {
  const list = currentList.value
  if (!list?.units) return
  list.units.splice(index, 1)
  save()
}

function renameCurrentList() {
  const list = currentList.value
  if (!list) return
  const next = prompt('Neuer Name:', list.name)
  if (next == null) return
  const trimmed = next.trim()
  if (!trimmed) return
  list.name = trimmed
  save()
}

function deleteCurrentList() {
  const list = currentList.value
  if (!list) return
  const ok = confirm(`Armeeliste „${list.name}“ wirklich löschen?`)
  if (!ok) return
  const idx = armyLists.value.findIndex((l) => l.id === list.id)
  if (idx >= 0) armyLists.value.splice(idx, 1)
  currentListId.value = armyLists.value[0]?.id ?? null
  if (!currentListId.value) createNewList()
  save()
}

function changeBudget() {
  const v = prompt('Neues Budget (Punkte):', String(budgetMax.value))
  const n = parseInt(v, 10)
  if (!Number.isNaN(n) && n > 0) {
    budgetMax.value = n
    if (currentList.value) currentList.value.budgetMax = n
    save()
  }
}

function save() {
  if (currentList.value) currentList.value.budgetMax = budgetMax.value
  const ok = saveArmyLists(armyLists.value)
  if (currentListId.value) setLastEditedArmyId(currentListId.value)
  saveNotice.value = ok ? 'Gespeichert.' : 'Speichern fehlgeschlagen (LocalStorage blockiert?)'
  window.clearTimeout(saveNotice._t)
  saveNotice._t = window.setTimeout(() => (saveNotice.value = ''), 1500)
}

function exportList() {
  const list = currentList.value
  if (!list) return
  const lines = [
    `Armee: ${list.name}`,
    `Budget: ${budgetMax.value} | Verbraucht: ${totalCost.value} | Verbleibend: ${remainingPoints.value}`,
    '',
    ...(list.units || []).map((u) => `- ${u.name} (${u.cost} Punkte)`),
  ]
  const blob = new Blob([lines.join('\n')], { type: 'text/plain;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `shroudfall-army-${list.name.replace(/\s/g, '-')}.txt`
  a.click()
  URL.revokeObjectURL(url)
}

function openCardPicker() {
  showCardPicker.value = true
  searchCard.value = ''
}
function closeCardPicker() {
  showCardPicker.value = false
}
</script>

<template>
  <div class="army-editor-view">
    <h1 class="page-title">Armeelisten-Editor</h1>

    <section class="section list-section">
      <h2>Armeeliste</h2>
      <div class="list-row">
        <select v-model="currentListId" class="list-select" aria-label="Armeeliste auswählen">
          <option v-for="l in armyLists" :key="l.id" :value="l.id">{{ l.name }}</option>
        </select>
        <button type="button" class="btn btn-secondary" @click="createNewList">Neu</button>
        <button type="button" class="btn btn-secondary" :disabled="!currentList" @click="renameCurrentList">
          Umbenennen
        </button>
        <button type="button" class="btn btn-secondary" :disabled="!currentList" @click="deleteCurrentList">
          Löschen
        </button>
      </div>
      <p v-if="saveNotice" class="save-notice">{{ saveNotice }}</p>
    </section>

    <section class="section budget-section">
      <h2>Budget</h2>
      <p class="budget-line">
        Gesamt: <strong>{{ budgetMax }}</strong> · Verbleibend: <strong>{{ remainingPoints }}</strong>
      </p>
      <button type="button" class="btn btn-secondary" @click="changeBudget">Budget ändern</button>
    </section>

    <section class="section army-section">
      <h2>Aktuelle Armee</h2>
      <ArmyList
        :units="currentUnits"
        :valid="armyValid"
        :validation-warning="validationWarning"
        @remove="removeUnit"
      />
    </section>

    <section class="section picker-section">
      <h2>Karten</h2>
      <button type="button" class="btn btn-primary" :disabled="!canAdd" @click="openCardPicker">
        Truppe hinzufügen
      </button>
    </section>

    <div class="actions">
      <button type="button" class="btn btn-primary" @click="save">Speichern</button>
      <button type="button" class="btn btn-secondary" @click="exportList">Exportieren (.txt)</button>
    </div>

    <div v-if="showCardPicker" class="modal-overlay" @click.self="closeCardPicker">
      <div class="modal-picker">
        <div class="picker-header">
          <input
            v-model="searchCard"
            type="search"
            placeholder="Karte suchen…"
            class="search-input"
          />
          <button type="button" class="modal-close" @click="closeCardPicker">×</button>
        </div>
        <div class="picker-gallery">
          <div
            v-for="card in filteredCardsForPicker"
            :key="card.id"
            class="picker-card-wrap"
            @click="addUnit(card); closeCardPicker()"
          >
            <CardComponent :card="card" :compact="true" />
            <span class="picker-cost">{{ card.cost }} Pkt</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.army-editor-view {
  padding: 1rem;
  max-width: 560px;
  margin: 0 auto;
}
.page-title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}
.section {
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: var(--color-background-mute);
  border-radius: 8px;
}
.section h2 {
  font-size: 1rem;
  margin-bottom: 0.5rem;
}
.list-row {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  align-items: center;
}
.list-select {
  flex: 1;
  min-width: 180px;
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  background: var(--color-background);
  color: var(--color-text);
}
.save-notice {
  margin-top: 0.5rem;
  font-size: 0.9rem;
  opacity: 0.85;
}
.budget-line {
  margin-bottom: 0.5rem;
}
.actions {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}
.btn {
  padding: 0.6rem 1rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  border: none;
}
.btn-primary {
  background: var(--color-accent);
  color: #fff;
}
.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.btn-secondary {
  background: var(--color-border);
  color: var(--color-text);
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
.modal-picker {
  background: var(--color-background);
  border-radius: 12px;
  padding: 1rem;
  max-width: 400px;
  width: 100%;
  max-height: 80vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
.picker-header {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}
.picker-header .search-input {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid var(--color-border);
  border-radius: 6px;
}
.modal-close {
  width: 2rem;
  height: 2rem;
  border: none;
  background: transparent;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--color-text);
}
.picker-gallery {
  overflow-y: auto;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.5rem;
}
.picker-card-wrap {
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 6px;
  background: var(--color-background-mute);
}
.picker-card-wrap:hover {
  background: var(--color-border-hover);
}
.picker-cost {
  font-size: 0.75rem;
  display: block;
  text-align: center;
  margin-top: 0.25rem;
}
</style>
