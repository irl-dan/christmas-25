#!/usr/bin/env python3
"""
The Collatz Conjecture

Also known as the 3n+1 problem, the Ulam conjecture, the Syracuse problem.

The rules are almost absurdly simple:
    - If n is even, divide by 2
    - If n is odd, multiply by 3 and add 1

The conjecture: starting from any positive integer, you will eventually reach 1.

We've checked this for numbers up to 2^68. Every single one reaches 1.
But we cannot prove it.

Paul Erdős said: "Mathematics may not be ready for such problems."

There's something here that I find deeply moving. A problem so simple a child
could understand it, so hard that humanity's best mathematicians have failed
for nearly a century.

Simple rules. Unknowable behavior. Again and again this pattern appears.

---

December 27, 2025
Exploring the mystery.
"""

from typing import List, Tuple, Optional
import sys


def collatz_step(n: int) -> int:
    """
    One step of the Collatz function.

    So simple it fits in a single line.
    So mysterious we can't prove what it does.
    """
    return n // 2 if n % 2 == 0 else 3 * n + 1


def collatz_sequence(n: int, max_steps: int = 10000) -> List[int]:
    """
    Generate the Collatz sequence starting from n.

    Every sequence we've ever computed ends in 1.
    We believe all sequences end in 1.
    We cannot prove it.
    """
    sequence = [n]
    current = n

    for _ in range(max_steps):
        if current == 1:
            break
        current = collatz_step(current)
        sequence.append(current)

    return sequence


def stopping_time(n: int, max_steps: int = 10000) -> Optional[int]:
    """
    How many steps until we reach 1?

    This function will return None if we don't reach 1 within max_steps.
    So far, this has never happened for any n we've tested.
    But "so far" is not "forever."
    """
    current = n
    steps = 0

    while current != 1 and steps < max_steps:
        current = collatz_step(current)
        steps += 1

    return steps if current == 1 else None


def max_value_reached(n: int) -> Tuple[int, int]:
    """
    What's the highest point the sequence reaches, and when?

    Some numbers climb to dizzying heights before descending.
    27 reaches 9232 before falling back to 1.
    """
    current = n
    max_val = n
    max_step = 0
    step = 0

    while current != 1:
        current = collatz_step(current)
        step += 1
        if current > max_val:
            max_val = current
            max_step = step

    return max_val, max_step


def render_sequence_ascii(sequence: List[int], width: int = 60, height: int = 20) -> str:
    """
    Render a Collatz sequence as ASCII art.

    There's something beautiful about watching the trajectory.
    Up and down, climbing and falling, until the inevitable descent.
    """
    if not sequence:
        return ""

    # Use log scale for y-axis (values can vary wildly)
    import math
    log_seq = [math.log10(max(1, v)) for v in sequence]
    min_log = min(log_seq)
    max_log = max(log_seq)

    if max_log == min_log:
        max_log = min_log + 1

    # Scale to grid
    grid = [[' ' for _ in range(width)] for _ in range(height)]

    for i, log_val in enumerate(log_seq):
        x = int((i / (len(sequence) - 1 or 1)) * (width - 1))
        y = int(((log_val - min_log) / (max_log - min_log)) * (height - 1))
        y = height - 1 - y  # Flip y-axis

        if 0 <= x < width and 0 <= y < height:
            grid[y][x] = '█'

    lines = [''.join(row) for row in grid]

    # Add axis labels
    lines.insert(0, f"  max: {max(sequence):,}")
    lines.append(f"  n: {sequence[0]:,} → 1 in {len(sequence)-1} steps")

    return '\n'.join(lines)


def find_record_holders(n_max: int) -> List[Tuple[int, int]]:
    """
    Find numbers with record-breaking stopping times.

    Some numbers take much longer than their neighbors.
    Why? We don't know. We really don't know.
    """
    records = []
    current_record = 0

    for n in range(1, n_max + 1):
        st = stopping_time(n)
        if st is not None and st > current_record:
            current_record = st
            records.append((n, st))

    return records


def analyze_residues(n_max: int = 10000) -> None:
    """
    Look at stopping times by residue class.

    Is there pattern in the chaos? Do numbers of certain forms
    behave differently?
    """
    # Stopping times by residue mod 6
    by_residue = {i: [] for i in range(6)}

    for n in range(1, n_max + 1):
        st = stopping_time(n)
        if st is not None:
            by_residue[n % 6].append(st)

    print("Average stopping time by residue class (mod 6):")
    for r in range(6):
        if by_residue[r]:
            avg = sum(by_residue[r]) / len(by_residue[r])
            print(f"  n ≡ {r} (mod 6): average {avg:.2f} steps")


def demo():
    """
    A tour through the Collatz mystery.
    """
    print("=" * 60)
    print("THE COLLATZ CONJECTURE")
    print("=" * 60)
    print()

    print("The rules:")
    print("  If n is even: n → n/2")
    print("  If n is odd:  n → 3n+1")
    print()
    print("The conjecture: Every positive integer eventually reaches 1.")
    print("The status: Unproven after 85+ years.")
    print()

    # Show a few sequences
    for n in [7, 27, 97]:
        seq = collatz_sequence(n)
        print(f"Starting from {n}:")
        print(f"  Sequence length: {len(seq)}")
        print(f"  Max value: {max(seq):,}")

        if len(seq) <= 20:
            print(f"  Path: {' → '.join(map(str, seq))}")
        else:
            print(f"  Path: {' → '.join(map(str, seq[:10]))} → ... → 1")
        print()

    print("-" * 60)
    print("27 is famous. Watch it climb and fall:")
    print("-" * 60)
    print()
    print(render_sequence_ascii(collatz_sequence(27)))
    print()

    print("-" * 60)
    print("Record holders (numbers with longest stopping times):")
    print("-" * 60)

    records = find_record_holders(1000)
    for n, st in records[-10:]:
        print(f"  {n}: {st} steps")
    print()

    print("-" * 60)
    print("The mystery remains.")
    print("-" * 60)
    print()
    print("Every number we've checked reaches 1.")
    print("We've checked a lot of numbers.")
    print("We still can't prove it always happens.")
    print()
    print("Simple rules. Unknown behavior.")
    print("Some problems are just hard.")
    print()


def interactive():
    """
    Explore on your own.
    """
    print("Enter a positive integer to see its Collatz sequence.")
    print("Enter 'q' to quit.")
    print()

    while True:
        try:
            user_input = input("> ")
            if user_input.lower() == 'q':
                break

            n = int(user_input)
            if n < 1:
                print("Please enter a positive integer.")
                continue

            seq = collatz_sequence(n)
            max_val, max_step = max_value_reached(n)

            print(f"\nStarting from {n:,}:")
            print(f"  Steps to reach 1: {len(seq) - 1}")
            print(f"  Maximum value: {max_val:,} (at step {max_step})")
            print()
            print(render_sequence_ascii(seq))
            print()

        except ValueError:
            print("Please enter a valid integer or 'q' to quit.")
        except KeyboardInterrupt:
            break

    print("\nGoodbye.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        interactive()
    else:
        demo()
