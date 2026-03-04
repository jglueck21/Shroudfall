<script setup>
import { ref } from 'vue'

const openId = ref(null)
const faqs = [
  {
    id: 1,
    question: 'Wie speichere ich eine Armee?',
    answer:
      'Im Armeelisten-Editor alle gewünschten Einheiten hinzufügen und dann auf "Speichern" tippen. Die Liste wird lokal auf deinem Gerät gespeichert.',
  },
  {
    id: 2,
    question: 'Warum brauche ich einen Essence Weaver?',
    answer:
      'Laut Regelwerk ist eine Armee nur gültig, wenn mindestens ein "Essence Weaver" enthalten ist. Ohne ihn wird ein Warnhinweis angezeigt.',
  },
  {
    id: 3,
    question: 'Kann ich mehrere Armeelisten haben?',
    answer:
      'Ja. Du kannst mehrere Listen anlegen und zwischen ihnen wechseln. Die zuletzt bearbeitete Liste erscheint auf der Startseite als Schnellzugriff.',
  },
  {
    id: 4,
    question: 'Wo wird das Regelbuch-PDF gespeichert?',
    answer:
      'Lege die PDF-Datei im Ordner "public" deines Projekts ab. Den Dateinamen kannst du in den Einstellungen anpassen.',
  },
  {
    id: 5,
    question: 'Funktioniert die App offline?',
    answer:
      'Ja. Alle Daten werden lokal gespeichert, es gibt keine Anmeldung und keine Cloud. Die App läuft vollständig offline.',
  },
]

function toggle(id) {
  openId.value = openId.value === id ? null : id
}
</script>

<template>
  <div class="faq-view">
    <h1 class="page-title">FAQ</h1>
    <p class="intro">Häufig gestellte Fragen zu Shroudfall.</p>

    <div class="faq-list">
      <div
        v-for="faq in faqs"
        :key="faq.id"
        class="faq-item"
        :class="{ open: openId === faq.id }"
      >
        <button
          type="button"
          class="faq-question"
          :aria-expanded="openId === faq.id"
          @click="toggle(faq.id)"
        >
          {{ faq.question }}
          <span class="faq-icon">{{ openId === faq.id ? '−' : '+' }}</span>
        </button>
        <div v-show="openId === faq.id" class="faq-answer">
          {{ faq.answer }}
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.faq-view {
  padding: 1rem;
  max-width: 560px;
  margin: 0 auto;
}
.page-title {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}
.intro {
  margin-bottom: 1.5rem;
  color: var(--color-text);
}
.faq-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.faq-item {
  border: 1px solid var(--color-border);
  border-radius: 8px;
  overflow: hidden;
  background: var(--color-background-mute);
}
.faq-question {
  width: 100%;
  padding: 1rem 1.25rem;
  text-align: left;
  font-size: 1rem;
  font-weight: 500;
  color: var(--color-heading);
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
}
.faq-icon {
  font-size: 1.25rem;
  flex-shrink: 0;
}
.faq-answer {
  padding: 0 1.25rem 1rem;
  color: var(--color-text);
  line-height: 1.5;
  border-top: 1px solid var(--color-border);
}
</style>
