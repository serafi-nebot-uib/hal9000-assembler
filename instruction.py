import struct as s

def _signext(k: int, size: int) -> int:
    mask = 2**size - 1
    max = 2**(size - 1)

    if k > 0:
        max -= 1

    if abs(k) > max:
        raise Exception(f"number overflow: {k} is too large for {size} bits")

    if k < 0:
        k = (~abs(k) & mask) + 1

    return k & mask

class Instruction:
    _FMT = ">H"

    def encode(self) -> bytes:
        return b''

class Constant(Instruction):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = int(value)

    def encode(self) -> bytes:
        return s.pack(self._FMT, _signext(self.value, 16))

class LOA(Instruction):
    OPCODE = 0b0000

    def __init__(self, m: str, ti: str) -> None:
        super().__init__()
        self.m = int(m)
        self.ti = int(ti.strip("T"))

    def encode(self) -> bytes:
        instr = self.OPCODE << 12
        instr |= self.m << 1
        instr |= self.ti
        return s.pack(self._FMT, instr)

class STO(Instruction):
    OPCODE = 0b0001

    def __init__(self, ti: str, m: str) -> None:
        super().__init__()
        self.ti = int(ti.strip("T"))
        self.m = int(m)

    def encode(self) -> bytes:
        instr = self.OPCODE << 12
        instr |= self.m << 1
        instr |= self.ti
        return s.pack(self._FMT, instr)

class LOIP(Instruction):
    OPCODE = 0b0010

    def __init__(self, xb: str, ti: str) -> None:
        super().__init__()
        self.xb = int(xb.strip("(X)"))
        self.ti = int(ti.strip("T"))

    def encode(self) -> bytes:
        instr = self.OPCODE << 12
        instr |= self.xb << 4
        instr |= self.ti
        return s.pack(self._FMT, instr)

class STIP(Instruction):
    OPCODE = 0b0011

    def __init__(self, ti: str, xb: str) -> None:
        super().__init__()
        self.ti = int(ti.strip("T"))
        self.xb = int(xb.strip("(X)"))

    def encode(self) -> bytes:
        instr = self.OPCODE << 12
        instr |= self.xb << 4
        instr |= self.ti
        return s.pack(self._FMT, instr)

class GOI(Instruction):
    OPCODE = 0b0100

    def __init__(self, m: str) -> None:
        super().__init__()
        self.m = int(m)

    def encode(self) -> bytes:
        instr = self.OPCODE << 12
        instr |= self.m << 1
        return s.pack(self._FMT, instr)

class GOZ(Instruction):
    OPCODE = 0b0101

    def __init__(self, m: str) -> None:
        super().__init__()
        self.m = int(m)

    def encode(self) -> bytes:
        instr = self.OPCODE << 12
        instr |= self.m << 1
        return s.pack(self._FMT, instr)

class GON(Instruction):
    OPCODE = 0b0110

    def __init__(self, m: str) -> None:
        super().__init__()
        self.m = int(m)

    def encode(self) -> bytes:
        instr = self.OPCODE << 12
        instr |= self.m << 1
        return s.pack(self._FMT, instr)

class EXIT(Instruction):
    OPCODE = 0b10

    def __init__(self) -> None:
        super().__init__()

    def encode(self) -> bytes:
        instr = self.OPCODE << 14
        return s.pack(self._FMT, instr)

class COPY(Instruction):
    OPCODE = 0b11000

    def __init__(self, rb: str, rc: str) -> None:
        super().__init__()
        self.rb = int(rb.strip("TX"))
        self.rc = int(rc.strip("TX"))

    def encode(self) -> bytes:
        instr = self.OPCODE << 11
        instr |= self.rb << 4
        instr |= self.rc
        return s.pack(self._FMT, instr)

class ADD(Instruction):
    OPCODE = 0b11001

    def __init__(self, ra: str, rb: str, rc: str) -> None:
        super().__init__()
        self.ra = int(ra.strip("TX"))
        self.rb = int(rb.strip("TX"))
        self.rc = int(rc.strip("TX"))

    def encode(self) -> bytes:
        instr = self.OPCODE << 11
        instr |= self.ra << 8
        instr |= self.rb << 4
        instr |= self.rc
        return s.pack(self._FMT, instr)

class SUB(Instruction):
    OPCODE = 0b11010

    def __init__(self, ra: str, rb: str, rc: str) -> None:
        super().__init__()
        self.ra = int(ra.strip("TX"))
        self.rb = int(rb.strip("TX"))
        self.rc = int(rc.strip("TX"))

    def encode(self) -> bytes:
        instr = self.OPCODE << 11
        instr |= self.ra << 8
        instr |= self.rb << 4
        instr |= self.rc
        return s.pack(self._FMT, instr)

class AND(Instruction):
    OPCODE = 0b11011

    def __init__(self, ra: str, rb: str, rc: str) -> None:
        super().__init__()
        self.ra = int(ra.strip("TX"))
        self.rb = int(rb.strip("TX"))
        self.rc = int(rc.strip("TX"))

    def encode(self) -> bytes:
        instr = self.OPCODE << 11
        instr |= self.ra << 8
        instr |= self.rb << 4
        instr |= self.rc
        return s.pack(self._FMT, instr)

class SET(Instruction):
    OPCODE = 0b11100

    def __init__(self, k: str, rc: str) -> None:
        super().__init__()
        self.k = int(k.strip("#"))
        self.rc = int(rc.strip("TX"))

    def encode(self) -> bytes:
        instr = self.OPCODE << 11
        instr |= _signext(self.k, 8) << 3
        instr |= self.rc
        return s.pack(self._FMT, instr)

class ADQ(Instruction):
    OPCODE = 0b11101

    def __init__(self, k: str, rc: str) -> None:
        super().__init__()
        self.k = int(k.strip("#"))
        self.rc = int(rc.strip("TX"))

    def encode(self) -> bytes:
        instr = self.OPCODE << 11
        instr |= _signext(self.k, 8) << 3
        instr |= self.rc
        return s.pack(self._FMT, instr)

class LSH(Instruction):
    OPCODE = 0b11110

    def __init__(self, p: str, rb: str, n: str) -> None:
        super().__init__()
        self.p = int(p.strip("#"))
        self.rb = int(rb.strip("TX"))
        self.n = int(n.strip("#"))

    def encode(self) -> bytes:
        instr = self.OPCODE << 11
        instr |= self.p << 8
        instr |= self.rb << 4
        instr |= self.n
        return s.pack(self._FMT, instr)

_INSTR_TABLE = {
        "LOA": LOA,
        "STO": STO,
        "LOIP": LOIP,
        "STIP": STIP,
        "GOI": GOI,
        "GOZ": GOZ,
        "GON": GON,
        "EXIT": EXIT,
        "COPY": COPY,
        "ADD": ADD,
        "SUB": SUB,
        "AND": AND,
        "SET": SET,
        "ADQ": ADQ,
        "LSH": LSH
}

class InvalidInstruction(Exception):
    pass

class InvalidSyntax(Exception):
    pass

def instr_for_mnemonic(mnemonic: str, *args: list[str]) -> Instruction:
    if mnemonic not in _INSTR_TABLE:
        try:
            return Constant(mnemonic)
        except:
            raise InvalidInstruction(f"unkown instruction: {mnemonic}")

    try:
        return _INSTR_TABLE[mnemonic](*args)
    except:
        raise InvalidSyntax(f"invalid syntax for instruction: {mnemonic} {', '.join(args)}")

