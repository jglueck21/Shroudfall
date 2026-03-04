<script setup>
import { RouterLink } from 'vue-router'
import { getLastEditedArmyId } from '@/services/storageService'

const lastArmyId = getLastEditedArmyId()
</script>

<template>
  <div class="home-view">
    <header class="home-header">
      <h1 class="app-title">Shroudfall</h1>
    </header>

    <nav class="nav-grid">
      <RouterLink to="/cards" class="nav-card">Kartenbrowser</RouterLink>
      <RouterLink to="/army" class="nav-card">Armeelisten</RouterLink>
      <RouterLink to="/characters" class="nav-card">Charaktere</RouterLink>
      <RouterLink to="/rulebook" class="nav-card">Regelbuch</RouterLink>
      <RouterLink to="/faq" class="nav-card">FAQ</RouterLink>
      <RouterLink to="/settings" class="nav-card">Einstellungen</RouterLink>
    </nav>

    <section v-if="lastArmyId" class="quick-access">
      <h2>Schnellzugriff</h2>
      <RouterLink :to="{ name: 'army-editor', query: { listId: lastArmyId } }" class="quick-link">
        Zuletzt bearbeitete Armeeliste öffnen
      </RouterLink>
    </section>
  </div>
</template>

<style scoped>
.home-view {
  padding: 1rem;
  max-width: 480px;
  margin: 0 auto;
}
.home-header {
  text-align: center;
  margin-bottom: 2rem;
}
.app-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--color-heading);
}
.nav-grid {
  display: grid;
  gap: 0.75rem;
}
.nav-card {
  display: block;
  padding: 1rem 1.25rem;
  background: var(--color-background-mute);
  border-radius: 8px;
  color: var(--color-heading);
  text-decoration: none;
  font-weight: 500;
  transition: background 0.2s;
}
.nav-card:hover {
  background: var(--color-border-hover);
}
.quick-access {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--color-border);
}
.quick-access h2 {
  font-size: 0.95rem;
  margin-bottom: 0.5rem;
  color: var(--color-text);
}
.quick-link {
  color: var(--color-accent);
  text-decoration: none;
  font-size: 0.9rem;
}
.quick-link:hover {
  text-decoration: underline;
}
</style>
