import requests


#create product class
class Product(object):
    def __init__(self,omdb_json, detailed=False):
        #if detailed:
        self.product_name = omdb_json["productName"]
        self.price = omdb_json["Price"]
        self.product_id = omdb_json["productID"]
        self.type = "Product"
        self.category = omdb_json["Category"]

    def __repr__(self):
        return self.product_name


class ProductClient(object):
    def search(self, search_string):
        #Used for the search bar on the website
        search_string = "+".join(search_string.split())
        page = 1

        search_url = f"s={search_string}&page={page}"

        resp = self.sess.get(self.base_url + search_url)

        if resp.status_code != 200:
            raise ValueError(
                "Search request failed; make sure your API key is correct and authorized"
            )

        data = resp.json()

        if data["Response"] == "False":
            raise ValueError(f'[ERROR]: Error retrieving results: \'{data["Error"]}\' ')

        search_results_json = data["Search"]
        remaining_results = int(data["totalResults"])

        result = []

        while remaining_results != 0:
            for item_json in search_results_json:
                result.append(Product(item_json))
                remaining_results -= len(search_results_json)
            page += 1
            search_url = f"s={search_string}&page={page}"
            resp = self.sess.get(self.base_url + search_url)
            if resp.status_code != 200 or resp.json()["Response"] == "False":
                break
            search_results_json = resp.json()["Search"]

        return result

    def retrieve_product_by_id(self, product_id):
        product_url = self.base_url + f"i={product_id}&plot=full"
        resp = self.sess.get(product_url)

        if resp.status_code != 200:
            raise ValueError(
                "Search request failed; make sure your API key is correct and authorized"
            )

        data = resp.json()

        if data["Response"] == "False":
            raise ValueError(f'Error retrieving results: \'{data["Error"]}\' ')

        product = Product(data, detailed=True)

        return product


# -- Example usage -- #
if __name__ == "__main__":
    import os

    # client = MovieClient(os.environ.get("OMDB_API_KEY")) #some other function

    # movies = client.search("guardians")

    # for movie in movies:
    #     print(movie)

    # print(len(movies))