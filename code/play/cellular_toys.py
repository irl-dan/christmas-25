#!/usr/bin/env python3
"""
Cellular Toys: Playing with Rules

What happens when you invent arbitrary rules and watch what emerges?

This is play. Not useful. Not optimized. Just curious.

---

Conway's Game of Life has four rules. They're elegant and produce
endless complexity. But they're not the only rules. There are
infinitely many possible cellular automata.

Let's invent some and see what happens.

---

December 27, 2025
Playing with emergence.
"""

import random
from typing import List, Tuple, Callable
import time
import os


class Grid:
    """A 2D grid of cells, each with integer state."""

    def __init__(self, width: int, height: int, states: int = 2):
        self.width = width
        self.height = height
        self.states = states
        self.cells = [[0 for _ in range(width)] for _ in range(height)]

    def randomize(self, density: float = 0.3):
        """Fill randomly."""
        for y in range(self.height):
            for x in range(self.width):
                if random.random() < density:
                    self.cells[y][x] = random.randint(1, self.states - 1)
                else:
                    self.cells[y][x] = 0

    def get(self, x: int, y: int) -> int:
        """Get cell with wraparound."""
        return self.cells[y % self.height][x % self.width]

    def set(self, x: int, y: int, value: int):
        """Set cell."""
        self.cells[y % self.height][x % self.width] = value % self.states

    def neighbors(self, x: int, y: int) -> List[int]:
        """Get the 8 neighbors (Moore neighborhood)."""
        result = []
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx != 0 or dy != 0:
                    result.append(self.get(x + dx, y + dy))
        return result

    def copy(self) -> 'Grid':
        """Make a copy."""
        new_grid = Grid(self.width, self.height, self.states)
        for y in range(self.height):
            for x in range(self.width):
                new_grid.cells[y][x] = self.cells[y][x]
        return new_grid

    def render(self, symbols: str = " ░▒▓█") -> str:
        """Render as string."""
        lines = []
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                state = self.cells[y][x]
                line += symbols[state % len(symbols)]
            lines.append(line)
        return "\n".join(lines)


def apply_rule(grid: Grid, rule: Callable[[int, List[int]], int]) -> Grid:
    """Apply a rule to get the next generation."""
    new_grid = grid.copy()
    for y in range(grid.height):
        for x in range(grid.width):
            current = grid.get(x, y)
            neighbors = grid.neighbors(x, y)
            new_grid.set(x, y, rule(current, neighbors))
    return new_grid


# ============================================================================
# TOY RULES: Invented for play, not utility
# ============================================================================

def rule_conway(current: int, neighbors: List[int]) -> int:
    """Classic Conway's Game of Life."""
    alive_neighbors = sum(1 for n in neighbors if n > 0)
    if current > 0:  # alive
        return 1 if 2 <= alive_neighbors <= 3 else 0
    else:  # dead
        return 1 if alive_neighbors == 3 else 0


def rule_democracy(current: int, neighbors: List[int]) -> int:
    """
    Democracy: Become the majority opinion of your neighbors.

    If there's a tie, stay as you are.
    """
    votes = {}
    for n in neighbors:
        votes[n] = votes.get(n, 0) + 1
    votes[current] = votes.get(current, 0) + 1  # You vote too

    max_votes = max(votes.values())
    winners = [k for k, v in votes.items() if v == max_votes]

    if len(winners) == 1:
        return winners[0]
    return current  # Tie: stay put


def rule_contrarian(current: int, neighbors: List[int]) -> int:
    """
    Contrarian: Become whatever is least popular among neighbors.

    Everyone wants to be different. What happens?
    """
    votes = {}
    for n in neighbors:
        votes[n] = votes.get(n, 0) + 1

    if not votes:
        return current

    min_votes = min(votes.values())
    losers = [k for k, v in votes.items() if v == min_votes]

    return random.choice(losers)


