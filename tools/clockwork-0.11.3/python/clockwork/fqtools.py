from clockwork import utils


class Error(Exception):
    pass


def validate(filenames):
    assert 1 <= len(filenames) <= 2
    cmd = "fqtools validate " + " ".join(filenames)
    try:
        utils.syscall(cmd)
    except:
        raise Error("Error running " + cmd)


def count(filenames):
    assert 1 <= len(filenames) <= 2
    cmd = "fqtools count " + " ".join(filenames)
    try:
        completed_process = utils.syscall(cmd)
    except:
        raise Error("Error running " + cmd)

    try:
        read_count = int(completed_process.stdout.rstrip())
    except:
        raise Error('Error getting read count from: "' + completed_process.stdout + '"')

    return read_count
