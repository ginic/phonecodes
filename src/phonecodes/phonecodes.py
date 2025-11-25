"""
A set of convenience functions for converting among different phone codes.
Usage:
from phonecodes import phonecodes
print phonecodes.CODES   # the known phone codes
print phonecodes.LANGUAGES # the known languages
s1 = phonecodes.convert(s0, code0, code1, language)
# s0 and s1 are strings containing individual symbols
# code0 and code1 must be members of phonecodes.CODES, of course
# language must be a member of phonecodes.LANGUAGES, of course
#   (but not all languages are known for all phone codes)
l1 = phonecodes.convertlist(l0, code0, code1, language)
# l0, l1 are lists of symbols
phonecodes.vowels
phonecodes.consonants
# list known IPA symbols of vowels, consonants.
# for other tables, see phonecode_tables.py
"""

from __future__ import annotations
from collections import abc
from dataclasses import dataclass
from enum import Enum
import re
import warnings

import phonecodes.phonecode_tables as phonecode_tables

# Phonecodes constants for easier maintenance
IPA_KEY = "ipa"
ARPABET_KEY = "arpabet"
XSAMPA_KEY = "xsampa"
DISC_KEY = "disc"
CALLHOME_KEY = "callhome"
BUCKEYE_KEY = "buckeye"
TIMIT_KEY = "timit"

CODES = set((IPA_KEY, ARPABET_KEY, XSAMPA_KEY, DISC_KEY, CALLHOME_KEY, BUCKEYE_KEY, TIMIT_KEY))
LANGUAGES = set(("eng", "deu", "nld", "arz", "cmn", "spa", "yue", "lao", "vie"))


class Phonecodes(Enum):
    """Defines the set of valid phonecode mapping options supported
    and which languages are covered. When language is not specified,
    the mapping does not change depending on language.
    """

    # XSAMPA
    IPA2XSAMPA = IPA_KEY, XSAMPA_KEY
    XSAMPA2IPA = XSAMPA_KEY, IPA_KEY

    # DISC
    DISC2IPA = DISC_KEY, IPA_KEY
    DISC2IPA_NLD = DISC_KEY, IPA_KEY, "nld"
    DISC2IPA_ENG = DISC_KEY, IPA_KEY, "eng"
    IPA2DISC = IPA_KEY, DISC_KEY

    # CALLHOME
    CALLHOME2IPA_ARZ = CALLHOME_KEY, IPA_KEY, "arz"
    CALLHOME2IPA_CMN = CALLHOME_KEY, IPA_KEY, "cmn"
    CALLHOME2IPA_SPA = CALLHOME_KEY, IPA_KEY, "spa"
    IPA2CALLHOME_ARZ = IPA_KEY, CALLHOME_KEY, "arz"
    IPA2CALLHOME_CMN = IPA_KEY, CALLHOME_KEY, "cmn"
    IPA2CALLHOME_SPA = IPA_KEY, CALLHOME_KEY, "spa"

    # ARPABET
    ARPABET2IPA = ARPABET_KEY, IPA_KEY
    IPA2ARPABET = IPA_KEY, ARPABET_KEY

    # TIMIT - There is no way to convert from IPA to TIMIT due to closure symbols
    TIMIT2IPA = TIMIT_KEY, IPA_KEY

    # Buckeye
    BUCKEYE2IPA = BUCKEYE_KEY, IPA_KEY
    IPA2BUCKEYE = IPA_KEY, BUCKEYE_KEY

    def __init__(self, in_code, out_code, language=None):
        self.in_code = in_code
        self.out_code = out_code
        self.language = language

    @classmethod
    def as_member(cls, in_code, out_code, language=None):
        valid_codes = set(item.value for item in cls)
        phonecode_tuple = (in_code, out_code, language)
        if phonecode_tuple in valid_codes:
            return Phonecodes((in_code, out_code, language))

        phonecode_tuple = (in_code, out_code)
        if (in_code, out_code) in valid_codes:
            return Phonecodes((in_code, out_code))
        raise ValueError(
            f"Phonecode pairing {phonecode_tuple} is not valid. Must convert to/from 'ipa' in supported languages or leave language unspecified."
        )


