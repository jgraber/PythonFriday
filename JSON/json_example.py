import json

def example():
    # You collect and combine data in an 
    # arbitrarily nested data structure:
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

    return data


def save():
    data = example()
    data_json = json.dumps(data, indent=4)

    with open("data.json", "w") as f:
        f.write(data_json)

def load():
    with open("data.json", "r") as f:
        data_json = f.read()
        data = json.loads(data_json)
        print(data)

if __name__ == '__main__':
    save()
    load()