"""Unit tests for phonecodes.phonecodes functionality"""

import phonecodes.phonecodes as phonecodes
from phonecodes.phonecode_tables import (
    BUCKEYE_IPA_TO_TIMIT_BUCKEYE_SHARED,
    TIMIT_IPA_TO_TIMIT_BUCKEYE_SHARED,
    STANDARD_TIMIT_IPA_REDUCTION,
)

import pytest


# Test the phonecode conversions
phonecode_cases = [
    ("arpabet", "ipa", phonecodes.arpabet2ipa, "eng"),
    ("ipa", "arpabet", phonecodes.ipa2arpabet, "eng"),
    ("ipa", "callhome", phonecodes.ipa2callhome, "arz"),
    ("ipa", "callhome", phonecodes.ipa2callhome, "cmn"),
    ("ipa", "callhome", phonecodes.ipa2callhome, "spa"),
    ("callhome", "ipa", phonecodes.callhome2ipa, "arz"),
    ("callhome", "ipa", phonecodes.callhome2ipa, "cmn"),
    ("callhome", "ipa", phonecodes.callhome2ipa, "spa"),
    ("ipa", "disc", phonecodes.ipa2disc, "deu"),
    ("ipa", "disc", phonecodes.ipa2disc, "eng"),
    ("ipa", "disc", phonecodes.ipa2disc, "nld"),
    ("disc", "ipa", phonecodes.disc2ipa, "deu"),
    ("disc", "ipa", phonecodes.disc2ipa, "eng"),
    ("disc", "ipa", phonecodes.disc2ipa, "nld"),
    ("ipa", "xsampa", phonecodes.ipa2xsampa, "amh"),
    ("ipa", "xsampa", phonecodes.ipa2xsampa, "ben"),
    ("xsampa", "ipa", phonecodes.xsampa2ipa, "amh"),
    ("xsampa", "ipa", phonecodes.xsampa2ipa, "ben"),
    # Buckeye conversion doesn't account for stress markers and language is ignored
    ("buckeye", "ipa", phonecodes.buckeye2ipa, "eng_no_stress"),
    ("ipa", "buckeye", phonecodes.ipa2buckeye, "eng_no_stress"),
    ("timit", "ipa", phonecodes.timit2ipa, "eng_no_stress"),
]


# Test basic functionality of the phonecodes.x2y conversion functions
@pytest.mark.parametrize("in_code, out_code, fn_call, language", phonecode_cases)
def test_conversion_functions(in_code, out_code, fn_call, language, sentences):
    result = fn_call(sentences[language][in_code], language)
    expected = sentences[language][out_code]
    assert result == expected


# Test basic functionality of the convert function with input and output phonecodes
@pytest.mark.parametrize("in_code, out_code, fn_call, language", phonecode_cases)
def test_convert(in_code, out_code, fn_call, language, sentences):
    s_in = sentences[language][in_code]
    expected = sentences[language][out_code]
    converted = phonecodes.convert(s_in, in_code, out_code, language)
    assert converted == expected


# Invalid phonecode pairs raise a value error
@pytest.mark.parametrize(
    "input_code, output_code",
    [
        ("arpabet", "buckeye"),
        ("ipa", "timit"),
    ],
)
def test_convert_value_error(input_code, output_code):
    with pytest.raises(ValueError):
        phonecodes.convert("DH IH S IH Z AH0 T EH1 S T", input_code, output_code)


@pytest.mark.parametrize(
    "ipa_str, buckeye_str", [("kæ̃n", "KAENN"), ("kæ̃n", "kaenn"), ("ʌpβoʊt", "AHPBFOWT"), ("bɪɡtɪps", "BIHGTIHPS")]
)
def test_additional_buckeye_examples(ipa_str, buckeye_str):
    assert phonecodes.buckeye2ipa(buckeye_str) == ipa_str
    assert phonecodes.ipa2buckeye(ipa_str) == buckeye_str.upper()