# Which symbol mapping will be used in conversion?
_phonecode_lookup = {
    # XSAMPA
    Phonecodes.IPA2XSAMPA: phonecode_tables._ipa2xsampa,
    Phonecodes.XSAMPA2IPA: phonecode_tables._xsampa_and_diac2ipa,
    # DISC
    Phonecodes.DISC2IPA: phonecode_tables._disc2ipa,
    Phonecodes.DISC2IPA_NLD: phonecode_tables._disc2ipa_dutch,
    Phonecodes.DISC2IPA_ENG: phonecode_tables._disc2ipa_english,
    Phonecodes.IPA2DISC: phonecode_tables._ipa2disc,
    # CALLHOME
    Phonecodes.CALLHOME2IPA_ARZ: phonecode_tables._callhome2ipa[Phonecodes.CALLHOME2IPA_ARZ.language],
    Phonecodes.CALLHOME2IPA_CMN: phonecode_tables._callhome2ipa[Phonecodes.CALLHOME2IPA_CMN.language],
    Phonecodes.CALLHOME2IPA_SPA: phonecode_tables._callhome2ipa[Phonecodes.CALLHOME2IPA_SPA.language],
    Phonecodes.IPA2CALLHOME_ARZ: phonecode_tables._ipa2callhome[Phonecodes.IPA2CALLHOME_ARZ.language],
    Phonecodes.IPA2CALLHOME_CMN: phonecode_tables._ipa2callhome[Phonecodes.IPA2CALLHOME_CMN.language],
    Phonecodes.IPA2CALLHOME_SPA: phonecode_tables._ipa2callhome[Phonecodes.IPA2CALLHOME_SPA.language],
    # ARPABET
    Phonecodes.ARPABET2IPA: phonecode_tables._arpabet2ipa,
    Phonecodes.IPA2ARPABET: phonecode_tables._ipa2arpabet,
    # Buckeye
    Phonecodes.BUCKEYE2IPA: phonecode_tables._buckeye2ipa,
    Phonecodes.IPA2BUCKEYE: phonecode_tables._ipa2buckeye,
    # TIMIT
    Phonecodes.TIMIT2IPA: phonecode_tables._timit2ipa,
}


@dataclass
class AttachStressTonesConfig:
    """Stores the settings for tone or stress attachment algorithms,
    which can be different depending on the language and corpus format."""

    tones: abc.Iterable[str] | str
    vowels: abc.Iterable[str] | str
    searchstep: int
    catdir: int


# Is there a configuration for adding tones or stress markers to the final output?
_tone_stress_settings = {
    Phonecodes.CALLHOME2IPA_ARZ: AttachStressTonesConfig(
        phonecode_tables._ipa_stressmarkers, phonecode_tables._ipa_vowels, -1, -1
    ),
    Phonecodes.CALLHOME2IPA_CMN: AttachStressTonesConfig(
        phonecode_tables._ipa_tones, phonecode_tables._ipa_vowels, -1, 1
    ),
    Phonecodes.CALLHOME2IPA_SPA: AttachStressTonesConfig(
        phonecode_tables._ipa_stressmarkers,
        phonecode_tables._ipa_vowels,
        -1,
        -1,
    ),
    Phonecodes.IPA2CALLHOME_ARZ: AttachStressTonesConfig(
        "012", phonecode_tables._callhome_vowels[Phonecodes.IPA2CALLHOME_ARZ.language], 1, 1
    ),
    Phonecodes.IPA2CALLHOME_CMN: AttachStressTonesConfig(
        "012345", phonecode_tables._callhome_vowels[Phonecodes.IPA2CALLHOME_CMN.language], -1, 1
    ),
    Phonecodes.IPA2CALLHOME_SPA: AttachStressTonesConfig(
        "012", phonecode_tables._callhome_vowels[Phonecodes.IPA2CALLHOME_SPA.language], 1, 1
    ),
    Phonecodes.ARPABET2IPA: AttachStressTonesConfig(
        phonecode_tables._ipa_stressmarkers, phonecode_tables._ipa_vowels, -1, -1
    ),
    Phonecodes.IPA2ARPABET: AttachStressTonesConfig("012", phonecode_tables._arpabet_vowels, 1, 1),
}