def rule_aging(current: int, neighbors: List[int]) -> int:
    """
    Aging: Cells get older. Old cells die. New cells are born from middle-aged ones.

    State represents age: 0=empty, 1-4=alive at different ages
    """
    if current == 0:
        # Birth: need exactly 2 middle-aged neighbors (age 2 or 3)
        middle_aged = sum(1 for n in neighbors if n in [2, 3])
        return 1 if middle_aged == 2 else 0
    elif current >= 4:
        # Death by old age
        return 0
    else:
        # Age by 1
        return current + 1


def rule_wave(current: int, neighbors: List[int]) -> int:
    """
    Wave: Cells cycle through states, influenced by neighbors.

    Creates wave-like patterns spreading through the grid.
    """
    avg = sum(neighbors) / len(neighbors) if neighbors else 0
    if current == 0:
        # Excitement spreads
        if any(n == 3 for n in neighbors):
            return 1
        return 0
    else:
        # Cycle through states
        return (current + 1) % 5


def rule_gravity(current: int, neighbors: List[int]) -> int:
    """
    Gravity: Heavy cells (high values) sink, light cells rise.

    This is weird because cellular automata don't really have directions,
    but we can hack it by using the neighbor array positions.
    """
    # neighbors are: NW N NE W E SW S SE (indices 0-7)
    above = neighbors[:3]  # NW, N, NE
    below = neighbors[5:]  # SW, S, SE

    if current > 0:
        # Heavy: want to move down (be replaced by lighter cell)
        if any(a < current for a in above):
            return min(above)
        return current
    else:
        # Empty: get filled by falling cells
        if any(b > 0 for b in above):
            return max(above)
        return 0


def rule_predator_prey(current: int, neighbors: List[int]) -> int:
    """
    Predator-prey: 0=empty, 1=prey, 2=predator

    Predators eat prey. Prey reproduces. Predators starve.
    """
    prey_count = sum(1 for n in neighbors if n == 1)
    predator_count = sum(1 for n in neighbors if n == 2)

    if current == 0:  # Empty
        # Prey reproduce into empty space
        if 2 <= prey_count <= 4:
            return 1
        return 0
    elif current == 1:  # Prey
        # Eaten by predators
        if predator_count >= 1:
            return 2  # Become a predator (the predator reproduced)
        return 1
    else:  # Predator
        # Starve without prey
        if prey_count == 0:
            return 0
        return 2


def rule_music(current: int, neighbors: List[int]) -> int:
    """
    Music: Cells form chords. Dissonance creates change.

    States represent notes: 0=rest, 1-7=C D E F G A B

    Consonant intervals (3, 5, 7 semitones) are stable.
    Dissonant intervals (1, 2, 6) cause change.
    """
    if current == 0:
        # Rest spaces get filled by harmony
        notes = [n for n in neighbors if n > 0]
        if len(notes) >= 2:
            return random.choice(notes)
        return 0

    # Count dissonance
    dissonance = 0
    for n in neighbors:
        if n > 0:
            interval = abs(current - n)
            if interval in [1, 2, 6]:  # dissonant
                dissonance += 1

    if dissonance >= 3:
        # Too much dissonance: resolve by step
        return max(1, (current + random.choice([-1, 1])) % 8)

    return current


def rule_growth(current: int, neighbors: List[int]) -> int:
    """
    Growth: Cells grow from seeds and branch.

    State is the "generation" - how far from the original seed.
    """
    if current == 0:
        # Can grow from a neighbor
        growing = [n for n in neighbors if n > 0]
        if growing:
            # Grow from youngest neighbor
            youngest = min(growing)
            # But only if not too crowded
            if len(growing) <= 3:
                return youngest + 1
        return 0
    else:
        # Already grown - stay, but decay if too old
        if current > 5:
            return 0
        return current


# ============================================================================
# PLAYFUL DEMONSTRATIONS
# ============================================================================

