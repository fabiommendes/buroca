import subprocess

LETTERS = list('abcdefghijklmnopqrstuvwxyz')
for _letter in 'abcd':
    LETTERS.extend(_letter + c for c in 'abcdefghijklmnopqrstuvwxyz')


class Sheet:
    """
    Represents a spreadsheet running in a LOCalc instance.
    """

    def __init__(self, file):
        self.file = file
        self.process = None

    def __del__(self):
        self.kill()

    def kill(self):
        "Kill current libreoffice process"
        self.process.kill()
        self.process = None

    def start(self):
        "Start calc process"
        cmd = [
            'libreoffice', '--calc',
            '--accept="socket,host=localhost,port=2002;urp;'
            'StarOffice.ServiceManager"',
            self.file,
        ]
        self.process = subprocess.Popen(cmd)
        return self.process

    def sheet(self):
        """
        Return an object representing the spreadsheet.

        Must start libreoffice process first.
        """
        if self.process is None:
            raise RuntimeError('must start libreoffice before starting.')

        from oosheet import OOSheet
        return OOSheet

    def template_cells(self):
        """
        Search all cells for jinja2 templates
        """
        sheet = self.sheet()
        rows = 57
        cols = LETTERS.index('m')
        cell_map = {}

        for i in range(rows):
            for j in range(cols):
                cell_name = cell(i, j)
                data = sheet(cell_name).string.strip()
                if data.startswith('{') and data.endswith('}'):
                    cell_map[cell_name] = data

        return cell_map


def cell(i, j):
    "Convert coordinates i,j to cell names"
    return LETTERS[j] + str(i + 1)
