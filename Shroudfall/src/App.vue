<script setup>
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
import UpdatePopup from '@/components/UpdatePopup.vue'
import AppNav from '@/components/AppNav.vue'
import { initCards } from '@/services/databaseService'

onMounted(() => {
  initCards()
})
</script>

<template>
  <div class="app-layout">
    <header class="app-header">
      <router-link to="/" class="logo">Shroudfall</router-link>
      <AppNav />
    </header>
    <main class="app-main">
      <RouterView />
    </main>
    <UpdatePopup />
  </div>
</template>

<style scoped>
.app-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  background: var(--color-background-mute);
  border-bottom: 1px solid var(--color-border);
  flex-shrink: 0;
}
.logo {
  font-weight: 700;
  font-size: 1.25rem;
  color: var(--color-heading);
  text-decoration: none;
}
.logo:hover {
  color: var(--color-accent);
}
.app-main {
  flex: 1;
  padding-bottom: 2rem;
}
</style>
