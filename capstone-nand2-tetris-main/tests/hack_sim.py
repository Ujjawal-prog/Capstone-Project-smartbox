"""Tiny Hack CPU simulator used only to test the assembler output (not part of the HDL)."""
def run(hack_lines, steps, ram_init=None, kbd=0):
    rom=[int(l,2) for l in hack_lines if l.strip()]
    ram=[0]*24577; ram[24576]=kbd
    for k,v in (ram_init or {}).items(): ram[k]=v
    A=D=pc=0
    def s16(x): x&=0xFFFF; return x-65536 if x&0x8000 else x
    for _ in range(steps):
        if pc>=len(rom): break
        i=rom[pc]
        if not i&0x8000: A=i; pc+=1; continue
        y=ram[A] if i&0x1000 else A
        c=(i>>6)&0x3F
        x=D
        if c&0x20: x=0
        if c&0x10: x=~x
        yy=y
        if c&0x08: yy=0
        if c&0x04: yy=~yy
        out=(x&0xFFFF)+(yy&0xFFFF) if c&0x02 else (x&yy)
        if c&0x01: out=~out
        out=s16(out)
        d=(i>>3)&7; j=i&7
        if d&1: ram[A]=out&0xFFFF
        if d&2: D=out
        old=A
        if d&4: A=out&0xFFFF
        jump=((j&4 and out<0) or (j&2 and out==0) or (j&1 and out>0))
        pc=old if jump else pc+1
        if jump: pass
    return ram
