from bs4 import BeautifulSoup
import requests

page = requests.get("https://www.tabroom.com/index/tourn/results/round_results.mhtml?tourn_id=32875&round_id=1227453")
soup = BeautifulSoup(page.content, "html.parser")
print(soup.)