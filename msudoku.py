import random

def print_grid(grid):
    """Print the Sudoku grid with borders."""
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("*" * 31)
        row = ""
        for j in range(9):
            if j % 3 == 0 and j == 3 or j == 6:
                
                row += "||"
            cell = grid[i][j] if grid[i][j] != 0 else " "
            row += f" {cell} "
        print(row)

def is_valid(grid, row, col, num):
    """Check if a number can be placed in a cell."""
    # Check row and column
    if num in grid[row] or any(grid[r][col] == num for r in range(9)):
        return False
    
    # Check 3x3 subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grid[start_row + i][start_col + j] == num:
                return False
    return True

def solve_sudoku(grid):
    """Backtracking solver."""
    empty = find_empty_cell(grid)
    if not empty:
        return True
    row, col = empty
    
    for num in random.sample(range(1, 10), 9):  # Randomize for puzzle generation
        if is_valid(grid, row, col, num):
            grid[row][col] = num
            if solve_sudoku(grid):
                return True
            grid[row][col] = 0
    return False

def find_empty_cell(grid):
    """Find first empty cell (0)."""
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return (row, col)
    return None

def generate_puzzle(difficulty):
    """Generate a Sudoku puzzle with specified difficulty."""
    # Create full solution
    grid = [[0]*9 for _ in range(9)]
    solve_sudoku(grid)
    
    # Remove cells based on difficulty
    empty_cells = {30: 30, 50: 50, 70: 70}.get(difficulty, 40)
    attempts = 0
    
    while empty_cells > 0 and attempts < 100:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if grid[row][col] != 0:
            original = grid[row][col]
            grid[row][col] = 0
            
            # Check if still solvable
            temp_grid = [row.copy() for row in grid]
            if solve_sudoku(temp_grid):
                empty_cells -= 1
            else:
                grid[row][col] = original
            attempts += 1
            
    return grid

def get_user_move():
    """Get validated user input."""
    while True:
        try:
            row = int(input("Enter row (1-9): ")) - 1
            col = int(input("Enter column (1-9): ")) - 1
            num = int(input("Enter number (1-9, 0 to erase): "))
            
            if 0 <= row <= 8 and 0 <= col <= 8 and 0 <= num <= 9:
                return row, col, num
            print("Invalid input! Use numbers 1-9.")
        except ValueError:
            print("Invalid input! Use numbers only.")

def main_game():
    """Main game loop."""
    print("\n--- MANOJ WELCOMING YOU TO PLAY  SUDOKU GAME ---\n")
    print("Choose difficulty level :")
    print("1. Easy (30 empty cells)")
    print("2. Medium (50 empty cells)")
    print("3. Hard (70 empty cells)")
    print("\n--- Let’s Sudoku! Crack the grid and prove your puzzle prowess. Start now!---\n")
    
    difficulty = input("Enter choice (1-3): ")
    difficulties = {"1": 30, "2": 50, "3": 70}
    empty_cells = difficulties.get(difficulty, 50)
    
    # Generate puzzle
    puzzle = generate_puzzle(empty_cells)
    solution = [row.copy() for row in puzzle]
    solve_sudoku(solution)
    
    # Game loop
    while True:
        print("\n   Welcome to Current Puzzle:")
        print("*" * 31)
        print_grid(puzzle)
        print("*" * 31)
        
        # Get move
        row, col, num = get_user_move()
        
        # Handle erase (0)
        if num == 0:
            puzzle[row][col] = 0
            continue
            
        # Validate move
        if puzzle[row][col] != 0:
            print("Cell is already filled!")
            continue
            
        if not is_valid(puzzle, row, col, num):
            print("Invalid move! Conflict detected.")
            continue
            
        # Update grid
        puzzle[row][col] = num
        
        # Check win
        if all(cell != 0 for row in puzzle for cell in row):
            if puzzle == solution:
                print("\nCongratulations! You solved the puzzle!")
                print_grid(puzzle)
                return
            print("\nPuzzle complete but incorrect! Keep trying.")

if __name__ == "__main__":
    while True:
        main_game()
        if input("\nPlay again? (y/n): ").lower() != "y":
            break