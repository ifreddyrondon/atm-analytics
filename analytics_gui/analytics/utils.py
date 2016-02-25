def build_table(date, error, mount):
    table = []

    for i in range(0, len(date)):
        tmp_row = [date[i], error[i], mount[i]]
        table.append(tmp_row)

    return table
