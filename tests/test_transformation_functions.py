from buroca.global_functions import render_markdown_table, make_chronogram_table


class TestGlobalFunctions:
    def test_render_markdown_table(self):
        data = [['name', 'age'], ['john lennon', '42']]
        assert render_markdown_table(data) == (
            'name          age\n'
            '-----------   ---\n'
            'john lennon   42 '
        )

    def test_make_cronogram(self):
        assert make_chronogram_table([(2, 0), (3, 1), (2, 4)]) == [
            ['\\#', 'JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN'],
            ['1', 'x', 'x', ' ', ' ', ' ', ' '],
            ['2', ' ', 'x', 'x', 'x', ' ', ' '],
            ['3', ' ', ' ', ' ', ' ', 'x', 'x'],
        ]