@pytest.mark.parametrize(
    "ipa_str, timit_str",
    [
        ("tʃ ɑ k l ɨ t", "h# ch aa kcl k l ix tcl t h#"),  # 'chocolate' with start/stop tokens and no initial closure
        ("tʃ ɑ k l ɨ t", "tcl ch aa k l ix tcl t"),  # 'chocolate' with mixed closure inclusion
        ("tʃ ɑ k l ɨ t", "tcl ch aa k l ix t"),  # 'chocolate' with mixed closure inclusion
        ("tʃɑklɨt", "tclchaaklixtclt"),  # 'chocolate' with mixed closure inclusion, no spaces
        ("tʃɑklɨt", "tclchaaklixt"),  # 'chocolate' with mixed closure inclusion, no spaces
        ("dʒ oʊ k", "JH OW K"),  # 'joke' without closures
        ("dʒ oʊ k", "DCL JH OW KCL K"),  # 'joke' with closures
        (
            "ɹ ɨ w ɔ ɹ ɾ ɪ d b aɪ b ɪ ɡ t ɪ p s",
            "R IX W AO R DX IH DCL B AY BCL B IH GCL T IH PCL P S",
        ),  # 'rewarded by big tips'
        ("bɪɡtɪps", "bclbihgcltihpclps"),  # 'big tips' lower case no spaces
        ("bɪɡtɪps", "bihgclgtcltihps"),  # 'big tips' lower case no spaces, flip closures
        # 'This has been attributed to helium film flow in the vapor pressure thermometer.'
        (
            "ðɪs hɛz bɛn ɪtʃɪbʉɾɪd tʉ ɦɪliɨm fɪlm floʊ ən ðɨ veɪpə pɹɛʃɝ θəmɑmɨɾɚ",
            "DHIHS HHEHZ BCLBEHN IHTCLCHIHBCLBUXDXIHDCL TUX HVIHLIYIXM FIHLM FLOW AXN DHIX VEYPCLPAX PCLPREHSHER THAXMAAMIXDXAXR",
        ),
        # 'About dawn he got up to blow.'
        ("ə̥baʊtdɔnɦiɡɑɾʌptɨbloʊ", "AX-HBCLBAWTCLDAONHVIYGCLGAADXAHPCLTIXBCLBLOW"),
        # 'As we ate, we talked.'
        ("ʔæzwieɪtwitɔkt", "QAEZWIYEYTCLWIYTCLTAOKCLT"),
        # 'The overweight charmer could slip poison into anyone's tea.'
        # Note that the space is lost at the word boundary between 'overweight charmer'
        # and 'slip poison'.
        (
            "ði oʊvɚweɪtʃɑɹmɚ kʊd slɪpɔɪzn̩ ɪntʔ ɛɾ̃iwənz ti",
            "DHIY OWVAXRWEYTCL CHAARMAXR KCLKUHDCLD SLIHPCL POYZEN IHNTCLTQ EHNXIYWAXNZ TCLTIY",
        ),
    ],
)
def test_additional_timit_examples(ipa_str, timit_str):
    assert phonecodes.timit2ipa(timit_str) == ipa_str


# Tests the check for potential cascading keys in postprocessing
@pytest.mark.parametrize(
    "mapping, expected_value",
    [
        # Valid - key set and value set are disjoint
        ({"a": "x", "b": "y"}, []),
        ({"a": "b", "bc": "a"}, [("a", "bc")]),
        # Diacritical markers alone won't cause cascasdes
        ({"◌̩": "", "ɹ̩": "ɝ"}, []),
        # These will cause cascades
        ({"ax": "b", "bc": "d"}, [("ax", "bc")]),
        ({"r": "ɹ", "ɹ̩": "ɝ"}, [("r", "ɹ̩")]),
        # These standard reductions should not have any cascading changes
        (phonecodes.phonecode_tables.STANDARD_TIMIT_IPA_REDUCTION, []),
        (phonecodes.phonecode_tables.BUCKEYE_IPA_TO_TIMIT_BUCKEYE_SHARED, []),
        (phonecodes.phonecode_tables.TIMIT_IPA_TO_TIMIT_BUCKEYE_SHARED, []),
    ],
)
def test_find_cascading_keys_in_inventory_map(mapping, expected_value):
    assert phonecodes._find_cascading_keys_in_symbol_mapping(mapping) == expected_value


@pytest.mark.parametrize(
    "example, incode, outcode, expected",
    [
        ("AE1 D V ER0 T", "arpabet", "ipa", "ˈæ d v ɚ t"),
        ("AE1 D V ER1 T", "arpabet", "ipa", "ˈæ d v ˈɝ t"),
        ("AE0 ER1 T", "arpabet", "ipa", "æ ˈɝ t"),
        ("AE0 D V ER1 T AH0 Z M AH0 N T", "arpabet", "ipa", "æ d v ˈɝ t ə z m ə n t"),
    ],
)
def test_arpabet_stress_attachment(example, incode, outcode, expected):
    assert phonecodes.convert(example, incode, outcode) == expected


# Tests the standard conversion mappings work as expected with the phonecodes.convert function
@pytest.mark.parametrize(
    "example, incode, outcode, post_conversion_mapping, expected",
    [
        ("h# ch aa kcl k l ix tcl t h#", "timit", "ipa", STANDARD_TIMIT_IPA_REDUCTION, "tʃ ɑ k l ɪ t"),
        ("h#chaakclklixzhh#", "timit", "ipa", STANDARD_TIMIT_IPA_REDUCTION, "tʃɑklɪʃ"),
        (
            "w iyn w ern k ih n aan nx eh tq",
            "buckeye",
            "ipa",
            BUCKEYE_IPA_TO_TIMIT_BUCKEYE_SHARED,
            "w i w ɹ̩ k ɪ n ɑ n ɛ ʔ",
        ),
        (
            "w ax w axr k ih n aa nx eh q hv zh",
            "timit",
            "ipa",
            TIMIT_IPA_TO_TIMIT_BUCKEYE_SHARED,
            "w ə w ɹ̩ k ɪ n ɑ n ɛ ʔ h ʒ",
        ),
    ],
)
def test_convert_with_post_conversion_mapping(example, incode, outcode, post_conversion_mapping, expected):
    assert phonecodes.convert(example, incode, outcode, post_conversion_mapping=post_conversion_mapping) == expected


