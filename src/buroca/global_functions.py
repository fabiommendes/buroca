import itertools

GLOBALS = {}
register = (lambda f: GLOBALS.setdefault(f.__name__, f))

MONTHS = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT',
          'NOV', 'DEZ']


@register
def cronogram(type, duration, start, month, tick_mark=None):
    """
    Make a cronogram table in the desired format.

    Type must be one of 'md', 'md-pipe', 'html' or 'latex'.

    All other arguments are identical to :func:`make_cronogram_table`.
    """

    if tick_mark is None:
        if type in ('md', 'md-pipe', 'markdown', 'markdown-pipe'):
            tick_mark = 'X'
        else:
            tick_mark = 'X'

    table = make_chronogram_table(zip(duration, start), month, tick_mark)

    if type in ('md', 'markdown'):
        result = '\n%s\n\n' % render_markdown_table(table)
    elif type in ('md-pipe', 'markdown-pipe'):
        result = '\n%s\n\n' % render_markdown_table(table, colsep='|')
    else:
        raise NotImplementedError

    return result


def make_chronogram_table(slots, first_month=1, tick_mark='x'):
    """
    Make a cronogram table.

    Args:
        slots:
            A list of (duration, offset) tuples specifing the duration and
            the offset values for each phase.
        first_month (int):
            Starting month. 1 - January, 2 - February, etc.
        tick_mark:
            The that tells which months are enabled.

    Returns:
        A list of lists with the table content.
    """
    data = list(slots)
    duration = [x for x, _ in data]
    start = [y for _, y in data]
    end = max(x + y for x, y in zip(duration, start))
    months = itertools.cycle(MONTHS)
    for _ in range(first_month - 1):
        next(months)

    table = [[] for _ in range(len(duration) + 1)]

    # Save months at header
    header = table[0]
    header.append('\#')
    header.extend(month for month, _ in zip(months, range(end)))

    # Save body
    for idx, row in enumerate(table[1:]):
        row.append(str(idx + 1))
        row.extend([' '] * end)

        start_idx = start[idx]
        end_idx = start_idx + duration[idx]
        for i in range(start_idx, end_idx):
            row[i + 1] = tick_mark

    return table


def render_markdown_table(table, min_width=3, colsep='   '):
    """
    Render table to markdown.

    Args:
        table:
            A list of lists with each cell content.
        min_width (int):
            Minimum width of each cell.
        wrap (str):
            A format string that is used to wrap the table contents usually to
            insert newlines before and after table data.
        colsep (str):
            The column separator. Use colsep='|' for pipe tables and 
            colsep='   ' for standard markdown tables.
    """

    # table geometry
    n_rows = len(table)
    n_cols = len(table[0])
    colsizes = [
        max(max(len(table[i][j]) for i in range(n_rows)), min_width)
        for j in range(n_cols)
    ]

    # Insert row with line geometry
    header, *body = table
    data = [header, ['-' * size for size in colsizes]]
    data.extend(body)

    # Justify cells according to column size
    for idx, row in enumerate(data):
        row = [cell.ljust(size) for cell, size in zip(row, colsizes)]
        data[idx] = colsep.join(row)

    return '\n'.join(data)
