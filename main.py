import click, pick, requests, json

class Bromide:
    def __init__(self, url: str = "http://127.0.0.1:8080", password: str = ""):
        self.url = url
        self.headers = {"Authorization": password, "Content-Type": "application/json"}

    def request(self, data, url_ext):
        r = requests.post(f"{self.url}{url_ext}", headers=self.headers, json=data)
        if r.status_code != 200:
            return None
        else:
            return r.json()

    def read(self, data: str):
        return self.request({"entry": data}, "/read")

    def create(self, data: dict) -> dict:
        return self.request(data, "/create")

    def delete(self, data: str) -> dict:
        return self.request({"entry": data}, "/delete")
    
def run_pick(bromide: Bromide):
    title = "please select an action."
    options = ["create", "read", "delete"]
    option, _ = pick.pick(options, title)
    data = input("enter valid JSON to send to the DB.\n")
    if option == "create":
        try:
            data = json.loads(data)
        except Exception as e:
            print(e)

    r = None

    if option == "create":
        r = bromide.create(data)
    if option == "read":
        r = bromide.read(data)
    if option == "delete":
        r = bromide.delete(data)

    input(f"{r}\nPress Enter to continue.")
    

@click.command()
@click.option('--password', default="")
@click.option('--url', default="http://127.0.0.1:8080")
def bromide(password, url):
    b = Bromide(url, password)
    while True:
        run_pick(b)

bromide()