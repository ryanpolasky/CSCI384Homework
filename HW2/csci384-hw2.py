# Written by Ryan Polasky - 2/26/25

import itertools
import random

def solve_zebra():
    houses = (1, 2, 3, 4, 5)
    orderings = list(itertools.permutations(houses))
    # Each ordering assigns a house position (1-5) for each attribute.
    for (red, green, white, yellow, blue) in orderings:
        # Constraint 4: white is immediately left of yellow.
        if white + 1 != yellow:
            continue
        for (British, Swedish, Danish, Norwegian, German) in orderings:
            # Constraint 9: German lives in the first house.
            if German != 1:
                continue
            # Constraint 14: German lives next to the red house.
            if abs(German - red) != 1:
                continue
            # Constraint 1: Swedish lives in the green house.
            if Swedish != green:
                continue
            for (dog, bird, horse, cat, raccoon) in orderings:
                # Constraint 2: Danish keeps dogs.
                if Danish != dog:
                    continue
                for (tea, coffee, milk, beer, water) in orderings:
                    # Constraint 8: center house drinks milk.
                    if milk != 3:
                        continue
                    # Constraint 3: Norwegian drinks tea.
                    if Norwegian != tea:
                        continue
                    # Constraint 5: White house’s owner drinks coffee.
                    if white != coffee:
                        continue
                    for (Prince, PallMall, Dunhill, Blend, Bluemaster) in orderings:
                        # Constraint 13: British smokes Prince.
                        if British != Prince:
                            continue
                        # Constraint 7: Owner of the blue house smokes Dunhill.
                        if blue != Dunhill:
                            continue
                        # Constraint 6: The person who smokes Pall Mall rears birds.
                        if PallMall != bird:
                            continue
                        # Constraint 10: The man who smokes Blend lives next to the one who keeps cats.
                        if abs(Blend - cat) != 1:
                            continue
                        # Constraint 11: The man who keeps the horse lives next to the one who smokes Dunhill.
                        if abs(horse - Dunhill) != 1:
                            continue
                        # Constraint 12: The owner who smokes Bluemaster drinks beer.
                        if Bluemaster != beer:
                            continue
                        # Constraint 15: The man who smokes Blend has a neighbor who drinks water.
                        if abs(Blend - water) != 1:
                            continue

                        # If all constraints are met, return the solution as a dictionary.
                        return {
                            "color": {"red": red, "green": green, "white": white, "yellow": yellow, "blue": blue},
                            "nationality": {"British": British, "Swedish": Swedish, "Danish": Danish, "Norwegian": Norwegian, "German": German},
                            "pet": {"dog": dog, "bird": bird, "horse": horse, "cat": cat, "raccoon": raccoon},
                            "beverage": {"tea": tea, "coffee": coffee, "milk": milk, "beer": beer, "water": water},
                            "cigarette": {"Prince": Prince, "Pall Mall": PallMall, "Dunhill": Dunhill, "Blend": Blend, "Bluemaster": Bluemaster}
                        }

print("===========================================================")
print("Q2. Zebra Logic Puzzle")
solution_zebra = solve_zebra()
if solution_zebra:
    print("Solution:")
    for category, mapping in solution_zebra.items():
        print(f"{category.capitalize()}:")
        for item, pos in mapping.items():
            print(f"-- {item}: House {pos}")
else:
    print("No solution found for the Zebra Puzzle.")
print("===========================================================\n")

# Above is Q2, below is Q3 #########################################################################################

initial_state = {
    'C': 2, 'P': 3, 'I': 5, 'S': 4, 'F': 9, 'U': 6,
    'N': 8, 'T': 1, 'R': 0, 'E': 7
}

variables = list(initial_state.keys())


def evaluate(state):
    CP = 10 * state['C'] + state['P']
    IS = 10 * state['I'] + state['S']
    FUN = 100 * state['F'] + 10 * state['U'] + state['N']
    TRUE = 1000 * state['T'] + 100 * state['R'] + 10 * state['U'] + state['E']
    return CP + IS + FUN - TRUE


def conflicts(state):
    value_counts = {}
    conflicts_count = 0
    for var, value in state.items():
        if value in value_counts:
            value_counts[value] += 1
        else:
            value_counts[value] = 1
    for value in value_counts:
        if value_counts[value] > 1:
            conflicts_count += value_counts[value] - 1
    return conflicts_count


def most_conflicted_variable(state):
    conflict_counts = {var: 0 for var in variables}
    seen_values = {}

    for var, value in state.items():
        if value in seen_values:
            conflict_counts[var] += 1
            conflict_counts[seen_values[value]] += 1
        seen_values[value] = var

    equation_error = abs(evaluate(state))

    for var in variables:
        contribution = abs(evaluate({**state, var: (state[var] + 1) % 10})) - equation_error
        conflict_counts[var] += contribution * 2

    return max(conflict_counts, key=conflict_counts.get)


def min_conflict():
    state = initial_state.copy()

    for step in range(500):  # Max 500 steps
        if evaluate(state) == 0 and conflicts(state) == 0:
            return state

        var = most_conflicted_variable(state)
        best_value = state[var]
        best_conflict = float('inf')

        available_values = set(range(10)) - set(state.values())  # Avoid duplicates
        if not available_values:
            available_values = set(range(10))

        for value in available_values:
            state[var] = value
            current_conflict = abs(evaluate(state)) + conflicts(state)

            if current_conflict < best_conflict:
                best_conflict = current_conflict
                best_value = value

        state[var] = best_value

    return None


solution_crypto = min_conflict()

print("===========================================================")
print("Q3. Cryptarithmetic Puzzle - Min-Conflict Algorithm")
if solution_crypto:
    print("\nSolution:")
    for var in sorted(solution_crypto.keys()):
        print(f"{var} = {solution_crypto[var]}")
    CP = 10 * solution_crypto['C'] + solution_crypto['P']
    IS = 10 * solution_crypto['I'] + solution_crypto['S']
    FUN = 100 * solution_crypto['F'] + 10 * solution_crypto['U'] + solution_crypto['N']
    TRUE = 1000 * solution_crypto['T'] + 100 * solution_crypto['R'] + 10 * solution_crypto['U'] + solution_crypto['E']
    print(f"\nVerification: {CP} + {IS} + {FUN} = {TRUE}")
else:
    print("No solution found after 500 steps.")
print("===========================================================")