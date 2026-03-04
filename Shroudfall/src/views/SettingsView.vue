<script setup>
import { ref, onMounted } from 'vue'
import { getSettings, saveSettings, clearAllData } from '@/services/storageService'

const settings = ref({
  updatePopupEnabled: true,
  defaultBudget: 200,
  rulebookVersion: '1.0',
  rulebookFilename: 'regelbuch.pdf',
})

onMounted(() => {
  settings.value = { ...getSettings() }
})

function save() {
  saveSettings(settings.value)
  alert('Einstellungen gespeichert.')
}

function confirmClear() {
  if (confirm('Wirklich alle gespeicherten Daten löschen? Armeen, Charaktere und Einstellungen gehen verloren.')) {
    clearAllData()
    settings.value = getSettings()
    alert('Daten gelöscht.')
  }
}
</script>

<template>
  <div class="settings-view">
    <h1 class="page-title">Einstellungen</h1>

    <section class="settings-section">
      <div class="setting-row">
        <label for="popup">Update-Pop-up bei neuem Changelog anzeigen</label>
        <input
          id="popup"
          v-model="settings.updatePopupEnabled"
          type="checkbox"
          @change="save"
        />
      </div>
      <div class="setting-row">
        <label for="budget">Standard-Budget (Punkte)</label>
        <input
          id="budget"
          v-model.number="settings.defaultBudget"
          type="number"
          min="1"
          max="999"
          class="input-narrow"
          @change="save"
        />
      </div>
      <div class="setting-row">
        <label>Regelbuch-Version (nur Anzeige)</label>
        <span class="value">{{ settings.rulebookVersion }}</span>
      </div>
      <div class="setting-row">
        <label for="filename">Regelbuch-Dateiname (z. B. regelbuch.pdf)</label>
        <input
          id="filename"
          v-model="settings.rulebookFilename"
          type="text"
          class="input"
          placeholder="regelbuch.pdf"
          @change="save"
        />
      </div>
    </section>

    <section class="danger-section">
      <h2>Daten</h2>
      <button type="button" class="btn btn-danger" @click="confirmClear">
        Gespeicherte Daten löschen
      </button>
    </section>
  </div>
</template>

<style scoped>
.settings-view {
  padding: 1rem;
  max-width: 480px;
  margin: 0 auto;
}
.page-title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}
.settings-section,
.danger-section {
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: var(--color-background-mute);
  border-radius: 8px;
}
.settings-section h2,
.danger-section h2 {
  font-size: 1rem;
  margin-bottom: 0.75rem;
}
.setting-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}
.setting-row:last-child {
  margin-bottom: 0;
}
.setting-row label {
  flex: 1;
  min-width: 180px;
  font-size: 0.95rem;
}
.input {
  width: 100%;
  max-width: 240px;
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  background: var(--color-background);
  color: var(--color-text);
}
.input-narrow {
  width: 5rem;
  padding: 0.5rem;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  background: var(--color-background);
  color: var(--color-text);
}
.value {
  color: var(--color-text);
}
.btn {
  padding: 0.6rem 1rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  border: none;
}
.btn-danger {
  background: #c0392b;
  color: #fff;
}
.btn-danger:hover {
  background: #a93226;
}
</style>
