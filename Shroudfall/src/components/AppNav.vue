<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'

const menuOpen = ref(false)
</script>

<template>
  <nav class="app-nav">
    <button
      type="button"
      class="nav-toggle"
      aria-label="Menü"
      aria-expanded="menuOpen"
      @click="menuOpen = !menuOpen"
    >
      ☰
    </button>
    <div class="nav-links" :class="{ open: menuOpen }">
      <RouterLink to="/" @click="menuOpen = false">Start</RouterLink>
      <RouterLink to="/cards" @click="menuOpen = false">Karten</RouterLink>
      <RouterLink to="/army" @click="menuOpen = false">Armee</RouterLink>
      <RouterLink to="/characters" @click="menuOpen = false">Charaktere</RouterLink>
      <RouterLink to="/rulebook" @click="menuOpen = false">Regelbuch</RouterLink>
      <RouterLink to="/faq" @click="menuOpen = false">FAQ</RouterLink>
      <RouterLink to="/settings" @click="menuOpen = false">Einstellungen</RouterLink>
    </div>
  </nav>
</template>

<style scoped>
.app-nav {
  position: relative;
}
.nav-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  padding: 0;
  border: none;
  background: transparent;
  font-size: 1.25rem;
  color: var(--color-heading);
  cursor: pointer;
  border-radius: 6px;
}
.nav-toggle:hover {
  background: var(--color-border);
}
.nav-links {
  display: none;
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 0.25rem;
  background: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  min-width: 160px;
  padding: 0.5rem;
  z-index: 50;
}
.nav-links.open {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}
.nav-links a {
  display: block;
  padding: 0.5rem 0.75rem;
  color: var(--color-heading);
  text-decoration: none;
  border-radius: 4px;
  font-size: 0.95rem;
}
.nav-links a:hover {
  background: var(--color-background-mute);
  color: var(--color-accent);
}
@media (min-width: 768px) {
  .nav-toggle {
    display: none;
  }
  .nav-links {
    display: flex;
    position: static;
    flex-direction: row;
    gap: 0.5rem;
    border: none;
    box-shadow: none;
    padding: 0;
    min-width: 0;
  }
  .nav-links a {
    padding: 0.4rem 0.6rem;
  }
}
</style>
