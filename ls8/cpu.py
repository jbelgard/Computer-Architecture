"""CPU functionality."""

import sys

#Program Actions
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010 

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.registers = [0] * 8
        self.pc = 0

    #access the RAM inside the CPU object MAR (Memory Address Register) - contains the address that is being read / written to
    def ram_read(self, MAR):
        #accepts the address to read and return the value stored there
        
        return self.ram[MAR]

    #access the RAM inside the CPU object MDR (Memory Data Register) - contains the data that was read or the data to write
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        if len(sys.argv) != 2:
            print("Usage: ls8.py filename")
            sys.exit(1)

        try:
            address = 0
            with open(sys.argv[1]) as f:
                for line in f:
                    split_line = line.split('#')
                    code_value = split_line[0].strip()

                    if code_value == '':
                        continue

                    try:
                        code_value = int(code_value, 2)

                    except ValueError:
                        print(f"Invalid Number: {code_value}")
                        sys.exit(1)

                    self.ram_write(address, code_value)
                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[1]} file not found")
            sys.exit(2)

        # For now, we've just hardcoded a program:

        #program = [
            # From print8.ls8
        #    0b10000010, # LDI R0,8
         #   0b00000000,
          #  0b00001000,
           # 0b01000111, # PRN R0
            #0b00000000,
            #0b00000001, # HLT
        #]

        #for instruction in program:
        #    self.ram[address] = instruction
        #    address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.registers[reg_a] *= self.registers[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.registers[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            #read the memory address (MAR) that's stored in register PC (self.pc) store the result in IR (Instruction Register)
            IR = self.ram_read(self.pc)

            #read bytes at PC + 1 and PC + 2 from RAM into variables aperand_a and operand_b
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            #Halt
            if IR == HLT:
                running = False
                self.pc += 1

            #Print
            elif IR == PRN:
                print(self.registers[operand_a])
                self.pc += 2

            #Load Immediate
            elif IR == LDI:
                self.registers[operand_a] = operand_b
                self.pc += 3

            #Multiply
            elif IR == MUL:
                self.registers[operand_a] *= self.registers[operand_b]
                self.pc += 3

            else:
                sys.exit()
