from gruut import sentences
from collections.abc import Iterable  # Import to check if an object is iterable

class PhonemeConverter:
    def phonemize(self, text):
        pass

class GruutPhonemizer(PhonemeConverter):
    def phonemize(self, text, lang='en-us'):
        phonemized = []
        for sent in sentences(text, lang=lang):  # Use the lang parameter
            for word in sent:
                # Check if word.phonemes is not None and is an iterable before joining
                if word.phonemes and isinstance(word.phonemes, Iterable):
                    phonemized.append(''.join(word.phonemes))
                elif word.phonemes:
                    # Handle the non-iterable but not None case, e.g., append directly if it's a string
                    phonemized.append(word.phonemes)
                # Ignore if word.phonemes is None
        phonemized_text = ' '.join(phonemized)
        return phonemized_text

class PhonemeConverterFactory:
    @staticmethod
    def load_phoneme_converter(name: str, **kwargs):
        if name == 'gruut':
            return GruutPhonemizer()
        else:
            raise ValueError("Invalid phoneme converter.")
