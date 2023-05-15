import sys
import argparse
import binascii

from instruction import *

def csplit(src: str, delim: str, offset: int = 0, maxsplit: int = 0) -> tuple[list[str], int]:
    items: list[str] = []
    i = offset
    prev = offset
    while i < len(src) and (len(items) < maxsplit or maxsplit < 1):
        if src[i] in delim:
            substr = src[prev:i].strip(delim)
            if len(substr) > 0:
                items.append(substr)
            prev = i
        i += 1

    return (items, prev)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HAL9000 compiler")
    parser.add_argument('file', nargs="?", help="Source code file path")
    parser.add_argument(
            "-o",
            "--output",
            help=f"File output path",
            default="stdout")
    parser.add_argument("--hide-numbers" , "-n", action=argparse.BooleanOptionalAction)
    parser.add_argument("--display-instruction", "--instr", action=argparse.BooleanOptionalAction)
    parser.add_argument("--display-hex", "--hex", action=argparse.BooleanOptionalAction)
    parser.add_argument("--display-bin", "--bin", action=argparse.BooleanOptionalAction)
    parser.add_argument("--format-m68k", "--m68k", action=argparse.BooleanOptionalAction)

    args = vars(parser.parse_args())

    input_file_path = args["file"]
    output_file_path = args["output"]
    output_instruction = args["display_instruction"]
    output_hex = args["display_hex"]
    output_bin = args["display_bin"]
    hide_numbers = args["hide_numbers"]
    format_m68k = args["format_m68k"]

    output_opts = (output_instruction, output_hex, output_bin)
    output_opts_defaults = [False, True, True, True]
    if not any(output_opts):
        hide_numbers, output_instruction, output_hex, output_bin = output_opts_defaults

    if input_file_path is None:
        parser.print_help()
        exit(-1)

    ln = 0
    fin = None
    fout = sys.stdout
    try:
        fin = open(input_file_path, "r")
        if output_file_path != "stdout":
            fout = open(output_file_path, "w")

        instrl = []
        addr = 0
        for l in fin:
            ln += 1
            l = l.strip("\t\r")
            tokens, *_ = csplit(l, " ,\n")

            if len(tokens) > 0:
                instr = instr_for_mnemonic(*tokens)
                data = instr.encode()
                instrl.append(data)

                if not format_m68k:
                    if not hide_numbers:
                        fout.write(f"@{addr:04}".ljust(8))

                    if output_bin:
                        fout.write(f"{int.from_bytes(data):016b} ")

                    if output_hex:
                        fout.write(binascii.hexlify(data).decode("utf-8") + " ")

                    if output_instruction:
                      fout.write(l.strip("\n").ljust(16))

                    fout.write("\n")
            addr += 1

        if format_m68k:
            l = ["$" + binascii.hexlify(x).decode("utf-8").upper() for x in instrl]
            for i in range(0, len(instrl), 8):
                print("\tDC.W " + ",".join(l[i:i+8]))
    except Exception as e:
        print(f"[ERROR] on line {ln}:", e)
        exit(-1)
    finally:
        if fin is not None:
            fin.close()

        if fout is not sys.stdout:
            fout.close()

