#!/usr/bin/env python3
from pathlib import Path


VALID_COMMANDS = set("><+-.,[]")


def expected_output() -> str:
    lines = []
    for value in range(1, 101):
        if value % 15 == 0:
            lines.append("FizzBuzz")
        elif value % 3 == 0:
            lines.append("Fizz")
        elif value % 5 == 0:
            lines.append("Buzz")
        else:
            lines.append(str(value))
    return "\n".join(lines) + "\n"


def run_brainfuck(program: str) -> str:
    tape = [0]
    pointer = 0
    pc = 0
    output = []
    jump_forward = {}
    jump_backward = {}
    stack = []

    for index, command in enumerate(program):
        if command == "[":
            stack.append(index)
        elif command == "]":
            if not stack:
                raise ValueError(f"unmatched closing bracket at {index}")
            start = stack.pop()
            jump_forward[start] = index
            jump_backward[index] = start
    if stack:
        raise ValueError(f"unmatched opening bracket at {stack[-1]}")

    while pc < len(program):
        command = program[pc]
        if command == ">":
            pointer += 1
            if pointer == len(tape):
                tape.append(0)
        elif command == "<":
            pointer -= 1
            if pointer < 0:
                raise ValueError("data pointer moved before start of tape")
        elif command == "+":
            tape[pointer] = (tape[pointer] + 1) % 256
        elif command == "-":
            tape[pointer] = (tape[pointer] - 1) % 256
        elif command == ".":
            output.append(chr(tape[pointer]))
        elif command == ",":
            tape[pointer] = 0
        elif command == "[" and tape[pointer] == 0:
            pc = jump_forward[pc]
        elif command == "]" and tape[pointer] != 0:
            pc = jump_backward[pc]
        pc += 1

    return "".join(output)


def main() -> None:
    program_path = Path(__file__).with_name("fizzbuzz.bf")
    program = program_path.read_text(encoding="utf-8").strip()
    invalid = sorted(set(program) - VALID_COMMANDS)
    if invalid:
        raise SystemExit(f"invalid Brainfuck commands found: {invalid}")

    actual = run_brainfuck(program)
    expected = expected_output()
    if actual != expected:
        raise SystemExit("FizzBuzz output mismatch")

    print("ok")
    print(f"commands={len(program)}")
    print(f"output_chars={len(actual)}")


if __name__ == "__main__":
    main()
