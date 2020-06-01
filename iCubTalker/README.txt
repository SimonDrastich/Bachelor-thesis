Táto aplikácie slúži na hlasové ovládanie pohybov tela humanoidného
robota iCuba, ktorého simulujeme v robotickom simulátore iCubSim. Hlasom dávame
iCubovi povel prostredníctvom mobilnej aplikácie Recognize4PC, ktorá na rozpoznávanie 
reči využíva Google speech API. Ovládanie je integrované chatbot systémom, ktorý
z povelov klasifikuje používateľove zámery a vyvoláva na ne relevantné iCubové reakcie.
Primárnou doménou robota iCub je pohyb, ktorý je rozdelený na pohyby jedným
kĺbom a komplexné pohyby, ktoré ho dokážeme učiť priamo počas interakcie. Robot
tvorí reakcie aj slovného charakteru syntetizovaným hlasom.


Inštalácia:
V podpriečinku apk sa nachádza inštalačný súbor mobilnej aplikácie Recognize4PC, ktorou budeme 
ovládať robota iCuba.

Potrebné Python knižnice sa nachádzajú v requirements.txt, ktoré môžete inštalovať aj pomocou 
pip install -r requirements.txt



Hlavný program sa spúšťa batch filom START.bat, štart môže trvať okolo minúty.
Občas môže nastať problém s spustením yarpserveru, v takom prípade treba v súbore 
iCubSim/run-iCubSim.bat pridať alebo naopak odobrať flag "--write" za príkazom "start yarpserver.exe"
V prípade že nastane tento problém, sa yarpserver hneď po spustení vypne a iCub Simulátor sa načíta 
iba ako čierne okno.

Po úspešnom spustení hlavného programu si pustíme mobilnú aplikáciu Recognize4PC, pomocou ktorej sa
pripojíme na hlavný program po lokálnej sieti vyplnením IP adresy do textového okna a stalčením tlačídla
connect. Po úspešnom pripojení sa v terminale v ktorom beží main vypíše vlajka connect.

Po stlačení buttonu speak zadávate príkaz, ktorý sa po spracovaní a ukončení nahrávania prepošle robotovi,
ktorý s vami začne interagovať.