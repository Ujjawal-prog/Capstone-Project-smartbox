#!/usr/bin/env python3
"""
Hack assembler (Nand to Tetris, Project 6) - two-pass.
Capstone: Ujjwal | Roll 2501730083 | K = 83 | K mod 3 = 2
Extra feature (K mod 3 == 2): print a warning if the same label is defined twice.

Usage:  python assembler.py Prog.asm [Prog.hack]
"""
import sys

COMP = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "!D": "0001101", "!A": "0110001",
    "-D": "0001111", "-A": "0110011", "D+1": "0011111", "A+1": "0110111",
    "D-1": "0001110", "A-1": "0110010", "D+A": "0000010", "D-A": "0010011",
    "A-D": "0000111", "D&A": "0000000", "D|A": "0010101",
    "M": "1110000", "!M": "1110001", "-M": "1110011", "M+1": "1110111",
    "M-1": "1110010", "D+M": "1000010", "D-M": "1010011", "M-D": "1000111",
    "D&M": "1000000", "D|M": "1010101",
}
DEST = {"": "000", "M": "001", "D": "010", "MD": "011",
        "A": "100", "AM": "101", "AD": "110", "AMD": "111"}
JUMP = {"": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
        "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"}


class AsmError(Exception):
    pass


def predefined():
    t = {"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
         "SCREEN": 16384, "KBD": 24576}
    for i in range(16):
        t["R%d" % i] = i
    return t


def clean(line):
    """Remove comment and all whitespace."""
    return "".join(line.split("//")[0].split())


def first_pass(lines, symbols, warnings):
    """Record label addresses. Returns list of (line_no, code) instructions."""
    code, labels = [], {}          # labels: name -> first line number
    for no, raw in enumerate(lines, 1):
        s = clean(raw)
        if not s:
            continue
        if s.startswith("("):
            if not s.endswith(")") or len(s) < 3:
                raise AsmError("Line %d: invalid label '%s'" % (no, s))
            name = s[1:-1]
            if name in labels:     # --- extra feature for K mod 3 == 2 ---
                warnings.append(
                    "Warning: Line %d: label '%s' is already defined at line %d "
                    "(keeping first definition)" % (no, name, labels[name]))
            else:
                labels[name] = no
                symbols[name] = len(code)
        else:
            code.append((no, s))
    return code


def c_instruction(no, s):
    dest, jump = "", ""
    body = s
    if "=" in body:
        dest, body = body.split("=", 1)
    if ";" in body:
        body, jump = body.split(";", 1)
    # dest letters may come in any order (e.g. DM= is the same as MD=)
    key = "".join(sorted(dest, key="AMD".index))
    if len(set(dest)) != len(dest) or key not in DEST:
        raise AsmError("Line %d: invalid destination '%s'" % (no, dest))
    dest = key
    if body not in COMP:
        raise AsmError("Line %d: invalid instruction '%s'" % (no, s))
    if jump not in JUMP:
        raise AsmError("Line %d: invalid jump '%s'" % (no, jump))
    return "111" + COMP[body] + DEST[dest] + JUMP[jump]


def second_pass(code, symbols):
    out, nxt = [], 16
    for no, s in code:
        if s.startswith("@"):
            sym = s[1:]
            if not sym:
                raise AsmError("Line %d: empty A-instruction" % no)
            if sym.isdigit():
                val = int(sym)
            else:
                if sym[0].isdigit():
                    raise AsmError("Line %d: invalid symbol '%s'" % (no, sym))
                if sym not in symbols:
                    symbols[sym] = nxt      # new variable
                    nxt += 1
                val = symbols[sym]
            if val > 32767:
                raise AsmError("Line %d: address %d out of range" % (no, val))
            out.append(format(val, "016b"))
        else:
            out.append(c_instruction(no, s))
    return out


def assemble(text):
    symbols, warnings = predefined(), []
    code = first_pass(text.splitlines(), symbols, warnings)
    return second_pass(code, symbols), warnings


def main():
    if len(sys.argv) < 2:
        print("Usage: python assembler.py Prog.asm [Prog.hack]")
        sys.exit(1)
    src = sys.argv[1]
    dst = sys.argv[2] if len(sys.argv) > 2 else src.rsplit(".", 1)[0] + ".hack"
    with open(src) as f:
        text = f.read()
    try:
        out, warnings = assemble(text)
    except AsmError as e:
        print("Error:", e)
        sys.exit(1)
    for w in warnings:
        print(w)
    with open(dst, "w") as f:
        f.write("\n".join(out) + "\n")
    print("Assembled %s -> %s (%d instructions)" % (src, dst, len(out)))


if __name__ == "__main__":
    main()
