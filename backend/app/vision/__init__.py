"""Modular, privacy-first computer-vision pipeline.

The pipeline is intentionally narrow: it detects *anonymous person-shaped
regions*, associates them across a few frames with **ephemeral** track ids, and
derives **aggregate** metrics (occupancy, queue pressure, table usage,
heatmaps). It never extracts identity, biometrics, or demographic attributes,
and never persists raw imagery.
"""
