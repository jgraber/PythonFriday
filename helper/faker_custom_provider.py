from typing import OrderedDict
from faker.providers import BaseProvider
from faker import Faker

class UniversityProvider(BaseProvider):
    university_names = [
        "Springfield University",
        "Shelbyville Institute of Technology",
        "Capitol City College",
        "Metropolis University",
        "Gotham City Academy"
    ]

    faculty_names = [
        "Faculty of Engineering",
        "Faculty of Arts and Sciences",
        "Faculty of Medicine",
        "Faculty of Business Administration",
        "Faculty of Law"
    ]

    course_titles = [
        "Introduction to Artificial Intelligence",
        "Advanced Python Programming",
        "Quantum Computing 101",
        "History of Modern Art",
        "Principles of Microeconomics"
    ]

    building_names = [
        "Newton Hall",
        "Curie Science Center",
        "Einstein Library",
        "Turing Auditorium",
        "Bohr Research Building"
    ]

    grades_name = OrderedDict(
    [
        ("A", 1),
        ("B", 2),
        ("C", 5),
        ("D", 3),
        ("F", 5)
    ])

    def university_name(self):
        return self.random_element(self.university_names)

    def faculty_name(self):
        return self.random_element(self.faculty_names)

    def course_title(self):
        return self.random_element(self.course_titles)

    def building_name(self):
        return self.random_element(self.building_names)
    
    def grades(self, count):
        return self.random_elements(self.grades_name, count, unique=False, use_weighting=True)
    

fake = Faker()
fake.seed_instance(42)
fake.add_provider(UniversityProvider)

# Generate data
print(fake.university_name())  
# Springfield University

print(fake.faculty_name())
# Faculty of Medicine

print(fake.course_title())
# Advanced Python Programming

print(fake.building_name())
# Einstein Library


from collections import Counter
for i in range(10):
    fake_grades = fake.grades(100)
    counter = Counter(fake_grades)
    print(counter)