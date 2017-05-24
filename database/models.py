from django.db import models

from urllib.parse import urlparse
from urllib import request, parse
from string import ascii_uppercase
from bs4 import BeautifulSoup
import re, sys


# Create your models here.
class Concern(models.Model):
    name = models.CharField(max_length=50)
    fair = models.IntegerField()
    eco = models.IntegerField()
    url = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = "Concern"

    def __str__(self):
        return self.name


class New_Concern_by_Users(models.Model):
    """
    This table is for concerns users are looking up and can't find them in the
    main concernces table. After checking the entries valid entries become
    transfered to the main concerns table
    """
    name = models.CharField(max_length=50)
    fair = models.IntegerField()
    eco = models.IntegerField()
    url = models.CharField(max_length=50, null=True)
    counter = models.CharField(max_length=1000, default=0)

    class Meta:
        db_table = "newConcernByUsers"

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=50)
    fair = models.IntegerField()
    eco = models.IntegerField()
    concern = models.ForeignKey("Concern", null=True)

    class Meta:
        db_table = "Company"

    def __str__(self):
        return self.name


class New_Company_by_Users(models.Model):
    """
    This table is for companies users are looking up and can't find them in the
    main concernces table. After checking the entries valid entries become
    transfered to the main table.
    """
    name = models.CharField(max_length=50)
    fair = models.IntegerField()
    eco = models.IntegerField()
    url = models.CharField(max_length=50, null=True)
    counter = models.CharField(max_length=1000, default=0)

    class Meta:
        db_table = "newCompanyByUsers"

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=50, null=True)
    altName = models.CharField(max_length=50, null=True)
    fair = models.IntegerField()
    eco = models.IntegerField()
    concern = models.ForeignKey("Concern", null=True)
    company = models.ForeignKey("Company", null=True)
    url = models.CharField(max_length=50, null=True)
    img = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = "Brand"

    def __str__(self):
        return self.name


class New_Brand_by_Users(models.Model):
    """
    This table is for brands users are looking up and can't find them in the
    main brand table. After checking the entries valid entries become
    transfered to the main table
    """
    name = models.CharField(max_length=50)
    fair = models.IntegerField()
    eco = models.IntegerField()
    url = models.CharField(max_length=50, null=True)
    counter = models.CharField(max_length=1000, default=0)

    class Meta:
        db_table = "newBrandByUsers"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    ean = models.IntegerField(17)
    fair = models.IntegerField()
    eco = models.IntegerField()
    company = models.ForeignKey("Company", null=True)
    concern = models.ForeignKey("Concern", null=True)

    class Meta:
        db_table = "Product"

    def __str__(self):
        return self.name


class New_Product_by_Users(models.Model):
    """
    This table is for products users are looking up and can't find them in the
    main brand table. After checking the entries valid entries become
    transfered to the main table.
    """
    name = models.CharField(max_length=50)
    fair = models.IntegerField()
    eco = models.IntegerField()
    url = models.CharField(max_length=50, null=True)
    counter = models.CharField(max_length=1000, default=0)

    class Meta:
        db_table = "newProductByUsers"

    def __str__(self):
        return self.name


