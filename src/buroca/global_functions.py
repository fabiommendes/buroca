import itertools

GLOBALS = {}
register = (lambda f: GLOBALS.setdefault(f.__name__, f))

MONTHS = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT',
          'NOV', 'DEZ']


@register
def cronogram(type, duration, start, month, tick_mark='x'):
    """
    Make a cronogram table in the desired format.

    Type must be one of 'md', 'md-pipe', 'html' or 'latex'.

    All other arguments are identical to :func:`make_cronogram_table`.
    """

    table = make_cronogram_table(duration, start, month, tick_mark)

    if type in ('md', 'markdown'):
        result = render_markdown_simple_table(table)
    elif type in ('md-pipe', 'markdown-pipe'):
        result = render_markdown_pipe_table(table)
    else:
        raise NotImplementedError

    return result


def make_cronogram_table(duration, start, first_month, tick_mark='x'):
    """
    Make a cronogram table.

    Args:
        duration:
            A list of durations for each phase.
        start:
            A list of offsets for each phase. (0 to start at the first month)
        first_month (int):
            Starting month. 1 - January, 2 - February, etc.
        tick_mark:
            The that tells which months are enabled.

    Returns:
        A list of lists with the table content.
    """
    duration, start = list(duration), list(start)
    end = max(x + y for x, y in zip(duration, start))
    months = itertools.cycle(MONTHS)
    for _ in range(first_month - 1):
        next(months)

    table = [[] for _ in range(len(duration) + 1)]

    # Save months at header
    header = table[0]
    header.append('#')
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


def render_markdown_simple_table(table, min_width=3):
    nrows = len(table)
    ncols = len(table[0])

    colsizes = [max(max(len(table[i][j]) for i in range(nrows)), min_width)
                for j in range(ncols)]
    header, *body = table
    data = [header, ['-' * size for size in colsizes]]
    data.extend(body)

    return '\n%s\n' % (
        '\n'.join('   '.join(cell.ljust(size)
                             for cell, size in zip(row, colsizes))
                  for row in data))


def render_markdown_pipe_table(table):
    header, *body = table
    data = [header, ['-' * min(len(cell), 3) for cell in header]]
    data.extend(body)
    return '\n%s\n' % ('\n'.join('|'.join(cell or ' ' for cell in row)
                                 for row in data))
