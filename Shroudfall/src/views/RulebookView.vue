<script setup>
import { ref, computed, onMounted } from 'vue'
import { getSettings } from '@/services/storageService'

const settings = ref({})
const pdfUrl = ref('')
const searchQuery = ref('')
const currentPage = ref(1)
const totalPages = ref(1)
const pdfRef = ref(null)

onMounted(() => {
  settings.value = getSettings()
  const filename = settings.value.rulebookFilename || 'regelbuch.pdf'
  // Vite: Dateien in public/ sind unter / verfügbar
  pdfUrl.value = '/' + filename.replace(/^\//, '')
})

const displayUrl = computed(() => {
  if (!pdfUrl.value) return ''
  return pdfUrl.value
})
</script>

<template>
  <div class="rulebook-view">
    <h1 class="page-title">Regelbuch</h1>
    <p class="version-info" v-if="settings.rulebookVersion">
      Version: {{ settings.rulebookVersion }}
    </p>

    <div class="toolbar">
      <input
        v-model="searchQuery"
        type="search"
        placeholder="Im Regelbuch suchen…"
        class="search-input"
        aria-label="Suchen"
      />
      <p class="page-info">Seite {{ currentPage }} von {{ totalPages }}</p>
    </div>

    <div class="pdf-container">
      <iframe
        v-if="displayUrl"
        ref="pdfRef"
        :src="displayUrl + '#page=' + currentPage"
        class="pdf-iframe"
        title="Regelbuch PDF"
      />
      <div v-else class="pdf-placeholder">
        <p>PDF nicht geladen. Bitte lege <code>regelbuch.pdf</code> in <code>public/</code>.</p>
        <p>Dateiname ist in den Einstellungen konfigurierbar.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.rulebook-view {
  padding: 1rem;
  max-width: 900px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  min-height: 60vh;
}
.page-title {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}
.version-info {
  font-size: 0.9rem;
  color: var(--color-text);
  opacity: 0.8;
  margin-bottom: 1rem;
}
.toolbar {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
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
.page-info {
  font-size: 0.9rem;
}
.pdf-container {
  flex: 1;
  min-height: 400px;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  overflow: hidden;
  background: var(--color-background-mute);
}
.pdf-iframe {
  width: 100%;
  height: 100%;
  min-height: 500px;
  border: none;
}
.pdf-placeholder {
  padding: 2rem;
  text-align: center;
  color: var(--color-text);
}
.pdf-placeholder code {
  background: var(--color-background);
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
}
</style>
