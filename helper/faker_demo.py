from faker import Faker

# Create a Faker instance
fake = Faker()

# Generate random fake data
print(fake.name())
print(fake.address())
print(fake.email())


print("*" * 50)
print("with locale de_DE\n")

fake_de = Faker('de_DE')
print(fake_de.name())


print("*" * 50)
print("with seed(42)\n")

fake_seed = Faker()
fake_seed.seed_instance(42)
print(fake_seed.name())  


print("*" * 50)

print(fake.text())
print("------")
print(fake.paragraph(nb_sentences=5))
print("------")
print(fake.sentence(nb_words=10, variable_nb_words=False))

print("*" * 50)
print("Credit Cards\n")

print(fake.credit_card_provider())
print(fake.credit_card_number())
print(fake.credit_card_expire())
print(fake.credit_card_security_code())
print("------")
print(fake.credit_card_full())

print("*" * 50)
print("e-mail\n")

print(fake.ascii_company_email())
print(fake.ascii_free_email())
print(fake.ascii_safe_email())

print("*" * 50)
print("phone numbers\n")

print(fake.basic_phone_number())
print(fake.country_calling_code())

print("*" * 50)
print("ISBN\n")

print(fake.isbn10())
print(fake.isbn13())

print("*" * 50)
print("Coordinates\n")

print(fake.coordinate())
print(fake.latitude())
print(fake.longitude())
print(fake.latlng())
print(fake.local_latlng())
print(fake.location_on_land())

# print(dir(fake))