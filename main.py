import os

def disassemble(filename):
    file = open(filename)

    opcodes = {
        0b00000: "nop",
        0b00001: "mov",
        0b00010: "add",
        0b00011: "sub",
        0b00100: "shl",
        0b00101: "shr",
        0b00110: "and",
        0b00111: "or",
        0b01000: "xor",
        0b01001: "not",
        0b01010: "cmp",
        0b01011: "jmp",
        0b01100: "jz",
        0b01101: "jnz",
        0b01110: "lpd"
    }

    operands = {
        0b0000: "r1",
        0b0001: "r2",
        0b0010: "r3",
        0b0011: "r4",
        0b0100: "sp",
        0b0101: "bp",
        0b0110: "ptr",
        0b0111: "nil",
        0b1000: "ip",
        0b1001: "mem",
        0b1010: "im",
        0b1011: "pma"
    }

    lines = file.readlines()

    code_lines = []

    for i in range(len(lines)):
        if i > 0 and int("0x" + lines[i-1].strip(), 16) >> 15 == 1:
            continue

        line = "0x" + lines[i].strip()

        num = int(line, 16)

        imm = num >> 15

        opcode = opcodes[(num >> 10) & 0b11111]

        op_a = operands[(num >> 4) & 0b1111]
        op_b = operands[num & 0b1111]

        if imm:
            line = "0x" + lines[i+1].strip()

            next_num = int(int(line, 16))

            if op_a == "im":
                instr = f"{opcode} {next_num}\n"
            else:
                instr = f"{opcode} {op_a}, {next_num}\n"
        elif opcode == "not":
            instr = f"{opcode} {op_b}"
        elif opcode == "lpd":
            if imm:
                line = "0x" + lines[i+1].strip()

                next_num = int(int(line, 16))

                instr = f"{opcode} {next_num}"
            else:
                instr = f"{opcode} {op_a}"
        else:
            instr = f"{opcode} {op_a}, {op_b}\n"

        code_lines.append(instr)

    f = open(f"{filename[:filename.find('.')]}.asm", "w")
    f.writelines(code_lines)


def main():
    is_open = True
    while is_open:
        name = input("Enter a file to disassemble: ")
        if name.lower() == "exit":
            is_open = False
        elif not os.path.exists(name):
            print("Invalid filename\n")
        else:
            disassemble(name)
            print(f'Disassembled file wrote to "{name[:name.find(".")]}.asm"')
            is_open = False


main()
