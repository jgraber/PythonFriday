from lingua import Language, LanguageDetectorBuilder

comments = [
    "Hi",
    "Welcome",
    "Hei",
    "Hej",
    "Hallå",
    "Hola",
    "God dag",
    "Guten Tag",
    "Ich spreche",
    "Bara lite grann",
    "Sólo un poco",
    "Gewoon een beetje",
    "Un peu",
    "Parlez-vous français? ",
    "Ich spreche nur ein bisschen Französisch.",
    "A little bit is better than nothing."
]


detector = LanguageDetectorBuilder.from_all_languages().with_preloaded_language_models().build()
for comment in comments:
    print(f"\n\n{comment}")
    confidence_values = detector.compute_language_confidence_values(comment)
    top_languages = confidence_values[:3]
    for confidence in top_languages:
        print(f"{confidence.language.name}: {confidence.value:.2f}")


languages = [Language.ENGLISH, Language.FRENCH, Language.GERMAN]
detector = LanguageDetectorBuilder.from_languages(*languages).build()
sentence = "Parlez-vous français? " + \
           "Ich spreche nur ein bisschen Französisch. " + \
           "A little bit is better than nothing."
for result in detector.detect_multiple_languages_of(sentence):
    print(f"{result.language.name}: '{sentence[result.start_index:result.end_index]}' - ")
# FRENCH: 'Parlez-vous français? '
# GERMAN: 'Ich spreche Französisch nur ein bisschen. '
# ENGLISH: 'A little bit is better than nothing.'