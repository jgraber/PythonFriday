# Example for PrettyPrinter to create a better output than print()

data = [
	{
		'name': "Rebecca Stephenson",
		'phone': "(154) 221-8558",
		'zipCode': "900185",
		'country': "South Korea",
		'options': ['a','b','c'],
		'total': "$74.79"
	},
	{
		'name': "Amos Nieves",
		'phone': "1-762-301-2264",
		'zipCode': "25566",
		'country': "Russian Federation",
		'options': {
            'a': 'full',
            'f': 'partial',
            'c': {'k1': 1,
                  'k2': 3}
        },
		'total': "$21.78"
	}
]

print("Regular print():")
print(data)
print("\n\n")

print("PrettyPrinter:")
import pprint
pp = pprint.PrettyPrinter()
pp.pprint(data)
print("\n\n")

print("PrettyPrinter with options:")
pp = pprint.PrettyPrinter(indent=5, depth=10, width=40, compact=False)
pp.pprint(data)
