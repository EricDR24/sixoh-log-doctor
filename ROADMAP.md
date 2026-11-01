# Roadmap

Status: draft, pre-alpha. Last updated 2026-10-31. Everything marked UNVERIFIED has not been confirmed on a real truck. See BRIEF.md for the product and SAFETY.md for the read-only rules.

## Principles

- Offline analyzer first, then read-only live capture feeding the same rules, then the monitor UI, then explanations.
- Prove each PID, each rule and each supported configuration separately. One truck can verify a decode. It cannot verify a diagnosis.
- Synthetic fixtures prove the code works. They do not prove a rule is right.
- A report always says what it checked and what it could not check.

## Phase 0: ground truth from the reference truck

The reference truck is a 2003 F250 6.0L with an OBDLink EX.
- Connect the EX in FORScan, note the protocol FORScan reports and the FORScan version.
- Record one reference log: key on engine off for 60 s, cold start and warm-up, hot idle for 5 min, steady unloaded cruise for 10 min, one moderate pull, key-off. Keep the PID list screenshot.
- Check the CSV decimal separator and header format.
Exit: protocol known, one real CSV in the repo as a scrubbed fixture.

## v0.1 Offline log doctor

- CSV loader, one internal schema, unit normalization, original input kept.
- Rules engine with the four assessment states and evidence labels on every threshold.
- Rules: FICM, key-off MAP and baro agreement, ICP actual versus desired, oil cooler delta (experimental).
- Templated three-sentence report with a coverage line.
Tests: the real log loads with no manual edits; each planted fault fixture trips only its own rule; healthy sections trip no FICM flag, or the flag is explained and confirmed with a meter; no unassessed check is shown as passed; the suite passes offline; a reviewer can trace each finding to readings to rule version.

## v0.2 Read-only capture, standard PIDs only

- One transport module is the only code that imports the serial library or writes to the adapter. It sends only a frozen allowlist of exact frames. The allowlist covers adapter commands too (ELM AT PP and STN ST can persist), not just OBD frames.
- Banned: 04, 14, 08, 10, 11, 27, 2E, 2F, 31, 34 to 37, 3B, ATMA, adapter configuration writes, raw passthrough. Do not depend on python-OBD (it exposes clearing codes).
- Protocol detection, stored per session. Mode 01 standard PIDs and adapter voltage. Sessions saved in the native log format. Measured PIDs per second published.
- Open decision: reading trouble codes (03, 07, 0A) is read-only. Included only if the maintainer says yes. Clearing codes is never included.
- Live-bus safety: one outstanding request at a time, a conservative rate cap (UNVERIFIED starting point near 5 requests per second), pause on low battery voltage, KOEO sessions time-limited, parked use first, no driving checks until proven.
Tests: import ban; fake serial port records every byte and matches the allowlist exactly; fuzz test over service IDs and malformed replies; 30 minute drive with no gap over 2 s; the capture loads in the v0.1 importer. This proves what our tool sends, not what adapter firmware does.

## v0.3 Mode 22, one PID at a time

- A per-model-year PID table. Each PID is enabled only after it is confirmed. A PID not in the table cannot be sent (test).
- A FORScan CSV shows names and values, not request bytes, so it cannot confirm a Mode 22 ID by itself. Confirm by a passive capture (second adapter, sends nothing) or by one candidate read compared with FORScan at the same moment. Never guess module headers.
- Starting candidates, all UNVERIFIED for this truck: ICP 22 1446 (2003 and 2004 may need ICP voltage 22 16AD), IPR 1434, EBP 1445 (reported 2005 and later), FICM main, logic and vehicle power 09D0, 09CF, 09CE, EOT 1310, MAP 1440, baro 1442. ScanGauge publishes 6.0 definitions for several of these, so the status is "vendor documented, not validated for this truck".
- All four rules run live where their PIDs are confirmed, and show "unavailable" where they are not.

## v0.4 Desktop monitor alpha (Windows)

- Fixed readable gauges, flag banner, loud stale-data state, automatic recording that survives a UI crash, key-off summary, and a driving mode with no touch input while moving.
- Key-off is detected explicitly (engine speed zero then bus silence). A disconnected adapter is not treated as key-off.
Tests: 20 normal session cycles; cable pull, host suspend, crash and reconnect; adapter sleep and parked power test; ten real commutes with zero false critical alerts; live analysis and replay of the saved session give the same findings.

## v0.5 Community logs and field beta

- Opt-in log contribution with an anonymizer (VIN, location, exact timestamps), known-repair tags, stock or tuned declared. A public PID table with status per line, a "confirmed on N trucks" count, a public changelog, and contributors credited by handle.
- History comparison of matched operating windows, behind a flag. Trend memory needs about 20 gated sessions from one truck and normalization for temperature, altitude and load.
- Targets: at least 5 independent trucks for integration learning; whole trucks held out from threshold tuning; a rule moves to "verified" only with at least 3 confirmed-fault logs and 10 healthy logs; false positive rates and misses published with denominators. A false alarm budget is set after the first 10 real sessions.

## v0.6 Android, v0.7 explanations

- Android needs a Bluetooth adapter. The same allowlist and fuzz tests must pass on the Android build.
- Explanations: templates first. An optional language model layer rewords findings only, with the number-match guard, off by default, cloud use opt-in. Output is identical with it off apart from wording.

## v1.0 criteria

- All four rules have verified decode status. At least FICM and ICP actual versus desired have verified thresholds backed by confirmed-repair logs.
- Both protocol families confirmed on real trucks.
- External review of the transport module.
- Disclaimers in the app and README: read-only, no emissions delete support, not a mechanic substitute.
- Public changelog, PID table and known-issues page.
- Core test: five non-developer owners plug in, drive, and at key-off get three sentences they can correctly explain, including what was not checked.

## Deferred or cut

Clearing codes, ever. Public claims that the tool rivals a dash monitor. A 0 to 60 timer. A health score number. Other engine packs until 6.0 reaches v1.0. EGT and fuel pressure probes (v1.x). Importing another vendor's log files or firmware until the license question is settled.

## Open questions

- Does the OBDLink EX connect to a 2003 truck on its bus? Phase 0 answers it.
- Which bus does each model year use? The tool detects it.
- Do the Mode 22 IDs above hold on this truck, and which module answers them?
- Does a 2003 truck have a usable EBP signal? Ford documents an inferred exhaust pressure on some early trucks.
- Which FICM thresholds survive real logs?
