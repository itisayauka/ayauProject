import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Настройка Selenium для запуска Chrome
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Открываем страницу с расписанием дорам
driver.get("https://dorama.land/calendar")

dorama_data = []  # Список для хранения информации о дорамах

# Ожидаем загрузку расписания
try:
    schedule_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.switch > a"))
    )

    print("\n📅 Найдено расписание дорам:")
    for month in schedule_elements:
        print("-", month.text)

    # Собираем ссылки на дорамы
    dorama_links = [month.get_attribute("href") for month in schedule_elements if month.get_attribute("href")]

    # Парсим каждую дораму
    for index, link in enumerate(dorama_links):
        print(f"\n🔍 Парсим дораму {index + 1}/{len(dorama_links)}: {link}")
        driver.get(link)
        time.sleep(3)  # Ждём загрузку страницы

        try:
            # Название дорамы
            title = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            ).text.strip()

            # Отзывы
            # review_elements = driver.find_elements(By.CSS_SELECTOR, "div.comment-content div.comment-footer div.review-serial-rate")
            review_elements = driver.find_elements(By.XPATH, '//*[@id="cid241374"]')
            
            print('FFFFFFFFF', review_elements)
            
            reviews = [review.text for review in review_elements] if review_elements else []

            # Озвучки
            sound_elements = driver.find_elements(By.CSS_SELECTOR, "#field-sound ul > li")
            ozvuchki = [sound.text for sound in sound_elements] if sound_elements else []

            # Добавляем данные в список
            dorama_data.append({
                "Название": title,
                "Ссылка": link,
                "Отзывы": reviews,
                "Озвучки": ozvuchki
            })

            print(f"✅ Успешно спарсили: {title}")

        except Exception as e:
            print(f"❌ Ошибка при парсинге страницы {link}: {e}")

except Exception as e:
    print("❌ Ошибка при парсинге расписания:", e)

# Сохраняем данные в JSON
with open("dorama_data.json", "w", encoding="utf-8") as file:
    json.dump(dorama_data, file, ensure_ascii=False, indent=4)

print("\n✅ Данные сохранены в dorama_data.json")

# Закрываем браузер
driver.quit()
