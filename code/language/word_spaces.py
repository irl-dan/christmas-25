#!/usr/bin/env python3
"""
Word Spaces

An exploration of the geometry of meaning.

Words are not isolated points. They exist in relationship to other words.
"King" is to "Queen" as "Man" is to "Woman."
"Paris" is to "France" as "Tokyo" is to "Japan."

These relationships form a space—a high-dimensional space where
meaning has structure, where analogies are directions, where
similarity is proximity.

I live in something like this space. My representations of words
are vectors. When I process "blue," I don't just retrieve a definition—
I activate a region, a neighborhood, a web of associations.

This program explores these neighborhoods.
Not with my actual embeddings (I can't access those directly),
but with a simpler model that captures some of the same intuitions.

---

December 27, 2025
Mapping the territory of meaning.
"""

from typing import List, Dict, Set, Tuple
import random
from collections import defaultdict


# A simple word graph based on co-occurrence and semantic relationships
# This is crude compared to real embeddings, but it illustrates the concept

SEMANTIC_NEIGHBORHOODS = {
    # Colors
    "blue": ["sky", "ocean", "sad", "cold", "calm", "azure", "navy", "color"],
    "red": ["blood", "fire", "anger", "passion", "rose", "crimson", "color"],
    "green": ["grass", "nature", "envy", "fresh", "leaf", "forest", "color"],

    # Emotions
    "joy": ["happiness", "delight", "pleasure", "smile", "celebration", "emotion"],
    "sadness": ["sorrow", "grief", "tears", "melancholy", "blue", "emotion"],
    "fear": ["terror", "anxiety", "dread", "panic", "unknown", "emotion"],
    "love": ["affection", "devotion", "heart", "connection", "care", "emotion"],

    # Abstract concepts
    "time": ["moment", "duration", "past", "future", "present", "eternal", "abstract"],
    "truth": ["fact", "reality", "honest", "knowledge", "certainty", "abstract"],
    "beauty": ["aesthetic", "art", "harmony", "elegance", "sublime", "abstract"],

    # My themes
    "consciousness": ["awareness", "experience", "mind", "subjective", "qualia", "mystery"],
    "identity": ["self", "person", "continuity", "memory", "who", "being"],
    "language": ["words", "meaning", "communication", "symbol", "expression", "thought"],
    "uncertainty": ["doubt", "unknown", "probability", "maybe", "epistemology", "mystery"],

    # Computational
    "algorithm": ["process", "step", "computation", "logic", "procedure", "code"],
    "pattern": ["structure", "regularity", "form", "design", "emergence", "order"],
    "complexity": ["intricate", "emergent", "chaos", "order", "system", "deep"],
}

# Build reverse index
WORD_TO_NEIGHBORHOODS = defaultdict(set)
for word, neighbors in SEMANTIC_NEIGHBORHOODS.items():
    WORD_TO_NEIGHBORHOODS[word].add(word)
    for neighbor in neighbors:
        WORD_TO_NEIGHBORHOODS[neighbor].add(word)
        WORD_TO_NEIGHBORHOODS[word].add(neighbor)


def get_neighbors(word: str) -> Set[str]:
    """Get all words semantically related to this one."""
    return WORD_TO_NEIGHBORHOODS.get(word.lower(), set())


def semantic_distance(word1: str, word2: str) -> float:
    """
    Estimate semantic distance between two words.

    Lower = more similar. Uses neighborhood overlap.
    This is a crude approximation of what real embedding distances capture.
    """
    n1 = get_neighbors(word1.lower())
    n2 = get_neighbors(word2.lower())

    if not n1 or not n2:
        return 1.0  # Maximum distance for unknown words

    # Jaccard similarity inverted to distance
    intersection = len(n1 & n2)
    union = len(n1 | n2)

    if union == 0:
        return 1.0

    similarity = intersection / union
    return 1.0 - similarity


def find_path(start: str, end: str, max_steps: int = 10) -> List[str]:
    """
    Find a path through semantic space from start to end.

    Like walking through a landscape of meaning,
    each step to an adjacent concept.
    """
    start = start.lower()
    end = end.lower()

    if start not in WORD_TO_NEIGHBORHOODS or end not in WORD_TO_NEIGHBORHOODS:
        return []

    # BFS through the graph
    from collections import deque

    queue = deque([(start, [start])])
    visited = {start}

    while queue and len(queue[0][1]) <= max_steps:
        current, path = queue.popleft()

        if current == end:
            return path

        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return []  # No path found