class Brands_Crawler():
    def show_crawled_brand(self):
        """Dieser Funktion crawlt einmal durch alle Marken von Nestle und speichert
        fasst dabei alle Markennamen ab, indem der Crawler die alternantiven Titel
        der Bilder auf der jeweiligen Seite abfragt."""

        url = "http://www.nestle.de"

        #filter nur das Protokoll inkl. :// heraus
        regExURLProto = r"^[a-z]*:\/\/"
        #filter alles was hinter dem protokoll :// kommt
        regExURLAbPro = r"(?:^[a-z]*:\/\/)(.*)"
        #Filter die Domain z.B. www.nestle.de, jedoch in zwei Teilen, in (www) und
        #in (nestle.de). So kann man in der URL seperat darauf prüfen ob ein (www)
        #benutzt wurde.
        regExDomain = r"(w{1,}\.)([a-zA-Z]+\.\w+)"

        #hier wird nur das Protkoll mit :// gespeichert, z.B. http://
        urlPro = re.findall(regExURLProto, url)[0]
        #hier wird alles von der URL nach dem :// gespeichert, z.B. www.nestle.de
        restUrl = re.findall(regExURLAbPro, url)
        #hier soll nur die Domain gespichert werden
        domain = re.findall(regExDomain, url)
        # durch regex wird die Domain in zwei Teile geteilt, in der nächsten Zeile
        # setze ich die Domain wieder zusammen.
        domain = domain[0][0]+ domain[0][1]

        #eine String mit den Buchstaben von A bis Z
        buchstabenLst = ascii_uppercase

        #um einzelne Seiten zu prüfen, nächste Zeile aktivieren
        # buchstaben = "A"

        #diese Variable speichert nacher die Markennamen
        brandLst = []

        # Um durch die Seiten crawlen zu können, muss sich das Ende der Domain dem
        # gesuchten Buchstaben entsprechenden ändern. Die folgende Schleife soll durch
        # alle Seite, also von A bis Z durchlaufen
        for buchstabe in buchstabenLst:
            print("Sammle nun alle Marken mit Anfangsbuchstaben {}".format(buchstabe))
            url = urlPro + domain + "/marken/a-z?char=" + buchstabe
            siteObject = request.urlopen(url)
            html = siteObject.read().decode()
            soup = BeautifulSoup(html, "html.parser")

            for prodName in soup.find_all("span", class_ = "title"):
                for child in prodName.children:
                    if child.get("alt"):
                        brandLst.append(child.get("alt"))

        # print(brandLst)
        return(brandLst)


    def save_brand(self):
        """Diese Funktion ruft die Funktion Crawler auf, jene eine Liste mit den
        zurück Marken von Nestlé zurück gibt. Diese Liste wird dann in die Datenbank
        gespeicehrt."""

        print("Sammle Nestle-Marken")

        """um auf die vorangegangende Funktion in erhalb der Klasse zugreifen zu
        können, muss vor dem Funktionsaufruf das Schlüsselwort "self." stehen"""
        brandLst = self.showCrawledBrand()

        for brand in brandLst:
            print(brand)
            obj, created = Brand.objects.get_or_create(name = brand, fair = 0,
                eco = 0, concern = Concern.objects.get(name="Nestle"))
            print("Saved")

class Company_Crawler():
    def show_Company(self):
        """Dieser Funktion crawlt einmal die deutsche Nestle-Seite und speichert
        dabei alle deutschen Unternehmen und deren Markennamen, indem der Crawler
        die alternantiven Titel der Bilder auf der jeweiligen Seite abfragt."""

        url = "http://www.nestle.de/unternehmen/struktur/marken"

        #filter nur das Protokoll inkl. :// heraus
        regExURLProto = r"^[a-z]*:\/\/"
        #filter alles was hinter dem protokoll :// kommt
        regExURLAbPro = r"(?:^[a-z]*:\/\/)(.*)"
        #Filter die Domain z.B. www.nestle.de, jedoch in zwei Teilen, in (www) und
        #in (nestle.de). So kann man in der URL seperat darauf prüfen ob ein (www)
        #benutzt wurde.
        regExDomain = r"(w{1,}\.)([a-zA-Z]+\.\w+)"

        #hier wird nur das Protkoll mit :// gespeichert, z.B. http://
        urlPro = re.findall(regExURLProto, url)[0]
        #hier wird alles von der URL nach dem :// gespeichert, z.B. www.nestle.de
        restUrl = re.findall(regExURLAbPro, url)
        #hier soll nur die Domain gespichert werden
        domain = re.findall(regExDomain, url)
        # durch regex wird die Domain in zwei Teile geteilt, in der nächsten Zeile
        # setze ich die Domain wieder zusammen.
        domain = domain[0][0]+ domain[0][1]

        #diese Variable speichert nacher die Unternehmensnamen
        companyLst = []

        url = urlPro + domain + "/unternehmen/struktur/marken"
        siteObject = request.urlopen(url)
        html = siteObject.read().decode()
        soup = BeautifulSoup(html, "html.parser")

        allSpanTags = soup.find_all("span", class_ = "as-struct")

        ignorWords = ["Nestlé Marken", "Kaffee", "Schokoladen", []]

        for brand in allSpanTags:
            if brand.string not in ignorWords and brand.string is not None:
                name = brand.string
                name = re.findall(r"\w", name)
                companyLst.append(name)

        # print(companyLst)
        return(companyLst)

    def save_Company(self):
        """Dieser Funktion crawlt einmal die deutsche Nestle-Seite und speichert
        dabei alle deutschen Unternehmen, indem der Crawler die alternantiven Titel
        der Bilder auf der jeweiligen Seite abfragt. Die Funktion gibt eine Liste
        mit den Firmennamen zurück."""

        # url = input("Gibt die URL ohen Protokoll ein (ohne http:// bzw. https://): ")
        url = "http://www.nestle.de/unternehmen/struktur/marken"
        #filter nur das Protokoll inkl. :// heraus
        regExURLProto = r"^[a-z]*:\/\/"
        #filter alles was hinter dem protokoll :// kommt
        regExURLAbPro = r"(?:^[a-z]*:\/\/)(.*)"
        #Filter die Domain z.B. www.nestle.de, jedoch in zwei Teilen, in (www) und
        #in (nestle.de). So kann man in der URL seperat darauf prüfen ob ein (www)
        #benutzt wurde.
        regExDomain = r"(w{1,}\.)([a-zA-Z]+\.\w+)"
        #hier wird nur das Protkoll mit :// gespeichert, z.B. http://
        urlPro = re.findall(regExURLProto, url)[0]
        #hier wird alles von der URL nach dem :// gespeichert, z.B. www.nestle.de
        restUrl = re.findall(regExURLAbPro, url)
        #hier soll nur die Domain gespichert werden
        domain = re.findall(regExDomain, url)
        # durch regex wird die Domain in zwei Teile geteilt, in der nächsten Zeile
        # setze ich die Domain wieder zusammen.
        domain = domain[0][0]+ domain[0][1]
        #diese Variable speichert nacher die Markennamen
        companyLst = []

        url = urlPro + domain + "/unternehmen/struktur/marken"
        siteObject = request.urlopen(url)
        html = siteObject.read().decode()
        soup = BeautifulSoup(html, "html.parser")

        allSpanTags = soup.find_all("span", class_ = "as-struct")

        ignorWords = ["Nestlé Marken", "Kaffee", "Schokoladen", []]

        nestle = Concern.objects.get(name="Nestle")

        for name in allSpanTags:
            if name.string not in ignorWords and name.string is not None:
                companyLst.append(name.string)

        for i in companyLst:
            print(i)
            # obj, created = Company.objects.get_or_create(name = i, fair = 0, eco = 0, concern = nestle)
            print(i,"saved")

        # print("Das sind Nestles Firmen in Deutschland:","\n",", ".join(companyLst), "\n")
        return(companyLst)


