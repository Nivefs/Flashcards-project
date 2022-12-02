import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--export_to', type=str, default=None)
parser.add_argument('--import_from', type=str, default=None)
args = parser.parse_args()


def reset_stats():
    for x in cards:
        cards[x][1] = 0
    print(log('Card statistics have been reset.'))


def hardest_card():
    value = tuple(map(lambda x: x[1], cards.values()))
    dict_tuple = tuple(cards)
    message = []
    count = 0
    for x, y in enumerate(value):
        if y != max(value) or y == 0:
            continue
        message.append(dict_tuple[x])
        count += 1

    if count == 1:
        print(log(f'The hardest card is "{", ".join(message)}". You have {max(value)} errors answering it.'))
    elif count > 1:
        print(log(f'The hardest cards are "{", ".join(message)}". You have {max(value)} errors answering them.'))
    else:
        print(log('There are no cards with errors.'))


def log(txt, log_mode='r'):
    if log_mode == 'r':
        log_lst.append(txt)
        return txt
    if log_mode == 's':
        print(log('File name:'))
        file_store = input()
        log(file_store)
        file = open(file_store, 'w')
        new_lst_hello = map(lambda x: x + '\n' if log_lst.index(x) < len(log_lst) - 1 else x, log_lst)
        print(log('The log has been saved.'))
        file.writelines(new_lst_hello)


def add():
    while True:
        print(log('The card:'))
        front = input()
        log(front)
        if front in cards:
            print(log(f'The card {front} already exists, Try again:'))
            continue
        print(log('The definition'))
        back = input()
        log(back)
        back_list = list(map(lambda x: x[0], cards.values()))
        if back in back_list:
            while back in back_list:
                print(log(f'The definition already exists, Try again:'))
                back = input()
                log(back)
        cards.update({front:[back, 0]})
        print(log(f'The pair ("{front}": "{back}") has been added.'))
        break


def remove():
    print(log('Which card?'))
    card_rm = input()
    log(card_rm)
    if card_rm not in cards:
        print(log(f"Can't remove {card_rm}: there is no such card."))
        return
    cards.pop(card_rm)
    print(log(f'The {card_rm} has been removed.'))


def import_():
    if args.import_from:
        file = open(args.import_from, 'r')
        file_read = file.readlines()
        if file_read == []:
            return
        cards.update({card.split(":")[0]:[card.split(':')[1], int(card.split(':')[2])] for card in file_read[0].split(';')})
        # length = len(file_read[0].split(';'))
        print(log(f'{len(file_read[0].split(";"))} cards have been loaded'))
        file.close()
    else:
        print(log('File Name:'))
        file_name = input()
        log(file_name)
        if not os.access(file_name, os.F_OK):
            print(log('File not found.'))
            return
        file = open(file_name, 'r')
        file_read = file.readlines()
        if file_read == []:
            return
        cards.update(
            {card.split(":")[0]: [card.split(':')[1], int(card.split(':')[2])] for card in file_read[0].split(';')})
        # length = len(file_read[0].split(';'))
        print(log(f'{len(file_read[0].split(";"))} cards have been loaded'))
        file.close()
        # print(cards)  # Proof


def export():
    if args.export_to:
        file = open(args.export_to, 'w')
        file.writelines(';'.join([f'{key}:{value[0]}:{value[1]}' for key, value in cards.items()]))
        print(log(f'{len(cards)} cards have been saved.'))
        file.close()
    else:
        print(log('File name:'))
        file_name = input()
        lst = []
        for front, back in cards.items():
            lst.append(f'{front}:{back[0]}:{back[1]}')
        new_lst = map(lambda x: x + ';' if lst.index(x) < len(lst) - 1 else x, lst)
        file = open(file_name, 'w')
        file.writelines(list(new_lst))
        print(log(f'{len(lst)} cards have been saved'))
        file.close()


def ask():
    print(log('How many times to ask?'))
    times = int(input())
    log(str(times))
    count = 0
    while True:
        filter_list = tuple(map(lambda x: x[0], cards.values()))
        for front, back in cards.items():
            if count == times:
                return
            print(log(f'Print the definition of "{front}"'))
            answer = input()
            log(answer)
            if answer == back[0]:
                print(log('Correct!'))

            elif answer in filter_list:
                print(
                    log(f'Wrong. The right answer is "{back[0]}", but your definition is correct for "{list(cards)[filter_list.index(answer)]}"'))
                cards[front][1] += 1
            else:
                print(log(f'Wrong the right answer is {back[0]}'))
                cards[front][1] += 1
            # print(front)
            count += 1
            # print(count)
        if count == times:
            break


log_lst = []
cards = {}
options = 'add', 'remove', 'import', 'export', 'ask', 'exit', 'log', 'hardest card', 'reset stats'

if args.import_from:
    import_()
while True:
    print(log('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):'))
    action = input()
    log(action)
    if action not in options:
        continue
    # Implementation of the options
    if action == 'add':
        add()

    elif action == 'remove':
        remove()

    elif action == 'import':
        import_()

    elif action == 'export':
        export()

    elif action == 'ask':
        ask()

    elif action == 'log':
        log('_', 's')

    elif action == 'hardest card':
        hardest_card()

    elif action == 'reset stats':
        reset_stats()

    elif action == 'exit':
        if args.export_to:
            export()
        print('Bye bye!')
        break

