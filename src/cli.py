from utils import read_data
from exercise3_functions import RdfData, conjuction_index, get_search_results
import fire

def exercise_3(query):
    content = read_data()
    rdf_data = RdfData(content)
    query_conjuctions = ["OR", "AND NOT", "AND"]
    query_index_value = conjuction_index(query_conjuctions, query)
    phrase_search_bool = False if query_index_value != "None" else True
    query_index = query_index_value if query_index_value != "None" else 0
    search_result = get_search_results(rdf_data(), query_conjuctions[query_index], query, phrase_search=phrase_search_bool)
    print(f'"{query}" found in:')
    if not isinstance(search_result, dict):
        value = []
        for idx in list(search_result):
            # print(f"{rdf_data.get_uri(idx)}")
            value.append(rdf_data.get_uri(idx))
        for x in sorted(value):
            print(f"{x}")
    else:
        id_to_text = {}
        for uri_idx in search_result:
            id_to_text[rdf_data.get_uri(uri_idx)] = search_result[uri_idx]
        for uri_id in dict(sorted(id_to_text.items())):
            # print(uri_id)
            # print(search_result[uri_id])
            print(f"{uri_id} {id_to_text[uri_id]}")



if __name__ == "__main__":
    # query = "IHÉS OR Damrosch"
    # exercise_3(query)
    fire.Fire(exercise_3)
