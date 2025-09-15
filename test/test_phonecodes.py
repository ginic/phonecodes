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
    ("timit", "ipa", phonecodes.timit2ipa, "eng_no_stress"),
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


@pytest.mark.parametrize("ipa_str, buckeye_str", [("kæ̃n", "KAENN"), ("kæ̃n", "kaenn"), ("ʌpβoʊt", "AHPBFOWT")])
def test_additional_buckeye_examples(ipa_str, buckeye_str):
    assert phonecodes.buckeye2ipa(buckeye_str) == ipa_str
    assert phonecodes.ipa2buckeye(ipa_str) == buckeye_str.upper()


@pytest.mark.parametrize(
    "ipa_str, timit_str",
    [
        (
            " tʃ ɑ k l ɨ t ",
            "h# ch aa kcl k l ix tcl t h#",
        ),  # 'chocolate' with start/stop tokens and no initial closure
        ("tʃ ɑ k l ɨ t", "tcl ch aa k l ix tcl t"),  # 'chocolate' with mixed closure inclusion
        ("tʃ ɑ k l ɨ t", "tcl ch aa k l ix t"),  # 'chocolate' with mixed closure inclusion
        ("tʃɑklɨt", "tclchaaklixtclt"),  # 'chocolate' with mixed closure inclusion, no spaces
        ("tʃɑklɨt", "tclchaaklixt"),  # 'chocolate' with mixed closure inclusion, no spaces
        ("dʒ oʊ k", "JH OW K"),  # 'joke' without closures
        ("dʒ oʊ k", "DCL JH OW KCL K"),  # 'joke' with closures
        (
            "ɹ ɨ w ɔ ɹ ɾ ɪ d b aɪ b ɪ g t ɪ p s",
            "R IX W AO R DX IH DCL B AY BCL B IH GCL T IH PCL P S",
        ),  # 'rewarded by big tips'
        ("bɪgtɪps", "bclbihgcltihpclps"),  # 'big tips' lower case no spaces
        ("bɪgtɪps", "bihgclgtcltihps"),  # 'big tips' lower case no spaces, flip closures
        # 'This has been attributed to helium film flow in the vapor pressure thermometer.'
        (
            "ðɪs hɛz bɛn ɪtʃɪbʉɾɪd tʉ ɦɪliɨm fɪlm floʊ ən ðɨ veɪpə pɹɛʃɹ̩ θəmɑmɨɾɚ",
            "DHIHS HHEHZ BCLBEHN IHTCLCHIHBCLBUXDXIHDCL TUX HVIHLIYIXM FIHLM FLOW AXN DHIX VEYPCLPAX PCLPREHSHER THAXMAAMIXDXAXR",
        ),
        # 'About dawn he got up to blow.'
        ("ə̥baʊtdɔnɦigɑɾʌptɨbloʊ", "AX-HBCLBAWTCLDAONHVIYGCLGAADXAHPCLTIXBCLBLOW"),
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
