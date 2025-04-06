from langdetect import detect, detect_langs

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


for comment in comments:
    print(f"\n\n{comment}")
    print(detect(comment))
    print(detect_langs(comment))


sentence = "Parlez-vous français? " + \
           "Ich spreche nur ein bisschen Französisch. " + \
           "A little bit is better than nothing."
print(f"\n\n{sentence}")
print(detect(sentence))
print(detect_langs(sentence))