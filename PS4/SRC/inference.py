import os
import itertools
from collections import deque

flag = False


def read_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    alpha = lines[0].strip()  # alpha is the first line of the file
    n = int(lines[1].strip())  # n is number of lines in KB
    kb = [line.strip() for line in lines[2:2+n]]  # kb is the rest of the lines
    return alpha, kb


def parse_clause(clause_str):
    # clause_str is a string of literals separated by OR
    # returns a list of literals
    return sorted([literal.strip() for literal in clause_str.split('OR')], key=lambda x: x[1:] if x.startswith('-') else x)


def to_cnf(clauses):
    # clauses is a list of clauses
    # returns a list of clauses in CNF
    return [parse_clause(clause) for clause in clauses]


def negate_alpha(alpha):
    return alpha[1:] if alpha.startswith('-') else f'-{alpha}'


def resolution(clause1, clause2):
    global flag
    # clause1 and clause2 are lists of literals
    # returns a list of resolvents
    for literal1 in clause1:
        neg_literal1 = negate_alpha(literal1)
        if neg_literal1 in clause2:
            new_clause = sorted(
                list(set(clause1 + clause2) - {literal1, neg_literal1}), key=lambda x: x[1:] if x.startswith('-') else x)
            # set used to remove duplicates
            # sorted used to sort the literals in the clause
            # - {literal1, neg_literal1} used to remove the literals that were resolved
            if new_clause == []:
                flag = True
            if new_clause and not any([literal in new_clause for literal in [negate_alpha(l) for l in new_clause]]):
                # if new_clause is not empty and there is no literal that is the negation of another literal in the clause
                yield new_clause


def pl_resolution(alpha, kb):
    alpha = negate_alpha(alpha)
    kb = to_cnf(kb)
    kb.append(parse_clause(alpha))
    resolvents_history = []
    new_resolvents = []
    while True:
        for pair in itertools.combinations(kb, 2):
            # create all possible pairs of clauses from kb
            if flag == True:
                new_resolvents.append(tuple(['{}']))
                resolvents_history.append(new_resolvents)
                return resolvents_history, True
            for resolvent in resolution(pair[0], pair[1]):
                if resolvent not in kb and tuple(resolvent) not in new_resolvents:
                    # check duplicates resolvents
                    new_resolvents.append(tuple(resolvent))
        if not new_resolvents:
            resolvents_history.append(new_resolvents)
            return resolvents_history, False
        # if new_resolvents is empty, then there are no new resolvents
        # therefore, the KB does not entail alpha
        kb += [list(resolvent) for resolvent in new_resolvents]
        resolvents_history.append(list(new_resolvents))
        new_resolvents = []
        # if new_resolvents is not empty, then we add the new resolvents to the KB


def export_output(file_path, resolvents_history, entails_alpha):
    with open(file_path, 'w') as file:
        for i, resolvents in enumerate(resolvents_history):
            file.write(f'{len(resolvents)}\n')
            for resolvent in resolvents:
                file.write(' OR '.join(resolvent) + '\n')
        file.write('YES' if entails_alpha else 'NO')


def implement(input_file, output_file):
    global flag
    flag = False
    alpha, kb = read_input(input_file)
    resolvents_history, entails_alpha = pl_resolution(alpha, kb)
    export_output(output_file, resolvents_history, entails_alpha)


def read_folder(folder_path):
    files = os.listdir(folder_path)
    for file in files:
        if file.endswith('.txt'):
            yield os.path.join(folder_path, file)


def main():
    for input_file in read_folder('./INPUT'):
        output_file = input_file.replace(
            'input', 'output').replace('INPUT', 'OUTPUT')
        implement(input_file, output_file)


main()
