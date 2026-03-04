<script setup>
defineProps({
  card: {
    type: Object,
    required: true,
  },
  compact: {
    type: Boolean,
    default: false,
  },
  showDescription: {
    type: Boolean,
    default: false,
  },
})
</script>

<template>
  <div class="card-component" :class="{ compact }">
    <div v-if="card.artwork" class="card-artwork">
      <img :src="card.artwork" :alt="card.name" />
    </div>
    <div v-else class="card-artwork placeholder">Kein Artwork</div>
    <div class="card-info">
      <h3 class="card-name">{{ card.name }}</h3>
      <p class="card-meta">
        <span class="cost">{{ card.cost }} Punkte</span>
        <span class="type">{{ card.type }}</span>
      </p>
      <p v-if="card.attributes?.length" class="card-attributes">
        {{ card.attributes.join(', ') }}
      </p>
      <p v-if="showDescription && card.description" class="card-description">
        {{ card.description }}
      </p>
    </div>
  </div>
</template>

<style scoped>
.card-component {
  background: var(--color-background-mute);
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--color-border);
  cursor: pointer;
  transition: transform 0.15s, box-shadow 0.15s;
}
.card-component:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
.card-artwork {
  aspect-ratio: 3/4;
  background: var(--color-background);
  display: flex;
  align-items: center;
  justify-content: center;
}
.card-artwork.placeholder {
  color: var(--color-text);
  font-size: 0.85rem;
  opacity: 0.7;
}
.card-artwork img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.card-info {
  padding: 0.6rem 0.75rem;
}
.card-name {
  font-size: 0.95rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
  color: var(--color-heading);
}
.card-meta {
  font-size: 0.8rem;
  color: var(--color-text);
  margin-bottom: 0.2rem;
}
.cost {
  font-weight: 500;
  margin-right: 0.5rem;
}
.card-attributes {
  font-size: 0.75rem;
  opacity: 0.9;
}
.card-description {
  font-size: 0.85rem;
  margin-top: 0.5rem;
  line-height: 1.4;
}
.card-component.compact .card-info {
  padding: 0.4rem 0.5rem;
}
.card-component.compact .card-name {
  font-size: 0.85rem;
}
.card-component.compact .card-meta {
  font-size: 0.75rem;
}
</style>
