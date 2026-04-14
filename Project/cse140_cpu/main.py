"""
Entry point — the only script you run (python cse140_cpu/main.py from Project).

Later: load program file, loop fetch -> decode -> execute -> mem -> writeback.
"""

from decode import decode_instruction, print_decoded_instruction


def main():
    input_binary = input("Enter an instruction: ")
    print_decoded_instruction(*decode_instruction(input_binary))


if __name__ == "__main__":
    main()
