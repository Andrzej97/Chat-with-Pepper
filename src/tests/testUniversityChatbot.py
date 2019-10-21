import unittest
from src.university_chatbot.university_conversation_bot import UniversityBot
from src.common_utils.database_service import DatabaseProxy

db = DatabaseProxy('mongodb://localhost:27017/', 'PepperChatDB')
_university_chatbot = UniversityBot('university_chatbot', db)

class TestUniversistyChatbot(unittest.TestCase):

    def check_response(self, question, correct_answer):
        response = _university_chatbot.get_bot_response(question)
        self.assertTrue(response.text.lower(), correct_answer.lower())

    def test_dziekan_wgig(self):
        self.check_response(
            'Kto jest dziekanem wydziału górnictwa i geoinżynierii',
            'Dziekanem wydziału górnictwa i geoinżynierii jest profesor doktor habilitowany inżynier marek cała'
        )

    def test_dziekan_wimip(self):
        self.check_response(
            'Kto jest dziekanem wydziału inżynierii metali i informatyki przemysłowej',
            'Dziekanem wydziału inżynierii metali i informatyki przemysłowej jest profesor doktor habilitowany inżynier tadeusz telejko'
        )

    def test_dziekan_weaiib(self):
        self.check_response(
            'Kto jest dziekanem wydziału elektrorechniki, automatykii, informatyki i inżynierii biomedycznej',
            'Dziekanem wydziału elektrorechniki, automatykii, informatyki i inżynierii biomedycznej jest doktor habilitowany inżynier Ryszard Sroka, profesor nadzwyczajny'
        )

    def test_dziekan_wiet(self):
        self.check_response(
            'Kto jest dziekanem wydziału informatyki elektroniki i telekomunikacji',
            'dziekanem wydziału informatyki, elektroniki i telekomunikacji jest profesor doktor habilitowany inżynier Krzysztof Boryczko'
        )

    def test_dziekan_wimir(self):
        self.check_response(
            'Kto jest dziekanem wydziału inżynierii mechanicznej i robotyki',
            'dziekanem wydziału inżynierii mechanicznej i robotyki jest profesor doktor habilitowany inżynier Antoni Kalukiewicz'
        )

    def test_dziekan_wggios(self):
        self.check_response(
            'Kto jest dziekanem wydziału geologii, geofizyki i ochrony środowiska',
            'dziekanem wydziału geologii, geofizyki i ochrony środowiska jest profesor doktor habilitowany inżynier Jacek Matyszkiewicz'
        )

    def test_dziekan_wggis(self):
        self.check_response(
            'Kto jest dziekanem wydziału wydziału geodezji górniczej i inżynierii środowiska',
            'dziekanem wydziału geodezji górniczej i inżynierii środowiska jest doktor habilitowany inżynier Anna Barańska'
        )

    def test_dziekan_wimic(self):
        self.check_response(
            'Kto jest dziekanem wydziału inżynierii materiałowej i ceramiki',
            'dziekanem wydziału inżynierii materiałowej i ceramiki jest profesor doktor habilitowany inżynier Włodzimierz Mozgawa'
        )

    def test_dziekan_wo(self):
        self.check_response(
            'Kto jest dziekanem wydziału odlewnictwa',
            'dziekanem wydziału odlewnictwa jest doktor habilitowany inżynier Rafał Dańko, profesor nadzwyczajny'
        )

    def test_dziekan_wmn(self):
        self.check_response(
            'Kto jest dziekanem wydziału metali nieżelaznych',
            'dziekanem wydziału metali nieżelaznych jest profesor doktor habilitowany inżynier Tadeusz Knych'
        )

    def test_dziekan_wwnig(self):
        self.check_response(
            'Kto jest dziekanem wydziału wiertnictwa, nafty i gazu',
            'dziekanem wydziału wiertnictwa, nafty i gazu jest profesor doktor habilitowany inżynier Rafał Wiśniowski'
        )

    def test_dziekan_wz(self):
        self.check_response(
            'Kto jest dziekanem wydziału zarządzania',
            'dziekanem wydziału zarządzania jest doktor habilitowany inżynier Piotr Łebkowski, profesor nadzwyczajny'
        )

    def test_dziekan_weip(self):
        self.check_response(
            'Kto jest dziekanem wydziału energetyki i paliw',
            'dziekanem wydziału energetyki i paliw jest profesor doktor habilitowany inżynier Wojciech Suwała'
        )

    def test_dziekan_wfis(self):
        self.check_response(
            'Kto jest dziekanem wydziału fizyki i informatyki stosowanej',
            'dziekanem wydziału fizyki i informatyki stosowanej jest profesor doktor habilitowany Janusz Wolny'
        )

    def test_dziekan_wms(self):
        self.check_response(
            'Kto jest dziekanem wydziału matematyki stosowanej',
            'dziekanem wydziału matematyki stosowanej jest doktor habilitowany Vsevolod Vladimirov, profesor nadzwyczajny'
        )

    def test_dziekan_wh(self):
        self.check_response(
            'Kto jest dziekanem wydziału humanistycznego',
            'dziekanem wydziału humanistycznego jest doktor habilitowany Barbara Gąciarz, profesor nadzwyczajny'
        )

    def test_adres(self):
        self.check_response(
            'Jaki jest adres agh',
            'adres agh: Akademia Górniczo-Hutnicza imienia Stanisława Staszica w Krakowie aleja Mickiewicza 30, 30-059 Kraków'
        )

    def test_kwestor(self):
        self.check_response(
            'Kto jest kwesorem agh',
            'Kwestor AGH - magister Maria Ślizień'
        )

    def test_rada_uczelni(self):
        self.check_response(
            'jaki jest skład rady uczelni',
            'w skład rady uczelni wchodzi sześć osób powołanych przez senat agh, w tym trzy osoby spoza wspólnoty uczelni'
        )

    def test_ksiega_jakosci(self):
        self.check_response(
            'czym jest księga jakości agh',
            'księga jakości agh jest jednym z instrumentów realizacji uczelnianego systemy zapewnienia jakości kształcenia'
        )

if __name__ == '__main__':
    unittest.main()
