/**
 * Lokale Speicherung (LocalStorage) – keine Cloud, offline.
 */

const PREFIX = 'shroudfall_'

export function getItem(key, defaultValue = null) {
  try {
    const raw = localStorage.getItem(PREFIX + key)
    if (raw == null) return defaultValue
    return JSON.parse(raw)
  } catch {
    return defaultValue
  }
}

export function setItem(key, value) {
  try {
    localStorage.setItem(PREFIX + key, JSON.stringify(value))
    return true
  } catch {
    return false
  }
}

export function removeItem(key) {
  try {
    localStorage.removeItem(PREFIX + key)
    return true
  } catch {
    return false
  }
}

export function getArmyLists() {
  return getItem('armyLists', [])
}

export function saveArmyLists(lists) {
  return setItem('armyLists', lists)
}

export function getCharacters() {
  return getItem('characters', [])
}

export function saveCharacters(characters) {
  return setItem('characters', characters)
}

export function getSettings() {
  return getItem('settings', {
    updatePopupEnabled: true,
    defaultBudget: 200,
    rulebookVersion: '1.0',
    rulebookFilename: 'regelbuch.pdf',
  })
}

export function saveSettings(settings) {
  return setItem('settings', settings)
}

export function getLastEditedArmyId() {
  return getItem('lastEditedArmyId', null)
}

export function setLastEditedArmyId(id) {
  return setItem('lastEditedArmyId', id)
}

/** Gespeicherte Daten löschen (für Einstellungen) */
export function clearAllData() {
  const keys = []
  for (let i = 0; i < localStorage.length; i++) {
    const k = localStorage.key(i)
    if (k?.startsWith(PREFIX)) keys.push(k)
  }
  keys.forEach((k) => localStorage.removeItem(k))
  return true
}
