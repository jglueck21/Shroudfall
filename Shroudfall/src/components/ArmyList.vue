<script setup>
defineProps({
  units: {
    type: Array,
    default: () => [],
  },
  valid: {
    type: Boolean,
    default: false,
  },
  validationWarning: {
    type: String,
    default: null,
  },
})

const emit = defineEmits(['remove'])
</script>

<template>
  <div class="army-list">
    <p v-if="validationWarning" class="validation-warning" :class="{ valid }">
      {{ validationWarning }}
    </p>
    <ul v-if="units.length" class="unit-list">
      <li v-for="(unit, index) in units" :key="index" class="unit-row">
        <span class="unit-name">{{ unit.name }}</span>
        <span class="unit-cost">{{ unit.cost }} Pkt</span>
        <button
          type="button"
          class="btn-remove"
          aria-label="Entfernen"
          @click="emit('remove', index)"
        >
          Entfernen
        </button>
      </li>
    </ul>
    <p v-else class="empty">Noch keine Einheiten. Füge Karten über „Truppe hinzufügen“ hinzu.</p>
  </div>
</template>

<style scoped>
.army-list {
  font-size: 0.95rem;
}
.validation-warning {
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  margin-bottom: 0.75rem;
  background: rgba(230, 126, 34, 0.2);
  color: #d35400;
}
.validation-warning.valid {
  background: rgba(39, 174, 96, 0.2);
  color: #27ae60;
}
.unit-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.unit-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--color-border);
  flex-wrap: wrap;
}
.unit-name {
  flex: 1;
  min-width: 100px;
}
.unit-cost {
  font-weight: 500;
  min-width: 4rem;
}
.btn-remove {
  padding: 0.35rem 0.6rem;
  font-size: 0.85rem;
  background: var(--color-border);
  border: none;
  border-radius: 4px;
  color: var(--color-text);
  cursor: pointer;
}
.btn-remove:hover {
  background: var(--color-border-hover);
}
.empty {
  color: var(--color-text);
  opacity: 0.8;
  font-size: 0.9rem;
}
</style>
