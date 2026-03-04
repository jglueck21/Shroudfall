<script setup>
/**
 * Update-Pop-up: wird angezeigt, wenn neue Changelog-Daten vorhanden.
 * Max. 1 Sekunde Verzögerung, schließbar, deaktivierbar (über Einstellungen).
 */
import { ref, onMounted } from 'vue'
import { getSettings } from '@/services/storageService'

const visible = ref(false)
const dismissed = ref(false)

onMounted(() => {
  const settings = getSettings()
  if (!settings.updatePopupEnabled || dismissed.value) return
  // Prüfen: Gibt es neue Changelog-Daten? (Platzhalter: immer aus nach 1s Verzögerung)
  const hasNewChangelog = false // TODO: echte Prüfung (z. B. lokale Version vs. Changelog)
  if (hasNewChangelog) {
    const t = setTimeout(() => {
      visible.value = true
    }, 1000)
    return () => clearTimeout(t)
  }
})

function close() {
  visible.value = false
  dismissed.value = true
}
</script>

<template>
  <div v-if="visible" class="update-popup-overlay">
    <div class="update-popup">
      <h3>Update verfügbar</h3>
      <p>Es gibt eine neue Version von Shroudfall mit Änderungen.</p>
      <button type="button" class="btn btn-close" @click="close">Schließen</button>
    </div>
  </div>
</template>

<style scoped>
.update-popup-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 200;
  padding: 1rem;
}
.update-popup {
  background: var(--color-background);
  border-radius: 12px;
  padding: 1.5rem;
  max-width: 360px;
  width: 100%;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}
.update-popup h3 {
  margin-bottom: 0.5rem;
  font-size: 1.25rem;
}
.update-popup p {
  margin-bottom: 1rem;
  color: var(--color-text);
}
.btn {
  padding: 0.6rem 1rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  border: none;
}
.btn-close {
  background: var(--color-accent);
  color: #fff;
  width: 100%;
}
</style>
