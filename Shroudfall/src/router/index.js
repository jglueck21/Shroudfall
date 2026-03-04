import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomeView.vue'),
      meta: { title: 'Shroudfall' },
    },
    {
      path: '/cards',
      name: 'card-browser',
      component: () => import('@/views/CardBrowserView.vue'),
      meta: { title: 'Kartenbrowser' },
    },
    {
      path: '/army',
      name: 'army-editor',
      component: () => import('@/views/ArmyEditorView.vue'),
      meta: { title: 'Armeelisten-Editor' },
    },
    {
      path: '/characters',
      name: 'characters',
      component: () => import('@/views/CharacterView.vue'),
      meta: { title: 'Charaktererstellung' },
    },
    {
      path: '/rulebook',
      name: 'rulebook',
      component: () => import('@/views/RulebookView.vue'),
      meta: { title: 'Regelbuch' },
    },
    {
      path: '/faq',
      name: 'faq',
      component: () => import('@/views/FAQView.vue'),
      meta: { title: 'FAQ' },
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('@/views/SettingsView.vue'),
      meta: { title: 'Einstellungen' },
    },
  ],
})

router.afterEach((to) => {
  document.title = to.meta.title ? `${to.meta.title} – Shroudfall` : 'Shroudfall'
})

export default router