class New_brand_crawler():
    def save(self):
        """Dieser Funktion crawlt einmal durch alle Marken von Nestle und speichert
        fasst dabei alle Markennamen ab, indem der Crawler die alternantiven Titel
        der Bilder auf der jeweiligen Seite abfragt."""

        url = "http://www.nestle.de"

        #filter nur das Protokoll inkl. :// heraus
        regExURLProto = r"^[a-z]*:\/\/"
        #filter alles was hinter dem protokoll :// kommt
        regExURLAbPro = r"(?:^[a-z]*:\/\/)(.*)"
        #Filter die Domain z.B. www.nestle.de, jedoch in zwei Teilen, in (www) und
        #in (nestle.de). So kann man in der URL seperat darauf prüfen ob ein (www)
        #benutzt wurde.
        regExDomain = r"(w{1,}\.)([a-zA-Z]+\.\w+)"

        #hier wird nur das Protkoll mit :// gespeichert, z.B. http://
        urlPro = re.findall(regExURLProto, url)[0]
        #hier wird alles von der URL nach dem :// gespeichert, z.B. www.nestle.de
        restUrl = re.findall(regExURLAbPro, url)
        #hier soll nur die Domain gespichert werden
        domain = re.findall(regExDomain, url)
        # durch regex wird die Domain in zwei Teile geteilt, in der nächsten Zeile
        # setze ich die Domain wieder zusammen.
        domain = domain[0][0]+ domain[0][1]

        #eine String mit den Buchstaben von A bis Z
        buchstabenLst = ascii_uppercase

        #um einzelne Seiten zu prüfen, nächste Zeile aktivieren
        # buchstaben = "A"

        #diese Variable speichert nacher die Markennamen
        brandLst = []
        allLi = []

        # Um durch die Seiten crawlen zu können, muss sich das Ende der Domain dem
        # gesuchten Buchstaben entsprechenden ändern. Die folgende Schleife soll durch
        # alle Seite, also von A bis Z durchlaufen
        for buchstabe in buchstabenLst:
            print("Sammle nun alle Marken mit Anfangsbuchstaben {}".format(buchstabe))
            url = urlPro + domain + "/marken/a-z?char=" + buchstabe
            siteObject = request.urlopen(url)
            html = siteObject.read().decode()
            soup = BeautifulSoup(html, "html.parser")
            allLiOdd = soup.find_all("li", class_="row odd")
            for i in range(len(allLiOdd)):
                allLi.append(allLiOdd[i])
            allLiEven = soup.find_all("li", class_="row even")
            for i in range(len(allLiEven)):
                allLi.append(allLiEven[i])

        for li in range(len(allLi)):
            urlZumHersteller = urlPro + domain + allLi[li].a["href"]
            print("1",urlPro + domain + urlZumHersteller)
            bildAltTitel = allLi[li].img["alt"]
            print("2",bildAltTitel)
            bildUrl= urlPro + domain + allLi[li].img["src"]
            print("3",urlPro + domain + bildUrl)
            productTitel = allLi[li].span.span.string
            print("4",productTitel)

            obj, created = Brand.objects.get_or_create(name = productTitel,
                altName = bildAltTitel, url = urlZumHersteller, fair = 0,
                eco = 0, concern = Concern.objects.get(name="Nestle"), img = bildUrl)


