from dice_patterns import Pattern

BOARD = [
    [Pattern.STRAIGHT, Pattern.DOUBLE(6,6), Pattern.DOUBLE(5,6), Pattern.DOUBLE(4,6), 
     Pattern.PAIR(2), Pattern.DOUBLE(3,6), Pattern.DOUBLE(2,6), Pattern.DOUBLE(1,6), Pattern.STRAIGHT],
    [Pattern.PAIR(6), Pattern.FULL_HOUSE, Pattern.DOUBLE(1,5), Pattern.DOUBLE(2,5), Pattern.DOUBLE(3,5),
     Pattern.DOUBLE(4,5), Pattern.DOUBLE(5,5), Pattern.FULL_HOUSE, Pattern.PAIR(4)],
    [],
    [],
    [],
    [],
    [],
    [],
    []
]