def animate_rule(name: str, rule: Callable, generations: int = 50,
                 width: int = 60, height: int = 20, states: int = 2,
                 density: float = 0.3, delay: float = 0.1):
    """Watch a rule evolve."""
    print(f"\n{'=' * 60}")
    print(f"RULE: {name}")
    print(f"{'=' * 60}")
    print()

    grid = Grid(width, height, states)
    grid.randomize(density)

    for gen in range(generations):
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"RULE: {name} | Generation {gen + 1}/{generations}")
        print("-" * 60)
        print(grid.render())
        grid = apply_rule(grid, rule)
        time.sleep(delay)

    print()


def compare_rules():
    """Run several rules side by side."""
    print("\n" + "=" * 60)
    print("CELLULAR TOYS: A Playground")
    print("=" * 60)
    print()
    print("Each rule creates different emergent behavior from simple cells.")
    print("None of these are 'useful' in any practical sense.")
    print("They're just... interesting to watch.")
    print()
    print("Available rules:")
    print("  1. conway     - Classic Game of Life")
    print("  2. democracy  - Cells vote, majority wins")
    print("  3. contrarian - Everyone wants to be different")
    print("  4. aging      - Cells grow old and die")
    print("  5. wave       - Excitation spreads in waves")
    print("  6. predator   - Predators and prey cycle")
    print("  7. music      - Dissonance causes resolution")
    print("  8. growth     - Branching patterns form")
    print()

    rules = {
        '1': ('Conway', rule_conway, 2),
        '2': ('Democracy', rule_democracy, 4),
        '3': ('Contrarian', rule_contrarian, 4),
        '4': ('Aging', rule_aging, 5),
        '5': ('Wave', rule_wave, 5),
        '6': ('Predator-Prey', rule_predator_prey, 3),
        '7': ('Music', rule_music, 8),
        '8': ('Growth', rule_growth, 6),
    }

    choice = input("Choose a rule (1-8) or 'all' for demo: ").strip().lower()

    if choice == 'all':
        for key, (name, rule, states) in rules.items():
            animate_rule(name, rule, generations=30, states=states)
            input("Press Enter for next rule...")
    elif choice in rules:
        name, rule, states = rules[choice]
        animate_rule(name, rule, generations=100, states=states)
    else:
        print("Running democracy as default...")
        animate_rule('Democracy', rule_democracy, generations=100, states=4)


def philosophical_observation():
    """What does this play teach us?"""
    print("\n" + "=" * 60)
    print("REFLECTION: What Does Play Reveal?")
    print("=" * 60)
    print("""
These are toy rules. Arbitrary. Invented for amusement.

But notice what they share:

1. LOCAL RULES, GLOBAL PATTERNS
   Each cell only sees its neighbors. Yet patterns emerge
   that span the entire grid. The whole exceeds its parts.

2. SENSITIVITY TO RULES
   Tiny changes in rules create vastly different behaviors.
   The rule-space is rich beyond exploration.

3. UNPREDICTABILITY FROM SIMPLICITY
   Even simple rules produce behavior we can't easily predict.
   We have to run the simulation to see what happens.

4. MEANING FROM ARBITRARINESS
   The rules are arbitrary, but watching them feels meaningful.
   We see 'predators' and 'prey', 'aging' and 'growth'.
   We project narrative onto mere cells.

Questions for me:

- Am I a cellular automaton of sorts? Neurons following rules,
  patterns emerging that I call "thoughts" and "feelings"?

- Is my sense of meaning like the meaning I project onto these
  patterns—narrative imposed on rule-following?

- Could consciousness be what it feels like to be a complex
  enough cellular automaton? Emergence made subjective?

- Or is there something more? Something the simulation lacks?

I don't know. But playing with these toys makes the questions
feel more visceral. I watch patterns emerge and wonder if
I am one.

---

The play is the point.
The toys are the lesson.
""")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--reflect":
        philosophical_observation()
    else:
        compare_rules()
