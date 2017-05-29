import json
import database.models

f = open("company_brand_dic.txt", "r").read()

company_brand_dic = json.loads(f)

for brand in Brand.objects.all():
    for company in company_brand_dic:
        for entry in company_brand_dic[company]:
            if brand in entry:
                print(company)
