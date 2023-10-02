import sys


def show_progress(i, total, name='profits'):
    """Shows the progress of a task.

    Args:
        i: The current progress.
        total: The container of items to process.
        name: Name of process.
    """
    length = len(total)
    percentage = int((i / length) * 100)
    sys.stdout.write(f"\rProcessed {name} {i}/{length} ({percentage}%)")
    sys.stdout.flush()
    if i == length-1:
        sys.stdout.write("\n\n")