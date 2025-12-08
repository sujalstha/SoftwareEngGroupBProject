# I chose CWE-787, Out-of-Bounds Write.
# My part of the project was building the UI flow (Start Screen → Name Entry →
# Difficulty Selection → Level Progress). Although Tkinter and Python handle
# memory safely compared to C/C++, out-of-bounds issues can still appear at the
# *logic level* when user input or UI components are not validated or when the
# program writes to unexpected places.

# Examples of where CWE-787 *could* happen in this UI:
#   1. Taking a username of unlimited length and blindly writing it into the
#      database or updating labels. Without bounds checks, extremely long names
#      would overflow UI components, crash the program, or corrupt state.
#
#   2. Destroying widgets incorrectly. If I removed widgets in the wrong order,
#      or referenced widgets after deletion, the UI could "write" into an invalid
#      state — the Tkinter equivalent of writing past the end of a buffer.
#
#   3. Updating player levels without restricting the range. A user could
#      trigger inconsistent or invalid writes (e.g., negative level or huge
#      values), which is a form of logical out-of-bounds write.
#
# Below is a simplified vulnerable version showing the type of mistake CWE-787
# refers to in UI programs.

def unsafe_set_username(screen, name):
    # ❌ Vulnerable example: no validation, writes unbounded data into UI
    screen.title_label.config(text=name)  # could crash if name is huge
    db.execute(f"INSERT INTO players VALUES('{name}', 1)")  # unsafe & unbounded


# Here is the safer version I actually implemented.

def safe_set_username(screen, name, db):
    # Trim whitespace
    cleaned = name.strip()

    # Proper bounds checking: enforce non-empty, reasonable length
    if not cleaned:
        screen.error_label.config(text="Please enter your name.")
        return
    if len(cleaned) > 40:
        screen.error_label.config(text="Name too long.")
        return

    # Safe DB write using parameter binding
    level = db.get_or_create_player(cleaned)

    # Safe UI update
    screen.title_label.config(text=f"Welcome, {cleaned}!")

    return level


# In summary:
# My UI code avoided CWE-787 by (1) validating input sizes, (2) preventing
# invalid widget access after destruction, and (3) strictly controlling how
# state (level, difficulty, name) is written to the UI and database. Without
# these checks, the app could easily write data into "out-of-bounds" UI states
# or corrupt persistent data — the Python/Tkinter equivalent of a buffer write.
