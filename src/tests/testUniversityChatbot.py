import unittest
from src.university_chatbot.university_conversation_bot import UniversityBot
from src.university_chatbot.university_conversation_logic_adapter import UniversityAdapter
from src.common_utils.database.database_service import DatabaseProxy
from chatterbot import ChatBot
from chatterbot.conversation import Statement

db = DatabaseProxy('mongodb://localhost:27017/', 'PepperChatDB')
chatbot = ChatBot(
            'jakis',
            logic_adapters=[
                {
                    'import_path': 'src.university_chatbot.university_conversation_logic_adapter'
                                   '.UniversityAdapter',
                    'database_proxy': db
                },
            ],
        )
_university_chatbot = UniversityBot('university_chatbot', db)
_university_adapter = UniversityAdapter(chatbot, database_proxy=db)

class TestUniversistyChatbot(unittest.TestCase):

    def check_phrase_response(self, question, correct_answer):
        response = _university_chatbot.get_bot_response(question)
        self.assertEqual(correct_answer.lower().strip(), response.text.lower().strip())

    def check_tags_response(self, question, correct_tags):
        # response = _university_chatbot.get_bot_response(question)
        resp = _university_adapter.process(Statement(question), None)
        doc = db.get_one_doc_from_collection_by_tags_list('MAIN_COLLECTION', correct_tags)
        if doc is None:
            self.fail('get_one_doc_from_collection_by_tags_list returned None')
        print('''doc['tags']: ''', doc['tags'])
        # print('response.text.lower(): ', response.text.lower())
        print('resp.lower(): ', resp.text.lower())
        print('''doc['text']: ''', doc['text'])
        # self.assertEqual(doc['text'].lower().strip(), response.text.lower().strip())
        self.assertEqual(doc['text'][0].lower().strip(), resp.text.lower().strip())


    # # TESTS with tags response expected
    # def test_tags_absolwent(self):
    #     self.check_tags_response(
    #         'opowiedz coś o absolwentach agh',
    #         ['absolwent']
    #     )
    #
    # def test_tags_aktualnosci(self):
    #     self.check_tags_response(
    #         'przedstaw akutalności o agh',
    #         ['aktualności:aktualność']
    #     )
    #
    # def test_tags_uczelnia(self):
    #     self.check_tags_response(
    #         'opowiedz o uczelni',
    #         ['uczelnia']
    #     )
    #
    # def test_tags_oferta_wspolpracy(self):
    #     self.check_tags_response(
    #         'jaka jest oferta współpracy dla biznesu',
    #         ['współpraca', 'oferta', 'biznes']
    #     )
    #
    # def test_tags_bip(self):
    #     self.check_tags_response(
    #         'czym jest biuletyn informacji publicznej',
    #         ['biuletyn', 'informacja', 'publiczny']
    #     )
    #
    # def test_tags_ksztalcenie(self):
    #     self.check_tags_response(
    #         'opowiedz o kształceniu na agh',
    #         ['kształcenie:kształcić']
    #     )
    #
    # def test_tags_historia_tradycja(self):
    #     self.check_tags_response(
    #         'jaka jest historia i tradycja uczelni',
    #         ['uczelnia', 'historia', 'tradycja']
    #     )
    #
    # def test_tags_wgig(self):
    #     self.check_tags_response(
    #         'opowiedz o wydziale górnictwa i geoinżynierii',
    #         ['wydział', 'podstawowy', 'jednostka', 'organizacyjny', 'wydział', 'górnictwo', 'geoinżynierii']
    #     )
    #
    # def test_tags_wimip(self):
    #     self.check_tags_response(
    #         'opowiedz o wydziale inżynierii metali i informatyki przemysłowej',
    #         ['wydział', 'podstawowy', 'jednostka', 'organizacyjny', 'wydział', 'inżynieria', 'metal', 'informatyk:informatyka', 'przemysłowy']
    #     )
    #
    # def test_tags_weaiib(self):
    #     self.check_tags_response(
    #         'opowiedz o wydziale elektrotechniki automatyki informatyki i inżynierii biomedycznej',
    #         ['wydział', 'podstawowy', 'jednostka', 'organizacyjny', 'wydział', 'elektrotechnik:elektrotechnika', 'automatyk:automatyka', 'informatyk:informatyka', 'inzynierii', 'biomedyczny']
    #     )
    #
    # def test_tags_wiet(self):
    #     self.check_tags_response(
    #         'opowiedz o wydziale informatyki elektroniki i telekomunikacji',
    #         ['wydział', 'podstawowy', 'jednostka', 'organizacyjny', 'wydział', 'informatyk:informatyka', 'elektronik:elektronika', 'telekomunikacja']
    #     )
    #
    # def test_tags_wimir(self):
    #     self.check_tags_response(
    #         'opowiedz o wydziale inżynierii mechanicznej i robotyki',
    #         ['wydział', 'podstawowy', 'jednostka', 'organizacyjny', 'wydział', 'inżynieria', 'mechaniczny', 'robotyk:robotyka']
    #     )
    #
    # def test_tags_wggios(self):
    #     self.check_tags_response(
    #         'opowiedz o wydziale geologii geofizyki i ochrony środowiska',
    #         ['wydział', 'podstawowy', 'jednostka', 'organizacyjny', 'wydział', 'geologia', 'geofizyk:geofizyka', 'ochrona', 'środowisko']
    #     )
    #
    # def test_tags_wggiis(self):
    #     self.check_tags_response(
    #         'opowiedz o wydziale geodezji górniczej i inżynierii środowiska',
    #         ['wydział', 'podstawowy', 'jednostka', 'organizacyjny', 'wydział', 'geodezja', 'górniczy', 'inzynierii', 'środowisko']
    #     )
    #
    # def test_tags_wimic(self):
    #     self.check_tags_response(
    #         'opowiedz o wydziale inżynierii materiałowej i ceramiki',
    #         ['wydział', 'podstawowy', 'jednostka', 'organizacyjny', 'wydział', 'inżynieria', 'materiałowy', 'ceramik:ceramika']
    #     )
    #
    # def test_tags_wo(self):
    #     self.check_tags_response(
    #         'opowiedz o wydziale odlewnictwa',
    #         ['wydział', 'podstawowy', 'jednostka', 'organizacyjny', 'wydział', 'odlewnictwo']
    #     )
    #
    # def test_tags_wmn(self):
    #     self.check_tags_response(
    #         'opowiedz o wydziale metali nieżelaznych',
    #         ['wydział', 'podstawowy', 'jednostka', 'organizacyjny', 'wydział', 'metal', 'nieżelazny']
    #     )
    #
    # def test_tags_wnig(self):
    #     self.check_tags_response(
    #         'opowiedz o wydziale wiertnictwa nafty i gazu',
    #         ['wydział', 'podstawowy', 'jednostka', 'organizacyjny', 'wydział', 'wiertnictwo', 'nafta', 'gaz:gazu']
    #     )
    #
    # def test_tags_wz(self):
    #     self.check_tags_response(
    #         'opowiedz o wydziale zarządzania',
    #         ['wydział', 'podstawowy', 'jednostka', 'organizacyjny', 'wydział', 'zarządzanie:zarządzać']
    #     )
    #
    # def test_tags_weip(self):
    #     self.check_tags_response(
    #         'opowiedz o wydziale energetyki i paliw',
    #         ['wydział', 'podstawowy', 'jednostka', 'organizacyjny', 'wydział', 'energetyk:energetyka', 'paliwo']
    #     )
    #
    # def test_tags_wfiis(self):
    #     self.check_tags_response(
    #         'opowiedz o wydziale fizyki i informatyki stosowanej',
    #         ['wydział', 'podstawowy', 'jednostka', 'organizacyjny', 'wydział', 'fizyk:fizyka', 'informatyk:informatyka', 'stosowany:stosować']
    #     )
    #
    # def test_tags_wms(self):
    #     self.check_tags_response(
    #         'opowiedz o wydziale matematyki stosowanej',
    #         ['wydział', 'podstawowy', 'jednostka', 'organizacyjny', 'wydział', 'matematyk:matematyka', 'stosowany:stosować']
    #     )
    #
    # def test_tags_wh(self):
    #     self.check_tags_response(
    #         'opowiedz o wydziale humanistycznym',
    #         ['wydział', 'podstawowy', 'jednostka', 'organizacyjny', 'wydział', 'humanistyczny']
    #     )
    #
    #
    # # TESTS with phrase response expected
    # def test_dziekan_wgig(self):
    #     self.check_phrase_response(
    #         'Kto jest dziekanem wydziału górnictwa i geoinżynierii',
    #         'Dziekanem wydziału górnictwa i geoinżynierii jest profesor doktor habilitowany inżynier marek cała'
    #     )
    #
    # def test_dziekan_wimip(self):
    #     self.check_phrase_response(
    #         'Kto jest dziekanem wydziału inżynierii metali i informatyki przemysłowej',
    #         'Dziekanem wydziału inżynierii metali i informatyki przemysłowej jest profesor doktor habilitowany inżynier tadeusz telejko'
    #     )
    #
    # def test_dziekan_weaiib(self):
    #     self.check_phrase_response(
    #         'Kto jest dziekanem wydziału elektrorechniki, automatykii, informatyki i inżynierii biomedycznej',
    #         'Dziekanem wydziału elektrorechniki, automatykii, informatyki i inżynierii biomedycznej jest doktor habilitowany inżynier Ryszard Sroka, profesor nadzwyczajny'
    #     )
    #
    # def test_dziekan_wiet(self):
    #     self.check_phrase_response(
    #         'Kto jest dziekanem wydziału informatyki elektroniki i telekomunikacji',
    #         'dziekanem wydziału informatyki, elektroniki i telekomunikacji jest profesor doktor habilitowany inżynier Krzysztof Boryczko'
    #     )
    #
    # def test_dziekan_wimir(self):
    #     self.check_phrase_response(
    #         'Kto jest dziekanem wydziału inżynierii mechanicznej i robotyki',
    #         'dziekanem wydziału inżynierii mechanicznej i robotyki jest profesor doktor habilitowany inżynier Antoni Kalukiewicz'
    #     )
    #
    # def test_dziekan_wggios(self):
    #     self.check_phrase_response(
    #         'Kto jest dziekanem wydziału geologii, geofizyki i ochrony środowiska',
    #         'dziekanem wydziału geologii, geofizyki i ochrony środowiska jest profesor doktor habilitowany inżynier Jacek Matyszkiewicz'
    #     )
    #
    # def test_dziekan_wggis(self):
    #     self.check_phrase_response(
    #         'Kto jest dziekanem wydziału wydziału geodezji górniczej i inżynierii środowiska',
    #         'dziekanem wydziału geodezji górniczej i inżynierii środowiska jest doktor habilitowany inżynier Anna Barańska'
    #     )
    #
    # def test_dziekan_wimic(self):
    #     self.check_phrase_response(
    #         'Kto jest dziekanem wydziału inżynierii materiałowej i ceramiki',
    #         'dziekanem wydziału inżynierii materiałowej i ceramiki jest profesor doktor habilitowany inżynier Włodzimierz Mozgawa'
    #     )
    #
    # def test_dziekan_wo(self):
    #     self.check_phrase_response(
    #         'Kto jest dziekanem wydziału odlewnictwa',
    #         'dziekanem wydziału odlewnictwa jest doktor habilitowany inżynier Rafał Dańko, profesor nadzwyczajny'
    #     )
    #
    # def test_dziekan_wmn(self):
    #     self.check_phrase_response(
    #         'Kto jest dziekanem wydziału metali nieżelaznych',
    #         'dziekanem wydziału metali nieżelaznych jest profesor doktor habilitowany inżynier Tadeusz Knych'
    #     )
    #
    # def test_dziekan_wwnig(self):
    #     self.check_phrase_response(
    #         'Kto jest dziekanem wydziału wiertnictwa, nafty i gazu',
    #         'dziekanem wydziału wiertnictwa, nafty i gazu jest profesor doktor habilitowany inżynier Rafał Wiśniowski'
    #     )
    #
    # def test_dziekan_wz(self):
    #     self.check_phrase_response(
    #         'Kto jest dziekanem wydziału zarządzania',
    #         'dziekanem wydziału zarządzania jest doktor habilitowany inżynier Piotr Łebkowski, profesor nadzwyczajny'
    #     )
    #
    # def test_dziekan_weip(self):
    #     self.check_phrase_response(
    #         'Kto jest dziekanem wydziału energetyki i paliw',
    #         'dziekanem wydziału energetyki i paliw jest profesor doktor habilitowany inżynier Wojciech Suwała'
    #     )
    #
    # def test_dziekan_wfis(self):
    #     self.check_phrase_response(
    #         'Kto jest dziekanem wydziału fizyki i informatyki stosowanej',
    #         'dziekanem wydziału fizyki i informatyki stosowanej jest profesor doktor habilitowany Janusz Wolny'
    #     )
    #
    # def test_dziekan_wms(self):
    #     self.check_phrase_response(
    #         'Kto jest dziekanem wydziału matematyki stosowanej',
    #         'dziekanem wydziału matematyki stosowanej jest doktor habilitowany Vsevolod Vladimirov, profesor nadzwyczajny'
    #     )
    #
    # def test_dziekan_wh(self):
    #     self.check_phrase_response(
    #         'Kto jest dziekanem wydziału humanistycznego',
    #         'dziekanem wydziału humanistycznego jest doktor habilitowany Barbara Gąciarz, profesor nadzwyczajny'
    #     )
    #
    # def test_adres(self):
    #     self.check_phrase_response(
    #         'Jaki jest adres agh',
    #         'adres agh: Akademia Górniczo-Hutnicza imienia Stanisława Staszica w Krakowie aleja Mickiewicza 30, 30-059 Kraków'
    #     )
    #
    # def test_kwestor(self):
    #     self.check_phrase_response(
    #         'Kto jest kwestorem agh',
    #         'Kwestor AGH - magister Maria Ślizień'
    #     )
    #
    # def test_rada_uczelni(self):
    #     self.check_phrase_response(
    #         'jaki jest skład rady uczelni',
    #         'w skład rady uczelni wchodzi sześć osób powołanych przez senat agh, w tym trzy osoby spoza wspólnoty uczelni'
    #     )
    #
    # def test_ksiega_jakosci(self):
    #     self.check_phrase_response(
    #         'czym jest księga jakości agh',
    #         'księga jakości agh jest jednym z instrumentów realizacji uczelnianego systemy zapewnienia jakości kształcenia'
    #     )

    # new tests:
    # 1
    def test_1_1(self):
        self.check_phrase_response(
            'ilu absolwentów wykształciła agh',
            'akademia wykształciła ponad 170 000 abwsolwentów - inżynierów i magistrów zapewniając kadrę dla naszej gospodarki'
        )

    def test_1_2(self):
        self.check_phrase_response(
            'czy istnieje jakiś dowód jakości i użyteczności wiedzy zdobywanej w agh',
            'błyskotliwe kariery wielu absolwentów agh, związane z piastowaniem przez nich wszelkich, w tym także bardzo często najwyższych stanowisk, stanowią łatwy do prześledzenia praktyczny dowód jakości i użyteczności wiedzy, jaką zdobyli oni w murach agh'
        )

    # 2
    def test_2_1(self):
        self.check_phrase_response(
            'jak obchodzono uroczystości jubileuszu otwarcia uczelni',
            'wspaniały jubileusz 100-lecia otwarcia uczelni rozpoczęliśmy 4 października 2018 roku inauguracją 100 roku akademickiego, a jego kulminacją były uroczystości w październiku 2019 roku'
        )

    # 3
    def test_3_1(self):
        self.check_phrase_response(
            'jak można poznać historię akademii',
            'historię akademii można lepiej poznać dzięki galeriom, filmom oraz wydawnictwom informacyjnym'
        )

    # 4
    def test_4_1(self):
        self.check_phrase_response(
            'kiedy została powołana uczelnia',
            'nasza uczelnia została powołana w 1913 roku, a jej otwarcie nastąpiło w 1919 roku'
        )

    def test_4_2(self):
        self.check_phrase_response(
            'kiedy otwarto uczelnię',
            'nasza uczelnia została powołana w 1913 roku, a jej otwarcie nastąpiło w 1919 roku'
        )

    def test_4_3(self):
        self.check_phrase_response(
            'oferowane kierunki kształcenia są nowe czy klasyczne',
            'zgodnie ze światowymi trendami rozwoju tworzymy nowe kierunki kształcenia, ale zachowujemy klasyczne, niezbędne do prawidłowego rozwoju nauki, techniki oraz gospodarki naszego kraju'
        )

    # 5
    def test_5_1(self):
        self.check_phrase_response(
            'jaka jest oferta dla biznesu',
            'oferta dla biznesu to: transfer, ochrona i promocja wyników badań, wynalazków oraz patentów: umowy oraz porozumienia z przemysłem, administracją oraz innymi instytucjami'
        )

    # 6
    def test_6_1(self):
        self.check_phrase_response(
            'na jakich rodzajach studiów kształci agh',
            'agh kształci na wszystkich rodzajach studiów: stacjonarnych, niestacjonarnych, doktoranckich i podyplomowych, oferując szeroki profil kształcenia dostosowany do pojawiających się trendów na rynku pracy'
        )

    def test_6_2(self):
        self.check_phrase_response(
            'kiedy wprowadzony został system boloński',
            'od roku akademickiego 2007/2008 akademia górniczo-hutnicza wprowadziła trzystopniowy system kształcenia (tak zwany system boloński)'
        )

    # 7
    def test_7_1(self):
        self.check_phrase_response(
            'ile jest oferowanych kierunków studiów podyplomowych',
            'w agh oferowanych jest około 100 kierunków studiów podyplomowych, a także kilkadziesiąt szkoleń i kursów dokształcających skierowanych zarówno do specjalistów kadry inżynierskiej , jak również do osób, które są zainteresowane zdobyciem nowej innej specjalizacji'
        )

    def test_7_2(self):
        self.check_phrase_response(
            'czy na agh istnieje kształcenie w zakresie poza inżynierskim',
            'Kształcenie w zakresie poza inżynierskim to między innymi studia w dziedzinie marketingu internetowego, informatyki i grafiki komputerowej, ochrony środowiska, rachunkowości i controllingu, bhp, szacowania i zarządzania nieruchomościami, zarządzania projektami, przedsiębiorstwem, organizacją it, zarządzania jakością oraz zarządzania sprzedażą'
        )

    # 8
    def test_8_1(self):
        self.check_phrase_response(
            'czy agh wykoszystuje e-materiały',
            'w swojej ofercie agh posiada e-materiały: e-materiały agh są dostępne bezpłatnie, na licencjach creative commons, dzięki czemu ich wykorzystanie nie ogranicza się jedynie do czytania, pobierania czy drukowania'
        )

    def test_8_2(self):
        self.check_phrase_response(
            'czy agh wykoszystuje e-learning',
            'dla pracowników i doktorantów agh, centrum e-learningu oferuje szkolenia na temat budowania i pisania e-podręczników oraz korzystania z otwartych zasobów edukacyjnych w dydaktyce akademickiej'
        )

    def test_8_3(self):
        self.check_phrase_response(
            'czy agh wykorzystuje e-podręczniki',
            'dla pracowników i doktorantów agh, centrum e-learningu oferuje szkolenia na temat budowania i pisania e-podręczników oraz korzystania z otwartych zasobów edukacyjnych w dydaktyce akademickiej'
        )

    # 10
    def test_10_1(self):
        self.check_phrase_response(
            'jaki jest adres agh',
            'adres agh: Akademia Górniczo-Hutnicza imienia Stanisława Staszica w Krakowie aleja Mickiewicza 30, 30-059 Kraków'
        )

    def test_10_2(self):
        self.check_phrase_response(
            'jaki jest telefon dla kandydatów',
            'Telefon dla kandydatów: 48 12 617 36 84'
        )

    def test_10_3(self):
        self.check_phrase_response(
            'jaki jest telefon do centrum rekrutacji',
            'Telefon centrum rekrutacji: 48 12 617 36 84'
        )

    def test_10_4(self):
        self.check_phrase_response(
            'jaki jest telefon w sprawie studiów stacjonarnych',
            'Telefon studia stacjonarne: 48 12 617 32 61'
        )

    def test_10_5(self):
        self.check_phrase_response(
            'jaki jest telefon w sprawie studiów niestacjonarnych',
            'Telefon studia niestacjonarne: 48 12 617 48 95'
        )

    def test_10_6(self):
        self.check_phrase_response(
            'jaki jest telefon w sprawie studiów podyplomowych',
            'Telefon studia podyplomowe: 48 12 617 32 81'
        )

    def test_10_7(self):
        self.check_phrase_response(
            'jaki jest telefon w sprawie studiów doktoranckich',
            'Telefon studia doktoranckie: 48 12 617 31 57 oraz 48 12 617 24 49'
        )

    def test_10_8(self):
        self.check_phrase_response(
            'jaki jest telefon do działu informacji i promocji',
            'Telefon dział informacji i promocji: 48 12 617 31 91'
        )

    def test_10_9(self):
        self.check_phrase_response(
            'jaki jest telefon do redakcji strony internetowej',
            'Telefon redakcja strony internetowej: magister Weronika Szewczyk 48 12 617 49 38, magister inżynier Maciej Tomczyk 48 12 617 48 97 oraz magister Katarzyna Wrzoszczyk 48 12 617 35 41'
        )

    def test_10_10(self):
        self.check_phrase_response(
            'jaki jest telefon do rzecznika prasowego agh',
            'Telefon rzecznik prasowy AGH magister Anna Żmuda-Muszyńska 48 12 617 25 45 oraz 48 605 109 858'
        )

    def test_10_11(self):
        self.check_phrase_response(
            'jaki jest telefon do inspektora ochrony danych osobowych',
            'Telefon inspektor ochrony danych osobowych magister Tomasz Józefko 48 12 617 53 25'
        )

    # 11
    def test_11_1(self):
        self.check_phrase_response(
            'czym jest centrum międzynarodowej promocji technologii i edukacji agh-unesco',
            'w agh od roku 2011 działa centrum międzynarodowej promocji technologii i edukacji agh-unesco, które jest pierwszą w polsce jednostką pod auspicjami unesco, inspirującą i koordynującą oraz wspierającą wymianę i transfer wiedzy i praktyki inżynierskiej oraz kształcenie na poziomie uniwersyteckim w dziedzinie nauk technicznych w wymiarze międzynarodowym, zwłaszcza adresowanym do krajów rozwijających się'
        )

    def test_11_2(self):
        self.check_phrase_response(
            'do kogo adresowane są działania centrum agh-unesco',
            'działania centrum agh-unesco wpisują się w priorytety unesco oraz agh i są adresowane do partnerów na całym świecie'
        )

    # 12
    def test_12_1(self):
        self.check_phrase_response(
            'czym jest biuletyn informacji publicznej',
            'biuletyn informacji publicznej to urzędowy publikator teleinformatyczny, składający się z ujednoliconego systemu stron w sieci informatycznej'
        )

    #
    def test_12_2(self):
        self.check_phrase_response(
            'w jakim celu został stworzony biuletyn informacji publicznej',
            'biuletyn informacji publicznej został stworzony w celu powszechnego udostępniania informacji publicznej'
        )

    # 13
    def test_13_1(self):
        self.check_phrase_response(
            'kto zatwierdził utworzenie wyższej szkoły górniczej w krakowie',
            '31 maja 1913 roku cesarz franciszek józef i zatwierdził utworzenie wyższej szkoły górniczej w krakowie'
        )

    def test_13_2(self):
        self.check_phrase_response(
            'kiedy zostało zatwierdzone  utworzenie wyższej szkoły górniczej w krakowie',
            '31 maja 1913 roku cesarz franciszek józef i zatwierdził utworzenie wyższej szkoły górniczej w krakowie'
        )

    def test_13_3(self):
        self.check_phrase_response(
            'kiedy został powołany komitet organizacyjny akademii górniczej',
            'w 1913 roku ministerstwo robót publicznych w wiedniu powołało komitet organizacyjny akademii górniczej, którego przewodniczącym został profesor józef morozewicz'
        )

    def test_13_4(self):
        self.check_phrase_response(
            'w którym roku został powołany komitet organizacyjny akademii górniczej',
            'w 1913 roku ministerstwo robót publicznych w wiedniu powołało komitet organizacyjny akademii górniczej, którego przewodniczącym został profesor józef morozewicz'
        )

    def test_13_5(self):
        self.check_phrase_response(
            'gdzie został powołany komitet organizacyjny akademii górniczej',
            'w 1913 roku ministerstwo robót publicznych w wiedniu powołało komitet organizacyjny akademii górniczej, którego przewodniczącym został profesor józef morozewicz'
        )

    def test_13_6(self):
        self.check_phrase_response(
            'kto był przewodniczącym komitetu organizacyjnego akademii górniczej',
            'w 1913 roku ministerstwo robót publicznych w wiedniu powołało komitet organizacyjny akademii górniczej, którego przewodniczącym został profesor józef morozewicz'
        )

    def test_13_7(self):
        self.check_phrase_response(
            'kiedy położono kamień węgielny pod budowę gmachu akademii górniczej',
            '15 czerwca 1923 roku położono kamień węgielny pod budowę przyszłego gmachu akademii górniczej'
        )

    def test_13_8(self):
        self.check_phrase_response(
            'kiedy powstał projekt godła akademii górniczej',
            'w 1925 roku powstał projekt godła akademii górniczej (zachowany w muzeum historii agh) sygnowany monogramem b t – bogdan treter, prawdopodobnie zatwierdzony przez zebranie ogólne profesorów'
        )

    def test_13_9(self):
        self.check_phrase_response(
            'jak zachowała się społeczność akademicka względem wpowadzenia stanu wojennego',
            '14 grudnia 1981 roku społeczność akademicka agh pod sztandarem „solidarności” odważyła się zaprotestować przeciwko stłumieniu – wprowadzeniem stanu wojennego – wywalczonego poczucia wolności i solidarności'
        )

    def test_13_10(self):
        self.check_phrase_response(
            'czy agh organizowało jakieś strajki okupacyjne podczas stanu wojennego',
            'niezależny samorządowy związek zawodowy „solidarność” agh był organizacją uczelnianą, jedyną w krakowie i jedną z trzech w kraju, które zorganizowały strajki okupacyjne w pierwszych dniach stanu wojennego'
        )

    # 14
    def test_14_1(self):
        self.check_phrase_response(
            'kiedy rozpoczęły się starania o utworzenie akademii górniczej',
            'starania o utworzenie w kraju uczelni górniczej oraz powołanie odpowiedniej kadry naukowej rozpoczęły się w drugiej połowie dziewiętnastego wieku i nasiliły wraz z uzyskaniem przez galicję autonomii'
        )

    def test_14_2(self):
        self.check_phrase_response(
            'kiedy otrzymano zezwolenie na otwarcie uczleni',
            'starania o powołanie w krakowie wyższej uczelni kształcącej inżynierów górnictwa zostały zwieńczone powodzeniem – 10 lipca 1912 roku władze krakowa otrzymały zezwolenie na otwarcie uczelni'
        )

    def test_14_3(self):
        self.check_phrase_response(
            'kto wystosował pisma do naczelnika państwa w sprawie mianowania pierwszych profesorów akademii górniczej',
            'w notatce z konferencji u prezydenta miasta krakowa juliusza lea widnieje dopisek w prawym dolnym rogu kartki na jednym z dokumentów: w kwietniu 1919 roku minister jan łukasiewicz wystosował pisma do naczelnika państwa w sprawie mianowania pierwszych profesorów akademii górniczej'
        )

    def test_14_4(self):
        self.check_phrase_response(
            'ilu profesorów mianował józef piłsudski',
            'sześciu profesorów zostało oficjalnie mianowanych przez józefa piłsudskiego 1 maja 1919 roku'
        )

    def test_14_5(self):
        self.check_phrase_response(
            'kto został wybrany pierwszym dziekanem wydziału górniczego',
            'na pierwszym posiedzeniu wydziału profesorów akademii górniczej na dziekana wydziału górniczego wybrany został profesor antoni hoborski, a prodziekanem został profesor jan stock'
        )

    def test_14_6(self):
        self.check_phrase_response(
            'kto został pierwszym prodziekanem wydziału górniczego',
            'na pierwszym posiedzeniu wydziału profesorów akademii górniczej na dziekana wydziału górniczego wybrany został profesor antoni hoborski, a prodziekanem został profesor jan stock'
        )

    def test_14_7(self):
        self.check_phrase_response(
            'kiedy odbyła się inauguracja pierwszego roku akademickiego akademii',
            '20 października 1919 roku odbyła się inauguracja pierwszego roku akademickiego w auli collegium novum uniwersytetu jagiellońskiego - józefa piłsudskiego powitała młodzież, ustawiona w szpalerze przed udekorowanym kwiatami gmachem'
        )

    def test_14_8(self):
        self.check_phrase_response(
            'gdzie odbyła się inauguracja pierwszego roku akademickiego akademii',
            '20 października 1919 roku odbyła się inauguracja pierwszego roku akademickiego w auli collegium novum uniwersytetu jagiellońskiego - józefa piłsudskiego powitała młodzież, ustawiona w szpalerze przed udekorowanym kwiatami gmachem'
        )

    def test_14_9(self):
        self.check_phrase_response(
            'kto zainaugurował pierwszy rok akademicki akademii',
            '20 października 1919 roku odbyła się inauguracja pierwszego roku akademickiego w auli collegium novum uniwersytetu jagiellońskiego - józefa piłsudskiego powitała młodzież, ustawiona w szpalerze przed udekorowanym kwiatami gmachem'
        )

    def test_14_10(self):
        self.check_phrase_response(
            'w jaki sposob akademia wychowuje studentów',
            'akademia pielęgnuje swoje tradycje i wychowuje studentów na ludzi mądrych i prawych, w duchu odpowiedzialności zawodowej i obywatelskiej, zgodnie ze swoją dewizą: „Labore creata, labori et scientiae servio”'
        )

    def test_14_11(self):
        self.check_phrase_response(
            'jaka jest dewiza agh',
            'akademia pielęgnuje swoje tradycje i wychowuje studentów na ludzi mądrych i prawych, w duchu odpowiedzialności zawodowej i obywatelskiej, zgodnie ze swoją dewizą: „Labore creata, labori et scientiae servio”'
        )

    # 15
    def test_15_1(self):
        self.check_phrase_response(
            'co stanowi godło agh',
            'godło akademii górniczo-hutniczej stanowi stylizowany orzeł z koroną i tarczą, na której umieszczone są perlik i żelazo (godło górnicze) oraz inicjały agh'
        )

    def test_15_2(self):
        self.check_phrase_response(
            'kiedy zaprojektowano godło agh',
            'obecna wersja godła agh została zaprojektowana na podstawie rysunku wykonanego w 1925 roku przez docenta krakowskiej asp bogdana tretera oraz graficznej aplikacji rysunku zachowanej na dyplomie przyznanym ignacemu mościckiemu w 1934 roku'
        )

    def test_15_3(self):
        self.check_phrase_response(
            'do czego przeznaczone jest godło agh',
            'godło agh przeznaczone jest wyłącznie do promowania historii oraz dziedzictwa naukowego uczelni i zostało zastrzeżone dla dokumentów rektora akademii górniczo-hutniczej'
        )

    def test_15_4(self):
        self.check_phrase_response(
            'czy godło agh jest zastrzeżone',
            'godło agh przeznaczone jest wyłącznie do promowania historii oraz dziedzictwa naukowego uczelni i zostało zastrzeżone dla dokumentów rektora akademii górniczo-hutniczej'
        )

    # 16
    def test_16_1(self):
        self.check_phrase_response(
            'z czego zbudowany jest znak graficzny agh',
            'znak graficzny akademii górniczo-hutniczej zbudowany jest z sygnetu oraz logotypu'
        )

    def test_16_2(self):
        self.check_phrase_response(
            'co służy identyfikacji wizualnej agh',
            'znak graficzny agh jest jedynym znakiem służącym codziennej identyfikacji wizualnej akademii górniczo-hutniczej'
        )

    # 17
    def test_17_1(self):
        self.check_phrase_response(
            'jaka jest symbolika barw agh',
            'symbolika barw agh jest nastęująca: zieleń odzwierciedla naturę, pola i lasy; czerń nawiązuje do głębi kopalń oraz symbolizuje cechy niezbędne w zawodzie górniczym i hutniczym, takie jak rozwaga, mądrość i stałość; czerwień to barwa ognia i roztopionego żelaza'
        )

    def test_17_2(self):
        self.check_phrase_response(
            'jakie są barwy agh',
            'barwami akademii górniczo-hutniczej są zieleń, czerń oraz czerwień'
        )

    # 18
    def test_18_1(self):
        self.check_phrase_response(
            'jakie są insygnia władzy agh',
            'insygnia władzy agh to: łańcuch, berło i topór ceremonialny oraz pierścień'
        )

    # 19
    def test_19_1(self):
        self.check_phrase_response(
            'kim jest doctor honoris causa',
            'doctor honoris causa (z łaciny dla zaszczytu) to honorowy tytuł naukowy nadawany przez uczelnie osobom szczególnie zasłużonym dla nauki i kultury'
        )

    def test_19_2(self):
        self.check_phrase_response(
            'czy istnieje jakiś honorowy tytuł naukowy dla osób szczególnie zasłużonych dla nauki i kultury',
            'doctor honoris causa (z łaciny dla zaszczytu) to honorowy tytuł naukowy nadawany przez uczelnie osobom szczególnie zasłużonym dla nauki i kultury'
        )

    # 20
    def test_20_1(self):
        self.check_phrase_response(
            'kto przyznaje tytuł zasłużony dla agh',
            'tytuł zasłużony dla agh przyznaje senat akademii podejmując uchwałę raz w roku na czerwcowym posiedzeniu'
        )

    def test_20_2(self):
        self.check_phrase_response(
            'kiedy przyznawane są tytuły zasłużony dla agh',
            'tytuł zasłużony dla agh przyznaje senat akademii podejmując uchwałę raz w roku na czerwcowym posiedzeniu'
        )

    def test_20_3(self):
        self.check_phrase_response(
            'kiedy odbywa się wręczenie tutułów zasłużony dla agh',
            'wręczenie insygniów związanych z tytułem "zasłużony dla agh" odbywa się w czasie inauguracji roku akademickiego'
        )

    # 21
    def test_21_1(self):
        self.check_phrase_response(
            'czym jest tytuł honorowego konsula agh',
            'tytuł honorowego konsula agh nadawany jest osobom związanym z uczelnią, których działalność przyczyniła się do jej rozwoju i promocji zgodnie z artykułem, tytułu tego nie mogą uzyskać aktualni pracownicy agh'
        )

    def test_21_2(self):
        self.check_phrase_response(
            'komu nadawany jest tytuł honorowego konsula agh',
            'tytuł honorowego konsula agh nadawany jest osobom związanym z uczelnią, których działalność przyczyniła się do jej rozwoju i promocji zgodnie z artykułem, tytułu tego nie mogą uzyskać aktualni pracownicy agh'
        )

    def test_21_3(self):
        self.check_phrase_response(
            'kto może otrzymać tytuł honorowego konsula agh',
            ''
        )

    # 22
    def test_22_1(self):
        self.check_phrase_response(
            'komu nadawany jest tytuł profesora honorowego agh',
            'tytuł profesora honorowego agh nadaje się wybitnym uczonym, twórcom techniki oraz innym osobom, które są czynnymi lub emerytowanymi pracownikami uczelni; kandydat do tytułu musi posiadać stopień naukowy doktora'
        )

    # 23
    def test_23_1(self):
        self.check_phrase_response(
            'jaki jest skład rady uczelni',
            'w skład rady uczelni wchodzi sześć osób powołanych przez senat agh, w tym trzy osoby spoza wspólnoty uczelni'
        )

    def test_23_2(self):
        self.check_phrase_response(
            'jakie osoby są członkami pierwszej rady uczelni',
            'Członkami pierwszej rady uczelni są: profesor doktor habilitowany inżynier Janusz Filipiak, magister inżynier Bogusław Ochab, doktor inżynier Krzysztof Pawiński, profesor doktor habilitowany inżynier Zbigniew Kąkol, profesor doktor habilitowany inżynier Kazimierz Wiatr oraz profesor doktor habilitowany inżynier Magdalena Hasik'
        )

    def test_23_3(self):
        self.check_phrase_response(
            'jakie są zadania rady uczelni',
            'Do zadań Rady Uczelni należy między innymi: opiniowanie projektu strategii uczelni, opiniowanie projektu statutu, monitorowanie gospodarki finansowej uczelni, monitorowanie zarządzania uczelnią'
        )

    def test_23_4(self):
        self.check_phrase_response(
            'kiedy kończy się kadencja rady uczelni',
            'Kadencja pierwszej rady uczelni potrwa do 31 grudnia 2020 roku'
        )

    # 24
    def test_24_1(self):
        self.check_phrase_response(
            'czym jest senat',
            'senat jest najważniejszym ciałem kolegialnym uczelni'
        )

    def test_24_2(self):
        self.check_phrase_response(
            'jakie sprawy rozpoznaje senat',
            'Senat rozpatruje każdą sprawę, którą uzna za istotną dla Uczelni'
        )

    def test_24_3(self):
        self.check_phrase_response(
            'co należy do kompetencji senatu',
            'Do kompetencji Senatu należy między innymi: uchwalanie Statutu Uczelni, uchwalanie Regulaminu Studiów, Regulaminu Studiów Doktoranckich oraz Regulaminu Studiów Podyplomowych'
        )

    def test_24_4(self):
        self.check_phrase_response(
            'jaki jest skład senatu',
            'W skład Senatu wchodzą: Rektor jako jego przewodniczący, prorektorzy, dziekani wydziałów, przedstawiciele poszczególnych grup społeczności akademickiej wybrani zgodnie z ordynacją wyborczą'
        )

    # 25
    def test_25_1(self):
        self.check_phrase_response(
            'jaka jest struktura agh',
            'struktura akademii górniczo-hutniczej obejmuje następujące jednostki organizacyjne: wydziały i inne podstawowe jednostki organizacyjne, jednostki pozawydziałowe, administracja centralna i inne jednostki związane z działalnością uczelni, szkoły doktorskie'
        )

    # 26
    def test_26_1(self):
        self.check_phrase_response(
            'jakie są piony administracji centralnej',
            'piony administracji centralnej to: Pion Rektora, Pion Kształcenia, Pion Nauki, Pion Współpracy, Pion Ogólny, Pion Spraw Studenckich, Pion Kanclerza, Pion Kwestury'
        )

    # 27
    def test_27_1(self):
        self.check_phrase_response(
            'co tworzy pion rektora',
            'pion rektora tworzą stanowiska i jednostki merytorycznie podległe rektorowi, a organizacyjnie podległe dyrektorowi biura rektora'
        )

    def test_27_2(self):
        self.check_phrase_response(
            'czym jest biuro rektora',
            'biuro rektora zapewnia administracyjną i merytoryczną obsługę urzędu i działalności rektora oraz senatu'
        )

    # 28
    def test_28_1(self):
        self.check_phrase_response(
            'co zapewnia pion kształcenia',
            'pion kształcenia zapewnia administracyjną realizację uprawnień i obowiązków prorektora do spraw kształcenia'
        )

    def test_28_2(self):
        self.check_phrase_response(
            'komu podlega uczelniana komisja rekrutacyjna',
            'prorektorowi do spraw kształcenia podlega Uczelniana Komisja Rekrutacyjna oraz Uczelniany Zespół do spraw Jakości Kształcenia'
        )

    def test_28_3(self):
        self.check_phrase_response(
            'komu podlega uczelniany zespół do spraw jakości kształcenia',
            'prorektorowi do spraw kształcenia podlega Uczelniana Komisja Rekrutacyjna oraz Uczelniany Zespół do spraw Jakości Kształcenia'
        )

    def test_28_4(self):
        self.check_phrase_response(
            'jakie jednostki są podległe prorektorowi do spraw kształcenia',
            'prorektorowi do spraw kształcenia podlega Uczelniana Komisja Rekrutacyjna oraz Uczelniany Zespół do spraw Jakości Kształcenia'
        )

    # 29
    def test_29_1(self):
        self.check_phrase_response(
            'jaki pion  zapewnia realizację uprawnień i obowiązków prorektora do spraw nauki',
            'pion nauki zapewnia administracyjną realizację uprawnień i obowiązków prorektora do spraw nauki, który kieruje pionem'
        )

    def test_29_2(self):
        self.check_phrase_response(
            'co zapewnia obsługę badań naukowych w uczelni',
            'pion nauki zapewnia administracyjną, formalno-prawną, techniczną i informacyjną obsługę sfery badań naukowych w uczelni i jej promocji w tym zakresie'
        )

    # 30
    def test_30_1(self):
        self.check_phrase_response(
            'czym jest pion współpracy',
            'pion współpracy zapewnia administracyjną realizację uprawnień i obowiązków prorektora do spraw współpracy, który kieruje pionem'
        )

    # 31
    def test_31_1(self):
        self.check_phrase_response(
            'czym jest pion spraw studenckich',
            'pion spraw studenckich zapewnia administracyjną realizację uprawnień i obowiązków prorektora do spraw studenckich, który kieruje pionem'
        )

    # 32
    def test_32_1(self):
        self.check_phrase_response(
            'czym jest pion ogólny',
            'pion ogólny zapewnia administracyjną realizację uprawnień i obowiązków prorektora do spraw ogólnych, który kieruje pionem'
        )

    # 33
    def test_33_1(self):
        self.check_phrase_response(
            'co obejmuje pion kanclerza',
            'pion kanclerza obejmuje gospodarcze, techniczne, organizacyjne, prawne i administracyjne funkcjonowanie uczelni w zakresie zwykłego zarządu'
        )

    def test_33_2(self):
        self.check_phrase_response(
            'kto kieruje pionem kanclerza',
            'pionem kanclerza kieruje kanclerz uczelni'
        )

    # 34
    def test_34(self):
        self.check_phrase_response(
            'kto jest kwestorem agh',
            'Kwestor AGH - magister Maria Ślizień'
        )

    # 35
    def test_35_1(self):
        self.check_phrase_response(
            'czym jest konwent agh',
            'konwent agh jest wyjątkowym w skali kraju ciałem kolegialnym działającym przy wyższej uczelni'
        )

    def test_35_2(self):
        self.check_phrase_response(
            'jakie jednostki skupia w swych szeregach konwent agh',
            'skupiając w swych szeregach ścisłe władze województw oraz menedżerów wiodących przedsiębiorstw, konwent agh stanowi cenny organ doradczy uczelni'
        )

    def test_35_3(self):
        self.check_phrase_response(
            'jak często odbywają się obrady konwentu agh',
            'odbywające się dwa razy w roku obrady konwentu agh są platformą wymiany doświadczeń na styku szkolnictwa wyższego z przemysłem oraz samorządami'
        )

    def test_35_4(self):
        self.check_phrase_response(
            'czym są obrady konewntu agh',
            'odbywające się dwa razy w roku obrady konwentu agh są platformą wymiany doświadczeń na styku szkolnictwa wyższego z przemysłem oraz samorządami'
        )

    # 36
    def test_36_1(self):
        self.check_phrase_response(
            'czym jest rada seniorów agh',
            'Rada seniorów agh jest kontynuatorką konwentu seniorów agh, powołanego 18 lutego 1985 roku przez ówczesnego rektora agh profesora antoniego kleczkowskiego'
        )

    def test_36_2(self):
        self.check_phrase_response(
            'jaka jest liczba członków rady seniorów agh',
            'Liczba członków rady seniorów nie może przekroczyć 30 osób; kadencja w radzie jest dożywotnia, ustanie członkostwa w radzie może nastąpić jedynie na podstawie decyzji osoby rezygnującego z członkostwa'
        )

    def test_36_3(self):
        self.check_phrase_response(
            'jak długa jest kadencja w radzie seniorów agh',
            'Liczba członków rady seniorów nie może przekroczyć 30 osób; kadencja w radzie jest dożywotnia, ustanie członkostwa w radzie może nastąpić jedynie na podstawie decyzji osoby rezygnującego z członkostwa'
        )

    # 37
    def test_37_1(self):
        self.check_phrase_response(
            'jaki jest pełny skład rady seniorów',
            'pełny skład rady seniorów jest następujący: profesor Jerzy Niewodniczański – przewodniczący rady seniorów; profesor Kazimierz Jeleń – wiceprzewodniczący rady seniorów; profesor Józef Dańko – sekretarz rady seniorów; pozostali członkowie rady seniorów to: profesor Bronisław Barchański, profesor Wojciech Batko, profesor Stanisław Białas, profesor Aleksander Długosz, profesor Zbigniew Fajklewicz, profesor Aleksander Garlicki, profesor Józef Giergiel, profesor Andrzej Gołaś, profesor Henryk Górecki, profesor Mirosław Handke, profesor Wojciech Kapturkiewicz, profesor Danuta Kisielewska, profesor Andrzej Korbel, profesor Zygmunt Kolenda, profesor Stanisław Kreczmer, profesor Barbara Kwiecińska, profesor Jan Lech Lewandowski, profesor Andrzej Łędzki, profesor Janusz Łuksza, profesor Lidia J. Maksymowicz, profesor Andrzej Manecki, profesor Stanisław Mitkowski, profesor Janusz Roszkowski, profesor Jerzy Sędzimir, profesor Zbigniew Sitek, profesor Andrzej Skorupa, profesor Józef Zasadziński'
        )

    def test_37_2(self):
        self.check_phrase_response(
            'kto jest przewodniczącym rady seniorów',
            'profesor Jerzy Niewodniczański – przewodniczący rady seniorów'
        )

    def test_37_3(self):
        self.check_phrase_response(
            'kto jest wiceprzewodniczącym rady seniorów',
            'profesor Kazimierz Jeleń – wiceprzewodniczący rady seniorów'
        )

    def test_37_4(self):
        self.check_phrase_response(
            'kto jest sekretarzem rady seniorów',
            'profesor Józef Dańko – sekretarz rady seniorów'
        )

    # 38
    def test_38_1(self):
        self.check_phrase_response(
            'kto prowadzi posiedzenia rady seniorów',
            'posiedzenia rady seniorów prowadził przewodniczący rady jerzy niewodniczański, lub – pod jego nieobecność – wiceprzewodniczący kazimierz jeleń'
        )

    def test_38_2(self):
        self.check_phrase_response(
            'co jest w programie posiedzeń rady seniorów agh',
            'stałymi pozycjami programów posiedzeń rady seniorów były wystąpienia rektora lub prorektora agh obecnego na posiedzeniu oraz sprawy bieżące (w tym sprawozdanie z ostatniego posiedzenia senatu agh)'
        )

    # 39
    def test_39_1(self):
        self.check_phrase_response(
            'czym jest system identyfikacji wizualnej agh',
            'system identyfikacji wizualnej agh to zespół reguł oraz konsekwentnie zaprojektowanych wzorców, które mają utrwalać pożądane opinie na temat uczelni wśród pracowników, studentów i szeroko rozumianych odbiorców zewnętrznych'
        )

    # 40
    def test_40_1(self):
        self.check_phrase_response(
            'czym jest księga identyfikacji wizualnej',
            'księga identyfikacji wizualnej to uproszczone kompendium wiedzy na temat systemu wizualnego akademii górniczo-hutniczej'
        )

    def test_40_2(self):
        self.check_phrase_response(
            'co zawiera księga identyfikacji wizualnej',
            'księga indentyfikacji wizualnej zawiera opis podstawowych elementów identyfikacji, porządkuje elementy wizualne w celu prawidłowego kreowania wizerunku uczelni oraz wyznacza zasady w zakresie wykorzystania elementów identyfikujących uczelnię w promocji'
        )

    # 41
    def test_41_1(self):
        self.check_phrase_response(
            'jakie są wersje znaku graficznego agh',
            'znak graficzny agh posiada trzy wersje podstawowe: wersję wielobarwną oraz dwie wersje jednobarwne - pozytywową i negatywową'
        )

    # 42
    def test_42_1(self):
        self.check_phrase_response(
            'jak umieszczona jest nazwa uczelni w znaku graficznym agh',
            'w znaku graficznym agh pełna nazwa uczelni umieszczona jest pod znakiem agh i wyśrodkowana względem pionowej osi sygnetu'
        )

    # 43
    def test_43_1(self):
        self.check_phrase_response(
            'gdzie znajduje się informacja o zamawianiu wizytówek',
            'informacja odnośnie zamawiania wizytówek dla pracowników agh znajduje się w  komunikacie biura kanclerza numer 29/2009'
        )

    # 44
    def test_44_1(self):
        self.check_phrase_response(
            'czy uczelnia dyspoonuje bogatą infrastrukturą',
            'uczelnia dysponuje niezwykle bogatą infrastrukturą, nowoczesnym zapleczem dydaktycznym i naukowym, bazą mieszkaniową oraz doskonale wyposażonymi obiektami sportowymi'
        )

    def test_44_2(self):
        self.check_phrase_response(
            'ile wynosi łączna powierzchnia użytkowa budynków należących do agh',
            'budynki należące do agh, których łączna powierzchnia użytkowa wynosi 350 tysięcy metrów kwadratowych, zlokalizowane są na terenie: Krakowa (98%), Łukęcina, Krynicy, Miękinii i Regulic'
        )

    def test_44_3(self):
        self.check_phrase_response(
            'gdzie zlokalizowane sa budynki należące do agh',
            'budynki należące do agh, których łączna powierzchnia użytkowa wynosi 350 tysięcy metrów kwadratowych, zlokalizowane są na terenie: Krakowa (98%), Łukęcina, Krynicy, Miękinii i Regulic'
        )

    def test_44_4(self):
        self.check_phrase_response(
            'ile miejsc posiada kompus agh',
            'agh posiada największy kampus w polsce - 8000 miejsc, 20 domów studenckich (akademików), 38 hektarów powierzchni'
        )

    def test_44_5(self):
        self.check_phrase_response(
            'ile domów studenckich posiada kampus agh',
            'agh posiada największy kampus w polsce - 8000 miejsc, 20 domów studenckich (akademików), 38 hektarów powierzchni'
        )

    # 45
    def test_45_1(self):
        self.check_phrase_response(
            'jakie są ostatnie inwestycje agh',
            'ostatnie inwestycje agh to między innymi: rozbudowa budynku S-1, nowy budynek dla Wydziału Informatyki, Elektroniki i Telekomunikacji, Akademickie Centrum Kultury Klub STUDIO, Centrum Energetyki – największa inwestycja w historii uczelni, Akademickie Centrum Materiałów i Nanotechnologii AGH, Hala maszyn ACK CYFRONET AGH, Centrum Informatyki, Centrum Ceramiki, budynek Wydziału Energetyki i Paliw, Basen AGH, Centrum Dydaktyki, Laboratorium Edukacyjno-Badawcze Odnawialnych Źródeł i Poszanowania Energii w Miękini, Biblioteka Główna AGH'
        )

    # 46
    def test_46_1(self):
        self.check_phrase_response(
            'gdzie położony jest kampus agh',
            'kampus akademicki o powierzchni 38 hektarów położony jest w obrębie ulic: aleje mickiewicza, reymonta, buszka, tokarskiego, armii krajowej, gramatyka, nawojki oraz czarnowiejskiej'
        )

    def test_46_2(self):
        self.check_phrase_response(
            'jaka jest lokalizacja kampusu agh',
            'niewątpliwym atutem kampusu akademickiego jest doskonała lokalizacja (kilkanaście minut spacerem do rynku głównego), jak również dostęp do szerokiej sieci połączeń autobusowych i tramwajowych'
        )

    def test_46_3(self):
        self.check_phrase_response(
            'jakie są atuty kampusu agh',
            'niewątpliwym atutem kampusu akademickiego jest doskonała lokalizacja (kilkanaście minut spacerem do rynku głównego), jak również dostęp do szerokiej sieci połączeń autobusowych i tramwajowych'
        )

    def test_46_4(self):
        self.check_phrase_response(
            'co wchodzi w skład kampusu agh',
            'w skład kampusu akademickiego wchodzą: Pawilony dydaktyczno-naukowe, Biblioteka Główna, Stołówki studenckie, Przychodnia zdrowia, Domy studenckie, Hale sportowe, Kluby studenckie, Obiekty handlowo-usługowe, Obiekty pomocnicze'
        )

    def test_46_5(self):
        self.check_phrase_response(
            'czy istnieją jakieś udogodnienia dla rowerzystów na terenie kampusu',
            'na terenie kampusu znajdują się liczne stojaki rowerowe, jak również zadaszone parkingi rowerowe'
        )

    # 47
    def test_47_1(self):
        self.check_phrase_response(
            'jaka jest powierzchnia miasteczka studenckiego agh',
            'największe miasteczko studenckie w polsce, o powierzchni 13 hektarów, zlokalizowane jest w obrębie kampusu akademickiego agh pomiędzy ulicami: reymonta, buszka, tokarskiego, armii krajowej, nawojki i miechowską'
        )

    def test_47_2(self):
        self.check_phrase_response(
            'gdzie zlokalizowane jest miasteczko studenckieg agh',
            'największe miasteczko studenckie w polsce, o powierzchni 13 hektarów, zlokalizowane jest w obrębie kampusu akademickiego agh pomiędzy ulicami: reymonta, buszka, tokarskiego, armii krajowej, nawojki i miechowską'
        )

    def test_47_3(self):
        self.check_phrase_response(
            'co znajduje się na terenie miasteczka studenckiego oprócz domów studenckich',
            'na terenie miasteczka studenckiego oprócz 20 domów studenckich znajdują się między innymi: kluby studenckie, boiska sportowe, przedszkole, żłobek, korty tenisowe, supermarket, basen agh, bank oraz różne punkty handlowe, gastronomiczne i usługowe'
        )

    def test_47_4(self):
        self.check_phrase_response(
            'jaki jest dostęp do internetu w akademikach',
            'w akademikach agh wszystkie pokoje oddane do dyspozycji studentów posiadają bezpłatny dostęp do internetu'
        )

    # 48
    def test_48_1(self):
        self.check_phrase_response(
            'gdzie odbywają się zajęcia dydaktyczne',
            'zajęcia dydaktyczne odbywają się w: ponad 150 salach wykładowych, ponad 200 salach ćwiczeniowych, ponad 680 salach laboratoryjnych, ponad 40 salach konferencyjnych'
        )

    def test_48_2(self):
        self.check_phrase_response(
            'jak wyposażone są sale wykładowe i konferencyjne',
            'sale wykładowe i konferencyjne wyposażone są między innymi w: projektory multimedialne, wizualizery, tablice i monitory interaktywne, ekrany projekcyjne, systemy wideokonferencji, mikrofony, profesjonalne nagłośnienie czy też system tłumaczeń symultanicznych'
        )

    # 49
    def test_49_1(self):
        self.check_phrase_response(
            'jakie są inwestycje w baze sportowo rekreacyjną',
            'inwestycje w baze sportowo rekreacyjną to unowocześnienie studium wychowania fizycznego i sportu przy ulicy piastowskiej oraz wybudowanie basen, w którym znajdują się sauna, kręgielnia i siłownia'
        )

    # 50
    def test_50_1(self):
        self.check_phrase_response(
            'jakie jest wyposażenie basenu agh',
            'wyposażenie basenu agh to: basen sportowy (25-metrowy, posiadający homologację pzp), basen szkoleniowy (25-metrowy) oraz basen rekreacyjny z hydromasażami, jak również: jacuzzi, zjeżdżalnia oraz sauny (sucha i mokra)'
        )

    def test_50_2(self):
        self.check_phrase_response(
            'co oferuje basen agh',
            'pod okiem doświadczonych i wykwalifikowanych instruktorów basen agh oferuje: naukę i doskonalenie pływania dla niemowląt, dzieci, młodzieży i dorosłych, gimnastykę w wodzie dla kobiet w ciąży, aquaaerobik oraz ćwiczenia rehabilitacyjne w wodzie'
        )

if __name__ == '__main__':
    unittest.main()
