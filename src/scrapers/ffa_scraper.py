from .Scrapper import Scrapper

URL = "https://www.athle.fr"
endpoints = {
    "competition_list": "/base/resultats",
    "competition_result" : "/bases/liste.aspx?frmbase=resultats&frmmode=1&frmespace=0&frmcompetition={id_competition}&frmepreuve={category}",
    "competition_search" : "/bases/liste.aspx?frmpostback=true&frmbase=resultats&frmmode=2&frmespace=0&frmsaison={saison}&frmdate1={date_debut}&frmdate2={date_fin}&frmposition={position}"
}

class FFAScraper:
    def __init__(self):
        self.scrapper = Scrapper(URL)

    def get_competition_list(self):
        full_url = self.scrapper.url + endpoints["competition_list"]
        self.scrapper.url = full_url
        page_content = self.scrapper.fetch_page()
        soup = self.scrapper.parse_page(page_content)
        return soup

    def extract_url(self, soup):
        urls = []
        for a_tag in soup.find_all('a', href=True):
            urls.append(a_tag['href'])
        return urls

    def extract_competition_ids(self, urls):
        ids = []
        for url in urls:
            if "frmcompetition=" in url:
                id_competition = url.split("frmcompetition=")[-1]
                ids.append(id_competition)
        return ids

    def get_competition_by_year(self, year, position=""):
        date_debut = f"{year}-01-01"
        date_fin = f"{year}-12-31"
        full_url = self.scrapper.url + endpoints["competition_search"].format(saison=year, date_debut=date_debut, date_fin=date_fin, position=position)
        self.scrapper.url = full_url
        page_content = self.scrapper.fetch_page()
        soup = self.scrapper.parse_page(page_content)
        return soup

    def get_competition_result(self, id_competition, category=""):
        full_url = self.scrapper.url + endpoints["competition_result"].format(id_competition=id_competition, category=category)
        self.scrapper.url = full_url
        page_content = self.scrapper.fetch_page()
        soup = self.scrapper.parse_page(page_content)
        return soup
    
    def extract_available_categories(self, soup):  
        categories = []      
        options_container = soup.find('div', {'id': 'optionsEpreuve'})
        
        if options_container:
            option_divs = options_container.find_all('div', class_='select-option')
            for option in option_divs:
                data_url = option.get('data-url', '')
                text = option.get_text(strip=True)    
                category_value = ""
                if "frmepreuve=" in data_url:
                    category_value = data_url.split("frmepreuve=")[-1]
                    if "&" in category_value:
                        category_value = category_value.split("&")[0]
                
                if text and text.lower() not in ['toutes les épreuves', 'toutes']:
                    categories.append({
                        'value': category_value,
                        'text': text.replace('> ', '').replace(' <', ''),  # Nettoyer le texte
                        'url': data_url
                    })
        
        return categories