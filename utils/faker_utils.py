from faker import Faker


fake = Faker("pt_BR")


def new_account():
    return {
        "name": fake.name(),
        "email": f"bugbank.{fake.uuid4()}@example.com",
        "password": "Teste@12345",
    }
