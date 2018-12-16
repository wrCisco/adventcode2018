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
            Register(3)
        )
        self.instructions = [
            Instruction(name='addr', func=self.addr),
            Instruction(name='addi', func=self.addi),
            Instruction(name='mulr', func=self.mulr),
            Instruction(name='muli', func=self.muli),
            Instruction(name='banr', func=self.banr),
            Instruction(name='bani', func=self.bani),
            Instruction(name='borr', func=self.borr),
            Instruction(name='bori', func=self.bori),
            Instruction(name='setr', func=self.setr),
            Instruction(name='seti', func=self.seti),
            Instruction(name='gtir', func=self.gtir),
            Instruction(name='gtri', func=self.gtri),
            Instruction(name='gtrr', func=self.gtrr),
            Instruction(name='eqir', func=self.eqir),
            Instruction(name='eqri', func=self.eqri),
            Instruction(name='eqrr', func=self.eqrr)
        ]
        self.converter = {}  # maps opcodes to instructions

    def register(self, name: int) -> int:
        return self.registers[name].value

    def get_all_registers(self) -> List[int]:
        return [r.value for r in self.registers]

    def put_register(self, name: int, value: int) -> None:
        self.registers[name].value = value

    def zero_registers(self) -> None:
        for reg in self.registers:
            reg.value = 0

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

    def __init__(self, instructions: Sequence[Sequence[int]]) -> None:
        self.instructions = [ProgramInstruction(instr) for instr in instructions]

    def execute(self, device: Device) -> None:
        for instr in self.instructions:
            device.converter[instr.opcode](*instr.valuesIO)


if __name__ == '__main__':
    with open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input_day16.txt'),
            encoding='utf-8'
        ) as fh:
        samples_raw, test_program_raw = fh.read().split('\n\n\n\n')

    samples_raw = samples_raw.split('\n\n')
    samples = []
    for sample in samples_raw:
        rows = sample.splitlines()
        args = []
        for i in (1, 0, 2):
            args.append([int(val) for val in re.findall(r'\d+', rows[i])])
        samples.append(Sample(*args))

    device = Device()
    more_than_three_opcodes = 0
    known_opcodes = set()

    for sample in samples:
        compatibles = []
        for instruction in device.instructions:
            for i, val in enumerate(sample.before):
                device.put_register(i, val)
            instruction(*sample.valuesIO)
            if sample.after == device.get_all_registers():
                compatibles.append((sample, instruction))
        if len(compatibles) >= 3:
            more_than_three_opcodes += 1
        elif len(compatibles) == 1:
            compatibles[0][1].opcode = compatibles[0][0].opcode
            known_opcodes.add(compatibles[0][1].opcode)
            device.converter[compatibles[0][1].opcode] = compatibles[0][1]

    print("Samples that behave like three or more opcodes:", more_than_three_opcodes)

    while len(known_opcodes) < len(device.instructions):
        for sample in samples:
            if sample.opcode in known_opcodes:
                continue
            compatible_opcodes = []
            for instruction in device.instructions:
                for i, val in enumerate(sample.before):
                    device.put_register(i, val)
                instruction(*sample.valuesIO)
                if sample.after == device.get_all_registers():
                    if instruction.opcode not in known_opcodes:
                        compatible_opcodes.append((sample.opcode, instruction))
            if len(compatible_opcodes) == 1:
                compatible_opcodes[0][1].opcode = compatible_opcodes[0][0]
                known_opcodes.add(compatible_opcodes[0][1].opcode)
                device.converter[compatible_opcodes[0][1].opcode] = compatible_opcodes[0][1]

    # for instruction in device.instructions:
    #     print(f"Name: {instruction.name} - Opcode: {instruction.opcode}")

    # simpler procedural solution
    # test_program = test_program_raw.splitlines()
    # device.zero_registers()
    # for row in test_program:
    #     instr = [int(val) for val in re.findall(r'\d+', row)]
    #     device.converter[instr[0]](*instr[1:])

    # object oriented solution
    rows = test_program_raw.splitlines()
    test_program = Program([[int(val) for val in re.findall(r'\d+', row)] for row in rows])
    device.zero_registers()
    test_program.execute(device)

    print(f"Value of register 0 after test program execution is:", device.register(0))
