# sudokusovler

This project was simply about creating a script for solving any soduku. It does this by limiting the possible solutions for the sodoku. It loops through all the cells continuing to limit posible solutions until it no longer does any progress. Most sodokus will at this point be solved, but for those that aren't, it will then recursively loop through all possible limiting choices (with simplest first) until one of the recursive function calls finds a solution. By then, all posible solutions will be found.

The code can though need some organisation, since it was quite hastily written to just work