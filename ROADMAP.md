# Roadmap (week one)

v0.1 is the CSV loader, the schema, the four rules, and the report. The Day 5 step (AI explanations of flagged data only; never tuning advice) is moved out of v0.1 and comes after live capture. See the order in the v0.2 plan.

1. **Day 1.** Repo, README safety statement, MIT license. CSV loader for FORScan exports. UNVERIFIED: exact FORScan CSV header format; capture a real file first.
2. **Day 2.** Map PID names to one schema. Handle units (psi/kPa, F/C). Add a `--generic` CSV option.
3. **Day 3.** Rules engine with four fixed checks: FICM main power under 45 V; ICP vs desired ICP and IPR stuck at 15% or 85%; EOT minus ECT delta; EBP vs MAP under load.
4. **Day 4.** Report: Markdown/HTML summary with charts (matplotlib).
5. **Days 6-7.** Run on real truck logs, tune thresholds, write docs, tag v0.1.

## v0.2 plan: read-only live monitor (not started, scoping only)

1. Goal: plug in an adapter, launch the tool, and it reads the truck and flags warning signs with no upload. Scope is one engine family (2003 to 2007 Ford 6.0L Power Stroke), read-only, not a FORScan replacement.
2. Design: one engine, two inputs. The rules engine is shared. Input A is live capture over a USB serial ELM327/STN-style adapter. Input B is CSV import of FORScan exports. Every live session is also saved as a local CSV log so odd readings become permanent test cases, and CSV import is how known-bad logs from other owners get added.
3. Read-only guarantee for live mode: exactly one module may import the serial library and write to the adapter; it sends only frames from a frozen allowlist of exact byte strings (setup AT commands, selected Mode 01 reads, Mode 03/07 reads, and later only verified Mode 22 reads). Banned: clear codes (04, 14), 08, 10, 11, 27, 2E, 2F, 31, 34 to 37, 3B, ATMA, adapter config writes, and any raw passthrough. Tests: import ban except in that module, a fake serial port that records every written byte and fails on anything off the list, a fuzz test over service IDs, explicit negative tests. Do not depend on python-OBD (it exposes clearing codes); borrow ideas only. This proves what our tool sends, not what adapter firmware does.
4. Adapters: designed for OBDLink-class USB adapters (OBDLink SX or EX; vLinker FS is a candidate); generic ELM327 clones are best effort and unsupported; J2534 devices are out of scope because they are built for reflashing. Adapter support is UNVERIFIED on a real 6.0 until tested.
5. Unverified items, each marked UNVERIFIED. Live mode sends no Mode 22 request until the PID is confirmed from a real FORScan log or capture.
   - Which diagnostic bus 2003 to 2007 trucks use (the tool must detect the protocol, not assume it). UNVERIFIED.
   - Every Mode 22 PID number and scaling (forum sourced, conflicting, and ICP/EBP availability differs by model year). UNVERIFIED.
   - Boost via standard MAP. UNVERIFIED.
6. Live-bus safety: one outstanding request at a time, conservative rate cap starting near 5 requests per second (UNVERIFIED), pause on low battery voltage, KOEO sessions time-limited, parked or idle use first, passenger operates the tool, no driving checks until proven.
7. Order: CSV loader and rules (v0.1), then live capture as a new input to the same rules (v0.2), then AI explanations of flagged events and a key-off summary, narrating validated findings only and never producing requests. Never tuning advice. Phone apps are a later problem.
8. Needed before v0.2 code: a real FORScan log with the PID list showing. The reference truck is a 2003 F250 6.0L. Forum sources (UNVERIFIED) say the standard ICP PID may not work on 2003 and 2004 trucks, which use the ICP voltage PID instead, and that the EBP PID is 2005 and later only. So on the reference truck the ICP rule may need the voltage PID and the EBP vs MAP rule may not be able to run. The first log decides this.
