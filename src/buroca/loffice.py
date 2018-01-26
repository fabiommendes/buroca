import subprocess


def headless_cmd(*args):
    """
    Execute libreoffice in headless mode
    """
    cmd = ['libreoffice', '-headless']
    subprocess.run(cmd)


def odt_to_rtf(source, dest):
    "Convert .odt file to rtf"

    return headless_cmd('-convert-to', 'rtf', source, '-o', dest)


def odt_to_pdf(source, dest):
    "Convert .odt to pdf"

    return headless_cmd('-convert-to', 'pdf', source, '-o', dest)


def launch_calc(fname):
    """
    Launch calc with open socket communication to start communication with 
    oosheet.
    """
    return headless_cmd(
        '--calc',
        '--accept="socket,'
        'host=localhost,port=2002;urp;StarOffice.ServiceManager"',
        fname,
    )
