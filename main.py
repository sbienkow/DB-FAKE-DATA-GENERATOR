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
    JEST_W_TRAKCIE = namedtuple('JEST_W_TRAKCIE', 'Pesel, Id_podróży, Data_od, Data_do')
    PRZEWODNIK = namedtuple('PRZEWODNIK', 'Imię, Nazwisko, Telefon, Pesel')
    PROWADZI = namedtuple('PROWADZI', 'Pesel, Id_podróży')
    ATRAKCJA = namedtuple('ATRAKCJA', 'Id_atrakcji, Nazwa, Miasto, Opis')
    PODCZAS = namedtuple('PODCZAS', 'Id_podróży, Id_atrakcji')

    class FunWithMul:

        def __init__(self, fun, mul):
            self.fun = fun
            self.mul = mul
            self.__name__ = fun.__name__

        def __call__(self, num):
            return self.fun(max(int(self.mul * num), 2))

    MIASTO = namedtuple('MIASTO', 'miasto, kraj, gmt, rodzaj_klimatu, punkty_gti')
    FAKE = faker.Faker('pl_PL')

    # COUNTRIES = {FAKE.country() for _ in range(30)}
    # CITIES = {CITY(FAKE.city(), country) for country in COUNTRIES for _ in range(100)}

    def __init__(self):
        self.queue = (
            self.FunWithMul(self.miasta, 0.1),
            self.FunWithMul(self.podróżnicy, 1),
            self.FunWithMul(self.ubezpieczenia, 3),
            self.FunWithMul(self.podróże, 5),
            self.FunWithMul(self.jest_w_trakcie, 4),
            self.FunWithMul(self.przewodnicy, 1),
            self.FunWithMul(self.prowadzi, 2),
            self.FunWithMul(self.atrakcje, 0.4),
            self.FunWithMul(self.podczas, 1),
        )

    def gen(self, num):
        return (self.FUN(fun.__name__, fun(num)) for fun in self.queue)

    def export_to_file(self, filename, num):
        with open(filename, 'w') as f:
            for name, data in self.gen(num):
                for entry in data:
                    f.write('{}\n'.format(self.sql(name, entry)))

    @staticmethod
    def sql(name, entry):
        return 'INSERT INTO {} ({}) VALUES ({});'.format(name,
                                                        ', '.join(k for k, v in entry._asdict().items()
                                                                  if v is not None),
                                                        ', '.join("'{}'".format(i)
                                                                  for i in entry._asdict().values()
                                                                  if i is not None))
    def miasta(self, num):
        self.Miasta = {self.MIASTO(self.FAKE.city(), 'Polska', 0, 'ZIMNO', 1) for _ in range(num)}
        return self.Miasta



    def podróżnicy(self, num):
        self.Podróżnicy = [self.PODRÓŻNIK(self.FAKE.first_name(),
                                          self.FAKE.last_name(),
                                          self.FAKE.street_name(),
                                          self.FAKE.random_int(min=1, max=999),
                                          None if self.FAKE.random_int(min=0,
                                                                       max=39) == 0 else self.FAKE.building_number(),
                                          self.FAKE.postcode(),
                                          self.FAKE.random_element(elements=self.Miasta).miasto,
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
                                                 *(date.strftime('%d-%b-%y')
                                                   for dates in (
                                                       (x, self.FAKE.date_between(x, '+1y'))
                                                       for x in (self.FAKE.past_date(),)
                                                   )
                                                   for date in dates
                                                   ),
                                                 self.FAKE.random_element(self.Podróżnicy).Pesel
                                                 )
                              for i in range(num)
                              ]
        return self.Ubezpieczenia

    def podróże(self, num):
        numery = random.sample(range(num * 1000), num)
        self.Podróże = [self.PODRÓŹ(numery[i], random.randrange(100, 10000, 50))
                        for i in range(num)]
        return self.Podróże

    def jest_w_trakcie(self, num):
        self.Jest_w_trakcie = []
        for _ in range(num):
            Pesel = self.FAKE.random_element(self.Podróżnicy).Pesel
            Id_podróży = self.FAKE.random_element(self.Podróże).Id_podróży
            Data_od = self.FAKE.past_date()
            Data_do = self.FAKE.date_between(Data_od, '+1y').strftime('%d-%b-%y')
            # TODO Should make sure given person isn't in any other trip at the same time
            self.Jest_w_trakcie.append(self.JEST_W_TRAKCIE(Pesel, Id_podróży, Data_od.strftime('%d-%b-%y'), Data_do))

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
            Pesel = self.FAKE.random_element(self.Przewodnicy).Pesel
            Id_podróży = self.FAKE.random_element(self.Podróże).Id_podróży
            self.Prowadzi.add(self.PROWADZI(Pesel, Id_podróży))

        return self.Prowadzi

    def atrakcje(self, num):
        self.Atrakcje = []
        for i in range(num):
            # Couldn't find anything better. Probably should use external word list.
            Nazwa = self.FAKE.company()
            Opis = self.FAKE.text(max_nb_chars=200)
            Miasto = self.FAKE.random_element(self.Miasta).miasto
            self.Atrakcje.append(self.ATRAKCJA(i, Nazwa, Miasto, Opis))

        return self.Atrakcje

    def podczas(self, num):
        self.Podczas = set()
        for _ in range(num):
            Id_podróży = self.FAKE.random_element(self.Podróże).Id_podróży
            Id_atrakcji = self.FAKE.random_element(self.Atrakcje).Id_atrakcji
            self.Podczas.add(self.PODCZAS(Id_podróży, Id_atrakcji))
        return self.Podczas

def main(filename, num):
    FakeDataGenerator().export_to_file(filename, num)




if __name__ == '__main__':
    main('inserts.sql', 1000)