# Product brief: Sixoh Log Doctor

Status: draft, pre-alpha. Last updated 2026-10-31.

## One line

An open-source, AI-assisted log doctor and live monitor for diesel trucks, starting with the 2003 to 2007 Ford 6.0L Power Stroke. It does not just show numbers. It tells the owner what the numbers mean, what was checked, and what was not.

## Who it is for

Owners of 6.0L Power Stroke trucks who already post readings in forums and ask whether the numbers are ok. The tool gives a plain answer from the same data, on an adapter that costs far less than a dedicated monitor, with open logs and open rules.

## How it compares with a dash monitor

Dash monitors such as the Edge Insight CTS3 (listed at $549.95 on Edge's site) are good closed hardware: a screen that starts with the truck, alarms, logging, code read and clear, and add-on sensors for EGT and fuel pressure. Sixoh does not replace that screen or those sensors, and does not claim to. What it adds is interpretation with operating context, a visible source and status on every threshold, open CSV logs, a public PID table and changelog, and a much cheaper adapter. Edge's tools do document warnings and saved recordings, so the claim is not that nothing else records or alerts. The claim is that Sixoh combines context, related readings and comparable sessions into findings an owner can follow back to the source.

## Product shape

1. **Capture.** Live OBD-II over an ELM327-class USB adapter, through one small transport module we own (see the read-only rules below). Sessions are recorded automatically. Imported FORScan CSV logs are the other input.
2. **Brain.** A deterministic rules engine over an engine pack. Rules watch the data and produce structured findings. Each finding is in one of four states: checked with no finding, checked with a finding, not checked (conditions never occurred), or unavailable (data missing, unsupported or stale). Silence is never reported as "all good". Every live session is saved in a native log format, with per-signal timing and freshness, so any real reading can become a permanent test case.
3. **Face.** A key-off summary in three plain sentences (what was checked, what was found, what to look at next, plus a coverage line saying what was not checked), a paste-ready summary card for forum threads, and later a desktop monitor with large gauges, a flag banner and a loud "not receiving data" state.

## Non-negotiables

- Read-only, forever. The tool only requests data. It never writes to, flashes, tunes or runs service functions on any module. Official releases and contributions follow this policy. The MIT license lets anyone fork, so it cannot bind forks.
- No emissions delete support of any kind.
- Not tuning advice and not a mechanic substitute. Warning wording only: "worth checking", "ask a shop". Never "safe to drive" or "replace this".
- AI, when added, only rewords structured findings. It may not add a value, a threshold or a cause. Template text is the default and the authority. A guard checks that every number in AI text matches a number in the finding, otherwise the template text is shown.
- Threshold honesty. Each threshold carries four labels: source (Ford bulletin, vendor documentation, community), applicability (build range, conditions), validation (documented only, decoded on a reference truck, evaluated on independent cases), and release status (supported, experimental, unavailable). Unverified stays visibly unverified until real logs settle it.
- Logs stay local by default. Sharing is deliberate, with VIN, location and exact timestamps stripped.
- We do not read or copy any other vendor's firmware or software.

## Version 1 engine pack: 6.0L Power Stroke

Context gating is required on every rule so the tool does not cry wolf. Rule status as of this draft:

1. **FICM health.** Main, logic and vehicle power together. Thresholds disagree between sources (45 V, 46.5 V, 47 to 48 V), so the tool shows two labeled tiers. Cranking is recorded but not evaluated until state detection is proven. Low main power with adequate recorded supplies is reported as "have the supply circuits and FICM evaluated", not as a verdict.
2. **High-pressure oil.** Actual ICP versus the truck's own desired ICP, which Ford service information supports as a screen. IPR rail checks (15 and 85 percent) and elevated hot-idle IPR are experimental. ICP voltage is not a drop-in for ICP pressure.
3. **Oil cooler delta.** Observed EOT minus ECT in comparable, eligible windows, experimental. Ford's 15 F test belongs to a high-load diagnostic sequence, so our steady-cruise version needs its own validation.
4. **Sensor agreement.** Key on, engine off agreement of MAP and barometric pressure first. EBP checks wait for a real log, because Ford documents some early trucks using an inferred exhaust pressure with no EBP sensor input. Under-load EBP versus MAP comparison is experimental.

Engine packs are data, but a pack may only reference request templates from a core-reviewed list, so a pack contribution is reviewed like a security change.

## Hardware and platform

- Recommended adapter: OBDLink EX (USB, listed at $69.95), developed on Windows first. Cheap ELM327 clones are best effort and unsupported. J2534 devices are out of scope.
- Whether the EX connects to a 2003 truck on its bus is UNVERIFIED and is the first thing the reference truck settles.
- Which bus each model year uses is UNVERIFIED. The tool detects the protocol and records it per session.
- A phone or tablet monitor needs a Bluetooth adapter. Android comes later. iOS is not promised.
- EGT and fuel pressure are not on the data bus and need physical probes. Add-on inputs are a later version.
- Many 6.0 trucks run tunes. Stock or tuned is declared at setup, and rules 2 and 4 are relabeled or suppressed on tuned trucks.

## Claims we are not making yet

"The 6.0 announces failures weeks early", "same data as a dash monitor", and "rivals the CTS3" are hypotheses or goals, not facts. They stay out of public copy until real logs and measured outcomes support them.

## What success looks like

An owner plugs in, drives, and at key-off gets three plain sentences that a non-expert can correctly explain, including what was not checked. See ROADMAP.md for phases and tests.
