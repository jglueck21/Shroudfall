<script setup>
defineProps({
  character: {
    type: Object,
    required: true,
  },
  selected: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['select', 'delete'])
</script>

<template>
  <div
    class="character-card"
    :class="{ selected }"
    role="button"
    tabindex="0"
    @click="emit('select', character)"
    @keydown.enter="emit('select', character)"
  >
    <div class="char-visual">
      <span class="char-icon">{{ character.icon || '?' }}</span>
    </div>
    <h3 class="char-name">{{ character.name }}</h3>
    <p v-if="character.attributes?.length" class="char-attrs">
      {{ character.attributes.join(', ') }}
    </p>
    <button
      type="button"
      class="btn-delete"
      aria-label="Charakter löschen"
      @click.stop="emit('delete', character.id)"
    >
      Löschen
    </button>
  </div>
</template>

<style scoped>
.character-card {
  background: var(--color-background-mute);
  border: 2px solid var(--color-border);
  border-radius: 8px;
  padding: 1rem;
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s;
  text-align: center;
}
.character-card:hover {
  background: var(--color-border-hover);
}
.character-card.selected {
  border-color: var(--color-accent);
  background: rgba(44, 62, 80, 0.15);
}
.char-visual {
  width: 64px;
  height: 64px;
  margin: 0 auto 0.5rem;
  border-radius: 50%;
  background: var(--color-background);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid var(--color-border);
}
.char-icon {
  font-size: 1.5rem;
  color: var(--color-text);
}
.char-name {
  font-size: 1rem;
  margin-bottom: 0.25rem;
  color: var(--color-heading);
}
.char-attrs {
  font-size: 0.8rem;
  color: var(--color-text);
  margin-bottom: 0.5rem;
}
.btn-delete {
  padding: 0.35rem 0.6rem;
  font-size: 0.8rem;
  background: transparent;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  color: var(--color-text);
  cursor: pointer;
}
.btn-delete:hover {
  background: rgba(192, 57, 43, 0.2);
  color: #c0392b;
}
</style>
