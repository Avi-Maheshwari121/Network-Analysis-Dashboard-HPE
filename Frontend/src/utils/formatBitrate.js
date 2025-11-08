// Frontend/src/utils/formatBitrate.js

/**
 * Converts a raw bitrate (in bits per second) to the most appropriate
 * human-readable unit (bps, Kbps, Mbps, Gbps) using 1000-based multiples.
 *
 * @param {number} bitsPerSecond The raw value in bits per second.
 * @returns {{value: string, unit: string}}
 */
export const formatBitrate = (bitsPerSecond) => {
  if (bitsPerSecond === undefined || bitsPerSecond === null || bitsPerSecond === 0) {
    return { value: "0.00", unit: "bps" };
  }

  const units = [
    { threshold: 1_000_000_000, divisor: 1_000_000_000, label: 'Gbps' }, // Giga-bits
    { threshold: 1_000_000,     divisor: 1_000_000,     label: 'Mbps' }, // Mega-bits
    { threshold: 1_000,         divisor: 1_000,         label: 'Kbps' }, // Kilo-bits
    { threshold: 0,             divisor: 1,             label: 'bps' }   // bits
  ];

  // Find the first unit where the value is greater than or equal to the threshold
  for (const unit of units) {
    if (bitsPerSecond >= unit.threshold) {
      return {
        value: (bitsPerSecond / unit.divisor).toFixed(2),
        unit: unit.label
      };
    }
  }

  // Fallback for very small (but non-zero) values, though "bps" unit should catch it.
  return { value: bitsPerSecond.toFixed(2), unit: 'bps' };
};