from collections import namedtuple
import faker
from pesel import pesel
import random


class FakeDataGenerator:
    FUN = namedtuple('FUN', 'name, data')
    PODRÓŻNIK = namedtuple('PODRÓŻNIK',
                           'Imię, Nazwisko, Ulica, Nr_domu, Nr_mieszkania, Kod_pocztowy, Miasto, Telefon, Email, Pesel')
    UBEZPIECZENIE = namedtuple('UBEZPIECZENIE', 'Numer, Cena, Opis, Data_od, Data_do, Pesel')
    PODRÓŹ = namedtuple('PODRÓŻ', 'Id_podróży, Cena')
    JEST_W_TRAKCIE = namedtuple('JEST_W_TRAKCIE', 'Id, Pesel, Id_podróży, Data_od, Data_do')
    PRZEWODNIK = namedtuple('PRZEWODNIK', 'Imię, Nazwisko, Telefon, Pesel')
    PROWADZI = namedtuple('PROWADZI', 'Pesel, Id_podróży')
    ATRAKCJA = namedtuple('ATRAKCJA', 'Id_atrakcji, Nazwa, Miasto, Opis')

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
                                          self.FAKE.random_element(elements=self.CITIES).name,
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
                                                 *("'{}'".format(date.strftime('%d-%b-%y'))
                                                   for dates in (
                                                       (x, self.FAKE.date_between(x, '+1y'))
                                                       for x in (self.FAKE.past_date(),)
                                                   )
                                                   for date in dates
                                                   ),
                                                 random.choice(self.Podróżnicy).Pesel
                                                 )
                              for i in range(num)
                              ]
        return self.Ubezpieczenia

    def podróże(self, num):
        numery = random.sample(range(num * 1000), num)
        self.Podróże = [self.PODRÓŹ(numery(i), random.randrange(100, 10000, 50))
                        for i in range(num)]
        return self.Podróże

    def jest_w_trakcie(self, num):
        self.Jest_w_trakcie = []
        for i in range(num):
            Pesel = random.choice(self.Podróżnicy).Pesel
            Id_podróży = random.choice(self.Podróże).Id_podróży
            Data_od = self.FAKE.past_date()
            Data_do = self.FAKE.date_between(Data_od, '+1y')
            # TODO Should make sure given person isn't in any other trip at the same time
            self.Jest_w_trakcie.append(self.JEST_W_TRAKCIE(i, Pesel, Id_podróży, Data_od, Data_do))

        return self.Jest_w_trakcie

    def przewodnicy(self, num):
        self.Przewodnicy = [self.PRZEWODNIK(self.FAKE.first_name(),
                                            self.FAKE.last_name(),
                                            self.FAKE.numerify("#########"),
                                            pesel()
                                            )
                            for _ in range(num)]
        return self.Przewodnicy

    def prowadzi(self, num):
        self.Prowadzi = set()
        for i in range(num):
            Pesel = random.choice(self.Przewodnicy).Pesel
            Id_podróży = random.choice(self.Podróże).Id_podróży
            self.Prowadzi.add(self.PROWADZI(Pesel, Id_podróży))

        return self.Prowadzi

    def atrakcje(self, num):
        self.Atrakcje = []
        for i in range(num):
            # Couldn't find anything better. Probably should use external word list.
            Nazwa = self.FAKE.company()
            Opis = self.FAKE.text(max_nb_chars=200)
            Miasto = random.choice(self.CITIES).name
            self.Atrakcje.append(self.ATRAKCJA(i, Nazwa, Miasto, Opis))

        return self.Atrakcje