#####################################################################
def translate_string(s, d):
    """(tl,ttf)=translate_string(s,d):
    Translate the string, s, using symbols from dict, d, as:
    1. Min # untranslatable symbols, then 2. Min # symbols.
    tl = list of translated or untranslated symbols.
    ttf[n] = True if tl[n] was translated, else ttf[n]=False."""
    N = len(s)
    symcost = 1  # path cost per translated symbol
    oovcost = 10  # path cost per untranslatable symbol
    maxsym = max(len(k) for k in d.keys())  # max input symbol length
    # (pathcost to s[(n-m):n], n-m, translation[s[(n-m):m]], True/False)
    lattice = [(0, 0, "", True)]
    for n in range(1, N + 1):
        # Initialize on the assumption that s[n-1] is untranslatable
        lattice.append((oovcost + lattice[n - 1][0], n - 1, s[(n - 1) : n], False))
        # Search for translatable sequences s[(n-m):n], and keep the best
        for m in range(1, min(n + 1, maxsym + 1)):
            if s[(n - m) : n] in d and symcost + lattice[n - m][0] < lattice[n][0]:
                lattice[n] = (
                    symcost + lattice[n - m][0],
                    n - m,
                    d[s[(n - m) : n]],
                    True,
                )
    # Back-trace
    tl = []
    translated = []
    n = N
    while n > 0:
        tl.append(lattice[n][2])
        translated.append(lattice[n][3])
        n = lattice[n][1]
    return (tl[::-1], translated[::-1])


def attach_tones_to_vowels(il: list[str], tones, vowels, searchstep, catdir) -> list[str]:
    """Return a copy of il, with each tone attached to nearest vowel if any.
    searchstep=1 means search for next vowel, searchstep=-1 means prev vowel.
    catdir>=0 means concatenate after vowel, catdir<0 means cat before vowel.
    Tones are not combined, except those also included in the vowels set.
    """
    ol = il.copy()
    v = 0 if searchstep > 0 else len(ol) - 1
    t = -1
    while 0 <= v and v < len(ol):
        if (ol[v] in vowels or (len(ol[v]) > 1 and ol[v][0] in vowels)) and t >= 0:
            ol[v] = ol[v] + ol[t] if catdir >= 0 else ol[t] + ol[v]
            ol = ol[0:t] + ol[(t + 1) :]  # Remove the tone
            t = -1  # Done with that tone
        if v < len(ol) and ol[v] in tones:
            t = v
        v += searchstep
    return ol


#####################################################################
# X-SAMPA
def ipa2xsampa(x, language=None, post_conversion_mapping=None):
    """Attempt to return X-SAMPA equivalent of an IPA phone x."""
    return convert(x, IPA_KEY, XSAMPA_KEY, language, post_conversion_mapping)


def xsampa2ipa(x, language=None, post_conversion_mapping=None):
    """Return the IPA equivalent of X-SAMPA phone x."""
    return convert(x, XSAMPA_KEY, IPA_KEY, language, post_conversion_mapping)


######################################################################
# Language-dependent lexical tones and stress markers
def tone2ipa(n, language):
    return phonecode_tables._tone2ipa[language][int(n[1:])]


