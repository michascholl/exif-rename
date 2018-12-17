from collections import defaultdict
from typing import DefaultDict, Dict, Iterable, Set

from exif_rename.parser import read_meta_data


def _add_samples(sample_dict: DefaultDict[str, set], samples: Dict[str, object]):
    """Add samples to the sample_dict

    :param sample_dict: dictionary with old samples. Entries are sets
    :param samples: dictionary with new samples (one for each key)
    """
    for key, value in samples.items():
        sample_dict[key].add('{!s}: "{}"'.format(type(value).__name__, value))


def _samples_str(samples: set, n_examples: int) -> str:
    """
    Get the total number of distinct entries and `n_examples` samples from the samples as a string.
    If more (or the string is to log), append three dots
    """
    res = ', '.join(list(samples)[:n_examples])
    if len(samples) > n_examples or len(res) > 120:
        res = res[:117] + '...'

    res = '{:3n}| {}'.format(len(samples), res)
    return res


def get_common_samples(files: Iterable[str]) -> Dict[str, Set[str]]:
    """
    Get samples for all tags common to all files
    """
    files = iter(files)
    try:
        exif_vars = read_meta_data(next(files))
        common_keys = set(exif_vars)
        samples = defaultdict(set)
        _add_samples(samples, exif_vars)
    except StopIteration:
        return dict()

    for file_name in files:
        exif_vars = read_meta_data(file_name)
        common_keys = common_keys.intersection(exif_vars)
        _add_samples(samples, exif_vars)
        for non_global in [k for k in samples if k not in common_keys]:
            samples.pop(non_global)

    return {
        key: samples[key]
        for key in common_keys
    }


def print_samples(samples_dict, n_examples=3) -> None:
    """Print tags"""
    for key, samples in samples_dict.items():
        print('{:20s}: {}'.format(key, _samples_str(samples, n_examples)))


def list_common_tags(files, n_examples=3):
    """
    List common tags and some samples for each tag
    """
    samples = get_common_samples(files)
    print_samples(samples, n_examples)