import pickle

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
    
    # Use binary mode for your file
    with open("pickle.bin", "wb") as f:
        pickle.dump(data, f)                     

  
  
def restore():
    # Use binary mode to read your file
    with open("pickle.bin", "rb") as f:
        data = pickle.load(f)
        for entry in data:
            for key in entry:
                print(f"{key} => {entry[key]}")


if __name__ == '__main__':
    save()
    restore()