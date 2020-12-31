grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'

test1 = dict(zip(boxes, [(s if s != '.' else '123456789') for s in grid]))
display(test1)

eliminate(test1)
display(test1)

only_choice(test1)
display(test1)

reduce_puzzle(test1)

# Harder puzzle

grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'

test2 = grid_values(grid2)

display(test2)

top_search(test2)

reduce_puzzle(test2)

display(test2)

grid3 = '....32.....4...23...6871.9...2..7.1.1...5...6.4.1..3...1.3847...23...6.....72....'
grid4 = '.5.6..7..3.6.8..1.....17.4..4...6..1....9....8..1...3..1.86.....8..7.2.4..5..2.6.'

test3 = grid_values(grid3)

display(test3)

reduce_puzzle(test3)

display(test3)

grid4 = '.5.6..7..3.6.8..1.....17.4..4...6..1....9....8..1...3..1.86.....8..7.2.4..5..2.6.'

test4 = grid_values(grid4)

display(test4)

reduce_puzzle(test4)

display(test4)

gridNov30 = '8...3..47.6.8...3....9.5....2...6.9.1.4.....6.5.....1....4.3........2.8.3...7...9'

testNov30 = grid_values(gridNov30)

display(testNov30)

reduce_puzzle(testNov30)

display(testNov30)