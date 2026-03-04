/**
 * Karten-Daten – lokal (später austauschbar mit SQLite/sql.js).
 * Ladezeit ≤ 2 Sekunden, keine Server-Calls.
 */

// Platzhalter-Daten; kann durch Laden aus .db/.json ersetzt werden
const MOCK_CARDS = [
  {
    id: '1',
    name: 'Essence Weaver',
    cost: 25,
    type: 'Unit',
    attributes: ['Magic', 'Support'],
    description: 'Verstärkt verbündete Einheiten in der Nähe.',
    artwork: null,
  },
  {
    id: '2',
    name: 'Shadow Stalker',
    cost: 35,
    type: 'Unit',
    attributes: ['Stealth', 'Melee'],
    description: 'Unsichtbar bis zum ersten Angriff.',
    artwork: null,
  },
  {
    id: '3',
    name: 'Flame Guardian',
    cost: 40,
    type: 'Unit',
    attributes: ['Fire', 'Defense'],
    description: 'Blockiert gegnerische Projektile.',
    artwork: null,
  },
  {
    id: '4',
    name: 'Storm Caller',
    cost: 55,
    type: 'Unit',
    attributes: ['Lightning', 'Ranged'],
    description: 'Ruft Blitze auf Feinde herab.',
    artwork: null,
  },
  {
    id: '5',
    name: 'Bone Soldier',
    cost: 15,
    type: 'Unit',
    attributes: ['Undead', 'Melee'],
    description: 'Einfacher Nahkampf-Skelett.',
    artwork: null,
  },
]

let cardsCache = null

/**
 * Alle Karten laden. Ziel: ≤ 2 Sekunden, lokal.
 * @returns {Promise<Array>}
 */
export async function loadCards() {
  if (cardsCache) return cardsCache
  // Kurze Verzögerung simulieren (später durch echte DB ersetzbar)
  await new Promise((r) => setTimeout(r, 50))
  cardsCache = [...MOCK_CARDS]
  return cardsCache
}

/**
 * Sofortige synchrone Rückgabe aus Cache (für sofortige Suche).
 */
export function getCardsSync() {
  return cardsCache || MOCK_CARDS
}

/**
 * Einmal beim App-Start laden, damit Suche sofort reagiert.
 */
export function initCards() {
  if (!cardsCache) loadCards().then(() => {})
}

export function getCardById(id) {
  const list = getCardsSync()
  return list.find((c) => c.id === id) || null
}
