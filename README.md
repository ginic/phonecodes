# phonecodes
This library provides tools for converting between the [International Phonetic Alphabet (IPA)](https://en.wikipedia.org/wiki/International_Phonetic_Alphabet) and other phonetic alphabets used to transcribe speech, including Callhome, [X-SAMPA](https://en.wikipedia.org/wiki/X-SAMPA), [ARPABET](https://en.wikipedia.org/wiki/ARPABET), [DISC/CELEX](https://catalog.ldc.upenn.edu/LDC96L14), [Buckeye Corpus Phonetic Alphabet](https://buckeyecorpus.osu.edu/), and [TIMIT](https://catalog.ldc.upenn.edu/LDC93S1). Additionally, tools for searching mappings between phonetic symbols and reading/writing pronounciation lexicon files in several standard formats are also provided.

These functionalities are useful for processing data for automatic speech recognition, text to speech, and linguistic analyses of speech.

# Setup and Installation
Install the library by running `pip install phonecodes` with python 3.10 or greater. It probably works with earlier versions of python, but this was not tested.

Developers may refer to the CONTRIBUTIONS.md for information on the development environment for testing, linting and contributing to the code.

# Basic Usage
## Converting between Phonetic Alphabets
If you want to convert to or from IPA to some other phonetic code, use `phonecodes.phonecodes` as follows:
```python
>>> from phonecodes import phonecodes
>>> print(phonecodes.CODES) # available phonetic alphabets
{'arpabet', 'buckeye', 'ipa', 'timit', 'callhome', 'xsampa', 'disc'}
>>> phonecodes.convert("DH IH S IH Z AH0 T EH1 S T", "arpabet", "ipa", "eng") # convert from IPA to ARPABET with language explicitly specified
'ð ɪ s ɪ z ə t ˈɛ s t'
>>> phonecodes.convert("ð ɪ s ɪ z ə t ˈɛ s t", "ipa", "arpabet") # convert from IPA to ARPABET with optional language left out
'DH IH S IH Z AH0 T EH1 S T'
>>> phonecodes.ipa2arpabet("ð ɪ s ɪ z ə t ˈɛ s t", "eng") # equivalent to previous with explicit language
'DH IH S IH Z AH0 T EH1 S T'
>>> phonecodes.ipa2arpabet("ð ɪ s ɪ z ə t ˈɛ s t") # equivalent to previous with optional language left out
'DH IH S IH Z AH0 T EH1 S T'
>>> phonecodes.convert("DH IH S IH Z AH0 T EH1 S T", "arpabet", "ipa") # convert from ARPABET to IPA, optional language left out
'ð ɪ s ɪ z ə t ˈɛ s t'
>>> phonecodes.arpabet2ipa("DH IH S IH Z AH0 T EH1 S T", "eng") # equivalent to previous with optional language explicit
'ð ɪ s ɪ z ə t ˈɛ s t'
```

For 'arpabet', 'buckeye', 'timit' and 'xsampa', specifying a language is optional and ignored by the code, since X-SAMPA is language agnostic and ARAPABET, Buckeye, and TIMIT were designed to work only for English.

For 'callhome' and 'disc' you should also specify a language code from the following lists:
- DISC/CELEX: Dutch `'nld'`, English `'eng'`, German `'deu'`. Uses German if unspecified.
- Callhome: Spanish `'spa'`, Egyptian Arabic `'arz'`, Mandarin Chinese `'cmn'`. You MUST specify an appropriate language code or you'll get a KeyError.

## Additional post-processing
An additional use case when converting between phonecodes is to normalize the final mapping to a subset of IPA symbols. This is useful if you are collapsing similar sounds together to a reduced symbol inventory or if you are standardizing two corpora with different IPA inventories/conventions to a shared subset.

We support this use case through the `post_conversion_mapping` keyword argument, an optional dictionary remapping provided with all phonecodes conversion functions. You can provide a custom mapping. Be aware that the remapping algorithm is greedy, proceeds in the order that keys appear in the dictionary, and diacritics need to appear with a base symbol in the mapping.

Additionally, we provide IPA-to-IPA post-processing dictionary mappings in `phonecodes.phonecode_tables`:
- `phonecodes.phonecode_tables.STANDARD_TIMIT_IPA_REDUCTION`: The 'standard' TIMIT label reduction used in Lee and Hon (1989) that reduces the original 64 TIMIT phonetic labels to 39 categories. This reduction is widely used in the speech recognition community.
- `phonecodes.phonecode_tables.BUCKEYE_IPA_TO_TIMIT_BUCKEYE_SHARED` and `phonecodes.phonecode_tables.TIMIT_IPA_TO_TIMIT_BUCKEYE_SHARED`: A conservative reduction from the Buckeye and TIMIT IPA inventories, respectively, to a shared symbol set. This maps nasalized vowels and flaps to their non-nasalized versions, r-colored vowels ('ɚ', 'ɝ') to syllabic r ('ɹ̩'), and normalizes variants of 'ʌ' and schwa to sch

```python
>>> from phonecodes import phonecodes
# Conversion from Buckeye to IPA using the original published Buckeye mapping
>>> phonecodes.convert("B AHN NX AAN NX AH", "buckeye", "ipa")
'b ʌ̃ ɾ̃ ɑ̃ ɾ̃ ʌ'
# Conversion from Buckeye to IPA with postprocessing to an IPA inventory shared with TIMIT
>>> phonecodes.convert("B AHN NX AAN NX AH", "buckeye", "ipa", post_conversion_mapping = phonecodes.phonecode_tables.BUCKEYE_IPA_TO_TIMIT_BUCKEYE_SHARED)
'b ə n ɑ n ə'
# Custom mapping example - note that the nasalized diacritics are not affected by the remapping
>>> phonecodes.convert("B AHN NX AAN NX AH", "buckeye", "ipa", post_conversion_mapping = {'ʌ':'ə'})
'b ə̃ ɾ̃ ɑ̃ ɾ̃ ə'
```

## Reading Corpus Files
If you are working with specific corpora, you can also convert between certain corpus formats as follows:
```
>>> from phonecodes import pronlex
>>> my_lex = pronlex.read("test/fixtures/isle_eng_sample.txt", "isle", "eng") # Read in an English ISLE corpus file
>>> my_lex.w2p # see orthographic to phonetic word mapping
{'a': ['#', 'ə', '#'], 'is': ['#', 'ɪ', 'z', '#'], 'test': ['#', 't', 'ˈɛ', 's', 't', '#'], 'this': ['#', 'ð', 'ɪ', 's', '#']}
new_lex = my_lex.recode('arpabet') # Convert mapping to ARPABET
>>> new_lex.w2p
{'a': ['#', 'AH0', '#'], 'is': ['#', 'IH', 'Z', '#'], 'test': ['#', 'T', 'EH1', 'S', 'T', '#'], 'this': ['#', 'DH', 'IH', 'S', '#']}
```

The supported corpus formats and their corresponding phonetic alphabets are as follows:
| Corpus Format | Phonetic Alphabet | Language Options   |
|---------------|-------------------|--------------------|
| 'babel' | 'xsampa' |'amh', 'asm', 'ben', 'yue', 'ceb', 'luo', 'kat', 'gug', 'hat', 'ibo', 'jav', 'kur', 'lao', 'lit', 'mon', 'pus', 'swa', 'tgl', 'tam', 'tpi', 'tur', 'vie', 'zul' |
| 'callhome' | 'callhome' | 'arz', 'cmn', 'spa' |
| 'celex' | 'disc' | 'eng', 'ndl', 'deu' |
| 'isle' | 'ipa' |  Not required |

# Known Limitations
- You cannot convert to TIMIT format from IPA or any other phonecode, because TIMIT marks closures of stops with separate symbols. There are no symbols corresponding to these closures in other phonecodes and the closure is not predictable from the transcription alone.