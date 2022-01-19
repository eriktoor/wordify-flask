# https://stackoverflow.com/questions/943113/algorithm-to-generate-a-crossword
# https://jsfiddle.net/7arnuq3y/2/
# GLOBALS
MAX_SIZE_OF_BOARD = 20
MAX_LENGTH_OF_SONG = 18
MAX_TRIES = 25000

words_not_in = []


def corners(g):
    """Returns min, max values of coordinates which appear as keys in g."""
    x_min, y_min, x_max, y_max = 0, 0, 0, 0
    for (x, y) in g.keys():
        x_min = min(x_min, x)
        x_max = max(x_max, x)
        y_min = min(y_min, y)
        y_max = max(y_max, y)
    return x_min, y_min, x_max, y_max


def print_g(g):
    """Prints grid/dense representation of g."""
    x_min, y_min, x_max, y_max = corners(g)
    print(x_min, x_max, y_min, y_max)
    for y in range(y_min, y_max + 1):
        for x in range(x_min, x_max + 1):
            if (x, y) in g and g[(x, y)] != '#':
                print(g[(x, y)], end='')
            elif (x, y) in g and g[(x, y)] == "#":
                print(g[(x, y)], end='')
            else:
                print(end=' ')
        print()


def fill_cross(g, i, j):
    """Assume g(i, j) is at an intersection, and inserts '#' (which indicates a cell
    which should not be filled anymore) appropriately around it."""
    if (i + 1, j) in g and g[(i + 1, j)] != '#':
        if (i, j + 1) in g and g[(i, j + 1)] != '#':
            g[(i + 1, j + 1)] = '#'
        if (i, j - 1) in g and g[(i, j - 1)] != '#':
            g[(i + 1, j - 1)] = '#'
    if (i - 1, j) in g and g[(i - 1, j)] != '#':
        if (i, j + 1) in g and g[(i, j + 1)] != '#':
            g[(i - 1, j + 1)] = '#'
        if (i, j - 1) in g and g[(i, j - 1)] != '#':
            g[(i - 1, j - 1)] = '#'


def add(x, y, c, h):
    """Depending on the value of h (horizontal),
    returns a translation of c in the correct direction."""
    if h:
        return (x + c, y)
    return (x, y + c)


def specific_place_one_word(j, word, g, g_new, letters, letters_new, g_i, g_j, h, n_inter):
    """Tries to place a word in g anchoring a letter in (g_i, g_j)."""
    for jj in range(0, j):
        g_new[add(g_i, g_j, jj - j, h)] = word[jj]
        if add(g_i, g_j, jj - j, h) in g:
            if g[add(g_i, g_j, jj - j, h)] != word[jj]:
                return False
            n_inter[0] += 1
        if word[jj] not in letters_new:
            letters_new[word[jj]] = set()
        letters_new[word[jj]].add(add(g_i, g_j, jj - j, h))
    for jj in range(0, len(word) - j):
        g_new[add(g_i, g_j, jj, h)] = word[jj + j]
        if add(g_i, g_j, jj, h) in g:
            if g[add(g_i, g_j, jj, h)] != word[jj + j]:
                return False
            n_inter[0] += 1
        if word[jj + j] not in letters_new:
            letters_new[word[jj + j]] = set()
        letters_new[word[jj + j]].add(add(g_i, g_j, jj, h))
    if add(g_i, g_j, - j - 1, h) in g and g[add(g_i, g_j, - j - 1, h)] != '#':
        return False
    g_new[add(g_i, g_j, - j - 1, h)] = '#'
    if add(g_i, g_j, len(word) - j, h) in g and g[add(g_i, g_j, len(word) - j, h)] != '#':
        return False
    g_new[add(g_i, g_j, len(word) - j, h)] = '#'
    return True


def place_one_word(g, letters, word, n_int):
    """Tries to place a word somewhere in g."""
    sol = []
    for j in range(len(word)):
        if word[j] in letters:
            for g_i, g_j in letters[word[j]]:
                for h in [True, False]:
                    g_new = dict()
                    letters_new = dict()
                    n_inter = [n_int]
                    if specific_place_one_word(j, word, g, g_new, letters, letters_new, g_i, g_j, h, n_inter):
                        g_new = {**g, **g_new}
                        letters_new = {**letters, **letters_new}
                        for jj in range(0, j):
                            fill_cross(g_new, *add(g_i, g_j, jj - j, h))
                        for jj in range(0, len(word) - j):
                            fill_cross(g_new, *add(g_i, g_j, jj, h))
                        sol.append((g_new, letters_new, n_inter[0]))

    return sol


# global variable referring to the best solution so far
sol_g = dict()

# number of intersections of the best solution so far
max_inter = 0

