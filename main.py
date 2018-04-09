from collections import namedtuple
import faker
from pesel import pesel
import random


class FakeDataGenerator:
    FUN = namedtuple('FUN', 'name, data')
    PODRÓŻNIK = namedtuple('PODRÓŻNIK',
                           'Imię, Nazwisko, Ulica, Nr_domu, Nr_mieszkania, Kod_pocztowy, Miasto, Kraj, Telefon, Email, Pesel')
    UBEZPIECZENIE = namedtuple('UBEZPIECZENIE', 'Numer, Cena, Opis, Data_od, Data_do, Pesel')

    CITY = namedtuple('CITY', 'name, country')
    FAKE = faker.Faker('pl_PL')

    # COUNTRIES = {FAKE.country() for _ in range(30)}
    # CITIES = {CITY(FAKE.city(), country) for country in COUNTRIES for _ in range(100)}

    def __init__(self):
        self.CITIES = {self.CITY(self.FAKE.city(), 'Polska') for _ in range(100)}
        self.queue = (self.podróżnicy,
         self.ubezpieczenia,
         )

    def gen(self, num):
        return (self.FUN(fun.__name__, fun(num)) for fun in self.queue)

    @staticmethod
    def sql(name, data):
        return 'INSERT INTO {} ({}) VALUES ({})'.format(name,
                                                        ', '.join(k for k, v in data._asdict().items()
                                                                  if v is not None),
                                                        ', '.join("'{}'".format(i)
                                                                  for i in data._asdict().values()
                                                                  if i is not None))

    def podróżnicy(self, num):
        self.Podróżnicy = [self.PODRÓŻNIK(self.FAKE.first_name(),
                                          self.FAKE.last_name(),
                                          self.FAKE.street_name(),
                                          self.FAKE.random_int(min=1, max=999),
                                          None if self.FAKE.random_int(min=0,
                                                                       max=39) == 0 else self.FAKE.building_number(),
                                          self.FAKE.postcode(),
                                          *self.FAKE.random_element(elements=self.CITIES),
                                          None if self.FAKE.random_int(min=0, max=39) == 0 else self.FAKE.numerify(
                                              "#########"),
                                          None if self.FAKE.random_int(min=0, max=39) == 0 else self.FAKE.email(),
                                          pesel()
                                          ) for _ in range(num)
                           ]
        return self.Podróżnicy

    def ubezpieczenia(self, num):
        numery = random.sample(range(num * 1000), num)
        self.Ubezpieczenia = [self.UBEZPIECZENIE(numery[i],
                                                 random.randrange(100, 10000, 50),
                                                 self.FAKE.text(max_nb_chars=200),
                                                # REALLY BAD CODING BELOW - JUST WANTED TO PLAY WITH IT
                                                 *("'{}'".format(i.strftime('%d-%b-%y'))
                                                   for m in (
                                                       (x, self.FAKE.date_between(x, "+1y"))
                                                       for x in (self.FAKE.past_date(),)
                                                   )
                                                   for i in m
                                                   ),
                                                 random.choice(self.Podróżnicy).Pesel
                                                 )
                              for i in range(num)
                              ]
        return self.Ubezpieczenia




