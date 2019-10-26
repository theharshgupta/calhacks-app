import pdfplumber as plum

def classify(pathToFile):
    global bank_name
    bank_name = ""
    firstPage = plum.open(path=pathToFile).pages[0]
    firstPageText = firstPage.extract_text()

    if "_________________________" in firstPageText:
        bank_name = "BOA"
    else:
        if "MORGAN" in firstPageText:
            bank_name = "JPM"
        else:
            bank_name = "JPM"

    print("Bank: ", bank_name)
    return bank_name
