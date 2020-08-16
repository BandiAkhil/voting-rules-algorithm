import xlrd

loc = ("./Votes2.xlsx")

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)


def get_states_data():
    states_votes = []
    for i in range(4, sheet.nrows):
        state_row = [sheet.cell_value(i, 0), int(sheet.cell_value(i, 2))]
        votes_row = []
        for j in range(4, sheet.ncols):
            order_votes = (sheet.col_values(j, 1, 4), int(sheet.cell_value(i, j)))
            votes_row.append(order_votes)
        state_row.append(votes_row)
        states_votes.append(state_row)
    return states_votes
