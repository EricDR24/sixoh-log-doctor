# PIDs

Nothing here is verified on the truck yet. Ford extended PIDs come from a community ScanGauge list (https://www.powerstroke.org/threads/scangauge-ii-pids.274854/), not from Ford. FORScan shows its own PID names; treat those as the source of truth.

## Standard OBD-II (Mode 01)
RPM, ECT, IAT, vehicle speed, probably MAP/boost. UNVERIFIED: which of these this PCM reports.

## Ford extended (Mode 22, header 07E0), community-sourced, UNVERIFIED on truck

| Signal | PID | Status |
|---|---|---|
| ICP pressure | 221446 | Community, unverified |
| ICP voltage | 2216AD | Community, unverified |
| IPR duty | 221434 | Community, unverified |
| EOT | 221310 | Community, unverified |
| VGT duty | 22096D | Community, unverified |
| Cam/crank sync | 2209CD | Community, unverified |
| FICM main power | 2209D0 | Community, unverified |
| FICM vehicle power | 2209CE | Community, unverified |
| FICM logic power | 2209CF | Community, unverified |
| EGR duty | 22166E | Community, unverified |
| EGR position | 2209FE | Community, unverified |
| Barometric pressure | 221127 | Community, unverified |
| EBP | none listed | UNVERIFIED |
| MAP | none listed | UNVERIFIED |
| Fuel pressure | none listed | UNVERIFIED |

## Reference values (community pages, not Ford service data)
- FICM main power 46-48 V; under 45 V is a problem.
- ICP voltage key on engine off: 0.16-0.28 V. Cranking: over 0.8 V and over 500 psi.
- IPR about 15% key on engine off; should never sit at 15% or 85% while running; about 30% at warm idle.
- EOT minus ECT over 15F when warm suggests an oil cooler problem. UNVERIFIED (no primary source read).
