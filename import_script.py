# -*- coding: Utf-8 -*

import json
import requests
import psycopg2
from pureButter_project.password import DBPASS

CATEGORIES = ["pizzas", "non-alcoholic-beverages", "ravioli", "sweet-spreads",
              "cheeses", "frozen-ready-made-meals", "yogurts", "sweet-snacks",
              "salty-snacks"]

# connection to postgresql
try:
    CONNECTION = psycopg2.connect(user="postgres",
                                  password=DBPASS,
                                  host="127.0.0.1",
                                  port="5432",
                                  database="pure_butter")
    CURSORDB = CONNECTION.cursor()
except (Exception, psycopg2.Error) as error :
    print("Error while connecting to PostgreSQL", error)

# Data import from open food fact.
for each_categories in CATEGORIES:
    sql = "INSERT INTO product_category (name) VALUES (%s)"
    val = (each_categories,)
    CURSORDB.execute(sql, val)
    CONNECTION.commit()
    # We select the first 60 product pages from each categories.
    for category_page in range(60):
        category_page_str = str(category_page)
        url = "https://fr-en.openfoodfacts.org/category/" + each_categories +\
              "/" + category_page_str + ".json"
        response = requests.get(url)
        found = json.loads(response.text)
        product_comp = found["products"]
        # We scan each product on a page
        for each_product in product_comp:
            try:
                # We check if each product is: French, has at least one
                # store, has the ingredients and a bare code. if
                # something is missing, we go to the next.
                if each_product["countries_tags"].count("en:france") >= 1 and\
                   each_product["ingredients_text_fr"] != "" and\
                   each_product["id"] != "" and\
                   each_product["nutrition_grades"] != "" and\
                   each_product["url"] != "":
                    clean_product_name =\
                        each_product["product_name"].replace("\\n", " ")
                    clean_product_name =\
                        clean_product_name.replace("\\r", " ")
                    print(clean_product_name)
                    clean_ingredient =\
                        each_product["ingredients_text_fr"].replace(
                            "\\n", " ")
                    clean_ingredient =\
                        clean_ingredient.replace("\\r", " ")
                    sql = """INSERT INTO product_product (name,
                            nutrition_grades, ingredients, url,
                            category_id)
                            VALUES (%s, %s, %s, %s, %s)"""
                    val = (clean_product_name,
                           each_product["nutrition_grades"],
                           clean_ingredient, each_product["url"],
                           (CATEGORIES.index(each_categories) + 1))
                    CURSORDB.execute(sql, val)
                    CONNECTION.commit()
            except KeyError:
                print("No French ingredients list, nutrition grade, url or ID.")
