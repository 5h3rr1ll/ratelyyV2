from django.db import models

from urllib.parse import urlparse
from urllib import request, parse
from string import ascii_uppercase
from bs4 import BeautifulSoup
import re, sys


# Create your models here.
class Concerns(models.Model):
    name = models.CharField(max_length=50)
    fair = models.IntegerField()
    eco = models.IntegerField()

    class Meta:
        db_table = "Concerns"

    def __str__(self):
        return self.name


class Companies(models.Model):
    name = models.CharField(max_length=50)
    fair = models.IntegerField()
    eco = models.IntegerField()
    concern = models.ForeignKey("Concerns", null=True)

    class Meta:
        db_table = "Companies"

    def __str__(self):
        return self.name


class Brands(models.Model):
    name = models.CharField(max_length=50, null=True)
    altName = models.CharField(max_length=50, null=True)
    fair = models.IntegerField()
    eco = models.IntegerField()
    concern = models.ForeignKey("Concerns", null=True)
    company = models.ForeignKey("Companies", null=True)
    url = models.CharField(max_length=50, null=True)
    img = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = "Brands"

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=50)
    ean = models.IntegerField(17)
    fair = models.IntegerField()
    eco = models.IntegerField()
    company = models.ForeignKey("Companies", null=True)
    concern = models.ForeignKey("Concerns", null=True)

    class Meta:
        db_table = "Products"

    def __str__(self):
        return self.name

# class Alles(models.Model):
#     name = models.()
#     ean = models.IntegerField(17)
#     fair = models.IntegerField()
#     eco = models.IntegerField()
#     company = models.ForeignKey("Companies", null=True)
#     concern = models.ForeignKey("Concerns", null=True)
#
#     class Meta:
#         db_table = "Alles"
#
#     def __str__(self):
#         return self.name


class brandsCrawler():

    def showCrawledBrands(self):
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


    def saveBrands(self):
        """Diese Funktion ruft die Funktion Crawler auf, jene eine Liste mit den
        zurück Marken von Nestlé zurück gibt. Diese Liste wird dann in die Datenbank
        gespeicehrt."""

        print("Sammle Nestle-Marken")

        """um auf die vorangegangende Funktion in erhalb der Klasse zugreifen zu
        können, muss vor dem Funktionsaufruf das Schlüsselwort "self." stehen"""
        brandLst = self.showCrawledBrands()

        for brand in brandLst:
            print(brand)
            obj, created = Brands.objects.get_or_create(name = brand, fair = 0,
                eco = 0, concern = Concerns.objects.get(name="Nestle"))
            print("Saved")

class companyCrawler():

    def showCompanies(self):
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

    def saveCompanies(self):
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

        nestle = Concerns.objects.get(name="Nestle")

        for name in allSpanTags:
            if name.string not in ignorWords and name.string is not None:
                companyLst.append(name.string)

        for i in companyLst:
            print(i)
            # obj, created = Companies.objects.get_or_create(name = i, fair = 0, eco = 0, concern = nestle)
            print(i,"saved")

        # print("Das sind Nestles Firmen in Deutschland:","\n",", ".join(companyLst), "\n")
        return(companyLst)


class NewCrawler():

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

            obj, created = Brands.objects.get_or_create(name = productTitel,
                altName = bildAltTitel, url = urlZumHersteller, fair = 0,
                eco = 0, concern = Concerns.objects.get(name="Nestle"), img = bildUrl)

                # print("Saved")

            # for prodName in soup.find_all("span", class_ = "title"):
            #     for child in prodName.children:
            #         if child.get("alt"):
            #             brandLst.append(child.get("alt"))

        # print(brandLst)
        # return(brandLst)


    def saveBrands(self):
        """Diese Funktion ruft die Funktion Crawler auf, jene eine Liste mit den
        zurück Marken von Nestlé zurück gibt. Diese Liste wird dann in die Datenbank
        gespeicehrt."""

        print("Sammle Nestle-Marken")

        """um auf die vorangegangende Funktion in erhalb der Klasse zugreifen zu
        können, muss vor dem Funktionsaufruf das Schlüsselwort "self." stehen"""
        brandLst = self.showCrawledBrands()

        for brand in brandLst:
            print(brand)
            obj, created = Brands.objects.get_or_create(name = brand, fair = 0,
                eco = 0, concern = Concerns.objects.get(name="Nestle"))
            print("Saved")
