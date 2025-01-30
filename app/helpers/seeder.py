from faker import Faker
import random as r
from app.models import db, Contact

def fake_us_phone() -> int:
    n = []
    n.append(r.randint(6, 9))
    for _ in range(1, 10):
        n.append(r.randint(0, 9))
    return int(''.join(map(str, n)))

def seed_contacts(count: int = 10) -> None:
    if Contact.count() > 0:
        print("Contacts already seeded")
        return None
    fake = Faker()
    for _ in range(count):
        c = Contact(
            name=fake.name(),
            fname=fake.first_name(),
            lname=fake.last_name(),
            email=fake.email(),
            phone=fake_us_phone(),
            address=f"{fake.city()}, {fake.state_abbr()}, {fake.zipcode()}"
        )
        if c.save():
            print(f"Contact {c.name} created successfully")
        else:
            print(f"Error creating contact {c.name}")
    return None