# Test cases for _get_extra_reduction_keys will
@pytest.mark.parametrize(
    "original_mapping, reduction_mapping, expected_extra_keys",
    [
        # Case 1: No extra keys - reduction keys are subset of original values
        ({"AA": "ɑ", "AE": "æ", "AH": "ə"}, {"ɑ": "a", "æ": "a"}, set()),
        # Case 2: Extra keys present - reduction has keys not in original values
        ({"AA": "ɑ", "AE": "æ"}, {"ɑ": "a", "ɪ": "i", "ʊ": "u"}, {"ɪ", "ʊ"}),
        # Case 3: All extra keys
        ({"AA": "ɑ", "AE": "æ"}, {"x": "y", "z": "w"}, {"x", "z"}),
        # Case 4: Empty reduction mapping
        ({"AA": "ɑ", "AE": "æ"}, {}, set()),
        # Case 5: Empty original mapping
        ({}, {"ɑ": "a", "æ": "e"}, {"ɑ", "æ"}),
        # Standard reductions should not have any extra keys
        (phonecodes.phonecode_tables._timit2ipa, STANDARD_TIMIT_IPA_REDUCTION, set()),
        (phonecodes.phonecode_tables._timit2ipa, TIMIT_IPA_TO_TIMIT_BUCKEYE_SHARED, set()),
        (phonecodes.phonecode_tables._buckeye2ipa, BUCKEYE_IPA_TO_TIMIT_BUCKEYE_SHARED, set()),
    ],
)
def test_get_extra_reduction_keys(original_mapping, reduction_mapping, expected_extra_keys):
    result = phonecodes._get_extra_reduction_keys(original_mapping, reduction_mapping)
    assert result == expected_extra_keys


# Test cases for _post_process_reduction without any warnings
@pytest.mark.parametrize(
    "input_string, original_mapping, reduction_mapping, expected_output",
    [
        # Simple single character substitution
        ("ɑ æ ə", {"AA": "ɑ", "AE": "æ", "AH": "ə"}, {"ɑ": "a", "æ": "a", "ə": "a"}, "a a a"),
        # Multi-character symbol substitution
        ("tʃɑklɪʃ", {"CH": "tʃ"}, {"tʃ": "č"}, "čɑklɪʃ"),
        # Partial substitution (some symbols not in reduction map)
        ("ɑ b æ c ə", {"AA": "ɑ", "AE": "æ"}, {"ɑ": "a", "æ": "e"}, "a b e c ə"),
        # No substitutions needed
        ("hello world", {"A": "a", "z": "x"}, {"x": "y"}, "hello world"),
        # Empty string
        ("", {"A": "a"}, {"a": "b"}, ""),
        # Deletion (map to empty string)
        ("ɑzæ", {"AA": "ɑ", "x": "z"}, {"z": ""}, "ɑæ"),
        # Order matters - greedy left-to-right substitution
        ("abc", {"A": "a", "B": "b", "z": "ab"}, {"a": "x", "b": "y", "ab": "z"}, "xyc"),
        # Real TIMIT reduction example
        ("tʃ ɑ k l ɨ ʃ", phonecodes.phonecode_tables._timit2ipa, STANDARD_TIMIT_IPA_REDUCTION, "tʃ ɑ k l ɪ ʃ"),
    ],
)
def test_post_process_reduction_substitution(input_string, original_mapping, reduction_mapping, expected_output):
    result = phonecodes._post_process_reduction(input_string, original_mapping, reduction_mapping)
    assert result == expected_output


# Test warning behavior for _post_process_reduction
def test_post_process_reduction_warns_on_cascading_keys():
    """Test that cascading keys trigger a warning"""
    input_string = "abc"
    original_mapping = {"A": "a", "B": "b", "z": "bc"}
    reduction_mapping = {"a": "b", "bc": "d"}  # "a"->"b" could cascade to "bc"

    with pytest.warns(UserWarning, match="cascading replacements"):
        phonecodes._post_process_reduction(input_string, original_mapping, reduction_mapping)


def test_post_process_reduction_warns_on_extra_keys():
    """Test that extra keys trigger a warning"""
    input_string = "ɑ æ"
    original_mapping = {"AA": "ɑ", "AE": "æ"}
    reduction_mapping = {"ɑ": "a", "ɪ": "i"}  # "ɪ" not in original mapping values

    with pytest.warns(UserWarning, match="do not appear in the original phonetable"):
        phonecodes._post_process_reduction(input_string, original_mapping, reduction_mapping)