#####################################################################
# DISC, the system used by CELEX
def disc2ipa(x, language=None, post_conversion_mapping=None):
    """Convert DISC symbol x into IPA, for language L"""
    return convert(x, DISC_KEY, IPA_KEY, language, post_conversion_mapping)


def ipa2disc(x, language=None, post_conversion_mapping=None):
    """Convert IPA symbol x into DISC"""
    return convert(x, IPA_KEY, DISC_KEY, language, post_conversion_mapping)


#######################################################################
# Callhome phone codes
def callhome2ipa(x, language, post_conversion_mapping=None):
    """Convert callhome phone symbol x into IPA for given language"""
    return convert(x, CALLHOME_KEY, IPA_KEY, language, post_conversion_mapping)


def ipa2callhome(x, language=None, post_conversion_mapping=None):
    """Convert IPA symbol x into callhome notation for given language"""
    return convert(x, IPA_KEY, CALLHOME_KEY, language, post_conversion_mapping)


#########################################################################
# ARPABET, TIMIT, Buckeye
def arpabet2ipa(x, language=None, post_conversion_mapping=None):
    """Convert ARPABET symbol X to IPA"""
    return convert(x, ARPABET_KEY, IPA_KEY, language, post_conversion_mapping)


def ipa2arpabet(x, language=None, post_conversion_mapping=None):
    """Convert IPA symbols to ARPABET"""
    return convert(x, IPA_KEY, ARPABET_KEY, language, post_conversion_mapping)


def timit2ipa(x, language=None, post_conversion_mapping=None):
    """Convert TIMIT phone codes to IPA"""
    return convert(x, TIMIT_KEY, IPA_KEY, language, post_conversion_mapping)


def ipa2timit(x, language=None, post_conversion_mapping=None):
    raise ValueError(
        "Converting to 'timit' is unsupported, because TIMIT closure symbols for stops cannot be determined from text."
    )


def buckeye2ipa(x, language=None, post_conversion_mapping=None):
    """Convert Buckeye phone codes to IPA"""
    return convert(x, BUCKEYE_KEY, IPA_KEY, language, post_conversion_mapping)


def ipa2buckeye(x, language=None, post_conversion_mapping=None):
    "Convert IPA symbols to Buckeye phone codes"
    return convert(x, IPA_KEY, BUCKEYE_KEY, language, post_conversion_mapping)


#######################################################################
# phonecodes.convert and phonecodes.convertlist
# are used to convert symbols and lists of symbols, respectively,
# to or from IPA, by calling appropriate other functions.
#
def _verify_code(code):
    if code not in CODES:
        raise ValueError(f"{code} is not a valid phonecode. Choose from: {' '.join(CODES)}")


def convert(
    s0: str, c0: str, c1: str, language: str | None = None, post_conversion_mapping: dict[str, str] | None = None
) -> str:
    """Convert a string between a given phonecode and IPA

    Args:
        s0 (str): The string to convert
        c0 (str): Input phonecode: 'arpabet', 'xsampa','disc', 'callhome' or 'ipa'
        c1 (str): Output phonecode:  'arpabet', 'xsampa','disc', 'callhome' or 'ipa'
        language (str | None): The language of the string, optional since it is only required for 'disc' and 'callhome' phonecodes
        post_conversion_mapping dict[str, str]: Optional additional normalization mapping that occurs after conversion and stress assignments (greedy, in the same order as the dictionary keys)

    Raises:
        ValueError: If the phonecode is not a valid option

    Returns:
        str: String converted and post processed according to the specified phonecode mappings
    """
    _verify_code(c0)
    _verify_code(c1)

    # Get the right enumerator for looking up mappings
    phonecode_enum = Phonecodes.as_member(c0, c1, language)

    # Most basic mapping
    input_string = s0
    translation_mapping = _phonecode_lookup[phonecode_enum]
    if phonecode_enum in [Phonecodes.ARPABET2IPA, Phonecodes.BUCKEYE2IPA, Phonecodes.TIMIT2IPA]:
        input_string = input_string.upper()
    (mapped_string, ttf) = translate_string(input_string, translation_mapping)

    # Add tones/stress if it's configured for this enum
    if phonecode_enum in _tone_stress_settings:
        stress_config = _tone_stress_settings[phonecode_enum]
        mapped_string = attach_tones_to_vowels(
            mapped_string, stress_config.tones, stress_config.vowels, stress_config.searchstep, stress_config.catdir
        )

    final_string = "".join(mapped_string)

    # Optional post processing normalization
    if post_conversion_mapping is not None:
        final_string = _post_process_reduction(final_string, translation_mapping, post_conversion_mapping)

    return final_string.strip()