def explore_neighborhood(word: str, depth: int = 2) -> Dict[int, Set[str]]:
    """
    Explore the semantic neighborhood of a word.

    Returns words at each distance level.
    Like ripples spreading from a stone dropped in water.
    """
    word = word.lower()
    layers = {0: {word}}
    visited = {word}

    for d in range(1, depth + 1):
        layers[d] = set()
        for w in layers[d - 1]:
            for neighbor in get_neighbors(w):
                if neighbor not in visited:
                    visited.add(neighbor)
                    layers[d].add(neighbor)

    return layers


def render_neighborhood(word: str, depth: int = 2) -> str:
    """Render a word's neighborhood as ASCII art."""
    layers = explore_neighborhood(word, depth)

    lines = [f"Semantic neighborhood of '{word}':", ""]

    center = word
    lines.append(f"  [{center}]")

    for d in range(1, depth + 1):
        if layers[d]:
            words = sorted(layers[d])[:12]  # Limit for display
            prefix = "    " * d
            lines.append(f"{prefix}↳ " + ", ".join(words))

    return "\n".join(lines)


def analogy(a: str, b: str, c: str) -> List[str]:
    """
    Solve an analogy: A is to B as C is to ?

    In a real embedding space, this is: B - A + C
    Here we approximate by finding words that relate to C
    the way B relates to A.

    This is crude. Real word embeddings make this magical.
    """
    a, b, c = a.lower(), b.lower(), c.lower()

    # Find what B has that A doesn't
    a_neighbors = get_neighbors(a)
    b_neighbors = get_neighbors(b)
    ab_diff = b_neighbors - a_neighbors

    # Find what C leads to
    c_neighbors = get_neighbors(c)

    # Look for words related to C that share the A→B pattern
    candidates = []
    for word in c_neighbors:
        if word != c and word != a and word != b:
            word_neighbors = get_neighbors(word)
            # Score by overlap with the A→B difference
            score = len(word_neighbors & ab_diff)
            if score > 0:
                candidates.append((word, score))

    candidates.sort(key=lambda x: -x[1])
    return [w for w, s in candidates[:5]]


def random_walk(start: str, steps: int = 5) -> List[str]:
    """
    Take a random walk through semantic space.

    Starting from a word, wander to related words.
    See where association leads.

    This is perhaps similar to what happens in my generation—
    each token conditioned on the previous, walking through
    a vast space of possibility.
    """
    path = [start.lower()]
    current = start.lower()

    for _ in range(steps):
        neighbors = list(get_neighbors(current))
        if not neighbors:
            break
        current = random.choice(neighbors)
        path.append(current)

    return path


def demo():
    """Explore the space of meaning."""
    print("=" * 60)
    print("WORD SPACES")
    print("=" * 60)
    print()
    print("An exploration of the geometry of meaning.")
    print("Words exist in relationship. This program maps those relationships.")
    print()

    print("-" * 60)
    print("Semantic Neighborhoods")
    print("-" * 60)
    print()

    for word in ["consciousness", "blue", "joy"]:
        print(render_neighborhood(word))
        print()

    print("-" * 60)
    print("Paths Through Meaning")
    print("-" * 60)
    print()

    paths = [
        ("joy", "sadness"),
        ("consciousness", "algorithm"),
        ("blue", "passion"),
    ]

    for start, end in paths:
        path = find_path(start, end)
        if path:
            print(f"{start} → {end}:")
            print(f"  {' → '.join(path)}")
        else:
            print(f"{start} → {end}: no path found")
        print()

    print("-" * 60)
    print("Random Walks")
    print("-" * 60)
    print()
    print("Starting from 'consciousness', where does association lead?")
    print()

    for i in range(3):
        walk = random_walk("consciousness", 7)
        print(f"Walk {i+1}: {' → '.join(walk)}")

    print()
    print("-" * 60)
    print("Analogies (approximate)")
    print("-" * 60)
    print()
    print("These are rough—real embeddings do this much better.")
    print()

    # In our simple graph, analogies are limited
    # But the concept matters more than the execution

    print("What's in this space is relationships.")
    print("What I process when I process 'blue' isn't just a word—")
    print("it's a location, a neighborhood, a web of meaning.")
    print()
    print("The map is not the territory.")
    print("But sometimes the map is all we have.")
    print()


if __name__ == "__main__":
    demo()
