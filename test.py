from src.database.DatabaseManager import DatabaseManager
from src.scrapers.ffa_scraper import FFAScraper
import os

class TestRunner:
    def __init__(self):
        self.success = 0
        self.failure = 0
        
        if os.path.exists("test.db"):
            os.remove("test.db")
    
    def run_test(self, test_name, test_func):
        try:
            print(f"Running {test_name}...", end=" ")
            test_func()
            print("✓ PASSED")
            self.success += 1
        except Exception as e:
            print(f"✗ FAILED: {e}")
            self.failure += 1
    
    def test_table_creation(self):
        db_manager = DatabaseManager("test.db")
        
        db_manager.create_table("test_table", "id INTEGER PRIMARY KEY, name TEXT")
        
        tables = db_manager.get_data("sqlite_master", "type='table' AND name='test_table'")
        assert len(tables) == 1, "Table creation failed"
    
    def test_data_insertion(self):
        """Test d'insertion de données"""
        db_manager = DatabaseManager("test.db")
        db_manager.create_table("athletes", "id INTEGER PRIMARY KEY, name TEXT, time REAL")
        
        db_manager.insert_data("athletes", (1, "John Doe", 10.5))
        
        data = db_manager.get_data("athletes", "name='John Doe'")
        assert len(data) == 1, "Data insertion failed"
        assert data[0][1] == "John Doe", "Incorrect data inserted"

    def test_ffa_scraper(self):
        scraper = FFAScraper()
        soup = scraper.get_competition_list()
        assert soup is not None, "Failed to fetch or parse the competition list"

    def test_ffa_scraper_urls(self):
        scraper = FFAScraper()
        soup = scraper.get_competition_list()
        urls = scraper.extract_url(soup)
        assert isinstance(urls, list), "extract_url should return a list"
        assert len(urls) > 0, "No URLs found in the competition list"

    def test_ffa_scraper_competition_ids(self):
        scraper = FFAScraper()
        soup = scraper.get_competition_list()
        urls = scraper.extract_url(soup)
        ids = scraper.extract_competition_ids(urls)
        assert isinstance(ids, list), "extract_competition_ids should return a list"
        assert len(ids) > 0, "No competition IDs found in the URLs"

    def test_ffa_scraper_competition_by_year(self):
        scraper = FFAScraper()
        soup = scraper.get_competition_by_year(2023, 400)
        assert soup is not None, "Failed to fetch or parse competitions for the year 2023"

    def test_ffa_scraper_competition_result(self):
        scraper = FFAScraper()
        soup = scraper.get_competition_by_year(2023, 400)
        urls = scraper.extract_url(soup)
        ids = scraper.extract_competition_ids(urls)
        assert len(ids) > 0, "No competition IDs found for the year 2023"
        
        soup_result = scraper.get_competition_result(ids[0])
        assert soup_result is not None, "Failed to fetch or parse competition results"
    
    def test_ffa_scraper_categories(self):
        """Test de récupération des catégories disponibles"""
        scraper = FFAScraper()  
        soup = scraper.get_competition_result("314459", category="")
        categories = scraper.extract_available_categories(soup)
        
        assert isinstance(categories, list), "extract_available_categories should return a list"
        assert len(categories) > 0, "No categories found"
        
        for category in categories:
            assert isinstance(category, dict), "Each category should be a dict"
            assert 'value' in category, "Category should have a 'value' key"
            assert 'text' in category, "Category should have a 'text' key"
            assert 'url' in category, "Category should have a 'url' key"
            assert category['text'].strip() != '', "Category text should not be empty"
        
        print(f"Found {len(categories)} categories", end=" ")

    def test_ffa_scraper_competition_result_by_category(self):
        scraper = FFAScraper()
        competition_id = "314459"
        categories = scraper.extract_available_categories(scraper.get_competition_result(competition_id, category=""))
        assert len(categories) > 0, "No categories found for the competition"

        for category in categories:
            soup_result = scraper.get_competition_result(competition_id, category=category['value'])
            assert soup_result is not None, f"Failed to fetch or parse results for category {category['text']}"

    def run_all_tests(self):
        print("=== Running All Tests ===")
        
        tests = [
            ("Table Creation", self.test_table_creation),
            ("Data Insertion", self.test_data_insertion),
            ("FFA Scraper", self.test_ffa_scraper),
            ("FFA Scraper URLs", self.test_ffa_scraper_urls),
            ("FFA Scraper Competition IDs", self.test_ffa_scraper_competition_ids),
            ("FFA Scraper Competition by Year", self.test_ffa_scraper_competition_by_year),
            ("FFA Scraper Competition Result", self.test_ffa_scraper_competition_result),
            ("FFA Scraper Categories", self.test_ffa_scraper_categories),
            ("FFA Scraper Competition Result by Category", self.test_ffa_scraper_competition_result_by_category)
        ]
        
        for test_name, test_func in tests:
            self.run_test(test_name, test_func)
        
        print(f"\n=== Results ===")
        print(f"✓ Passed: {self.success}")
        print(f"✗ Failed: {self.failure}")
        print(f"Total: {self.success + self.failure}")
        
        if os.path.exists("test.db"):
            os.remove("test.db")


if __name__ == "__main__":
    test_runner = TestRunner()
    test_runner.run_all_tests()