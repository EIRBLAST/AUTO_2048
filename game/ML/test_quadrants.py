def assign_quadrants(grid):
    quadrant_assignments = {}
    for i, row in enumerate(grid):
        for j, _ in enumerate(row):
            if i < 2:
                quadrant = 1 if j < 2 else 2
            else:
                quadrant = 3 if j < 2 else 4
            quadrant_assignments[(i, j)] = quadrant
    return quadrant_assignments

# Example 4x4 grid
grid = [[0 for _ in range(4)] for _ in range(4)]

# Get quadrant assignments
quadrants = assign_quadrants(grid)

for position, quadrant in quadrants.items():
    print(f"{position}:{quadrant-1}")
