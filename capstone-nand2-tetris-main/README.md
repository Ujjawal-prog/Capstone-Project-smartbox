# Capstone: Make the Computer Draw a Box
Nand to Tetris – I (ETCNTC301), K.R. Mangalam University
**Ujjwal · Roll No. 2501730083 · K = 83**

| Item | Value |
|---|---|
| K mod 3 = 2 | extra assembler feature: warning when a label is written twice |
| K mod 4 = 3 | box width = 16 × 4 = 64 pixels (4 words) |
| Box | starts at row 83, 20 rows tall, rows 83–102, columns 0–63 |
| Address | SCREEN + 32×83 = 19040 |

## Files
- `CPU.hdl`, `Memory.hdl`, `Computer.hdl` – Part A
- `assembler.py` – Part B (two-pass Hack assembler)
- `Box.asm`, `Box.hack` – Part C (`Box.hack` made with `assembler.py`)
- `tests/` – Add/Max/Rect/Pong sources, official .hack references, test scripts and results

## Use
```
python assembler.py Box.asm            # writes Box.hack
python assembler.py Prog.asm Out.hack  # custom output name
```
Load `Box.hack` in the CPU Emulator (animate: no animation), hold any key: a black box appears; release it: it disappears.