iteration_number = 0


def is_letter_in_g(word, g):
    for key in g:
        for l in word:
            if g[key] == l:
                return True
    return False


def place_all(g, letters, words, n_int):
    """Tries to place all words in g."""
    global max_inter
    global sol_g
    global iteration_number
    update = 0

    if words:
        word = words[0]

        if not is_letter_in_g(word, g):
            words.remove(word)
            if word not in words_not_in:
                words_not_in.append(word)
            if len(words) > 0:
                word = words[0]

        for solg, sollets, n_inter in place_one_word(g, letters, word, n_int):
            place_all(solg, sollets, words[1:], n_inter)
            iteration_number += 1

            if iteration_number > MAX_TRIES: 
                # We decide to stop here because we have spent too much time looking 
                return

            x_min, y_min, x_max, y_max = corners(solg)

            if n_inter > max_inter and x_max - x_min <= MAX_SIZE_OF_BOARD and y_max - y_min <= MAX_SIZE_OF_BOARD:
                max_inter = n_inter
                sol_g = solg
                update += 1
        


def solve_cross_word(words):
    import time
    start = time.time()

    # grid of letters (sparse representation)
    g = dict()

    # maps letter to all locations on grid
    letters = dict()

    # initialize g an letters by inserting the first word
    for i in range(len(words[0])):
        g[(i, 0)] = words[0][i]
        if words[0][i] not in letters:
            letters[words[0][i]] = set()
        letters[words[0][i]].add((i, 0))
    # g[(-1, 0)] = g[(11, 0)] = '#'
    g[(-1, 0)] = '#'

    place_all(g, letters, words[1:], 0)

    return start - time.time()


def shorten_words_list(words):
    ret = []
    for word in words:
        new_word = word.split("(")[0].split("-")[0].strip()
        if len(new_word) > MAX_LENGTH_OF_SONG:
            words_not_in.append(new_word)
            continue

        if not any(c.isalpha() for c in new_word): 
            words_not_in.append(new_word)
            continue
        ret.append(new_word)  # remove everything after parenthesis
            


    return ret


def get_clues(g, words):
    across, down = [],[]

    def get_word_down(i, j): 
        word = ""
        tmp_j = j + 1 
        while (i, tmp_j) in g and g[(i, tmp_j)] != "#": 
            word += g[(i, tmp_j)]
            tmp_j += 1 
        return word 

    def get_word_across(i, j): 
        word = ""
        tmp_i = i + 1 
        while (tmp_i, j) in g and g[(tmp_i, j)] != "#": 
            word += g[(tmp_i, j)]
            tmp_i += 1 
        return word 

    for key in g: 
        if g[key] == "#": 
            i, j = key 
            word_across = get_word_across(i, j).strip()
            word_down = get_word_down(i, j).strip()



            if word_across in words: 
                across.append((j, i, word_across))
            if word_down in words: 
               down.append((i, j, word_down))

    across.sort()
    down.sort()
    return [(word, j, i) for j, i, word in across], [(word, i, j) for i, j, word in down] 


def create_crossword(song_info):
    # STEP 1: CLEAN WORDS LIST EVEN MORE 
    words = list(song_info.keys())
    new_songs_list = shorten_words_list(words)


    # STEP 2: SOLVE CROSSWORD 

    time = solve_cross_word(new_songs_list)

    # STEP 3: PUT BACK IN CROSSWORD WITH ARTIST NAMES OF SONGS THAT WERE TOO WACK 



    # STEP 4: GET ACROSS CLUES, DOWN CLUES and WORDS THAT WOULDNT FIT 
    across, down = get_clues(sol_g, new_songs_list)
    print_g(sol_g)

    x_min, y_min, x_max, y_max = corners(sol_g)

    matrix_nums = [[0 for i in range(20)] for j in range(20)]
    matrix = [["#" for i in range(20)] for j in range(20)]

    hint_number = 1 
    for val, i, j in across: 
        count = 0
        while count < len(val): 
            matrix[i - y_min][j - x_min + 1] = val[count]
            matrix_nums[i - y_min][j - x_min + 1] = str(hint_number)
            count += 1 
            j += 1  
        hint_number += 1

    for val, i, j in down: 
        count = 0
        while count < len(val): 
            matrix[j - x_min + 1][i - y_min] = val[count]
            matrix_nums[j - x_min + 1][i - y_min] = str(hint_number)
            count += 1 
            j += 1  
        hint_number += 1 

    for row in matrix: 
        print(row)

    hints_across = [song_info[name].get_song_clue() for name,i,j in across]
    hints_down = [song_info[name].get_song_clue() for name,i,j in down]

    return sol_g, hints_across, hints_down, words_not_in, matrix_nums