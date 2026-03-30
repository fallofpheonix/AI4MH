const ALERT_THRESHOLD = 0.75;
const WARNING_THRESHOLD = 0.4;

export function scoreColor(value) {
  if (value >= ALERT_THRESHOLD) return "#dc2626";
  if (value >= WARNING_THRESHOLD) return "#d97706";
  return "#16a34a";
}

export function formatScore(value, digits = 3) {
  return Number(value || 0).toFixed(digits);
}
