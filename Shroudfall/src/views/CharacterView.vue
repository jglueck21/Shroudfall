<script setup>
import { ref, onMounted } from 'vue'
import CharacterCard from '@/components/CharacterCard.vue'
import { getCharacters, saveCharacters } from '@/services/storageService'

const characters = ref([])
const selectedId = ref(null)
const form = ref({
  name: '',
  attributes: [],
  icon: '',
})
const attributeInput = ref('')
const availableIcons = ['warrior', 'mage', 'rogue', 'healer', 'ranger']

onMounted(() => {
  characters.value = getCharacters()
})

const selected = ref(null)
function selectChar(c) {
  selectedId.value = c?.id ?? null
  if (c) {
    form.value = {
      name: c.name,
      attributes: [...(c.attributes || [])],
      icon: c.icon || '',
    }
  } else {
    form.value = { name: '', attributes: [], icon: '' }
  }
}

function addAttribute() {
  const v = attributeInput.value.trim()
  if (v && !form.value.attributes.includes(v)) {
    form.value.attributes.push(v)
    attributeInput.value = ''
  }
}
function removeAttribute(idx) {
  form.value.attributes.splice(idx, 1)
}

function saveCharacter() {
  const name = form.value.name.trim()
  if (!name) return
  const payload = {
    id: selectedId.value || 'char_' + Date.now(),
    name,
    attributes: [...form.value.attributes],
    icon: form.value.icon,
  }
  const idx = characters.value.findIndex((c) => c.id === payload.id)
  if (idx >= 0) characters.value[idx] = payload
  else characters.value.push(payload)
  saveCharacters(characters.value)
  selectChar(null)
}

function deleteCharacter(id) {
  characters.value = characters.value.filter((c) => c.id !== id)
  saveCharacters(characters.value)
  if (selectedId.value === id) selectChar(null)
}
</script>

<template>
  <div class="character-view">
    <h1 class="page-title">Charaktererstellung</h1>

    <section class="form-section">
      <h2>Neuer Charakter / Bearbeiten</h2>
      <div class="field">
        <label for="char-name">Name</label>
        <input id="char-name" v-model="form.name" type="text" placeholder="Name" class="input" />
      </div>
      <div class="field">
        <label>Attribute</label>
        <div class="attribute-row">
          <input
            v-model="attributeInput"
            type="text"
            placeholder="Attribut hinzufügen"
            class="input"
            @keydown.enter.prevent="addAttribute"
          />
          <button type="button" class="btn btn-small" @click="addAttribute">+</button>
        </div>
        <ul v-if="form.attributes.length" class="attribute-list">
          <li v-for="(a, i) in form.attributes" :key="i">
            {{ a }}
            <button type="button" class="btn-remove" @click="removeAttribute(i)">×</button>
          </li>
        </ul>
      </div>
      <div class="field">
        <label>Symbol / Icon</label>
        <div class="icon-options">
          <button
            v-for="icon in availableIcons"
            :key="icon"
            type="button"
            class="icon-btn"
            :class="{ active: form.icon === icon }"
            @click="form.icon = form.icon === icon ? '' : icon"
          >
            {{ icon }}
          </button>
        </div>
      </div>
      <button type="button" class="btn btn-primary" @click="saveCharacter">Speichern</button>
      <button v-if="selectedId" type="button" class="btn btn-secondary" @click="selectChar(null)">
        Abbrechen
      </button>
    </section>

    <section class="list-section">
      <h2>Gespeicherte Charaktere</h2>
      <div class="character-grid">
        <CharacterCard
          v-for="c in characters"
          :key="c.id"
          :character="c"
          :selected="selectedId === c.id"
          @select="selectChar(c)"
          @delete="deleteCharacter(c.id)"
        />
      </div>
    </section>
  </div>
</template>

<style scoped>
.character-view {
  padding: 1rem;
  max-width: 560px;
  margin: 0 auto;
}
.page-title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}
.form-section,
.list-section {
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: var(--color-background-mute);
  border-radius: 8px;
}
.form-section h2,
.list-section h2 {
  font-size: 1rem;
  margin-bottom: 0.75rem;
}
.field {
  margin-bottom: 1rem;
}
.field label {
  display: block;
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
}
.input {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  background: var(--color-background);
  color: var(--color-text);
}
.attribute-row {
  display: flex;
  gap: 0.5rem;
}
.attribute-row .input {
  flex: 1;
}
.attribute-list {
  margin-top: 0.5rem;
  padding-left: 1.25rem;
}
.attribute-list li {
  margin-bottom: 0.25rem;
}
.btn-remove {
  margin-left: 0.5rem;
  background: none;
  border: none;
  color: var(--color-text);
  cursor: pointer;
  opacity: 0.8;
}
.icon-options {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}
.icon-btn {
  padding: 0.4rem 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  background: var(--color-background);
  color: var(--color-text);
  cursor: pointer;
  font-size: 0.85rem;
}
.icon-btn.active {
  background: var(--color-accent);
  color: #fff;
  border-color: var(--color-accent);
}
.btn {
  padding: 0.6rem 1rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  margin-right: 0.5rem;
  margin-top: 0.5rem;
}
.btn-small {
  padding: 0.5rem 0.75rem;
}
.btn-primary {
  background: var(--color-accent);
  color: #fff;
}
.btn-secondary {
  background: var(--color-border);
  color: var(--color-text);
}
.character-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 1rem;
}
</style>
