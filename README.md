# sixoh-log-doctor

A pre-alpha project for an offline datalog analyzer targeting 2003 to 2007 Ford 6.0L Power Stroke vehicles. The planned workflow is to export a FORScan CSV on Windows and analyze it locally. CSV import, analysis, and reporting are not implemented yet. macOS and Windows support are planned but have not been validated.

This project is not affiliated with or endorsed by Ford or FORScan.

## Safety statement

**This project only reads logged data. It never writes to, flashes, or tunes any vehicle module, and it does not support removing or disabling emissions equipment. It is not tuning advice and not a substitute for a qualified diesel mechanic. Use at your own risk. Logging while driving must be done by a passenger, or it is recording without driver interaction.**

- Reads log files only. It never connects to, writes to, or flashes an ECU, PCM, or FICM.
- No emissions-delete support of any kind. Requests for it will be closed.
- Not tuning advice. Not a substitute for a mechanic.

See [SAFETY.md](SAFETY.md).

## Status

**Pre-alpha.** Nothing works yet. The exact FORScan CSV export format is UNVERIFIED; a real FORScan log from the truck is needed to confirm it.

## Planned checks (four fixed rules)

1. FICM main power under 45 V
2. ICP vs desired ICP, and IPR stuck at 15% or 85% while running
3. EOT minus ECT delta (rule of thumb: over 15F warm; UNVERIFIED)
4. EBP vs MAP under load (EBP and MAP PIDs UNVERIFIED)

Thresholds come from community sources, not Ford service data, and will be checked against real logs.

## PIDs

The Ford extended PIDs are community-sourced and not from Ford. See [docs/pids.md](docs/pids.md) for verified and unverified marks.

## Roadmap

See [ROADMAP.md](ROADMAP.md).

## License

MIT. See [LICENSE](LICENSE).
