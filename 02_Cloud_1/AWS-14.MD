# Netwerkapparatuur

Er bestaat geen netwerk zonder netwerkapparatuur als je meer dan twee computers aan elkaar wilt schakelen. 
Een korte, en zeker niet complete, lijst van netwerkapparatuur volgt:

- router
- switch
- repeaters
- access point 

Elk apparaat in de lijst dragen bij dat je data bezorgd wordt bij de juiste computer. En vaak zijn ze slim genoeg om samen te onderhandelen zodat jij, als gebruiker, geen zorgen hoeft te maken over de instellingen. Je netwerkapparaten blijven het doen zelfs als je computers toegevoegd of verwijderd van je netwerk. Protocollen zijn hier belangrijk in.
Implementaties van netwerkapparatuur kan ook verschillen: er bestaan meerdere vormen van een switch die werken op verschillende lagen van het OSI-model.
AWS en Azure bieden diensten aan die gelijk zijn aan wat netwerkapparatuur doen. En ieder netwerkconcept (routing, switching, gateways) heeft één of meerdere cloud equivalenten.


## Key-terms

DHCP: Een apparaat dat je aansluit op je netwerk via een kabel of wifi krijgt automatisch een verbinding met het netwerk en internet. Je router bevat hiervoor een DHCP-server (Dynamic Host Configuration Protocol). Deze zorgt ervoor dat netwerkapparatuur die je aansluit op het netwerk automatisch een ip-adres en andere netwerkinstellingen krijgt toegewezen. Je kunt in de webinterface van je router instellen hoeveel ip-adressen de dhcp-server kan gebruiken.

DNS: Dns, dat staat voor Domain Name System, zorgt voor de vertaling tussen de urls die je in je browser tikt en de ip-adressen van de achterliggende webservers. Wanneer je in je browser een webadres intikt, dan zorgt dns ervoor dat het adres automatisch naar het juiste ip-adres wordt omgezet, zodat de site op het internet ‘vindbaar’ is. Dns-gegevens worden gecached, waardoor je een website bij bijvoorbeeld een migratie naar een andere server mogelijk tijdelijk niet kunt bereiken.

DDNS: Met een DDNS of Dynamic Domain Name System koppel je een url aan je ip-adres. Hierdoor kun je je ip-adres van je netwerkverbinding en − indien je dit hebt ingesteld − je apparatuur in je netwerk bereiken via een url.
Het bijzondere van een DDNS zit hem in het woordje dynamic. Je internetverbinding heeft doorgaans een dynamisch ip-adres dat door je internetprovider veranderd kan worden. Door een DDNS-dienst te koppelen met je nas (of router) wordt dit nieuwe ip-adres doorgegeven aan de DDNS-dienst en blijven de ingestelde apparaten in je thuisnetwerk bereikbaar via de ingestelde url. Een DDNS-mogelijkheid is zeker handig als je de nas wilt gebruiken als vpn-server. Sommige router- en nas-fabrikanten bieden een gratis DDNS-dienst.

## Opdracht

- Benoem en beschrijf de functies van veel voorkomend netwerkapparatuur


- Meeste routers hebben een overzicht van alle verbonden apparaten, vindt deze lijst. Welke andere informatie heeft de router over aangesloten apparatuur?
De standaard instellingen


- Waar staat je DHCP server op jouw netwerk? Wat zijn de configuraties hiervan?
- Bekijk wat netwerkapparatuur voor bedrijven meer kunnen doen.

### Gebruikte bronnen
[Plaats hier de bronnen die je hebt gebruikt.]

### Ervaren problemen
[Geef een korte beschrijving van de problemen waar je tegenaan bent gelopen met je gevonden oplossing.]

### Resultaat
[Omschrijf hoe je weet dat je opdracht gelukt is (gebruik screenshots waar nodig).]