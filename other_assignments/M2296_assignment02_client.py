#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 17:41:00 2019

@author: tuukka

Instructions:
    Modify the client and server example (from the slides) to work 
    correctly for arbitrarily sized messages. This means two things:

    Make sure everything gets sent and received
    Figure out a way to specify the length of the message to 
    the receiver

Feel free to use any of the methods covered in the slides!

Again, just copy pasting from the slides is not enough. 
If you have trouble understanding what this assignment is all about, 
then please ask!
"""
#client program
import socket
localhost = "127.0.0.5"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f'connecting to {localhost}')
s.connect((localhost, 8888))
#toSend = "Asuntomarkkinoilla on revennyt isoja eroja siinä, miten erilaiset asunnot eri puolilla Suomea käyvät nyt kaupaksi. Kiinteistömaailman kiinteistönvälittäjäbarometrin mukaan asuntomarkkina porskuttaa pääosassa Suomea hyvin talouden ikävistä signaaleista huolimatta. Myös OP:n asuntomarkkinakatsauksen mukaan asuntokauppa piristyi keväällä ja kesällä. Silti kauppa käy yhä hiljaisempana kuin 2010-luvun alkupuolella. /nMarkkinoille on ilmestynyt kuitenkin paljon alueita, joilla myytäviä asuntoja on ostajia enemmän. Ylitarjonta on keskittynyt erityisesti pieniin, uusiin asuntoihin tietyillä alueilla. Syynä on se, että pieniä asuntoja on rakennettu tänä ja viime vuonna valtavia määriä erityisesti sijoittajamarkkinoille, mutta tänä vuonna sijoittajien kiinnostus ostoihin on laimentunut./nYlitarjonta luo etenkin pitkittyessään 'ostajan markkinat' eli lisää ostajan neuvotteluvoimaa. Tämä näkyy jo erilaisina tarjouksina. Uusien asuntojen myyjät tarjoavat monilla alueilla esimerkiksi ostajan puolesta maksettuja yhtiövastikkeita asumisen alkuajalle. /nMyynti-ilmoituksista voi löytää myös ilmaisia muuttopalveluita, kaupan päälle tulevia autopaikkoja ja muita tarjouksia./nKiinteistömaailman välittäjien barometrissä Suomi on jaettu neljään osaan: Pääkaupunkiseutu, muu Uusimaa, isoimmat aluekeskukset ja muu Suomi./nSuurimmat epätasapainot ovat ilmaantuneet uusien asuntojen kauppaan./nUusissa asunnoissa eniten ylitarjontaa on pienissä kerrostaloasunnoissa isoissa aluekeskuksissa, joita ovat Tampere, Turku, Oulu, Lahti, Jyväskylä, Kuopio, Seinäjoki, Vaasa ja Hämeenlinna./nEsimerkiksi Oulussa on myynnissä reilusti yli 1 300 uudiskohdetta. Vuonna 2018 tai sitä aiemminkin valmistuneita uusia asuntoja on Oikotie- ja Etuovi-palveluissa myynnissä vielä yli 150 kappaletta pelkästään Oulussa./nAstetta pienemmistä kaupungeista Kuopiossa on myynnissä yli 800 uudiskohdetta ja Jyväskylässä yli 700 uudiskohdetta./nMyymättömiä asuntoja on Kiinteistömaailman mukaan myynnissä paljon pääkaupunkiseudun ulkopuolisella Uudellamaalla./nPääkaupunkiseudulla vastaavaa ylitarjontaa ei barometrin mukaan ole. Tosin paikoin myymättömiä uusia asuntoja voi olla tarjolla paljonkin, kuten HS on kertonut esimerkiksi Vantaan Kivistön osalta käyneen./nKiinteistömaailman toimitusjohtaja Risto Kyhälä uskoo, että pääkaupunkiseudulla ylitarjonta purkautuu itsestään ilman alennusmyyntejä, koska alueen asuntoihin kohdistuu niin kova kysyntä.'Uudiskohteissa on ylitarjontaa, mutta pääkaupunkiseudun vetovoima on niin suuri, että se tulee lisäämään kauppamääriä', Kyhälä uskoo.Asuntomarkkinoilla on revennyt isoja eroja siinä, miten erilaiset asunnot eri puolilla Suomea käyvät nyt kaupaksi. Kiinteistömaailman kiinteistönvälittäjäbarometrin mukaan asuntomarkkina porskuttaa pääosassa Suomea hyvin talouden ikävistä signaaleista huolimatta. Myös OP:n asuntomarkkinakatsauksen mukaan asuntokauppa piristyi keväällä ja kesällä. Silti kauppa käy yhä hiljaisempana kuin 2010-luvun alkupuolella. /nMarkkinoille on ilmestynyt kuitenkin paljon alueita, joilla myytäviä asuntoja on ostajia enemmän. Ylitarjonta on keskittynyt erityisesti pieniin, uusiin asuntoihin tietyillä alueilla. Syynä on se, että pieniä asuntoja on rakennettu tänä ja viime vuonna valtavia määriä erityisesti sijoittajamarkkinoille, mutta tänä vuonna sijoittajien kiinnostus ostoihin on laimentunut./nYlitarjonta luo etenkin pitkittyessään 'ostajan markkinat' eli lisää ostajan neuvotteluvoimaa. Tämä näkyy jo erilaisina tarjouksina. Uusien asuntojen myyjät tarjoavat monilla alueilla esimerkiksi ostajan puolesta maksettuja yhtiövastikkeita asumisen alkuajalle. /nMyynti-ilmoituksista voi löytää myös ilmaisia muuttopalveluita, kaupan päälle tulevia autopaikkoja ja muita tarjouksia./nKiinteistömaailman välittäjien barometrissä Suomi on jaettu neljään osaan: Pääkaupunkiseutu, muu Uusimaa, isoimmat aluekeskukset ja muu Suomi./nSuurimmat epätasapainot ovat ilmaantuneet uusien asuntojen kauppaan./nUusissa asunnoissa eniten ylitarjontaa on pienissä kerrostaloasunnoissa isoissa aluekeskuksissa, joita ovat Tampere, Turku, Oulu, Lahti, Jyväskylä, Kuopio, Seinäjoki, Vaasa ja Hämeenlinna./nEsimerkiksi Oulussa on myynnissä reilusti yli 1 300 uudiskohdetta. Vuonna 2018 tai sitä aiemminkin valmistuneita uusia asuntoja on Oikotie- ja Etuovi-palveluissa myynnissä vielä yli 150 kappaletta pelkästään Oulussa./nAstetta pienemmistä kaupungeista Kuopiossa on myynnissä yli 800 uudiskohdetta ja Jyväskylässä yli 700 uudiskohdetta./nMyymättömiä asuntoja on Kiinteistömaailman mukaan myynnissä paljon pääkaupunkiseudun ulkopuolisella Uudellamaalla./nPääkaupunkiseudulla vastaavaa ylitarjontaa ei barometrin mukaan ole. Tosin paikoin myymättömiä uusia asuntoja voi olla tarjolla paljonkin, kuten HS on kertonut esimerkiksi Vantaan Kivistön osalta käyneen./nKiinteistömaailman toimitusjohtaja Risto Kyhälä uskoo, että pääkaupunkiseudulla ylitarjonta purkautuu itsestään ilman alennusmyyntejä, koska alueen asuntoihin kohdistuu niin kova kysyntä.'Uudiskohteissa on ylitarjontaa, mutta pääkaupunkiseudun vetovoima on niin suuri, että se tulee lisäämään kauppamääriä', Kyhälä uskoo.Asuntomarkkinoilla on revennyt isoja eroja siinä, miten erilaiset asunnot eri puolilla Suomea käyvät nyt kaupaksi. Kiinteistömaailman kiinteistönvälittäjäbarometrin mukaan asuntomarkkina porskuttaa pääosassa Suomea hyvin talouden ikävistä signaaleista huolimatta. Myös OP:n asuntomarkkinakatsauksen mukaan asuntokauppa piristyi keväällä ja kesällä. Silti kauppa käy yhä hiljaisempana kuin 2010-luvun alkupuolella. /nMarkkinoille on ilmestynyt kuitenkin paljon alueita, joilla myytäviä asuntoja on ostajia enemmän. Ylitarjonta on keskittynyt erityisesti pieniin, uusiin asuntoihin tietyillä alueilla. Syynä on se, että pieniä asuntoja on rakennettu tänä ja viime vuonna valtavia määriä erityisesti sijoittajamarkkinoille, mutta tänä vuonna sijoittajien kiinnostus ostoihin on laimentunut./nYlitarjonta luo etenkin pitkittyessään 'ostajan markkinat' eli lisää ostajan neuvotteluvoimaa. Tämä näkyy jo erilaisina tarjouksina. Uusien asuntojen myyjät tarjoavat monilla alueilla esimerkiksi ostajan puolesta maksettuja yhtiövastikkeita asumisen alkuajalle. /nMyynti-ilmoituksista voi löytää myös ilmaisia muuttopalveluita, kaupan päälle tulevia autopaikkoja ja muita tarjouksia./nKiinteistömaailman välittäjien barometrissä Suomi on jaettu neljään osaan: Pääkaupunkiseutu, muu Uusimaa, isoimmat aluekeskukset ja muu Suomi./nSuurimmat epätasapainot ovat ilmaantuneet uusien asuntojen kauppaan./nUusissa asunnoissa eniten ylitarjontaa on pienissä kerrostaloasunnoissa isoissa aluekeskuksissa, joita ovat Tampere, Turku, Oulu, Lahti, Jyväskylä, Kuopio, Seinäjoki, Vaasa ja Hämeenlinna./nEsimerkiksi Oulussa on myynnissä reilusti yli 1 300 uudiskohdetta. Vuonna 2018 tai sitä aiemminkin valmistuneita uusia asuntoja on Oikotie- ja Etuovi-palveluissa myynnissä vielä yli 150 kappaletta pelkästään Oulussa./nAstetta pienemmistä kaupungeista Kuopiossa on myynnissä yli 800 uudiskohdetta ja Jyväskylässä yli 700 uudiskohdetta./nMyymättömiä asuntoja on Kiinteistömaailman mukaan myynnissä paljon pääkaupunkiseudun ulkopuolisella Uudellamaalla./nPääkaupunkiseudulla vastaavaa ylitarjontaa ei barometrin mukaan ole. Tosin paikoin myymättömiä uusia asuntoja voi olla tarjolla paljonkin, kuten HS on kertonut esimerkiksi Vantaan Kivistön osalta käyneen./nKiinteistömaailman toimitusjohtaja Risto Kyhälä uskoo, että pääkaupunkiseudulla ylitarjonta purkautuu itsestään ilman alennusmyyntejä, koska alueen asuntoihin kohdistuu niin kova kysyntä.'Uudiskohteissa on ylitarjontaa, mutta pääkaupunkiseudun vetovoima on niin suuri, että se tulee lisäämään kauppamääriä', Kyhälä uskoo."
toSend = str("A" * 10000)
#raise ValueError(toSend)
check = len(toSend)
lenC= len("%i" % check)
check = check + lenC + 1 #lisätään +1 (huutomerkki)
#print(lenC)
toSend =  str(check) + "!" + toSend
#raise ValueError(toSend)
print(f"sending message of {check} characters to server")
s.sendall(bytes(toSend, "utf-8"))
ack = int(str(s.recv(1024), "utf-8"))
#raise ValueError(ack)
#str(client.recv(1024), "utf-8")
print(f'received acknowledgment message {ack} from server')
status = 0
if ack == check:
    status = 1
    print(f'Ack message {ack}. Message was received succesfully')
#else:
#    while ack != check:
#        status = 0
#        print(f'Ack message {ack}. Message was not received succesfully')
#        #s.send(bytes(toSend[ack:], "utf-8"))
#        ack = int(str(s.recv(1024), "utf-8"))
#        if ack == check:
#            status = 1
#            print(f'Ack message {ack}. Message was received succesfully')
#            break
    
print()
s.close()