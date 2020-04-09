hard_table = {
    '2': {
        '9': 'Hit',
        '10': 'Double or Hit',
        '11': 'Double or Hit',
        '12': 'Hit',
        '13': 'Stand',
        '14': 'Stand',
        '15': 'Stand',
        '16': 'Stand'
    },
    '3': {
        '9': 'Double or Hit',
        '10': 'Double or Hit',
        '11': 'Double or Hit',
        '12': 'Hit',
        '13': 'Stand',
        '14': 'Stand',
        '15': 'Stand',
        '16': 'Stand'
    },
    '4': {
        '9': 'Double or Hit',
        '10': 'Double or Hit',
        '11': 'Double or Hit',
        '12': 'Stand',
        '13': 'Stand',
        '14': 'Stand',
        '15': 'Stand',
        '16': 'Stand'
    },
    '5': {
        '9': 'Double or Hit',
        '10': 'Double or Hit',
        '11': 'Double or Hit',
        '12': 'Stand',
        '13': 'Stand',
        '14': 'Stand',
        '15': 'Stand',
        '16': 'Stand'
    },
    '6': {
        '9': 'Double or Hit',
        '10': 'Double or Hit',
        '11': 'Double or Hit',
        '12': 'Stand',
        '13': 'Stand',
        '14': 'Stand',
        '15': 'Stand',
        '16': 'Stand'
    },
    '7': {
        '9': 'Hit',
        '10': 'Double or Hit',
        '11': 'Double or Hit',
        '12': 'Hit',
        '13': 'Hit',
        '14': 'Hit',
        '15': 'Hit',
        '16': 'Hit'
    },
    '8': {
        '9': 'Hit',
        '10': 'Double or Hit',
        '11': 'Double or Hit',
        '12': 'Hit',
        '13': 'Hit',
        '14': 'Hit',
        '15': 'Hit',
        '16': 'Hit'
    },
    '9': {
        '9': 'Hit',
        '10': 'Double or Hit',
        '11': 'Double or Hit',
        '12': 'Hit',
        '13': 'Hit',
        '14': 'Hit',
        '15': 'Hit',
        '16': 'Hit'
    },
    '10': {
        '9': 'Hit',
        '10': 'Hit',
        '11': 'Double or Hit',
        '12': 'Hit',
        '13': 'Hit',
        '14': 'Hit',
        '15': 'Hit',
        '16': 'Hit'
    },
    'A': {
        '9': 'Hit',
        '10': 'Hit',
        '11': 'Double or Hit',
        '12': 'Hit',
        '13': 'Hit',
        '14': 'Hit',
        '15': 'Hit',
        '16': 'Hit'
    }
}

soft_table = {
    '2': {
        'A2': 'Hit',
        'A3': 'Hit',
        'A4': 'Hit',
        'A5': 'Hit',
        'A6': 'Hit',
        'A7': 'Double or Stand',
        'A8': 'Stand',
        'A9': 'Stand',
        'A10': 'Stand'
    },
    '3': {
        'A2': 'Hit',
        'A3': 'Hit',
        'A4': 'Hit',
        'A5': 'Hit',
        'A6': 'Double or Hit',
        'A7': 'Double or Stand',
        'A8': 'Stand',
        'A9': 'Stand',
        'A10': 'Stand'
    },
    '4': {
        'A2': 'Hit',
        'A3': 'Hit',
        'A4': 'Double or Hit',
        'A5': 'Double or Hit',
        'A6': 'Double or Hit',
        'A7': 'Double or Stand',
        'A8': 'Stand',
        'A9': 'Stand',
        'A10': 'Stand'
    },
    '5': {
        'A2': 'Double or Hit',
        'A3': 'Double or Hit',
        'A4': 'Double or Hit',
        'A5': 'Double or Hit',
        'A6': 'Double or Hit',
        'A7': 'Double or Stand',
        'A8': 'Stand',
        'A9': 'Stand',
        'A10': 'Stand'
    },
    '6': {
        'A2': 'Double or Hit',
        'A3': 'Double or Hit',
        'A4': 'Double or Hit',
        'A5': 'Double or Hit',
        'A6': 'Double or Hit',
        'A7': 'Double or Stand',
        'A8': 'Double or Stand',
        'A9': 'Stand',
        'A10': 'Stand'
    },
    '7': {
        'A2': 'Hit',
        'A3': 'Hit',
        'A4': 'Hit',
        'A5': 'Hit',
        'A6': 'Hit',
        'A7': 'Stand',
        'A8': 'Stand',
        'A9': 'Stand',
        'A10': 'Stand'
    },
    '8': {
        'A2': 'Hit',
        'A3': 'Hit',
        'A4': 'Hit',
        'A5': 'Hit',
        'A6': 'Hit',
        'A7': 'Stand',
        'A8': 'Stand',
        'A9': 'Stand',
        'A10': 'Stand'
    },
    '9': {
        'A2': 'Hit',
        'A3': 'Hit',
        'A4': 'Hit',
        'A5': 'Hit',
        'A6': 'Hit',
        'A7': 'Hit',
        'A8': 'Stand',
        'A9': 'Stand',
        'A10': 'Stand'
    },
    '10': {
        'A2': 'Hit',
        'A3': 'Hit',
        'A4': 'Hit',
        'A5': 'Hit',
        'A6': 'Hit',
        'A7': 'Hit',
        'A8': 'Stand',
        'A9': 'Stand',
        'A10': 'Stand'
    },
    'A': {
        'A2': 'Hit',
        'A3': 'Hit',
        'A4': 'Hit',
        'A5': 'Hit',
        'A6': 'Hit',
        'A7': 'Hit',
        'A8': 'Stand',
        'A9': 'Stand',
        'A10': 'Stand'
    }
}

rank_to_value = {
    'Ace': 1,
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5,
    'Six': 6,
    'Seven': 7,
    'Eight': 8,
    'Nine': 9,
    'Ten': 10,
    'Jack': 10,
    'Queen': 10,
    'King': 10
}

def is_soft(cards):
    if len(cards) == 2:
        if cards[0]['best_rank_match'] != cards[1]['best_rank_match']:
            if cards[0]['best_rank_match'] == 'Ace' or cards[1]['best_rank_match'] == 'Ace':
                return True
    return False

def tally_hard_total(cards):
    return sum([rank_to_value[card['best_rank_match']] for card in cards])

def tally_soft_total(cards):
    if cards[0]['best_rank_match'] != 'Ace':
        return 'A' + str(rank_to_value[cards[0]['best_rank_match']])
    else:
        return 'A' + str(rank_to_value[cards[1]['best_rank_match']])

def get_action(upcard, cards):
    dcard = str(rank_to_value[upcard['best_rank_match']]) if upcard['best_rank_match'] != 'Ace' else 'A'
    if is_soft(cards):
        return soft_table[dcard][tally_soft_total(cards)]
    else:
        total = tally_hard_total(cards)
        if total > 16:
            return 'Stand'
        elif total < 9:
            return 'Hit'
        else:
            return hard_table[dcard][str(total)]


if __name__ == '__main__':
    upcard = {'best_rank_match': 'Jack'}
    cards = [
        {'best_rank_match': 'Nine'},
        {'best_rank_match': 'Queen'}
    ]
    print(get_action(upcard, cards))