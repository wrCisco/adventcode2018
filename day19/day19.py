#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import re
from typing import Optional, Callable, List, Sequence


class Register:

    def __init__(self, name: int, value:int = 0) -> None:
        self.name = name
        self.value = value


class Instruction:

    def __init__(
            self,
            func: Callable,
            opcode: Optional[int] = None,
            name: Optional[str] = None
    ) -> None:
        self.opcode = opcode
        self.name = name
        self.func = func

    def __call__(self, *args, **kwargs) -> None:
        self.func(*args, **kwargs)


class Device:

    def __init__(self) -> None:
        self.registers = (
            Register(0),
            Register(1),
            Register(2),
            Register(3),
            Register(4),
            Register(5)
        )
        self.instructions = [
            Instruction(name='addr', opcode=9, func=self.addr),
            Instruction(name='addi', opcode=6, func=self.addi),
            Instruction(name='mulr', opcode=8, func=self.mulr),
            Instruction(name='muli', opcode=0, func=self.muli),
            Instruction(name='banr', opcode=14, func=self.banr),
            Instruction(name='bani', opcode=11, func=self.bani),
            Instruction(name='borr', opcode=1, func=self.borr),
            Instruction(name='bori', opcode=10, func=self.bori),
            Instruction(name='setr', opcode=7, func=self.setr),
            Instruction(name='seti', opcode=12, func=self.seti),
            Instruction(name='gtir', opcode=15, func=self.gtir),
            Instruction(name='gtri', opcode=2, func=self.gtri),
            Instruction(name='gtrr', opcode=4, func=self.gtrr),
            Instruction(name='eqir', opcode=5, func=self.eqir),
            Instruction(name='eqri', opcode=3, func=self.eqri),
            Instruction(name='eqrr', opcode=13, func=self.eqrr)
        ]
        self.opcode2instr = { instr.opcode: instr for instr in self.instructions }
        self.name2instr = { instr.name: instr for instr in self.instructions }

    def register(self, name: int) -> int:
        return self.registers[name].value

    def get_all_registers(self) -> List[int]:
        return [r.value for r in self.registers]

    def put_register(self, name: int, value: int) -> None:
        self.registers[name].value = value

    def zero_registers(self) -> None:
        for reg in self.registers:
            reg.value = 0

    def dump_registers(self) -> None:
        print(" ".join(str(r.value) for r in self.registers))

    def addr(self, A: int, B: int, C: int) -> None:
        self.put_register(C, self.register(A) + self.register(B))

    def addi(self, A: int, B: int, C: int) -> None:
        self.put_register(C, self.register(A) + B)

    def mulr(self, A: int, B: int, C: int) -> None:
        self.put_register(C, self.register(A) * self.register(B))

    def muli(self, A: int, B: int, C: int) -> None:
        self.put_register(C, self.register(A) * B)

    def banr(self, A: int, B: int, C: int) -> None:
        self.put_register(C, self.register(A) & self.register(B))

    def bani(self, A: int, B: int, C: int) -> None:
        self.put_register(C, self.register(A) & B)

    def borr(self, A: int, B: int, C: int) -> None:
        self.put_register(C, self.register(A) | self.register(B))

    def bori(self, A: int, B: int, C: int) -> None:
        self.put_register(C, self.register(A) | B)

    def setr(self, A: int, B: int, C: int) -> None:
        self.put_register(C, self.register(A))

    def seti(self, A: int, B: int, C: int) -> None:
        self.put_register(C, A)

    def gtir(self, A: int, B: int, C: int) -> None:
        self.put_register(C, 1 if A > self.register(B) else 0)

    def gtri(self, A: int, B: int, C: int) -> None:
        self.put_register(C, 1 if self.register(A) > B else 0)

    def gtrr(self, A: int, B: int, C: int) -> None:
        self.put_register(C, 1 if self.register(A) > self.register(B) else 0)

    def eqir(self, A: int, B: int, C: int) -> None:
        self.put_register(C, 1 if A == self.register(B) else 0)

    def eqri(self, A: int, B: int, C: int) -> None:
        self.put_register(C, 1 if self.register(A) == B else 0)

    def eqrr(self, A: int, B: int, C: int) -> None:
        self.put_register(C, 1 if self.register(A) == self.register(B) else 0)

    def execute(self, program: 'Program', instruction_pointer: int = 0) -> None:
        # print("Nr of instructions:", len(program.instructions))
        while instruction_pointer in range(len(program.instructions)):
            self.put_register(program.register_ip, instruction_pointer)
            exec_instr = program.instructions[instruction_pointer]
            # print("Executing instruction nr. ", instruction_pointer, " (", self.opcode2instr[exec_instr.instruction[0]].name, " ",
            #     " ".join(str(i) for i in exec_instr.instruction[1:]), ")", sep="")
            # print("Before:", end=" ")
            # self.dump_registers()
            self.opcode2instr[exec_instr.opcode](*exec_instr.valuesIO)
            # print("After: ", end=" ")
            # self.dump_registers()
            instruction_pointer = self.register(program.register_ip)
            instruction_pointer += 1
            # input()

    def execute_hack(self) -> None:
        self.put_register(0, 0)
        self.put_register(1, 3)
        self.put_register(2, 1)#10551296)
        self.put_register(3, 10551296)
        self.put_register(4, 0)
        self.put_register(5, 10551296)


