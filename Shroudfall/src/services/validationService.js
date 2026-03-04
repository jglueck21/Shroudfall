/**
 * Validierung – z. B. Armee muss mindestens einen "Essence Weaver" enthalten.
 */

const ESSENCE_WEAVER_NAMES = ['Essence Weaver', 'essence weaver']

export function armyHasEssenceWeaver(units) {
  if (!Array.isArray(units)) return false
  return units.some(
    (u) =>
      ESSENCE_WEAVER_NAMES.includes(u.name) ||
      (u.card && ESSENCE_WEAVER_NAMES.includes(u.card.name))
  )
}

export function getArmyValidationMessage(units) {
  return armyHasEssenceWeaver(units)
    ? null
    : 'Die Armee ist nur gültig, wenn mindestens ein "Essence Weaver" enthalten ist.'
}

export function isArmyValid(units) {
  return armyHasEssenceWeaver(units)
}
