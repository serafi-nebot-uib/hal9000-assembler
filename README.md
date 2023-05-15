# HAL9000 Assembler

A very basic HAL9000 "assembler" only meant to be used as support. It has not been thoroughly tested, so use it at your own risk.

## HAL9000 Insctruction set

| Instruction       | Encoding              | Action                                                        |
--------------------|-----------------------|---------------------------------------------------------------|
| `LOA M, Ti`       | `0000xxxmmmmmmmmi`    | Ti &larr; [M]                                                 |
| `STO Ti, M`       | `0001xxxmmmmmmmmi`    | M &larr; [Ti]                                                 |
| `LOIP (Xb), Ti`   | `0010xxxxxbbbxxxi`    | Ti &larr; \[[Xb]], Xb &larr; [Xb] + 1                         |
| `STIP Ti, (Xb)`   | `0011xxxxxbbbxxxi`    | [Xb] &larr; [Ti], Xb &larr; [Xb] + 1                          |
| `GOI M`           | `0100xxxmmmmmmmmx`    | PC &larr; M                                                   |
| `GOZ M`           | `0101xxxmmmmmmmmx`    | if Z = 1, PC &larr; M                                         |
| `GON M`           | `0110xxxmmmmmmmmx`    | if N = 1, PC &larr; M                                         |
| `EXIT`            | `10xxxxxxxxxxxxxx`    | Stop execution                                                |
| `COPY Rb, Rc`     | `11000xxxxbbbxccc`    | Rc &larr; [Rb]                                                |
| `ADD Ra, Rb, Rc`  | `11001aaaxbbbxccc`    | Rc &larr; [Rb] + [Ra]                                         |
| `SUB Ra, Rb, Rc`  | `11010aaaxbbbxccc`    | Rc &larr; [Rb] - [Ra]                                         |
| `AND Ra, Rb, Rc`  | `11011aaaxbbbxccc`    | Rc &larr; [Rb] ∧ [Ra]                                         |
| `SET #k, Rc`      | `11100kkkkkkkkccc`    | Rc &larr; k (extended sign)                                   |
| `ADQ #k, Rc`      | `11101kkkkkkkkccc`    | Rc &larr; [Rc] + k (extended sign)                            |
| `LSH #p, Rb, #n`  | `11110pppxbbbxxxn`    | if n = 0, Rb &larr; [Rb] << p<br>else Rb &larr; [Rb] >> p     |

## Requirements

- Python3

## Usage

Display usage:

```bash
$ python3 assembler.py
usage: assembler.py [-h] [-o OUTPUT] [--hide-numbers | --no-hide-numbers | -n] [--display-instruction | --no-display-instruction | --instr | --no-instr]
                   [--display-hex | --no-display-hex | --hex | --no-hex] [--display-bin | --no-display-bin | --bin | --no-bin]
                   [file]

HAL9000 Assembler

positional arguments:
  file                  Source code file path

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        File output path
  --hide-numbers, --no-hide-numbers, -n
  --display-instruction, --no-display-instruction, --instr, --no-instr
  --display-hex, --no-display-hex, --hex, --no-hex
  --display-bin, --no-display-bin, --bin, --no-bin
```

Example:

```bash
$ cat example.h9k
	SET 16,X2
	SET 19,X3
	SET 22,X4
	SET 3,X5
	LOIP (X2),T0
	COPY T0,X6
	LOIP (X3),T1
	COPY T1,X7
	LSH 1,X6,0
	LSH 1,X7,0
	ADD X6,X7,T0
	STIP T0,(X4)
	ADQ -1,X5
	GOZ 15
	GOI 4
	EXIT
	1
	1
	1
	1
	1
	1
	0
	0
	0
$ python3 assembler.py example.h9k
@0000   SET 16, X2      1110000010000010 e082
@0001   SET 19, X3      1110000010011011 e09b
@0002   SET 22, X4      1110000010110100 e0b4
@0003   SET 3, X5       1110000000011101 e01d
@0004   LOIP (X2), T0   0010000000100000 2020
@0005   COPY T0, X6     1100000000000110 c006
@0006   LOIP (X3), T1   0010000000110001 2031
@0007   COPY T1, X7     1100000000010111 c017
@0008   LSH 1, X6, 0    1111000101100000 f160
@0009   LSH 1, X7, 0    1111000101110000 f170
@0010   ADD X6, X7, T0  1100111001110000 ce70
@0011   STIP T0, (X4)   0011000001000000 3040
@0012   ADQ -1, X5      1110111111111101 effd
@0013   GOZ 15          0101000000011110 501e
@0014   GOI 4           0100000000001000 4008
@0015   EXIT            1000000000000000 8000
@0016   1               0000000000000001 0001
@0017   1               0000000000000001 0001
@0018   1               0000000000000001 0001
@0019   1               0000000000000001 0001
@0020   1               0000000000000001 0001
@0021   1               0000000000000001 0001
@0022   0               0000000000000000 0000
@0023   0               0000000000000000 0000
@0024   0               0000000000000000 0000
```

