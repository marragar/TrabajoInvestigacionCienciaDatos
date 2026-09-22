from ddgs import DDGS

with DDGS() as ddgs:
    resultados = ddgs.text("Juan José Fernández Domínguez Universidad de León", max_results=3)
    for r in resultados:
        print(r["title"])
        print(r["body"])
        print(r["href"])
        print("---")