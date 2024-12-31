from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from google.cloud import datastore
import time

# Initialize headless Firefox driver
options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)

# Initialize Datastore client
client = datastore.Client()

try:
    driver.get("https://play.google.com/store/apps/top")
    wait = WebDriverWait(driver, 5)  # Reduce wait time

    app_data = []

    # Scroll and collect app containers
    for _ in range(1):  # Reduce scrolling range
        elems = wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//div[contains(@class, "ULeU3b neq64b")]')
            )
        )

        for elem in elems:
            if len(app_data) >= 2:  # Collect up to 10 apps
                break

            try:
                app_link = elem.find_element(By.XPATH, './/a[contains(@href, "/store/apps/details")]').get_attribute("href")
                app_logo = elem.find_element(By.XPATH, './/img').get_attribute("src")
                package_name = app_link.split("id=")[-1]
                app_name = package_name.split(".")[1].capitalize()

                if app_link not in [app['app_url'] for app in app_data]:  # Ensure uniqueness
                    app_data.append({"app_url": app_link, "app_img": app_logo, "app_name": app_name, "app_package": package_name})
            except Exception:
                continue

        if len(app_data) >= 2:
            break

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)  # Minimize sleep

    print(f"Collected {len(app_data)} apps from the initial page.")

    for app in app_data:
        try:
            driver.get(app['app_url'])
            time.sleep(1)  # Minimize sleep

            try:
                app_developer = driver.find_element(By.XPATH, '//div[contains(@class, "Vbfug auoIOc")]/a/span').text or "N/A"
                app_ratings = driver.find_element(By.XPATH, '//div[contains(@class, "TT9eCd")]').text or "N/A"
                app_price = "free"
                app_description = driver.find_element(By.XPATH, '//div[contains(@class, "bARER")]').text or "N/A"
                if len(app_description.encode('utf-8')) > 1400:
                    app_description = app_description[:1397] + "..."
                screenshot_elements = driver.find_elements(By.XPATH, '//img[contains(@class, "T75of")]')
                app_screenshots = [img.get_attribute("src") for img in screenshot_elements[:10]]

                app.update({
                    "app_developer": app_developer,
                    "app_ratings": app_ratings,
                    "app_price": app_price,
                    "content": app_description,
                    "img_arr": app_screenshots,
                })

                key = client.key('top_new_apps_1', app['app_package'])
                entity = client.get(key)
                if not entity:
                    entity = datastore.Entity(key=key)
                    entity.update(app)
                    client.put(entity)
                    print(f"Added {app['app_name']} to Datastore.")
                else:
                    print(f"{app['app_name']} already exists in Datastore.")
            except Exception as e:
                print(f"Error extracting additional details: {e}")
        except Exception as e:
            print(f"Error processing app detail page: {e}")
            continue
finally:
    driver.quit()
