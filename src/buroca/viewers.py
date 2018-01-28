import os
import subprocess

from buroca.errors import SkipViewer


def launch_document_viewer(file):
    """
    Launch a document viewer for the given file.
    """
    ext = os.path.splitext(file)[-1].lstrip('.')

    try:
        viewers = SYSTEM_VIEWERS[ext]
        for viewer in viewers:
            try:
                execute_viewer(viewer, file)
            except SkipViewer:
                pass
    except KeyError:
        show_file(file)


def execute_viewer(viewer, file):
    """
    Execute a viewer for the given file.

    Viewer can be a string (interpreted as a command name) or a python function.
    """
    if isinstance(viewer, str):
        try:
            result = subprocess.check_output([viewer, file])
        except FileNotFoundError:
            raise SkipViewer
        else:
            print('Running %s' % viewer)
            print(result)

    elif callable(viewer):
        viewer(file)

    else:
        raise TypeError('invalid viewer type: %s' % type(viewer).__name__)


def show_file(file):
    """
    A rough pure python implementation of the unix cat command.
    """
    with open(file) as F:
        for line in F:
            print(line, end='')
    print()


SYSTEM_VIEWERS = {
    'pdf': ['evince', 'kpdf', show_file],
    'md': ['less', show_file],
}