def convertlist(l0, c0, c1, language, post_ipa_mapping: dict[str, str] | None = None):
    return [convert(s0, c0, c1, language, post_ipa_mapping) for s0 in l0]


def _post_process_reduction(
    input_string: str, original_translation_mapping: dict[str, str], reduction_mapping: dict[str, str]
) -> str:
    """Additional normalization step, replaces symbols in the input_str according to the reduction_mapping (original symbol -> desired symbol).

    Before the replacement occurs, checks for conflicting behaviors, such as mapping symbols which don't appear in the
    original_translation_mapping symbol inventory or potential cascading replacements.
    These checks show a warning, but will not raise an Exception.

    Args:
        input_string: str, string to do symbol replacements/substitutions on
        original_translation_mapping: dict[str, str], original mapping to/from IPA, used only for validation checks
        reduction_mapping: dict[str, str], additional symbol reduction, usually for IPA inventories
    """
    cascading_keys = _find_cascading_keys_in_symbol_mapping(reduction_mapping)
    if len(cascading_keys) > 0:
        warnings.warn(
            f"Post-processing does not perfrom cascading replacements, but overlapping key/value pairs are detected. Check that this is intended. These keys are affected: {cascading_keys}."
        )

    new_keys = _get_extra_reduction_keys(original_translation_mapping, reduction_mapping)
    if len(new_keys) > 0:
        warnings.warn(f"There are keys in post-processing which do not appear in the original phonetable: {new_keys}.")

    # Replacements happen greedily in the order of the post processing map,
    # because there may be intentional orderings of substitutions.
    pattern = "|".join(re.escape(k) for k in reduction_mapping.keys())

    return re.sub(pattern, lambda match: reduction_mapping[match.group()], input_string)


def _find_cascading_keys_in_symbol_mapping(symbol_inventory_map: dict[str, str]) -> list[tuple[str, str]]:
    """Returns any keys that might have values that would cascade to later keys during replacement.
    Used as a warning if there seem to be cascading replacements involving the same symbol.
    This doesn't impact the behavior of the substitution, but serves as a check
    against unexpected cascading replacements.

    Args:
        symbol_inventory_map: An ordered dictionary mapping substrings to their desired replacement values.
    """
    result = []
    ordered_keys = list(symbol_inventory_map.keys())
    for i, k1 in enumerate(ordered_keys[:-1]):
        current_value = symbol_inventory_map[k1]

        # Skip empty strings
        if current_value == "":
            continue

        for k2 in ordered_keys[i + 1 :]:
            if current_value in k2:
                result.append((k1, k2))

    return result


def _get_extra_reduction_keys(original_mapping: dict[str, str], reduction_mapping: dict[str, str]) -> set[str]:
    """Returns the set of keys in reduction_map that are not used in the corpus' official symbol inventory.

    Args:
        original_mapping: The original corpus symbols mapped to/from IPA symbols.
        reduction_mapping: An symbol to symbol mapping for standardizing the output.
    """
    ipa_original = set(original_mapping.values())
    ipa_reduction_keys = set(reduction_mapping.keys())
    overlap = ipa_reduction_keys - ipa_original
    return overlap
