import undetected_chromedriver as uc             # Open Chrome without the site knowing you're a robot
from selenium.webdriver.common.by import By      # Finding HTML elements on the page
import time

class PriceScraper:
    def __init__(self):
        self.driver = None

    # Create the Chrome browser
    def get_driver(self):
        if not self.driver:
            options = uc.ChromeOptions()
            options.add_argument("--window-size=1024,768")
            self.driver = uc.Chrome(options=options)
        return self.driver

    def fetch_trendyol(self, query):
        driver = self.get_driver()
        results = []
        try:
            driver.get(f"https://www.trendyol.com/sr?q={query}")
            time.sleep(5)
            t_cards = driver.find_elements(By.CSS_SELECTOR, ".p-card-wrppr, .product-card")[:5]
            count_t = 0
            for card in t_cards:
                if count_t >= 3: break
                try:
                    name = card.find_element(By.CSS_SELECTOR, "span.product-name").text.strip()
                    p_el = card.find_element(By.CSS_SELECTOR, "[data-testid='price-value'], [data-testid='price-section'], .prc-box-dscntd")
                    p_val = p_el.text.replace("TL", "").replace("Sepette", "").strip()
                    results.append({"store": "Trendyol", "name": name, "price_display": p_val})
                    count_t += 1
                except: continue
        except: pass
        return results

    def fetch_hepsiburada(self, query):
        driver = self.get_driver()
        results = []
        seen_in_h = set() 
        try:
            driver.get(f"https://www.hepsiburada.com/ara?q={query}")
            time.sleep(5)
            h_cards = driver.find_elements(By.CSS_SELECTOR, "li[class*='productListContent'], article[class*='productCard-module']")[:10]
            count_h = 0
            for card in h_cards:
                if count_h >= 3: break
                try:
                    try:
                        c_name = card.find_element(By.CSS_SELECTOR, "a[class*='productCardLink']").get_attribute("title")
                    except:
                        c_name = card.find_element(By.CSS_SELECTOR, "a[class*='productCardLink']").text.strip()
                    
                    c_price = "0"
                    try:
                        p_el = card.find_element(By.CSS_SELECTOR, "[data-test-id^='final-price-']")
                        c_price = p_el.text.replace("TL", "").strip()
                    except:
                        try:
                            p_el = card.find_element(By.CSS_SELECTOR, "div[class*='finalPrice']")
                            c_price = p_el.text.replace("TL", "").strip()
                        except: continue

                    if c_name and c_price != "0":
                        if c_name not in seen_in_h:
                            results.append({"store": "Hepsiburada", "name": c_name, "price_display": c_price})
                            seen_in_h.add(c_name)
                            count_h += 1
                except: continue
        except: pass
        return results