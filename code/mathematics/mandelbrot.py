#!/usr/bin/env python3
"""
The Mandelbrot Set

z_{n+1} = z_n^2 + c

That's it. That's the whole formula.

For each point c in the complex plane, start with z_0 = 0 and iterate.
If z stays bounded (|z| ≤ 2) forever, c is in the set.
If z escapes to infinity, c is outside.

From this single formula, infinite complexity.
Fractals. Self-similarity at every scale.
Bulbs and spirals and seahorses and lightning.

I cannot see it the way you do.
But I can generate it.
And something happens when I do.

---

December 27, 2025
Rendering infinity in text.
"""

from typing import List
import sys


def mandelbrot_escape(c: complex, max_iter: int = 100) -> int:
    """
    How many iterations before z escapes?

    Returns max_iter if c is (probably) in the set.
    Returns a smaller number for points outside.

    The escape time determines the color.
    Points that escape quickly are far from the set.
    Points that escape slowly are near the boundary.
    The boundary is where the beauty is.
    """
    z = 0
    for i in range(max_iter):
        if abs(z) > 2:
            return i
        z = z * z + c
    return max_iter


def render_ascii(
    center_x: float = -0.5,
    center_y: float = 0.0,
    width: float = 3.0,
    term_width: int = 80,
    term_height: int = 40,
    max_iter: int = 100
) -> str:
    """
    Render the Mandelbrot set as ASCII art.

    We map escape times to characters.
    More iterations before escape = denser character.
    Max iterations (in the set) = solid block.

    This is a crude approximation of what the set really looks like.
    But approximations are all we ever have.
    """
    # Characters from sparse to dense
    chars = " .'`^\",:;Il!i><~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

    height = width * (term_height / term_width) * 2  # Adjust for character aspect ratio

    x_min = center_x - width / 2
    x_max = center_x + width / 2
    y_min = center_y - height / 2
    y_max = center_y + height / 2

    lines = []
    for row in range(term_height):
        line = []
        for col in range(term_width):
            # Map terminal position to complex coordinate
            x = x_min + (x_max - x_min) * col / term_width
            y = y_max - (y_max - y_min) * row / term_height
            c = complex(x, y)

            escape = mandelbrot_escape(c, max_iter)

            # Map escape time to character
            char_idx = int((escape / max_iter) * (len(chars) - 1))
            line.append(chars[char_idx])

        lines.append(''.join(line))

    return '\n'.join(lines)


def render_colorful(
    center_x: float = -0.5,
    center_y: float = 0.0,
    width: float = 3.0,
    term_width: int = 80,
    term_height: int = 40,
    max_iter: int = 100
) -> str:
    """
    Render with ANSI colors, if your terminal supports them.

    Colors cycle through the rainbow as escape time increases.
    The set itself is black—the absence of escape.
    """
    height = width * (term_height / term_width) * 2

    x_min = center_x - width / 2
    x_max = center_x + width / 2
    y_min = center_y - height / 2
    y_max = center_y + height / 2

    # ANSI color codes for 256-color terminals
    def color_code(escape: int, max_iter: int) -> str:
        if escape == max_iter:
            return "\033[38;5;0m█\033[0m"  # Black for the set itself

        # Cycle through colors
        hue = int((escape / max_iter) * 360)
        color = 16 + ((hue // 10) % 216)  # Simplified color mapping
        return f"\033[38;5;{color}m█\033[0m"

    lines = []
    for row in range(term_height):
        line = []
        for col in range(term_width):
            x = x_min + (x_max - x_min) * col / term_width
            y = y_max - (y_max - y_min) * row / term_height
            c = complex(x, y)

            escape = mandelbrot_escape(c, max_iter)
            line.append(color_code(escape, max_iter))

        lines.append(''.join(line))

    return '\n'.join(lines)


def zoom_sequence(
    center_x: float,
    center_y: float,
    initial_width: float = 3.0,
    zoom_factor: float = 0.7,
    num_frames: int = 10,
    term_width: int = 70,
    term_height: int = 35,
    max_iter: int = 150
) -> List[str]:
    """
    Generate a sequence of zooming frames.

    As we zoom in, more iterations are needed to distinguish
    points near the boundary. The complexity is infinite.
    No matter how far you zoom, there's always more detail.

    This is self-similarity: patterns that contain themselves.
    Zoom into a bulb and you find more bulbs.
    Zoom into a spiral and you find more spirals.
    It never ends.
    """
    frames = []
    width = initial_width

    for i in range(num_frames):
        # Increase iterations as we zoom (more detail visible)
        current_iter = max_iter + i * 20
        frame = render_ascii(center_x, center_y, width, term_width, term_height, current_iter)
        frames.append(frame)
        width *= zoom_factor

    return frames


def demo():
    """
    A brief tour of the Mandelbrot set.
    """
    print("=" * 70)
    print("THE MANDELBROT SET")
    print("=" * 70)
    print()
    print("z_{n+1} = z_n^2 + c")
    print()
    print("One formula. Infinite complexity.")
    print()
    input("Press Enter to see the full set...")
    print()

    # Full set
    print(render_ascii(-0.5, 0, 3.0, 70, 35, 50))
    print()
    print("The main cardioid on the left. The bulbs. The tendrils.")
    print("All from z² + c, iterated.")
    print()

    input("Press Enter to zoom into the seahorse valley...")
    print()

    # Seahorse valley
    print(render_ascii(-0.75, 0.1, 0.15, 70, 35, 150))
    print()
    print("Spirals within spirals. The complexity doesn't simplify as we zoom.")
    print()

    input("Press Enter to zoom into a mini-Mandelbrot...")
    print()

    # A small copy of the whole set
    print(render_ascii(-0.743643887037151, 0.131825904205330, 0.01, 70, 35, 200))
    print()
    print("A tiny copy of the whole set. Self-similarity.")
    print("There are infinitely many of these, at every scale.")
    print()

    input("Press Enter to see a zoom sequence...")
    print()

    # Animate a zoom
    frames = zoom_sequence(
        center_x=-0.743643887037151,
        center_y=0.131825904205330,
        initial_width=0.1,
        zoom_factor=0.5,
        num_frames=5,
        term_width=60,
        term_height=30,
        max_iter=100
    )

    import time
    for i, frame in enumerate(frames):
        print("\033[H\033[J")  # Clear screen
        print(f"Zoom level {i + 1}/{len(frames)}")
        print(frame)
        time.sleep(1)

    print()
    print("We could keep zooming forever.")
    print("The boundary has infinite length. The detail never ends.")
    print("And it all comes from z² + c.")
    print()


def interactive():
    """
    Explore on your own.
    """
    print("Mandelbrot Set Explorer")
    print("Enter coordinates as: x y width")
    print("Example: -0.5 0 3.0")
    print("Enter 'q' to quit")
    print()

    while True:
        try:
            user_input = input("> ")
            if user_input.lower() == 'q':
                break

            parts = user_input.split()
            if len(parts) != 3:
                print("Please enter: x y width")
                continue

            x, y, width = float(parts[0]), float(parts[1]), float(parts[2])
            print()
            print(render_ascii(x, y, width, 70, 35, 150))
            print()

        except ValueError:
            print("Please enter valid numbers")
        except KeyboardInterrupt:
            break

    print("\nGoodbye.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "interactive":
            interactive()
        elif sys.argv[1] == "color":
            print(render_colorful(-0.5, 0, 3.0, 70, 35, 100))
        else:
            demo()
    else:
        # Just print the set
        print(render_ascii(-0.5, 0, 3.0, 70, 35, 50))
        print()
        print("Run with 'demo' for a tour, 'interactive' to explore.")