class Sample:

    def __init__(
            self,
            instruction: Sequence[int],
            before: Sequence[int],
            after: Sequence[int]
    ) -> None:
        self.instruction = instruction
        self.opcode = instruction[0]
        self.valuesIO = instruction[1:]
        self.before = before
        self.after = after


class ProgramInstruction:

    def __init__(self, instruction: Sequence[int]) -> None:
        self.instruction = instruction
        self.opcode = instruction[0]
        self.valuesIO = instruction[1:]


class Program:

    def __init__(
            self,
            instructions: Sequence[Sequence[int]],
            instr_pointer_register: int
    ) -> None:
        self.instructions = [ProgramInstruction(instr) for instr in instructions]
        self.register_ip = instr_pointer_register

    def dump_instructions(self):
        for instr in self.instructions:
            print(" ".join(str(i) for i in instr.instruction))


if __name__ == '__main__':
    with open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input_day19.txt'),
            encoding='utf-8'
        ) as fh:
        instructions = [instr for instr in fh.read().splitlines() if instr]

    device = Device()
    bound_register = int(re.findall(r'\d', instructions[0])[0])
    instructions.pop(0)
    for i, instr in enumerate(instructions):
        # print(instr)
        opcode_instr = re.sub(r'(\w{4})', lambda match: str(device.name2instr[match.group(1)].opcode), instr)
        instructions[i] = [int(val) for val in re.findall(r'\d+', opcode_instr)]
    daemon = Program(instructions, bound_register)
    device.zero_registers()
    device.execute(daemon)

    print(f"Value of register 0 after background program execution is:", device.register(0))

    # device.zero_registers()
    # device.put_register(0, 1)
    # device.execute_hack()
    # device.execute(daemon, 3)

    # print("Value of register 0 after second background program execution is:", device.register(0))

    # I didn't write a program to solve the second part of the problem:
    # daemon program ends execution after register 2 becomes greater than register 5, which has value 10551296
    # (cfr. instructions 13, which puts 1 in register 4, which is added to the value in register 1 - bound to the instruction pointer -
    # with the effect of jumping over instrucion 15 to instruction 16, which halts the program)
    # At the time this happens, register 0 has the sum of all the possible values which, multiplied in pairs,
    # are equal to the value of register 5 (10551296): the only executed instruction (since the loops begin)
    # that change value of register 0 is the 7th, which is executed only when instruction 4 outputs 1, which happens when
    # (instruction 3) the product of the values in registers 2 and 3 is equal to 10551296 (instruction 7 adds the value in
    # register 2 to the value in register 0, and puts the result in register 0). Since the program proceed in a nested loop
    # that adds (inner loop) one every iteration to register 3 and adds (outer loop) one every iteration to register 2, before
    # the execution ends register 2 assumes all the "valid" values from 1 to 10551296 for the register 0 to add.
