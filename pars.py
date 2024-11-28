import requests
from bs4 import BeautifulSoup
from datetime import datetime

class pars:
    def __init__(self):
        self.url = 'https://www.championat.com/football/_europeleague/tournament/6008/calendar/'

        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'uk,en-US;q=0.9,en;q=0.8,ru;q=0.7',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
        }

    def main(self):
        response = requests.get(self.url, headers=self.headers)
        response.raise_for_status()
        #получаем разметку страницы
        soup = BeautifulSoup(response.text, 'lxml')
        #находим тег td с классом
        result = soup.find_all('td', class_='stat-results__count _order_3')
        all = soup.find_all('tr', class_='stat-results__row js-tournament-filter-row')

        # узнаем сегодняшнюю дату
        current_datetime = datetime.now().date()
        # меняем формат даты с гггг-мм-дд на дд.мм.ггг.
        date_lst = str(current_datetime).split('-')
        date = f'{date_lst[2]}.{date_lst[1]}.{date_lst[0]}'

        # Список для хранения извлеченных данных
        matches = []

        for row in all:
            # Извлечение названия команд
            teams_tag = row.find('div', class_='stat-results__title-teams _margin-fav')
            if not teams_tag:
                continue
            teams = " - ".join([team.text.strip() for team in teams_tag.find_all('span', class_='table-item__name')])

            # Извлечение даты и времени
            datetime_tag = row.find('td', class_='stat-results__date-time _hidden-td')
            if not datetime_tag:
                continue
            datetime_text = datetime_tag.get_text(strip=True)

            # Извлечение названия турнира
            tournament_tag = row.find('a', title=True)
            tournament_title = tournament_tag['title'].split(', ')[-1] if tournament_tag else "Неизвестный турнир"

            # Извлечение счета
            score_tag = row.find('span', class_='stat-results__count-main')
            score = score_tag.text.strip() if score_tag else "Счет не указан"

            # Добавляем данные в список
            matches.append([teams, datetime_text.split()[0], tournament_title, datetime_text.split()[1], score])
        today_matches = []
        # выводим сегодняшние матчи
        for i in matches:
            if i[1] == date:
                today_matches.append(i)
        return today_matches


start = pars()
today_matches = start.main()
for i in today_matches:
    print(i)