def add_new_concern(name=None, fair=None, eco=None, url=None):
    counter = 0
    if name == None:
        print("Du hast keinen Namen eingegeben")
        return
    if fair == "Ja":
        fair = 1
    else:
        fair = 0
    if eco == "Ja":
        eco = 1
    else:
        eco = 0
    if url == None:
        url = "Null"
    print("Gesucht wird:",name)
    try:
        print("Sind im Try-Abschnitt")
        Concern.objects.get(name=name)
        return "Existiert bereits"
    except Concern.DoesNotExist as e:
        try:
            New_Concern_by_Users.objects.get(name=name)
            concern = New_Concern_by_Users.objects.get(name=name)
            counter = int(concern.counter)
            counter += 1
            concern.counter = counter
            concern.save()
            print("Der Konzern wurde bereits angefragt, schon mal wird es ihn in der",
                "Datenbank geben. Danke Dir!")
        except New_Concern_by_Users.DoesNotExist as e:
            print("Exception wurde Abgefangen:")
            New_Concern_by_Users.objects.create(name=name, fair=fair, eco=eco, url=url)
            return "Wurde neu angelegt. Danke dir!"

def add_new_company(name=None, fair=None, eco=None, url=None):
    counter = 0
    if name == None:
        print("Du hast keinen Namen eingegeben")
        return
    if fair == "Ja":
        fair = 1
    else:
        fair = 0
    if eco == "Ja":
        eco = 1
    else:
        eco = 0
    if url == None:
        url = "Null"
    print("Gesucht wird:",name)
    try:
        print("Sind im Try-Abschnitt")
        Company.objects.get(name=name)
        return "Existiert bereits"
    except Company.DoesNotExist as e:
        try:
            New_Company_by_Users.objects.get(name=name)
            company = New_Company_by_Users.objects.get(name=name)
            counter = int(company.counter)
            counter += 1
            company.counter = counter
            company.save()
            print("Das Unternehmen wurde bereits angefragt, schon mal wird es das"
                " Unternehemn in der Datenbank geben. Danke Dir!")
        except New_Company_by_Users.DoesNotExist as e:
            print("Exception wurde Abgefangen:")
            New_Company_by_Users.objects.create(name=name, fair=fair, eco=eco, url=url)
            return "Wurde neu angelegt. Danke dir!"


def add_new_brand(name=None, fair=None, eco=None, url=None):
    counter = 0
    if name == None:
        print("Du hast keinen Namen eingegeben")
        return
    if fair == "Ja":
        fair = 1
    else:
        fair = 0
    if eco == "Ja":
        eco = 1
    else:
        eco = 0
    if url == None:
        url = "Null"
    print("Gesucht wird:",name)
    try:
        print("Sind im Try-Abschnitt")
        Brand.objects.get(name=name)
        return "Existiert bereits"
    except Brand.DoesNotExist as e:
        try:
            New_Brand_by_Users.objects.get(name=name)
            brand = New_Brand_by_Users.objects.get(name=name)
            counter = int(brand.counter)
            counter += 1
            brand.counter = counter
            brand.save()
            print("Das Marke wurde bereits angefragt, schon bald wird es sie in der",
                "Datenbank geben. Danke Dir!")
        except New_Brand_by_Users.DoesNotExist as e:
            print("Exception wurde Abgefangen:")
            New_Brand_by_Users.objects.create(name=name, fair=fair, eco=eco, url=url)
            return "Wurde neu angelegt. Danke dir!"


def add_new_product(name=None, ean=None, fair=None, eco=None, url=None):
    counter = 0
    if name == None:
        print("Du hast keinen Namen eingegeben")
        return
    if fair == "Ja":
        fair = 1
    else:
        fair = 0
    if eco == "Ja":
        eco = 1
    else:
        eco = 0
    if url == None:
        url = "Null"
    print("Gesucht wird:",name)
    try:
        print("Sind im Try-Abschnitt")
        Product.objects.get(name=name)
        return "Existiert bereits"
    except Product.DoesNotExist as e:
        try:
            New_Product_by_Users.objects.get(name=name)
            brand = New_Product_by_Users.objects.get(name=name)
            counter = int(brand.counter)
            counter += 1
            brand.counter = counter
            brand.save()
            print("Das Marke wurde bereits angefragt, schon bald wird es sie in der",
                "Datenbank geben. Danke Dir!")
        except New_Product_by_Users.DoesNotExist as e:
            print("Exception wurde Abgefangen:")
            New_Product_by_Users.objects.create(name=name, fair=fair, eco=eco, url=url)
            return "Wurde neu angelegt. Danke dir!"
