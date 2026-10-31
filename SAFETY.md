# Safety

This project is offline analysis of previously exported log files only. It contains no vehicle connection, diagnostic command, actuator control, configuration or programming functions. This tool sends nothing.

External logging software (for example FORScan with an OBD adapter) does communicate with the vehicle, and OBD polling sends requests. The read-only guarantee applies to the analyzer, not to the logger.

It is not tuning advice and not a substitute for a qualified diesel mechanic. Use at your own risk. While moving, only a passenger may operate or inspect the logger. The logger may be recording without driver interaction.

## What this tool does not do

- It does not connect to the vehicle. It only reads CSV files you export.
- It sends nothing. It has no vehicle connection, diagnostic command, actuator control, configuration, or programming function.
- It does not support emissions-delete or disabling emissions equipment (see the EPA Clean Air Act tampering policy).
- It does not give tuning advice. AI notes only explain flagged data.
- It is not a substitute for a qualified mechanic.

## Logging safely

Live PID reading with the key on and the engine off is allowed. During every logging session use PID reading only, with stored DTC retrieval when needed. Do not use Output Control or actuator tests, do not clear DTCs, do not reset modules or adaptations, do not run tests or service procedures, and do not use Configuration or Programming functions, in any engine state.

1. Key on, engine off: live PID reading is allowed, with stored DTC retrieval when needed.
2. Idle logs: parked, outdoors, parking brake set.
3. Drive logs: configure and test recording while parked. Secure the computer and adapter, keep cables clear of pedals and steering, and verify power settings let recording continue. While moving, only a passenger may operate or inspect the logger. Stop safely before addressing any recording problem. The driver leaves the session recording without driver interaction. Keep cables away from the pedals.
4. Disconnect the adapter afterward unless its manufacturer supports leaving it connected.
