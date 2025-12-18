import unittest
from analyzer import CVAnalyzer, read_file

class TestCVAnalyzer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sample_cv = "Python, Java, ohjelmointi, ohjelmistokehitys, web-kehitys"
        cls.sample_job = "Python, ohjelmointi, backend, tietokannat, ohjelmistokehitys"
    
    def test_word_count(self):
        analyzer = CVAnalyzer(self.sample_cv, self.sample_job)
        self.assertEqual(analyzer.word_count(), 5)
    
    def test_extract_keywords(self):
        analyzer = CVAnalyzer(self.sample_cv, self.sample_job)
        keywords = analyzer.extract_keywords(self.sample_cv)
        self.assertGreaterEqual(len(keywords), 3)
        self.assertIn("python", keywords)
    
    def test_match_score(self):
        analyzer = CVAnalyzer(self.sample_cv, self.sample_job)
        score = analyzer.match_score()
        self.assertTrue(0 <= score <= 100)
    
    def test_sentiment(self):
        analyzer = CVAnalyzer("I love programming", "Python developer needed")
        self.assertIn(analyzer.sentiment(), ['Positiivinen', 'Neutraali', 'Negatiivinen'])
    
    def test_read_file(self):
        # Tässä voit lisätä testin tiedoston lukemiselle
        # Huom: Luo väliaikainen testitiedosto tai käytä olemassa olevaa
        pass

if __name__ == '__main__':
    unittest.main()