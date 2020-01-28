from random import randint, random
from uuid import uuid4

from app.settings import DISEASES_LIST, POPULATION


def decision(probability: float) -> bool:
    return random() < probability


class StandardPerson:

    def __init__(self, id):
        self.luck = randint(10, 90) / 100
        self.last_test_was = randint(1, 180)
        self.diseases = []
        self.name = id

        for disease in DISEASES_LIST:
            if len(self.diseases) > 14:
                break
            if decision(DISEASES_LIST.get(disease)):
                self.diseases.append({disease: DISEASES_LIST.get(disease)})


persons = []

for i in range(POPULATION):
    persons.append(StandardPerson(uuid4))

print(len(list(filter(lambda person: len(person.diseases) < 1, persons))))
