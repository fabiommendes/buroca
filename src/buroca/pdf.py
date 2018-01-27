from .paths import expand_glob


def join_pdf_command(glob, dest):
    """
    Execute the "buroca join-pdf <glob> <dest>" command
    """
    pdfs = expand_glob('reports', glob)
    return pdfs


def to_pdf(base, glob):
    """
    Convert all files that conforms with the given glob pattern inside base
    path.
    """


def file_to_pdf(source, dest):
    """
    Convert file at source path to a PDF in the given destination path.
    """


def join_pdfs(base, glob, dest):
    """
    Join all PDF files conforming to the given glob pattern and generate a
    pdf file.
    """
