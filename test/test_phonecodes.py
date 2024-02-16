"""Load some pronlexes from the 'fixtures' subdirectory,
test phone code conversion, and test both word and phone searches.
"""
import phonecodes.phonecodes as phonecodes

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
]


@pytest.mark.parametrize("in_code, out_code, fn_call, language", phonecode_cases)
def test_conversion_functions(in_code, out_code, fn_call, language, sentences):
    result = fn_call(sentences[language][in_code], language)
    expected = sentences[language][out_code]
    assert result == expected


@pytest.mark.parametrize("in_code, out_code, fn_call, language", phonecode_cases)
def test_convert(in_code, out_code, fn_call, language, sentences):
    s_in = sentences[language][in_code]
    expected = sentences[language][out_code]
    converted = phonecodes.convert(s_in, in_code, out_code, language)
    assert converted == expected


def test_convert_value_error():
    with pytest.raises(ValueError):
        phonecodes.convert("DH IH S IH Z AH0 T EH1 S T", "arpabet", "buckeye")


@pytest.mark.parametrize("ipa_str, buckeye_str", [("kæ̃n", "KAENN"), ("kæ̃n", "kaenn")])
def test_additional_buckeye_examples(ipa_str, buckeye_str):
    assert phonecodes.buckeye2ipa(buckeye_str) == ipa_str
    assert phonecodes.ipa2buckeye(ipa_str) == buckeye_str.upper()
