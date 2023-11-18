def read_data():
    with open("assets/dbpedia_long_abstracts_en_l1-12k.ttl", "r", encoding="utf-8") as file:
        content = file.read()
    return content
