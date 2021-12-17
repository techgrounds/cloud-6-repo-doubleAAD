# Protocols

Een netwerk protocol is een afspraak die wij mensen gemaakt hebben over hoe computers met elkaar communiceren. Deze afspraken maken het mogelijk dat het Internet kan bestaan, zonder dat je voor iedere verbinding een andere standaard moet aanhouden.
Het OSI-model is een goed hulpmiddel om te beschrijven waar een protocol ‘leeft’ en wat het doel is van een protocol. Vaak genoeg ‘leeft’ een protocol in meerdere lagen van het OSI-model.



![SCREENSHOT](../00_includes/Cloud8-01.png)



## Opdracht

- Begrijp hoe een HTTPS TCP/IP-pakket opgebouwd is:


![SCREENSHOT](../00_includes/Cloud08-1.png)

Hypertext Transfer Protocol (HTTP) is een application layer protocol. HTTP gebruikt TCP/IP protocol om de website op je browser te kunnen zien.
TCP/IP en OSI protocol bestaat uit lagen en beide protocolen zijn bijna het zelfde, TCP/IP en OSI protocol gebruiken beide 7 lagen om data te transferen. OSI maakt gebruik van lagen 5 en 6 maar TCP/IP maakt geen gebruik van lagen 5 en 6.

- Begrijp wie bepaalt welke protocols wij gebruiken en wat je zelf moet doen om een nieuw protocol te introduceren.

Bedrijven en developers


- Identificeer op zijn minst één protocol per OSI-laag.


![SCREENSHOT](../00_includes/Cloud08-3.png)


        Layer 7	    Application	    SMTP, HTTP, FTP, POP3, SNMP
        Layer 6	    Presentation	MPEG, ASCH, SSL, TLS
        Layer 5	    Session	        NetBIOS, SAP
        Layer 4	    Transport	    TCP, UDP
        Layer 3	    Network	        IPV5, IPV6, ICMP, IPSEC, ARP, MPLS.
        Layer 2	    Data Link	    RAPA, PPP, Frame Relay, ATM, Fiber Cable, etc.
        Layer 1	    Physical	    RS232, 100BaseTX, ISDN, 11.


![SCREENSHOT](../00_includes/Cloud8-01.png)
    

- Facebook was recent een lange tijd niet beschikbaar. Ontdek waarom. Tip: BGP.

BGP: Border Gateway Protocol is het belangrijkste routeringsprotocol van het internet: het wordt gebruikt om verkeer tussen verschillende providers te routeren. BGP is te vinden in Laag 4 (Transport).

Door een configuratiewijzigingen met betrekking tot BGP waardoor routers van internetproviders geen toegang hadden om de data te ontvangen.

### Gebruikte bronnen

- https://tweakers.net/nieuws/187706/facebook-downtime-kwam-door-configuratiefout-backbonerouters.html
- https://www.guru99.com/layers-of-osi-model.html

### Ervaren problemen

Geen

### Resultaat

Ik heb geprobeerd om zo veel mogelijk in eigen woorden te typen wat de betekenis is van bepaalde termen en diensten en dat is hier boven te zien met fotos.