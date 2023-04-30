# HAL9000 Compiler

This is a very basic HAL9000 "compiler" only meant to be used as support. Use at your own risk.

## HAL9000 Insctruction set


## Requirements

- Python3

## Usage

Display usage:

```bash
$ python3 compiler.py
usage: compiler.py [-h] [-o OUTPUT] [--hex | --no-hex] [--bin | --no-bin] [file]

HAL9000 compiler

positional arguments:
  file                  Source code file path

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        File output path
  --hex, --no-hex
  --bin, --no-bin
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
$ python3 compiler.py example.h9k
1110000010000010 e082
1110000010011011 e09b
1110000010110100 e0b4
1110000000011101 e01d
0010000000100000 2020
1100000000000110 c006
0010000000110001 2031
1100000000010111 c017
1111000101100000 f160
1111000101110000 f170
1100111001110000 ce70
0011000001000000 3040
1110111111111101 effd
0101000000011110 501e
0100000000001000 4008
1000000000000000 8000
0000000000000001 0001
0000000000000001 0001
0000000000000001 0001
0000000000000001 0001
0000000000000001 0001
0000000000000001 0001
0000000000000000 0000
0000000000000000 0000
0000000000000000 0000
```


