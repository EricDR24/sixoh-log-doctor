# Roadmap (week one)

1. **Day 1.** Repo, README safety statement, MIT license. CSV loader for FORScan exports. UNVERIFIED: exact FORScan CSV header format; capture a real file first.
2. **Day 2.** Map PID names to one schema. Handle units (psi/kPa, F/C). Add a `--generic` CSV option.
3. **Day 3.** Rules engine with four fixed checks: FICM main power under 45 V; ICP vs desired ICP and IPR stuck at 15% or 85%; EOT minus ECT delta; EBP vs MAP under load.
4. **Day 4.** Report: Markdown/HTML summary with charts (matplotlib).
5. **Day 5.** AI explanations of flagged data only. Never tuning advice.
6. **Days 6-7.** Run on real truck logs, tune thresholds, write docs, tag v0.1.
