const MIN_SCORE = 0;
const MAX_SCORE = 1;

function clampScore(value) {
  return Math.min(Math.max(Number(value) || 0, MIN_SCORE), MAX_SCORE);
}

export function scoreColor(value) {
  const normalized = clampScore(value);
  const hue = 120 - normalized * 120;
  return `hsl(${hue} 72% 42%)`;
}

export function formatScore(value, digits = 3) {
  return Number(value || 0).toFixed(digits);
}
