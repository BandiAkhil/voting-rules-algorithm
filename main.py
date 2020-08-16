import networkx as nx
import operator
from util import *


DATA_FROM_EXCEL = get_states_data()


def state_based_winner(runoff=False):
    candidate_seats = dict()
    for state_data in DATA_FROM_EXCEL:
        num_seats = state_data[1]
        votes = state_data[2]
        if runoff:
            loser = get_plurality_first_round_current_system(votes)[1]
            winner = get_plurality_second_round_current_system(votes, loser)
            plurality_winner = winner[0]
        else:
            plurality_winner = get_plurality_first_round_current_system(votes)[0][0]
        candidate_seats[plurality_winner] = candidate_seats.get(plurality_winner, 0) + num_seats
    return max(candidate_seats.items(), key=operator.itemgetter(1))


def get_plurality_first_round_current_system(ballots_votes):
    candidate_votes = dict()
    for ballot_vote in ballots_votes:
        candidate_votes[ballot_vote[0][0]] = candidate_votes.get(ballot_vote[0][0], 0) + ballot_vote[1]
    return max(candidate_votes.items(), key=operator.itemgetter(1)), min(candidate_votes.items(), key=operator.itemgetter(1))


def get_plurality_second_round_current_system(order_votes, loser=None):
    candidate_votes = dict()
    for order_vote in order_votes:
        if order_vote[0][0] == loser[0]:
            candidate_votes[order_vote[0][1]] = candidate_votes.get(order_vote[0][1], 0) + order_vote[1]
        else:
            candidate_votes[order_vote[0][0]] = candidate_votes.get(order_vote[0][0], 0) + order_vote[1]
    return max(candidate_votes.items(), key=operator.itemgetter(1))


def overall_us_candidate_results():
    candidate_votes = dict()
    for state_data in DATA_FROM_EXCEL:
        for state_votes in state_data[2]:
            votes = state_votes[1]
            candidate = state_votes[0][0]
            candidate_votes[candidate] = candidate_votes.get(candidate, 0) + votes
    return candidate_votes


def overall_us_plurality_winner():
    candidate_votes = overall_us_candidate_results()
    return max(candidate_votes.items(), key=operator.itemgetter(1))


def overall_us_plurality_loser():
    candidate_votes = overall_us_candidate_results()
    return min(candidate_votes.items(), key=operator.itemgetter(1))


def overall_us_plurality_runoff_winner():
    candidate_votes = dict()
    loser = overall_us_plurality_loser()
    for state_data in DATA_FROM_EXCEL:
        for state_votes in state_data[2]:
            votes = state_votes[1]
            candidate = state_votes[0][1] if state_votes[0][0] == loser[0] else state_votes[0][0]
            candidate_votes[candidate] = candidate_votes.get(candidate, 0) + votes
    return max(candidate_votes.items(), key=operator.itemgetter(1))


def get_tally():
    tally = dict()
    for state in get_states_data():
        ballots_votes = state[2]
        for ballot_vote in ballots_votes:
            for candidate in ballot_vote[0]:
                if len(ballot_vote[0]) <= 1:
                    break;
                candidate1 = ballot_vote[0].pop(0)
                for candidate2 in ballot_vote[0]:
                    pairwise = (candidate1, candidate2)
                    tally[pairwise] = tally.get(pairwise, 0) + ballot_vote[1]
    print("\nFirst step, tally: ", tally)
    return tally


def sort(tally):
    sorted_tally = dict(sorted(tally.items(), key=operator.itemgetter(1), reverse=True))
    print("\nSecond step, sorted tally: ", sorted_tally)
    return sorted_tally


def lock(sort):
    lock = dict()
    for k in sort:
        if sort[k] > sort[k[::-1]]:
            lock[k] = sort[k]
        else:
            continue
    print("\nThird step, locked the candidates: ", lock)
    return lock


def remove_cycles(lock):
    candidate_list = [k for k in lock]
    result = []
    for candidate in candidate_list:
        result.append(candidate)
        G = nx.DiGraph(result)
        if len(list(nx.simple_cycles(G))) > 0:
            result.pop(len(result) - 1)
    print("\nFourth step, remove cycles: ", result)
    return result


def ranked_pair_winner():
    tally = get_tally()
    sorted_tally = sort(tally)
    locked_candidates = lock(sorted_tally)
    candidate_list = remove_cycles(locked_candidates)
    G = nx.DiGraph(candidate_list)
    for node in G.nodes():
        if len(G.in_edges(node)) == 0:
            return node



print("Current system winner:", state_based_winner(False))
print("Plurality winner overall US:", overall_us_plurality_winner())
print("Plurality with runoff winner for each state:", state_based_winner(True))
print("Plurality with runoff winner overall US:", overall_us_plurality_runoff_winner())
print("\nOwn voting rule: Ranked Pairs")
print("\nRanked pair Winner: ", ranked_pair_winner())