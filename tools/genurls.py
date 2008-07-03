#!/usr/bin/python
# -*- encoding: utf-8 -*-
# containsvfrom the eff-bot archives:
# extract anchors from an HTML document
# fredrik lundh, may 1999
# fredrik@pythonware.com
# http://www.pythonware.com

import htmllib
import formatter
import string
import urllib, urlparse
import httplib
import re
import signal
import time, random
import socket
import threading

import httplib2

MAXLEVEL = 2
MAXTHREADS = 10
STARTTIME = time.time()
urlcount = 0

searchterms = """
HUDORA
Hudora
hudora
hondora
hodora
hondura

02191 609120
02191-60912-0
02191 60912-0
02191 60912 0
2191 60912 0
2191 60912
+49 (0) 21 91/6 09 12-50
+49 (0) 21 91/6 09 12-0

02363-9156-10
02363-9156-0
02363 9156-10
02363 9156-0
02363 9156 10
02363 9156 0
2363 9156

02763-9156-0
02763-9156-10
02763 9156-0
02763 9156-10
02763 9156 0
02763 9156 10
02763 9156
2763 9156
(49) 2763 - 9156 - 10
(49) 2763 - 9156 - 0
(49) 2763 9156 10
(49) 2763 9156 0

0700 HUDORA 4U 
0700/483672-48

Inlineskate RX-23
Tischtennis Set
Tischtennis Tasche
Tischtennis-Set Allround
Tischtennis-Set New Contest
Tischtennis-Set Smash XL
Tischtennisbälle farbig
Tischtennisbälle
Tischtennisnetz
Tischtennisschläger Junior  
Tischtennisschläger New Topmaster
Tischtennisschläger Smash 
Tischtennisset Match
Tischtennisset New Contest
Tischtennistasche
Topfstelzen STATS
Topmaster
Tischtennisschläger
Tor Komplett-Set
Tor Komplettset
Tor mit Reboundset
Torkomplettset Triple Kick
Torwand mit Heringen
Torwarthandschuhe
Torwarthandschuhe Crystal
Torwarthandschuhe Magnum
Torwarthandschuhe Victory
Touring Nordic Walking Set
Tragegurt für Hudora Big Wheel 
HUDORA Big Wheel
Hudora Big Wheel
Trainer Fußballtor mit Torwand
Trainingsbank 
Crane Sports
HY SPORTS
Trampolinfuß
Travel Fitness-Set
Travel Fitnessset
Trekker Rucksack
Trekking 1803 Teleskop Stöcke
Trekking/Tourenstöcke
HY TREK
Trekking/Tourenstöcke HY TREK
Trekkingstöcke Norma
Trekkingstöcke
Triathlonmaske Hawaii
Triple Kick Fußballtor
Triple Kick
Fußballtor
Trommelbremse für Roller Bold Buddy
Turf 2006 Fußballschuh
Turf Fußballschuhe
Turf Fußballschuhe mit Gumminocken
Twist Ball 2 teilig.Stahlgestänge
Twist Lateral Stepper
Twist Lateralstepper mit Expandern SR 3.0
Twistballset
Türreck Pull-Fit
Pull-Fit
Ultra Carbon NW Stock
HUDORA Walk
Ultra NW Stöcke, 100% Carbon
Ultra NW Stöcke
Up Stepper
VIVA Fußballtor
Velcro Dart STATS
Verleihschlittschuh Hudora PRO
Hudora PRO
X-Kids
Inline Skate X-Kids
Verstellbarer Inline Skate X-Kids
Verstellbarer Inline Skate joey
Verstellbarer Inline Skate
Verstellbarer Inliner MIC-168
Verstellbarer Inlineskate HD-99
Verstellbarer Schlittschuh HD-087
Verstellbarer Schlittschuh joey
Verstellbarer Schlittschuh
Vinyl-Minihanteln
Vinylhantel
Vinylhanteln
Vinylhantelset
Vinylhantelset im Koffer
Viper
Visionline AirVent
Visionline Atmo
Visionline
Visionline, Softboot
Visionline,Softboot
Viva Sport Fußballtor
Viva Sport Torwand
Torwand
Choppa
Choppa Streetmonster
Power Trike
Walker Aluminiumstelzen
Aluminiumstelzen
Wassernudel
Skateboard Design Fireball
Whirl Heimtrainer
Work Out Display
Wurfscheibe
XCIT Verstellbarer Soft Inlineskate
XCIT Skateboard
XCIT
Yokari
joey Aluminiumstelzen 
joey Boccia Set 
joey Fahrradanhänger
joey Fahrradhelm für Kinder
joey Fun
joey Fun Set
joey I
joey Ice-Set
joey Iceskate
joey Kinder Schnorchel Set
joey Kinder Schwimmbrille
joey Kinderball, Gr. 4
joey Kinderboxset
joey Kinderhüpfball
joey Protektorenset
joey Sicherheits-Set mit Helm
joey Soft
joey Soft I
joey Soft II
joey Soft III
joey Soft
joey Softtennis Set
joey Topfstelzen
joey's Skate Set
joey-Kindertrampolin
joey’s Skate Set
joey’s Trampolin
The Skate Factory
Icesoftskate
Joey
HUDORA Joey ABEC1
Joey Soft II
Hyskate JuniorXTEND Kidz
Hyskate JuniorXTEND
Hyskate JuniorXTEND Teenz
Senior Eis-/Streethockeystock
Schienbeinschoner
Shape Fit
Shape Fit Bauchtrainer
Shape Fit Bauchtrainer mit Kopfstütze
Shape-Fit Bauchmuskeltrainer
Shinguards
Shuttle Tennisschläger
Sicherheits-Kinderweste dreieckig
Sicherheits-LED-Bänder
Sicherheits-Trampolin joey Jump in
Sicherheits-Trampolin
joey Jump in
Sicherheitsarmbänder
Sicherheitsnetz
Skate-Guard-Set
Skateboard Set mit Skateboard Wheels
Skateboard TOP SKATE
Skateboard Watch it!
Skateboard White Dragon
Skateboard double kick
Skateboard mit Rucksack
Skateboard-Ersatzrollen
Skateboarddisplay
Skateboarder Helm
Skateboarderhelm
Skateboardrampe Outbreak
Skateboards
Skateboardset
Skaterhelm
Skateroller
Hantelbank
Hanteln
Hantel
Skateroller Scooter
Ski Brille Größe
Skibrille
Skihelm Downhill
Slam it Basketball Set
Smash Tischtennisschläger
Smash Volleyball/Badminton
Sno Speedster
SnoWoody
Soccer Fun
Soccer Kicker
Soccerball "FINAL" STATS
Soccerball FINAL STATS
Soccerball GOAL
Soccerball "GOAL"
STATS
Soccerball PRO
Soccerball COPA
Soft Touch Beachvolleyball
Soft-Touch-Beachvolleyball
Softboomerang -
Softboot
Softboot Resolution
Softboot SF- Slicks Hornet
Softboot SF- Slicks II
Softboot m. Alu Chassis Gr. 38, F 2006
Softboot mit Alu-Chassis
Softdartscheibe Liverpool
Softiceskate Lady
Softiceskate Spirit
Softiceskate
Softskate
K-Line
Softspitze
Softtennis
Softtennis Set
Speed Ball Ständer
Speed, Naturfederbälle
Speedline
Spielerhandschuhe
Spin Heimtrainer
Spin Tischtennisschläger
Spirit II
Semisoft Schlittschuh in Tasche
Spirit II Semisoft Schlittschuh in Tasche
Spirit Iceskate
Spirit Woman
Sportartikel Display
Sportdisplay  
Sports Balls Miniature
Sprig II
Sprig III
Hartschalen Inlineskate
Springseil + Gummitwist -
Springseil Holzgriff
Springseil Natur
Springseil mit Digitalanzeige
Springseil mit Holzgriff
Springseil mit Holzgriffen
Springseil mit Holzkugelgriffen
Springseil mit Softgriff
Springseil mit Softgriffen
Springseil mit Zählwerk
Springseil ohne Griff
Springseil
Sprungmatte
Sprungtuch
Squashbälle
Stadion Tor-Set
Star Badmintonschläger
Straßenrollschuh
Stopper 
joey I
Stopperhalter
Storm Squashschläger
Street Hockey Set Powerplay
Street King MC 205 Wheelworx
Street Minibadmintonset
Street-Hockey-Set
Streetboard Nimbus
Streetboy BC 125
Streetgirl GC 125
Streethockey Set
Streethockey Set Face Off
Streethockey Set Junior
Streethockey Tor
Streethockeyset Junior
Streethockeystock
Strike Fußballtor-Set
Fußballtor
Super Soft Dart
Surf Board
Surfboard Shark
Surfboard
Survivor
Swing Elliptical Trainer
TOP SKATE Skateboard
Tanzband Rainbow 
Tauchmaske Atlantic
Tauchmaske joey Seal
Tauchmaske 
Tauchringe Softgrip
Tauchringe
Tauchset
Tauchset Sea Hunter
Tauchset joey Aqua
Tauchset joey 
Tauchset joey Aqua Mission
Tauchstäbe
Tauchstäbe Softgrip
Tauchstäbe joey Dive Sticks
Tauziehseil für Kinder Hau Ruck
Tauziehseil
Team-Walker
Team Badminton Set
Teleskop Trekking Stöcke
Teleskop Wanderstock Tirol
Teleskop-Kinderstöcke joey
Teleskop-Kinderstöcke
Tellerschaukel
Tennis Trainer
Tennisbälle
Tennisschläger Attack
Tennisset Junior 
Tennistrainer
Semisoft Iceskate
Speed 55
Semisoft Iceskate Speed 55
Semisoft Iceskate
Speed 66
Semisoft Iceskate Speed 66
Semisoft Iceskate
Spirit 66
Semisoft Iceskate Spirit 66
Semisoft Inliner
Element XF II
Semisoft Inliner Element XF II
Semisoft Inlineskate
HD-11.06
Semisoft Inlineskate HD-11.06
Semisoft Inlineskate
HD-33.06
Semisoft Inlineskate HD-33.06
Semisoft Inlineskate
HD-66.06
Semisoft Inlineskate HD-66.06
Semisoft Inlineskate
RX-23
Semisoft Inlineskate RX-23
Semisoft
Kinderinliner
joey Soft III
Semisoft Kinderinliner joey Soft III
Semisoft
Ladyskate
Spirit Woman
Semisoft Ladyskate
Spirit Woman
Semisoft Ladyskate Spirit Woman
Semisoft Power II
Semisoft Power OU
Semisoft Schlittschuh joey II
Semisoft-Iceskate Spirit 66
Semisoftboot Element XF
Semisoftboot ElementXF
Semisoftboot Lady Flow
Semisoftboot Lady XF
Semisoftboot Performance TS1
Semisoftboot
Semisoftboot Resolution XF I
Semisoftschlittschuh joey II, Gr. 28 - 30
RX-06
RX-23 ohne Ersatzstopper
Ratzfratz
Rebound Fußballtor
Reflektorenset für Erwachsene
Reflektorenset für Kinder
Regenabdeckung für Trampoline
Resolution XF 2
Riesen Trampolin
Rollenset
Roller Benji 
Roller Joey
Roller Speedy
Roller Stuntboy
Roller Wizard 
Roller Wizard Luftbereift Bremse vorne und hinten
Roller joey
Rollschuh 801
Rollschuh 901
Rollschuh Cargo
Rollschuh Girlie
Rollschuh Modell 1001
Rollschuh Modell 3001
Rollschuh Modell 901
Rotor Spin Twistball
Rubbertwist STATS
Rucksack Allround
Rucksack Excursion
Rucksack Go Wheeling
Rucksack
Rucksack Trekker
Rudergerät RW 1
Rückenprotektor
STATS Basketball
SX 4100
SX 582
SX-4100
SX-582
Sandsack Ball
Sauseschritt
Sauseschritt Laufradaus Birke
Sauseschritt Laufradaus Holz
Schaukel
Schaukel-Turngarnitur 
Schaumstoffgriff
Schaumstoffgriffe
Schienbeinschoner Junior
Schienbeinschoner Senior
Schienbeinschoner sortiert
Schienbeinschützer
Schienbeinschützer Fusion
Schienbeinschützer Pro
Schienbeinschützer Swift
Schienbeinschützer
Victory
Schienbeinschützer Victory
Schlittschuh
Hysports
Schlittschuh
Topskate
Schlittschuh
Schlittschuhe für Erwachsene
Schlittschuhhandschuh Sortiment aus Fleece
Schlittschuhhandschuhe
Schlittschuhhandschuhe aus Fleece
Schneeteller
Schnellspanner
Schnellspannhebel
Schnellverschluss

Schnorchel Airway
Schnorchelset Discovery
Schutzausrüstung für Kids im Rucksack

Schwimmboard joey Glide
Schwimmbrille Mirror, Silikon
Schwimmbrille New Freestyle
Schwimmbrille Ocean
Schwimmbrille joey Sea Monsters
Schwimmbrille joey
Sea Monsters
Schwimmbrille joey 
Sea Star
Schwimmbrille joey Sili
Silikon
Schwimmgürtel joey Swim Up
Schwimmgürtel joey
Swim Up
Schwimmset joey Diver
Schwungseil
Schwungseil mit Softgriff
Schwungtuch mit 8 Griffen

Scooter Bremse -
Scooter Hornet 120
Scooter Hornet 120 2.0
Scooter Hornet 120-Flash
Scooter Hornet 144
Scooter Hornet 205
Scooter Hornet
Scooter Tasche
Scooter Viva 
Scooter X-Slide 120
Scooter X-Slide
Scooter
X-Slide
Scooter X-Slide 144
Xpulse
Scooter XCIT
Aluscooter
STIWA GUT
Scooter mit 120 mm Rollen
Scooter mit Luftbereifung
Scootergriffbeleuchtungen (2) auf Blisterkarte
Scootertasche 
Score More
Score More faltbares Tor mit Torwand Stats
Score More faltbares Tor
Score More faltbares Tor mit Torwand 
Stats
Score More faltbares Tor mit Torwand
Semi - Softboot
Semi-Softboot
Semisoft
Blue Rocket
Semisoft Blue Rocket Hornet
Semisoft Blue
Rocket Hornet
Hornet
Miniflaggenball
"Cup" Weltmeisterschafts-Set
Fußballset
Lateral Stepper
Ersatzrolle HUDORA Big Wheel
Ersatzrolle
Ersatzstopper
Expander für Double Stepper
Inliner-Stopperhalter
Schraubenschutzkappe für Laufrad Ratz Fratz
Stopper
Stopper
Inliner
Rollschuh 901
Rollschuh 3001
Rollschuh 1001
Bremsklötze
Gewichtsmanschetten
Schneeteller
Schnellspannhebel
HY SKORE
ABEC
Kugellager
Action-Skateboard
Aerobic Step
Aerobic Stepper
Air Punch Boxsack
Air Punch
Anna
Kunstlaufkomplet
Kunstlaufschnürschuh
Aqua Beach Set
Aqua Kit
Aqua Safe
Artikel Divers
Asphalt Pads
Attack Fußball
Attack Jugend-Fußball
Aufblasbares Fußballfeld Arena
Aufblasbares Fußballtorset
BLU Dunk It!
Babyhochschaukel
Babyschaukel
Babyschaukel joey Boogy
Babyschaukel joey Twistie
Babyschaukel mit Fußstützen
Badeset
Badminton Set 
Badminton-Set Team
Badmintonbälle Training
Badmintonschläger Crusader RX-8
Badmintonschläger Hawk RX-3
Badmintonschläger Viper RX-5
Badmintonset Champion RS-88
Badmintonset Fly High RS-11
Badmintonset Fly High
Badmintonset Fun
Badmintonset Generation
Badmintonset No Limit RS-99
Badmintonset Street
Badmintonset Team RQ-44
Badmintonset Team
Balancer Einrad
Ball Champ
Ball Ersatznadel Set
Ballpumpe 
Ballsortiment
Ballständer
Bandagen
Baseball
Baseballglove
Baseballhandschuh
Baseballschlägerset
Baseballset für Kinder
Basketb-Korb Set
Basketball Gr. 3
Basketball Gr. 5
Basketball Gr. 7
Basketball Größe 3
Basketball, Gr. 3
Basketball, Gr. 3 - 7
Basketball, Gr. 5
Basketball, Gr. 7
Basketball, Größe 3
Basketball, Größe 5
Basketball, Größe 7
Basketball-Korb Set Junior
Basketball-Korb Set Profi
Basketballkorbset
Basketballnetz groß
Basketballnetz klein
Basketballspiel
Basketballständer All Stars
Basketballständer Chicago
Basketballständer Giant XXL
Basketballständer One on One
Basketballständer, Kinder Outdoor Set
Basketballständerset
Bauchmuskel-Trainer TPR-Tube (540x13mm(3mm)
Bauchmuskeltrainer
Bauchmuskeltrainer Shape-Fit
Bauchmuskeltrainer Shape-Fit Lady
Bauchtrainer Shape Fit
Beach
Beach Fußball Set
Beach Volleyball
Beach ball set
Beach-/Klettballspiel
Beach-Fußball-Set
Beach-Set
Beach-Volleyball
Beach/Klettballspiel
Beachball Ersatzbälle
Beachball-Set
Beachballset
Beachset
Beachsoccerball
Beachvolleyball
Beachvolleyball Hero 
Beachvolleyball Mega
Beachwurfball
Beachwurfringe
Becken Bandage
Beckengurt Athlet
Beckengurt Trail 
Bein- Oberarmtrainer 
Benji Roller
Bike Fit Heimtrainer
Gelenkschoner für Kinder
Gelenkschoner
Biomechanischer Handgelenkschoner Kinder
Handgelenkschoner Kinder
Biomechanischer Handgelenkschoner Mesh
Handgelenkschoner
Biomechanische Handgelenkschoner Mesh
Biomechanische Knie/Ellbogenschoner Mesh
Biomechanische Protectoren Kinder-Set
Biomechanische Protektoren
Biomechanisches Protektorenset 
crane Sports
Black-Jack
Blue Chip
Boccia
Tricycle
Boccia Set
Boccia Spiel
Body Board
Body Board Delfin Junior
Body Board Wave
Body Board
Bodyboard
Bodytrimmer mit Softgriff
Bodytrimmer
Boing-Ball Spiel
Boing-Ball
Boingballspiel
Bold Buddy
Bold Buddy´s
Boomerang -
Boule Set
Bouleset
Bouncing Ball -
Box Set
Box-Handschuhe STATS
Box-Handschuhe
Handschuhe
Boxbirne
Boxsack
Bremsbacken
Brettschaukel joey Bounty
Schaukel
Schaukelpferd
Bristle Dartscheibe
VIVA Sport
CHOPPA Ralley rot
Cargo Rollschuhe
Cargo, Semisoft
Challenger Badmintonset
Champ Ball
Champ Fußball
Champion Badmintonset
Champion Kicker
Skateboard Bone
Choppa Street Monster
Chrom Hantel Set
Chromhantel Set
Chromhantel-Set
Chromhantelset
Classic Torwarthandschuhe
Torwarthandschuhe
Comfort Plus
Innensohle
Complete Tischtennisschlägerset
Composite Nordic Walking Set
Contest Tischtennisset
Cool Kick
Cool-Bike
Cool-Scooter
Cool-Trike
Copa Fußball
Crane Sports
Trampoline Exercise
Crocket Set
Crooked
Cross Fit Elliptical Trainer
Cross Fit
Elliptical Trainer
Crosstrainer CR 1
Crosstrainer
Xpulse
Crosstrainer Cross 201 Xpulse
Crosstrainer XP-Ergo
Cruiser Streetboy
Cruiser Streetgirl
Crusader
Cruiser
Crystal 2.0 Torwarthandschuhe
Crystal Torwarthandschuhe
Cup Weltmeisterschafts-Set
Cup Tischtennisschläger
Cup-Fußball Set
Cyberline Air-Vent
Cyberline
AirVent
Cyberline Atmo
Cyberline
Atmo
Inlineskate
Cyberline
Softboot
Cyberline, Softboot
Cyberspeed Fahrradhelm
Cyberspeed
Fahrradhelm
Dance'N Role, Rollerboot
Kunststoffchassis
Dance'N Role
Rollerboot
Dart Board
Dartboard
Dartscheibe York 
Defender
Defender, Hartshale
Hartshale
Deutschland Fußballtor
Digitales Springseil
Double Goal
Double Goal Tor-Set
Double Stepper
Double Stepper
Downhill Skihelm
Downhill
Skihelm
Drei Tennisbälle
Dubble4's
Rollerskate
Dumbell Set
Eagle Badmintonschläger
Easy Role
dubble*4
Rollerboot
Easy Role
dubble*4 Rollerboot
Easy Role dubble*4 Rollerboot
Rollerboot, Design 56
Rollerboot Design 56
Rollerboot
Design 56
Easyline
Easyline II
Easyline Softboot Inliner
Edeka
Badminton Set No Limit
Badminton Set
No Limit
Eierlauf-Set
Einrad Balancer B20
Einrad Balancer
Einrad Balancer P16
Einrad Balancer R16
Einrad Balancer
laser rot
Einrad
Balancer
Eiskomplet HUDORA Luzzy
Eiskomplet
HUDORA Luzzy
Eiskunstlaufkomplet Dancing
Eiskunstlaufkomplet
Dancing
Eiskunstlaufkomplet Katja
Eiskunstlaufkomplet
Katja
Eiskunstlaufkomplet Princess
Eiskunstlaufkomplet
Princess
Elektronik Dartscheibe Holzschrank
Elektronik Dartscheibe Schrank
Elektronik Dartscheibe Sherwood
Elektronik Dartscheibe
Elektronische Dartscheibe
Elektronische Dartscheibe LCD 200
Elektronische Dartscheibe Lancester LC2
Elektronische Dartscheibe Leeds LE1
Elektronische Dartscheibe London LE3
Dartscheibe
Elektronische Mini-Dartscheibe
Elektronische
Mini-Dartscheibe
Ellenbogen-Bandage
Elliptical Trainer SR 2.0
Schwungrad
Ergo-Crosstrainer CR 3
Ergo-Crosstrainer CR 5
Ergo-Crosstrainer 
Ergometer EG 3
Ergometer EG 5
Benji Roller
Fahrradcomputer
Fahrradhelm Flash ST
Fahrradhelm
Flash ST
Fahrradhelm Hurricane
Fahrradhelm
Hurricane
Speedy
Fairline
Fairline verstellbarer Inlineskate
Faltbares Fußballtor Fold up
Fold up
Family, Tischtennisset
TT Schläger
Fan 2006
Torwand
Fangzaun
Riesen-Trampolin
Federballset Travel
Federballset
Federballspiel
Fish-Bone
Fitness Accessories
Fitness Bänder
CraneSports
Fitness Chrome Dumbbell Set
Fitness Rope
Fitness Rope/Band
Fitness Set
Fitness Skipping Ropes
Fitness Springseil
Fitness Tube Set
Fitness Tube
Fitness-Expander-Set
Fitness-Expanderset
Fitness-Rope
Fitness-Set
Fitnessband
Fitnessbänder
Fitnessbänder Set
Fitnessbänder-Set
Fitnessset
Fitnessset Travel
Fitnessspringseil
Fitnessspringseile
Fitschi Schnorchel-Set mit Flossen
Fitschi Schnorchel-Set
Fitschi
Schnorchel-Set
Flossen
Five Star Skateboard-Set
Fly High Badmintonset
Fly High
Fold Up Fußballtor
Freestyle Schwimmbrille
Schwimmbrille
Freeze Alu Skateboard
Fun Minibadmintonset
Schläger
Fusion Schienbeinschoner
Fussball Pro
Fußball Attack
Fußball Copa
Scooter
Fußball Copa
Fußball Diamond
Fußball Diamond Star 2007
Fußball Diamond Star
Fußball Europa
Fußball Optima
Fußball Pro 2.0
Fußball Pro
Fußball Pro, Optima
Fußball Supreme
Fußballset Tor
Fußballtor
Fußballtor High Score mit Torwand
Fußballtor High Score
Fußballtor Match
Fußballtor Metall
Fußballtor Rebound mit Rebound-Set
Fußballtor Rebound mit Reboundset
Fußballtor Rebound
Fußballtor Set
Fußballtor Trainer
Fußballtor XXL
Fußballtor mit Torwand Wilde Kerle
Fußballtor-Set XXL
Gartentrampolin
Gelenkschoner Hornet
Gelenkschoner
Gelenkschoner OU Graphite
Gelenkschoner OU
Geschicklichkeitsspiel Diabolo
Geschicklichkeitsspiel Junior Diabolo
Diabolo
Geschicklichkeitsspiel
Get Up, Federballset,2 Schläger TS Ohne Ösen im Netz 1 Fede
Get Up
Hantelset
Hartschalen Kinderinliner Joey Shape
Hartschalen Kinderinliner
Hartschalen
Kinderinliner
Joey Shape
Hawk
Heimtrainer
Bike SR 2.0,
Magnetbremse
Schwungrad
Heimtrainer EG 1
Heimtrainer HT 1
Heimtrainer HT 1
Trinkflasche
Heimtrainer XB
Magnetbremse
Schwungrad
Heimtrainer XP-200
Heimtrainer XP-226
Heimtrainer XP-Ergo 100
Heimtrainer XP-Ergo 1000
Heimtrainer
XP-200
Heimtrainer
XP-226
Heimtrainer
XP-Ergo 100
Heimtrainer
XP-Ergo 1000
Hero Beach-Volleyball
Hero
Beach-Volleyball
Herren Komplett Golf Set Greenfield GT
Herren Komplett Golf Set
Greenfield GT
High Score Fußballtor
High Score
Fußballtor
Torwand
152x213x76cm
High Speed Badmintonschläger
High Speed
Badmintonschläger
Kiddy Scooter
Hinterrad Choppa
Hinterrad für Power Trike
Hockey Goal Set STATS
Hockey Schlittschuh HD-77
Hockey Schlittschuh
HD-77
Schlittschuh
Hockey-Schläger
HD-216
Hockeystock Junior "K"
Hockeystock Junior
Hockeystock Senior
Holzboomerang -
Holzbrettschaukel
Holzbumerang
Holzbumerang 
Holzlaufrad "Easy Rider"
Holzlaufrad Cop
Holzlaufrad Sauseschritt, 12"
Holzlaufrad Sauseschritt
Holzlaufrad
Easy Rider
Holzlaufrad
Cop
Holzlaufrad
Sauseschritt
Holzlaufrad
Sauseschritt
Holzleiter
Holzleiter joey Tree-Top
joey Tree-Top
Hornet Protection Set
Hudora Big Wheel Bremse
Hudora Cheeky Chick
Hudora G-Force
Hudora HX-01, Hockeyskate Gr.36
Hudora
Big Wheel Bremse
Hudora
Cheeky Chick
Hudora
G-Force
Hudora
HX-01, Hockeyskate Gr.36
Hy Skate
Bio-DynamicProtection
Hy Skate
Skateboard
Ant Attack für Aldi Süd
Hunter
Original
Skater
Double kick
HyWalk NW Stöcke
HyWalk
Ice Skate Boy
Ice Skate Girl
Ice Skate
Ice-Skate-Set
Iceskate HD-23
Iceskate
HD-23
Indoor
Fußballschuh
Fußballschuhe für die Halle
Element XF II
Lady Flow I
Resolution XF2
Inline Skate
X-Skill
Inliner Performance
Inliner Rucksack -
Schutz-Set
Top Skate
HD-33.07
HD-88
RX-23 3.0
RX-23 M2.0
X.Skill
Inlineskate joey Soft
joey Soft
Inlineskater Schutz-Set
Inlineskater
Schutz-Set
Innensohle
Iron Buckles
JAKO-O
JOEY Teleskop Kinderstöcke
Joey Fun Set
Fun Set
Joey Go II
Joey Iceskate
Joey Kinder Wurfscheibe
Kinder Wurfscheibe
Joey Kinderklettball Dartboard
Joey Kinderklettball
Dartboard
Joey
Kinderklettball
Dartboard
Joey Lernflossen
Joey
Lernflossen
Joey Run II
Joey Skaterhelm
Skaterhelm
Joey Soft III
Air-Vent System
Air-Vent
Joey Soft III Gr.37 -39, Air-Vent System,blau
Joey's Sicherheitsset
Helm
Gewicht für Handgelenk
Gewichtsmanschetten
Giant Basketballständer
Gipsy Kinderhelm Design Signal
Gipsy Kinderhelm
Kinderhelm
Girlie Role
Girlie Rollschuhe
Girlie
Girls soccer set
Gitterschaukel
Gitterschaukel joey Swingie
joey Swingie
Gleiterhinterriemen 
Gleitschuhe
Glider 1 Stück
Glitzerspringseil
Goal-Fever Fußballtor mit Torwand
Goal-Fever
Goaly gloves
Goaly, Minitor Set
Goaly
Golf Juniorkomplettset Graphite
Golfschläger Damenkomplettset Graphite
Golfset Rooky
Golfschläger
Golf
Golftrolley Greenfield
Grashero
Grashero Fußballschuhe für Rasen 
Grashero Fußballschuhe
Großtrampolin
Gummibänderset latex
Gummitwist
Gym Band
Skipping Rope
Gymnastikball
Gymnastikbänder
Hy Sport
Gymnastikmatte
Gymnastikmatte process
Gymnastikmatten Set
HORNET Aerobic Stepper
HORNET
Aerobic Stepper
HORNET Air Walker
HORNET Liegestützgriffe
HORNET Schnallenschuh
BIG WHEEL
Big Wheel Scooter
Big Wheel XXL laserblau
Big Wheel XXL rot
Big Wheel XXL silber 
Big Wheel Air AW-125
Big Wheel BC 125
Big Wheel BC 144
Big Wheel Bremse
Big Wheel CC
Big Wheel Cargo grün
Big Wheel Colour Edition gelb
Big Wheel Colour Edition rot
Big Wheel Colour Edition rot
Big Wheel DC 125
Big Wheel DC 125, STIWA Gut
Big Wheel FC 125, 125 mm Rolle
Big Wheel FC 125
Big Wheel GC 125, 125 mm Rolle
Big Wheel GS 205, 205 mm Rolle
Big Wheel GC 125
Big Wheel GS 205
Big Wheel Gold Edition
Big Wheel KS3-125
Big Wheel Kick-It KG-125
Big Wheel Kick-It, KG-125
Big Wheel Laser Star gelb
Big Wheel MC 205
Big Wheel RC 125
Big Wheel RC 144
Big Wheel Spezial
Big Wheel XXL
Xpulse
Big Wheel XXL blau
Big Wheel XXL laserblau
Big Wheel XXL rot
Big Wheel XXL rot-laser
Big Wheel XXL silber
Big Wheel XXXL
Big Wheel Xpulse
Big Wheel blau
Big Wheel rot
Big Wheel rot-laser
Big Wheel silber
Big Wheel, blau
Aluscooter
Big Wheel, laserblau
Big Wheel, rot
Big Wheel, silber

HUDORA GLACIER
Softice-Skates
HUDORA Gleitschuh
HUDORA Gleitschuhe
HUDORA Hockey-Schläger
HUDORA
Hockey-Schläger
Hockey-Schläger,Junior
HUDORA Katalog

Knie/Ellbogenschoner
Ellbogenschoner
Knieschoner
Kombi-Laufschoner Größe
Laufschoner
Eishockeyskates

Handgelenkschutz
Schnürriemen
Schnürsenkel
Sno Glider
Sprig
Stopper Sprig
Stunt-Rolle
Ultimate Handgelenkschutz
Ultimate Knieschoner
joey verstellbarer Inline Skate
joey Inline Skate
HY SKATE for Kids
Hallenfußball Kick In
Hand-Federball
Handfederball
Handgelenk-Bandage
Handgelenkschoner
Handtrainer
Handtrainer mit Softgriff
Hantelbank, faltbar
Hantelbank

Joey, Rucksackset
Protektoren
Joey, Sicherheitsset
Sicherheitsset
Jonglier Set
JumpPooline
Aufblasbares Trampolin
Jumping rope
Jun. Inliner, KIDZ 1
Jun. Inliner
KIDZ 1
Jun. Inliner, TEENZ 1
Jun. Inliner
TEENZ 1
Junior Body Board
Junior Golfset Starter
Schienbeinschoner
Junior In-Line Skates
Junior In/Outdoor Basketball-Korb Set
Junior Inline Skates
Junior Skate Set
Junior Street HockeySet
Junior Street Hockey Set
Junior Tischtennisset
Junior, Kunststoff Eis-/Streethockeystock
Eis-/Streethockeystock
Junior, Tischtennisschläger-
Junior, Tischtennisset
Justierschrauben für Kicker
K-/Jugend-Schlittschuh
Katinka Eiskunstlauf-Komplet
Katinka
Kunstlaufkomplet
Weiss/Fell-Optik
Katja
Eiskunstlaufkomplet
Kick-Spaß Vinylfußball
Kicker Kick It
Kicker Silver Goal
Kicker Standard
Kicker Turnier-Design
Kicker World Cup
Kickertisch
Kiddy Scooter joey 
Kiddy Scooter
Kiddyscooter
joey 2.0
Kiddyscooter
joey Pinky
Kinder Angelset
Kinder Boxsack
Kinder Inline Skate Nico
Kinder 
Inline Skate Nico
Kinder
Inline Skate
Nico
SP-222XS
Inlinerset
Protectoren
Kinder Schlittschuh
Schlittschuh
Kinder Schlittschuhe
Schlittschuhe
Kinder Soft Iceskate
Soft Iceskate
Kinder-/Jugendschlittschuhe
Kinder-Rucksack joey Peak
Kinder-Rucksack joey Rock
Kinder-Rucksack 
joey Peak
Kinder-Rucksack 
joey Rock
Kinder-Schutzset
Helm und Protektoren
Kinderbox-Set Handschuhe und Punchsack
Kinderboxsack
Kinderboxset joey 
Kinderfahrrad
Kinderfahrradhelm Flames
Kinderfahrradhelm Monsun
Kinderinliner KIDZ Extend
Kinderinliner TEENZ Extend
Kinderinliner joey Fleur II
Kinderinliner joey Fleur
Kinderinliner
joey Fleur II
joey Fleur
joey Go
Kinderinliner joey Go
Kinderinliner joey Soft IV
joey Soft IV
Kinderklettball Dartboard STATS
Kinderpartyset
Kinderroller Rowdy 2.0
Kinderroller Rowdy
Rowdy
Kinderroller joey Bold Buddy
Kinderroller Bold Buddy
Bold Buddy
Kinderroller joey Rowdy
joey Rowdy
Kinderrollschuh 3001
3001
Kinderrollschuh 901
9001
Kinderschlittschuh IP-33XT
Kinderschlittschuh
IP-33XT
Kinderschlittschuh Joey Soft boy 3.0
Kinderschlittschuh Joey Soft boy
Joey Soft boy 3.0
Joey Soft boy
Kinderschlittschuh Joey Soft girl 3.0
Kinderschlittschuh Joey Soft girl
Kinderschlittschuh
Joey Soft girl
Kinderschlittschuh Nico
Nico
Kinderschlittschuh Orange Flame
Kinderschlittschuh
Orange Flame
Kinderschlittschuh Pink
Pink
Kinderschlittschuh joey II
Kinderschlittschuh
joey II
Kinderschlittschuh
joey Soft boy 3.0
joey Soft boy
Kindersicherheitsweste
Kinderskateboard
Klappmechanismus für Big Wheel
Klettball-Ersatzbälle
Klettballspiel
Klingel für Benji Roller
Klingel für Roller Rowdy
Klingel für Roller Stuntboy
Knie-Bandage, Größe L
Knie-Bandage, Größe M
Knie-Bandage, Größe S
Knie-Bandage
Knie/Ellbogenschoner
Hudora für KIDS
Knöchel-Bandage
Komet Wurfscheibe
Kopfleuchte
Kopfleuchte Shining Star
Shining Star
Krocketset für Kinder joey Hit
Krocketset für Kinder joey Strike
Krocketset für Kinder 
joey Hit
Krocketset für Kinder 
joey Strike
Kugellager ABEC 1
Kugellager ABEC 3
Kunstlaufschlittschuh
Kunststoffbrettschaukel
Kunststoffstepper Let's Step
Kunststoffstepper
Let's Step
Kurzhantel 10,3 kg
Kurzhantel
Lady Flow I
Lady Flow
Lady Skate XF 1, rosa
Lady Skate XF 1
XF 1
Lateral Stepper SR 2.0
Laufrad Bikey
Laufrad Cruiser 2.0
Laufrad Cruiser
Laufrad FlitzKidz
Laufrad RatzFratz 
Laufrad Ratzfratz 2.0 Princess
Laufrad Ratzfratz 2.0 lila/schwarz
Laufrad Ratzfratz 2.0 orange/schwarz
Laufrad Ratzfratz 2.0,
Laufrad Ratzfratz 2.0, 12' Luftreifen, 
Laufrad Ratzfratz Princess
Laufrad Ratzfratz lila/schwarz
Laufrad Ratzfratz orange/schwarz
Laufrad Ratzfratz 
Laufrad Ratzfratz 12' Luftreifen, 
V-Bremse
Laufrad Ratzfratz Pinkie 2.0
Laufrad Ratzfratz
Laufrad Streetboy
Laufrad Streetgirl
Laufrad joey Cruiser B2
Laufrad joey Cruiser B3
Laufrad joey Cruiser O1
Laufrad joey Cruiser
Liegestützen Push-Up-Bar
Push-Up-Bar
Liegestützgriffe 
Long Jumping Rope
Lotus Yoga Set
Magic Jump
Magic Jump 120 cm Ø
Magic Jump Trampolin faltbar
Manga
Manga Skateboard
Stakeboard Manga



tunturi.com
tunturi
accell-group.com
accell-group

Royalbeach Spiel- & Sportartikel Vertriebs GmbH
Watzmannstraße 1
83417 Kirchanschöring
mail@royalbeach.de
Royalbeach Spiel- & Sportartikel Vertriebs GmbH Verkaufsbüro West
Richard-Klinger-Straße 6
65510 Idstein,
at@royalbeach.de
Royalbeach AustriaRoyalbeach Austria Spiel- & Sportartikel Vertriebs GesmbH
is@royalbeach.de
royalbeach.de
Royalbeach International Ltd. Hong Kong
Office 1522, 15/F, Chinachem Golden Plaza
77, Mody Road, Tsim Sha Tsui
mail@royalbeach.com.hk
royalbeach.com.hk
Royalbeach Spiel- & Sportartikel Vertriebs GmbH
Watzmannstraße 1
83417 Kirchanschöring
0 86 85-98 89-0
0 86 85-98 89-88
@royalbeach.de
royalbeach.de
Ust-IdNr: DE 131 56 22 57
Hans-Jürgen Münch
www.royalbeach.de
mail@royalbeach.de
royalbeach GmbH
InnNet Michael Kellner
Internet-Services
Am Gerblanger 20
83512 Wasserburg/Inn
www.innnet.de
info@innnet.de
innnet.de

Bremshey Orbit Explorer Crosstrainer
Bremshey
www.royalbeach.de
www.royalbeach.at
BREMSHEY SPORT®
TUNTURI GmbH 
M. Nelissen 
R. Takens 
H. Sybesma 
Heidenfelder Str. 5 
97525 Schwebheim 
+49 9723 9345 0 
+49 9723 9345 19 
info@tunturi.de
tunturi.de
bremshey.de
Orbit Explorer
Crosstrainer
42897 Remscheid
57489 Drolshagen-Bleche
BigWheel
HUDORA BigWheel
Californian Products mbH
D-42897 Remscheid
D-57489 Drolshagen-Bleche
service@californian-products.de
californian-products.de
HUDORA GmbH
Jaegerwald 13
Jägerwald 13

LA Sports
LA sports bergisch gladbach
Prof. Rüsche Str. 10
STAMM Sport & Freizeit GmbH
Thomas Fentrop
Vertriebsgesellschaft Californian Products mbH
Vertriebsgesellschaft. Californian Products mbH
californian products
hudora.de
Eike Dornseif
Thomas Ludwig
Lothar Stamm
Maximillian Dornseif
hiskate.de
http://www.hudora.de/
http://www.californian-products.de/
hyskate.de
info@cphk.de
cphk.de
rollschuhe
stamm
stamm gummersbach
swingstick
www.KookaburraSpiel.com
www.cphk.de
+49 [0]2204 - 3046-0 
+49 [0]2204 - 3046-26 
info@la-sports.de
L.A. Sports GmbH & Co. KG
Siebenmorgen 13 - 15
Siebenmorgen 13-15
51427 Bergisch Gladbach
+49-2204-3046-0
+49-2204-3046-26
info@la-sports.de
la-sports.de
Body Sculpture Int’l USA Ltd.
19 Worlds Fair Drive
Somerset, NJ 08873
+1-732-357-1223
+1-732-563-6937
info@bodysculptureus.com
bodysculptureus.com
Cathasia S.A.S
9, rue Louis Rameau
30044-95870 Bezons CEDEX
+33-1-34344838
+33-1-34344847
pascaline@amco-sport.com
amco-sport.com
Body-Sculpture International LTD
11F, No. 149 Roosevelt Rd. Sec. 3
+886-2-2363-2222
+886-2-2362-8877
info@body--sculpture.com
body--sculpture.com
Solex Industries Inc.
7F, No. 149 Roosevelt Rd. Sec. 3
+886-2-2362-3232
+886-2-2362-8272
solex@solexsports.com.tw
solexsports.com.tw
Body Sculpture Int´l U.K. Ltd.
Morley Carr Road, Low Moor
BD12 ORW Bradford, U.K.
+44-1274-693888
+44-1274-693700
info@bodysculpture.co.uk
bodysculpture.co.uk
Body Sculpture Int’l China Ltd.
2F, No. 485 Gong Xiu Road
+86-571-8271-1558
+86-571-8271-6808
bodyxs@xs.hz.zj.cn
xs.hz.zj.cn
CP Twister Holzlaufrad
Holzlaufrad 
Laufrad
Twister Holzlaufrad
Aldi
Lidl
Plus

Panther Junior
UAB Baltik Vairas
Pramones 3
78138 Siauliai
+370 41 599202
+370 41 599209
sales@baltikvairas.lt
baltikvairas.lt
Internet: www.panther-junior.com
Vertretungsberechtigter Geschäftsführer: 
Dirk Zwick
LT 105 999 314
Dirk Zwick
ScoodoLine
Trixx

puky.de
PUKY GmbH & Co. KG 
Fortunastrasse 11 
D-42489 Wülfrath 
Postfach 14 60
Rolf Kuchenbecker
Ralf Puslat
HRA 19050
HRB 13612 
DE 189468331
PUKY GmbH & Co. KG 
Fortunastrasse 11 
42489 Wülfrath 
Postfach 14 60
+49 (0) 2058 773 0
info@puky.de
www.puky.de

Alu-Rad
Spiel + Kind
(757)427-0183
0131/826436
01527/62423
02938/2022
03/8442464
0388/473283
0493/310739
0662/620501-20
15053 Castelnuovo Scrivia
2627 Schelle
5, Rue du Château
5753 RJ Deurne
59469 Ense-Parsit
64-92 Pila
67/3512617
67133 Schirmeck Cédex
5020 Salzburg
Brandekensweg 9
contact@kettler.net
ERSRL@COMM2000.it
Fax 757-427-0183
Freizeitprodukte GmbH	
Dr. Karin Kettler
Ginzkeyplatz 10
HEINZ KETTLER
HEINZ KETTLER GmbH und Co. KG
Hauptstrasse 28
Hauptstraße 28
Heimstadt GmbH
Indumastraat 18
Info@kettlerusa.com
www.kettler.net
kettlern.net
KETTLER Austria GmbH
KETTLER Benelux B.V.
KETTLER GB Ltd.
KETTLER International Inc.
KETTLER S.R.L.
KETTLER S.a.r.l.
KETTLER mbH
KETTLER-Marken
KETTLER International , Inc.
1355 London Bridge Rd
Kettler 
Lutzelhouse
Merse Road
North Moons Moat
P.O. Box 2747
parts@kettlerusa.com
kettlerusa.com
757-427-2400 
Polska Sp. z.o.o.
Redditch, Worcestershire B 98 9 HL
HRB 4042
Rohrwerk Sönnern
Strada per Pontecurone 5
+49 2938 / 2022
+49 2938/810
Ul. Kossaka 110
DE 126631236
Virginia Beach, VA 23450 USA
Werk Hanweiler
Werk Kamen I
Werk Kamen II
Werk Mersch
Werk Sönnern I
Werk WKW
alu-rad@kettler.net
comm@kettler-france.fr
kettler-france.fr
(757)427-2400
0131/855848
01527/591901
02938/810
03/8886111
0388/475580
0493/310345
0662/620501-0
67/3512616
freizeitmoebel@kettler.net
info@kettler.be
kettler.be
info@kettler.nl
kettler.nl
info@kettlerusa.com	
kettler@pro.onet.pl
office@kettler.at
kettler.at
kettler.net
profiline@kettler.net
sales@kettler.co.uk
kettler.co.uk
service.sport@kettler.net
solarien@kettler.net
kettler.net
sonntex
sport@kettler.net
toys@kettler.net

http://www.uhlsport.de/
uhlsport.de
uhlsport.com
uhlsport GmbH
Klingenbachstrasse 3
72336 Balingen
+49 07433 268-0
+49 07433 268-194
DE 144851459
uhlsport GmbH
Klingenbachstrasse 3
72336 Balingen
Germany
+49 (07433) 268-0
+49 (07433) 268-194
info@uhlsport.com
www.uhlsport.com
Günter Daiss
Thomas Keppler
hrb 196
DE 144851459

http://www.vaude.de/
VAUDE Sport GmbH & Co. KG
Vaude Straße 2
88069 Tettnang
+49-(0)-7542-5306-0
+49-(0)-7542-5306-60
info@vaude.com
www.vaude.com
vaude.com
VAUDE Sport Verwaltungs-GmbH
HRB 631715
Gertrud Schmohl
Albrecht von Dewitz
HRA 631071
VAUDE Sport GmbH & Co. KG
HRB 631715
VAUDE Sport Verwaltungs-GmbH
DE 203894755
Stefanie Raaf

Otto Simon
Reusch
Crane Sports
Paffensport
K2
Fila
Rollerblade
Spielzeug
Sportartikel
Togu
Energetics

Hou-Sport
Unterortstr. 30
65760 Eschborn

+49-(0)6196-42-873
+49-(0)6196-42-872
hou-sport@t-online.de

"""
searchterms = [y.lower() for y in [x.strip() for x in searchterms.split('\n')] if y]

searchengines = [
'http://clusty.com/search?input-form=clusty-simple&v%3Asources=http://www.sportscheck.com/is-bin/INTERSHOP.enfinity/WFS/Sportscheck-SportscheckDe-Site/de_DE/-/EUR/SPM_BrowseCatalog-Start;sid=_PHZNufT-andNqEyfHHE9LKDsZ3e4tpMMVFC3iHH5VyeqkU8eXGtKZBqqnx8Tw==?CategoryName=sh13113514&Pfad=line&query=XXX',
'http://de.altavista.com/web/results?itag=ody&q=XXX&kgs=1&kls=0',
'http://de.search.yahoo.com/search?p=XXX&fr=yfp-t-501&ei=UTF-8&meta=vl%3D',
'http://de.vivisimo.com/search?input-form=simple-vivisimo-com&query=XXX&v%3Aproject=de-vivisimo-com&v%3Asources=Web&dlang=de&language=all&x=0&y=0',
'http://de.vivisimo.com/search?input-form=simple-vivisimo-com&query=XXXX&v%3Aproject=de-vivisimo-com&v%3Asources=Web&dlang=de&language=german&x=0&y=0',
'http://del.icio.us/search/?fr=del_icio_us&p=XXX&type=all',
'http://en.wikipedia.org/wiki/Special:Search?search=XXX&go=Go',
'http://meta.rrzn.uni-hannover.de/meta/cgi-bin/meta.ger1?start=1&eingabe=XXX&mm=and&maxtreffer=200&time=3&hitsPerServer=2&textmenge=2&wissRank=on&sprueche=on&QuickTips=beschleuniger&linkTest=no&check_time=3&dmoz=on&exalead=on&suchclip=on&wiki=on&harvest=on&witch=on&overture=on&fastbot=on&fportal=on&Nachrichten=on&Usenet=on&firstsfind=on&cpase=on&metarss=on&neomo=on&nebel=on&audioclipping=on',
'http://msxml.excite.com/info.xcite/search/web/XXX',
'http://preis.info/index.aspx?such=XXX&image2.x=0&image2.y=0',
'http://preisvergleich.getprice.de/jsp/partner/getprice2005/search.jsp?name=XXX&Submit=suchen&navCategoryID=&priceRangeFrom=&priceRangeTo=',
'http://produktsuche.web.de/search.do?s=XXX',
'http://sads.myspace.com//Modules/Search/Pages/Search.aspx?fuseaction=advancedFind.results&searchtarget=tms&searchtype=myspace&t=tms&get=1&websearch=1&searchBoxID=Profile&searchString=hudora&q=XXX',
'http://search-desc.ebay.de/XXX_W0QQfsooZ2QQfsopZ19QQftsZ2QQsalisZ77',
'http://search-desc.ebay.de/search/search.dll?sofocus=bs&sbrftog=1&from=R10&satitle=XXX&sacat=-1%26catref%3DC6&bs=Finden&fts=2&sargn=-1%26saslc%3D3&sadis=200&fpos=Postleitzahl&sabfmts=1&saobfmts=insif&ga10244=10425&ftrt=1&ftrv=1&saprclo=&saprchi=&salis=77&fhlc=1&fsop=1%26fsoo%3D1&coaction=compare&copagenum=1&coentrypage=search&fgtp=',
'http://search.abacho.com/de/abacho.de/index.cfm?q=XXX&country=de&x=0&y=0',
'http://search.ebay.de/search/search.dll?fsop=1&fsoo=1&from=R3&strKw=+&shortcut=4&siteid=77&satitle=XXX',
'http://search.lycos.com/?query=XXX&x=0&y=0',
'http://search.msn.com/results.aspx?q=XXX&FORM=MSNH',
'http://search.yahoo.com/search?ei=UTF-8&trackingType=go_search_home&p=XXX&fr=hsusgo1&sa.x=0&sa.y=0',
'http://search.yahoo.com/search?ei=UTF-8&trackingType=go_search_home&p=XXX&fr=hsusgo1',
'http://shopping.freenet.de/search.do?suggestItem=&searchFlags=0&categoryIdsSuggest=&userQuery=1&searchText=XXX&categoryId=&submit.x=0&submit.y=0',
'http://shopping.kelkoo.de/ctl/do/search?siteSearchQuery=XXX&fromform=true&x=0&y=0',
'http://shopping.yahoo.de/ctl/do/search?siteSearchQuery=XXX&fromform=true&x=0&y=0',
'http://suche.baur.de/servlet/weikatec.search.SearchServlet?ls=0&prodDetailUrl=http%3A%2F%2Fwww.baur.de%2Fis-bin%2FINTERSHOP.enfinity%2FWFS%2FBaur-BaurDe-Site%2Fde_DE%2F-%2FEUR%2FBV_DisplayProductInformation-ProductRef%3Bsid%3D8BABmNTUETIDmJI1jy4XWoGEvZygnH3hNmkoFkJ2pR8KfteTkhoVmhkWMDD7wg%3D%3D%3Fls%3D0%26ProductRef%3D%253CSKU%253E%2540Baur-BaurDe%26SearchBack%3D-1%26SearchDetail%3Dtrue&source=&resultsPerPage=99&searchandbrowse=&category2=&query=XXX&category=',
'http://suche.fireball.de/cgi-bin/pursuit?cat=fb_loc&x=0&y=0&query=XXX',
'http://suche.lycos.de/cgi-bin/pursuit?query=XXX&SITE=de&cat=loc',
'http://suche.web.de/search/dir/?mc=verzeichnis%40rubrik.eintrag%40home&su=XXX&smode=',
'http://suche.web.de/search/web/?mc=hp%40suche.suche%40home&su=hudora&su1=XXX&su2=',
'http://www.accoona.com/search?col=ac&expw=1&expb=0&expn=0&pg=1&order=0&qc=de&ql=de&qt=XXX#thebusiness',
'http://www.allesklar.de/s.php?words=XXX&location=&Submit=suchen',
'http://www.alltheweb.com/search?cat=web&cs=iso88591&q=XXX&rys=0&itag=crv&_sb_lang=pref',
'http://www.amazon.de/s/?url=index%3Daps&field-keywords=XXX&Go.x=0&Go.y=0&Go=Go',
'http://www.apollo7.de/a7db/index.php?query=XXX&template=E_RESULTS&ads=true&max_result=200&max_time=10000000&land=de%2Bcom&de_lycos=true&de_mirago=true&de_msn=true&de_sharelook=true&de_witch=true&de_yahoo=true&suchen=suchen',
'http://www.billiger.de/suche.html?searchstring=XXX&search=1&stat=1&implicit=1',
'http://www.bonprix.de/bp/search.htm?id=163980085878606507-0-46e17b22&nv=0%7C0%7C&qu=XXX',
'http://www.ciao.de/sr/q-XXX',
'http://www.dino-online.de/suchergebnis.html?query=XXX&submit.x=0&submit.y=0&fref=suche.dino-online.de&js=on',
'http://www.dooyoo.de/kinderzubehoere/_XXX/',
'http://www.erwinmueller.de/eshop/index.php?db_sess=1f3c454558b84272f1f6406d61d35579&dbsid=11&ss_shop=em&ss_a=em|suche||||||||||||XXX||&wmn=2003653akt=no',
'http://www.evendi.de/jsp/eVendi2004/search.jsp?name=XXX+&Submit=OK&navCategoryID=&priceRangeFrom=&priceRangeTo=',
'http://www.exalead.de/search/results?q=XXX&x=15&y=17&%24mode=allweb',
'http://www.excite.de/search/web/results/?q=XXX&l=',
'http://www.excite.de/shopping/productresults/?from_search=1&query=XXX&cid=',
'http://www.flickr.com/search/?q=XXX&w=all',
'http://www.google.de/products?q=XXX&btnG=Produkte+suchen',
'http://www.google.de/search?hl=de&q=XXX&btnG=Google-Suche&meta=',
'http://www.heise.de/preisvergleich/?fs=XXX&x=0&y=0&in=',
'http://www.hotbot.com/?query=XXX&ps=&loc=searchbox&tab=web&mode=search&currProv=ask',
'http://www.jako-o.de/produkt/de/produkt_detail.mb1?mb_f020_id=Z7XIR8k6Y-EQzasjszz8&fag=d&lang=de&set=suche&subset=suche&suchtext=XXX&detail=on&p_id=5017283&mb_v301_g=1&wmnr_show=92&mb_v301_ch=74845',
'http://www.kanoodle.com/results.html?query=XXX&x=0&y=0',
'http://www.kidoh.de/suche.php?start=0&mode=suche&suche=XXX&x=0&y=0',
'http://www.mamma.com/Mamma?utfout=1&qtype=0&query=XXX&Submit=  Search  ',
'http://www.metacrawler.com/info.metac/search/web/XXX/1/-/1/-/-/-/1/-/-/-/1/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/417/top/-/-/-/1',
'http://www.mister-wong.com/search/?search_type=w&keywords=XXX&btn=search',
'http://www.mistershoplister.de/XXX',
'http://www.mytoys.de/is-bin/INTERSHOP.enfinity/eCS/Store/de/-/DEU/Mt_BrowseCatalog-N;sid=sq5c9rxWmrNe9vq3MtU8_r1cO32-UsiqyLk=?CategoryName=de_DE-so%2eka%2e15%2e40&pg=0&sz=16&lnav=sport/inc/sport_navi_left&bnr=232_so_outdoor.jpg&ziel=sportnavi&mc=ove_095',
'http://www.mytoys.de/is-bin/INTERSHOP.enfinity/eCS/Store/de/-/DEU/Mt_DisplaySearchResult-Start;sid=2MQSlDiqwbIRlH521oJxnDmgyoH4USDlFB0=?key=XXX&cat=de_DE&sort=sd&pg=0',
'http://www.mytoys.de/is-bin/INTERSHOP.enfinity/eCS/Store/de/-/DEU/Mt_DisplaySearchResult-Start?key=XXX&cat=de_DE&sort=sd&pg=0',
'http://www.otto.de/is-bin/INTERSHOP.enfinity/WFS/Otto-OttoDe-Site/de_DE/-/EUR/OV_ViewFHSearch-Search;sid=Rkrckgssg0eUk03wQuT8UF58jGc6Kb-ez6a6CvqGFFV53Fkz4wR3_gb05L1l-Q==?ls=0&commit=true&fh_search=XXX&fh_search_initial=hudora&stype=N',
'http://www.otto.de/is-bin/INTERSHOP.enfinity/WFS/Otto-OttoDe-Site/de_DE/-/EUR/OV_ViewFHSearch-Search?ls=0&commit=true&fh_search=XXX&fh_search_initial=hudora&stype=N',
'http://www.paperazzi.de/cgi-bin/pap_engine_v8.pl?suche=XXX&image.x=0&image.y=0',
'http://www.paperball.de/index.html?send=true&query=XXX&x=0&y=0&cat=loc',
'http://www.preistrend.de/suchen.php?q=XXX&s=0&a=&z=&x=0&y=0',
'http://www.quelle.de/is-bin/INTERSHOP.enfinity/WFS/Quelle-quelle_de-Site/de_DE/-/EUR/Q_FreeSearch-Start;sid=FoQD8ABd2egO8Ea8lv2BphTxbZruGzuZrOl47u22?search_input=hudora&search_free=XXX&fh_view_size=10&fh_sort_by=&enfaction=msearch&action=search&Linktype=E&fh_location=%2F%2Fquelle_de%2Fde_DE',
'http://www.quelle.de/is-bin/INTERSHOP.enfinity/WFS/Quelle-quelle_de-Site/de_DE/-/EUR/Q_FreeSearch-Start?search_input=hudora&search_free=XXX&fh_view_size=10&fh_sort_by=&enfaction=msearch&action=search&Linktype=E&fh_location=%2F%2Fquelle_de%2Fde_DE',
'http://www.rollsport.de/advanced_search_result.php?keywords=XXX&osCsid=1fdd16378f3e607dd03a4476bb8b9f2e&x=0&y=0',
'http://www.rollsport.de/advanced_search_result.php?keywords=XXX&x=0&y=0',
'http://www.sharelook.de/sldb/SLDB_db.php?keyword=XXX&suche_starten=suchen&seite=400001&template=template_suchen&next_results=0&ad=1',
'http://www.shopping-profis.de/preisvergleich/suche-n1.html?q=XXX&mc=&x=0&y=0',
'http://www.spock.com/q/XXX',
'http://www.sportscheck.com/is-bin/INTERSHOP.enfinity/WFS/Sportscheck-SportscheckDe-Site/de_DE/-/EUR/SPM_ParametricSearch-Progress;sid=_PHZNufT-andNqEyfHHE9LKDsZ3e4tpMMVFC3iHH5VyeqkU8eXGtKZBqqnx8Tw==',
'http://www.sportscheck.com/is-bin/INTERSHOP.enfinity/WFS/Sportscheck-SportscheckDe-Site/de_DE/-/EUR/SPM_ParametricSearch-Progress',
'http://www.supabillig.com/a/result.jsp?cr=f&query=XXX',
'http://www.tchibo.de/is-bin/INTERSHOP.enfinity/eCS/Steore/de/-/EUR/TdTchParametricSearch-Start?search_query_keyword=XXX',
'http://www.topxplorer.de/cgi-bin/search.cgi?query=XXX&where=de',
'http://www.topxplorer.de/cgi-bin/search.cgi?query=XXX&where=web',
'http://www.web-archiv.de/index.php?qry=XXX&cms=suche_internet&imageField.x=0&imageField.y=0',
'http://www.webcrawler.com/webcrawler/ws/results/Web/XXX/1/417/TopNavigation/Relevance/zoom=off/_iceUrlFlag=7?_IceUrl=true',
'http://www.wisenut.com/search/query.dll?q=XXX',
'http://www.witch.de/search-result.php?cn=0&search=XXX',
'http://www.xing.com/app/search?op=universal&universal=XXX',
'http://www.yatego.com/index.htm?&cl=mallsearch&tab=shopping&std=1&startCat=&query=XXX&catonly=false&x=0&y=0',
'http://www.yopi.de/index.php?template=search_result&search_mode=basic&search_string=XXX&cat_id=0',
'http://www.yopi.de/index.php?template=search_result&w=XXX&l=a&search_mode=category&cat_id=343',
'http://www.yopi.de/index.php?template=search_result&w=XXX&l=a&search_mode=category&cat_id=516',
'http://www.yopi.de/index.php?template=search_result&w=XXX&l=a&search_mode=category&cat_id=744',
'http://search.dooyoo.de/search/both/hudora/0/?suche=XXX',
]


def urls_for_searchengines(searchterm):
    random.shuffle(searchengines)
    for engineurl in searchengines:
        yield engineurl.replace('XXX', urllib.quote_plus(searchterm))

starturls = [
'http://babybutt.erwinmueller.de/eshop/index.php?db_sess=fa516d7246872e3c8e785402253ee51a&dbsid=11&ss_shop=bb&',
'http://clusty.com/search?input-form=clusty-simple&v%3Asources=http://www.sportscheck.com/is-bin/INTERSHOP.enfinity/WFS/Sportscheck-SportscheckDe-Site/de_DE/-/EUR/SPM_BrowseCatalog-Start;sid=_PHZNufT-andNqEyfHHE9LKDsZ3e4tpMMVFC3iHH5VyeqkU8eXGtKZBqqnx8Tw==?CategoryName=sh13113514&Pfad=line&query=hudora',
'http://de.altavista.com/web/results?itag=ody&q=hudora&kgs=1&kls=0',
'http://de.search.yahoo.com/search?p=hudora&fr=yfp-t-501&ei=UTF-8&meta=vl%3D',
'http://de.vivisimo.com/search?input-form=simple-vivisimo-com&query=hudora&v%3Aproject=de-vivisimo-com&v%3Asources=Web&dlang=de&language=all&x=0&y=0',
'http://de.vivisimo.com/search?input-form=simple-vivisimo-com&query=hudora&v%3Aproject=de-vivisimo-com&v%3Asources=Web&dlang=de&language=german&x=0&y=0',
'http://del.icio.us/search/?fr=del_icio_us&p=hudora&type=all',
'http://en.wikipedia.org/wiki/Special:Search?search=hudora&go=Go',
'http://meta.rrzn.uni-hannover.de/meta/cgi-bin/meta.ger1?start=1&eingabe=hudora&mm=and&maxtreffer=200&time=3&hitsPerServer=2&textmenge=2&wissRank=on&sprueche=on&QuickTips=beschleuniger&linkTest=no&check_time=3&dmoz=on&exalead=on&suchclip=on&wiki=on&harvest=on&witch=on&overture=on&fastbot=on&fportal=on&Nachrichten=on&Usenet=on&firstsfind=on&cpase=on&metarss=on&neomo=on&nebel=on&audioclipping=on',
'http://msxml.excite.com/info.xcite/search/web/hudora',
'http://preis.info/index.aspx?such=hudora&image2.x=0&image2.y=0',
'http://preisvergleich.getprice.de/jsp/partner/getprice2005/search.jsp?name=hudora&Submit=suchen&navCategoryID=&priceRangeFrom=&priceRangeTo=',
'http://produktsuche.web.de/search.do?s=hudora',
'http://sads.myspace.com//Modules/Search/Pages/Search.aspx?fuseaction=advancedFind.results&searchtarget=tms&searchtype=myspace&t=tms&get=1&websearch=1&searchBoxID=Profile&searchString=hudora&q=hudora',
'http://search-desc.ebay.de/rollschuhe_W0QQfsooZ2QQfsopZ19QQftsZ2QQsalisZ77',
'http://search-desc.ebay.de/search/search.dll?sofocus=bs&sbrftog=1&from=R10&satitle=hudora&sacat=-1%26catref%3DC6&bs=Finden&fts=2&sargn=-1%26saslc%3D3&sadis=200&fpos=Postleitzahl&sabfmts=1&saobfmts=insif&ga10244=10425&ftrt=1&ftrv=1&saprclo=&saprchi=&salis=77&fhlc=1&fsop=1%26fsoo%3D1&coaction=compare&copagenum=1&coentrypage=search&fgtp=',
'http://search.abacho.com/de/abacho.de/index.cfm?q=hudora&country=de&x=0&y=0',
'http://search.ebay.de/search/search.dll?fsop=1&fsoo=1&from=R3&strKw=+&shortcut=4&siteid=77&satitle=hudora',
'http://search.lycos.com/?query=hudora&x=0&y=0',
'http://search.msn.com/results.aspx?q=hudora&FORM=MSNH',
'http://search.yahoo.com/search?ei=UTF-8&trackingType=go_search_home&p=hudora&fr=hsusgo1&sa.x=0&sa.y=0',
'http://search.yahoo.com/search?ei=UTF-8&trackingType=go_search_home&p=hudora&fr=hsusgo1',
'http://shopping.freenet.de/search.do?suggestItem=&searchFlags=0&categoryIdsSuggest=&userQuery=1&searchText=hudora&categoryId=&submit.x=0&submit.y=0',
'http://shopping.kelkoo.de/ctl/do/search?siteSearchQuery=hudora&fromform=true&x=0&y=0',
'http://shopping.yahoo.de/ctl/do/search?siteSearchQuery=hudora&fromform=true&x=0&y=0',
'http://suche.baur.de/servlet/weikatec.search.SearchServlet?ls=0&prodDetailUrl=http%3A%2F%2Fwww.baur.de%2Fis-bin%2FINTERSHOP.enfinity%2FWFS%2FBaur-BaurDe-Site%2Fde_DE%2F-%2FEUR%2FBV_DisplayProductInformation-ProductRef%3Bsid%3D8BABmNTUETIDmJI1jy4XWoGEvZygnH3hNmkoFkJ2pR8KfteTkhoVmhkWMDD7wg%3D%3D%3Fls%3D0%26ProductRef%3D%253CSKU%253E%2540Baur-BaurDe%26SearchBack%3D-1%26SearchDetail%3Dtrue&source=&resultsPerPage=99&searchandbrowse=&category2=&query=hudora&category=',
'http://suche.fireball.de/cgi-bin/pursuit?cat=fb_loc&x=0&y=0&query=hudora',
'http://suche.lycos.de/cgi-bin/pursuit?query=hudora&SITE=de&cat=loc',
'http://suche.web.de/search/dir/?mc=verzeichnis%40rubrik.eintrag%40home&su=hudora&smode=',
'http://suche.web.de/search/web/?mc=hp%40suche.suche%40home&su=hudora&su1=hudora&su2=',
'http://www.accoona.com/search?col=ac&expw=1&expb=0&expn=0&pg=1&order=0&qc=de&ql=de&qt=hudora#thebusiness',
'http://www.allesklar.de/s.php?words=hudora&location=&Submit=suchen',
'http://www.alltheweb.com/search?cat=web&cs=iso88591&q=hudora&rys=0&itag=crv&_sb_lang=pref',
'http://www.amazon.de/s/?url=index%3Daps&field-keywords=hudora&Go.x=0&Go.y=0&Go=Go',
'http://www.apollo7.de/a7db/index.php?query=hudora&template=E_RESULTS&ads=true&max_result=200&max_time=10000000&land=de%2Bcom&de_lycos=true&de_mirago=true&de_msn=true&de_sharelook=true&de_witch=true&de_yahoo=true&suchen=suchen',
'http://www.billiger.de/suche.html?searchstring=hudora&search=1&stat=1&implicit=1',
'http://www.bonprix.de/bp/search.htm?id=163980085878606507-0-46e17b22&nv=0%7C0%7C&qu=hudora',
'http://www.ciao.de/Hudora_Scooter_Big_Wheel__2433141',
'http://www.ciao.de/sr/q-hudora',
'http://www.dino-online.de/suchergebnis.html?query=hudora&submit.x=0&submit.y=0&fref=suche.dino-online.de&js=on',
'http://www.dooyoo.de/kinderzubehoere/_hudora/',
'http://www.erwinmueller.de/eshop/index.php?db_sess=1f3c454558b84272f1f6406d61d35579&dbsid=11&ss_shop=em&ss_a=em|suche||||||||||||hudora||&wmn=2003653akt=no',
'http://www.evendi.de/jsp/eVendi2004/search.jsp?name=hudora+&Submit=OK&navCategoryID=&priceRangeFrom=&priceRangeTo=',
'http://www.exalead.de/search/results?q=hudora&x=15&y=17&%24mode=allweb',
'http://www.excite.de/search/web/results/?q=hudora&l=',
'http://www.excite.de/search/web/results/?q=hudora&x=0&y=0&l=',
'http://www.excite.de/shopping/productresults/?from_search=1&query=hudora&cid=',
'http://www.flickr.com/search/?q=hudora&w=all',
'http://www.google.de/products?q=hudora&btnG=Produkte+suchen',
'http://www.google.de/search?hl=de&q=hudora&btnG=Google-Suche&meta=',
'http://www.heise.de/preisvergleich/?cat=spbadmin',
'http://www.heise.de/preisvergleich/?cat=spbasketball',
'http://www.heise.de/preisvergleich/?cat=spboxen',
'http://www.heise.de/preisvergleich/?cat=spcrosst',
'http://www.heise.de/preisvergleich/?cat=spfittsonst',
'http://www.heise.de/preisvergleich/?cat=spfootball',
'http://www.heise.de/preisvergleich/?cat=spfussball',
'http://www.heise.de/preisvergleich/?cat=spgym',
'http://www.heise.de/preisvergleich/?cat=sphandball',
'http://www.heise.de/preisvergleich/?cat=sphantelbank',
'http://www.heise.de/preisvergleich/?cat=sphanteln',
'http://www.heise.de/preisvergleich/?cat=sphomet',
'http://www.heise.de/preisvergleich/?cat=spkleintrain',
'http://www.heise.de/preisvergleich/?cat=spkraft',
'http://www.heise.de/preisvergleich/?cat=splaufbae',
'http://www.heise.de/preisvergleich/?cat=spoutfbfan',
'http://www.heise.de/preisvergleich/?cat=spoutfbschuhe',
'http://www.heise.de/preisvergleich/?cat=spoutprotek',
'http://www.heise.de/preisvergleich/?cat=spoutskate',
'http://www.heise.de/preisvergleich/?cat=spouttorwart',
'http://www.heise.de/preisvergleich/?cat=spradkinder',
'http://www.heise.de/preisvergleich/?cat=spruder',
'http://www.heise.de/preisvergleich/?cat=spsquash',
'http://www.heise.de/preisvergleich/?cat=spstepper',
'http://www.heise.de/preisvergleich/?cat=sptennis',
'http://www.heise.de/preisvergleich/?cat=sptennissaiten',
'http://www.heise.de/preisvergleich/?cat=sptischtennis',
'http://www.heise.de/preisvergleich/?cat=spvolleyball',
'http://www.heise.de/preisvergleich/?fs=hudora&x=0&y=0&in=',
'http://www.heise.de/preisvergleich/?o=82',
'http://www.heise.de/preisvergleich/?o=83',
'http://www.heise.de/preisvergleich/?o=87',
'http://www.hotbot.com/?query=hudora&ps=&loc=searchbox&tab=web&mode=search&currProv=ask',
'http://www.idealo.de/preisvergleich/MainSearchProductCategory.html',
'http://www.jako-o.de/produkt/de/produkt_detail.mb1?mb_f020_id=WHxE-mPC0-kQzasjajz8&fag=d&lang=de&set=suche&subset=suche&suchtext=hudora&detail=on&p_id=5017283&mb_v301_g=1&wmnr_show=92&mb_v301_ch=43737',
'http://www.jako-o.de/produkt/de/produkt_detail.mb1?mb_f020_id=Z7XIR8k6Y-EQzasjszz8&fag=d&lang=de&set=suche&subset=suche&suchtext=hudora&detail=on&p_id=5017283&mb_v301_g=1&wmnr_show=92&mb_v301_ch=74845',
'http://www.kanoodle.com/results.html?query=hudora&x=0&y=0',
'http://www.kidoh.de/suche.php?PUBLICAID=7c9610797ac2e411222cc2450de697c2&start=0&mode=suche&suche=hudora&x=0&y=0',
'http://www.mamma.com/Mamma?utfout=1&qtype=0&query=hudora&Submit=  Search  ',
'http://www.metacrawler.com/info.metac/search/web/hudora/1/-/1/-/-/-/1/-/-/-/1/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/417/top/-/-/-/1',
'http://www.mister-wong.com/search/?search_type=w&keywords=hudora&btn=search',
'http://www.mistershoplister.de/hudora',
'http://www.mytoys.de/is-bin/INTERSHOP.enfinity/eCS/Store/de/-/DEU/Mt_BrowseCatalog-N;sid=sq5c9rxWmrNe9vq3MtU8_r1cO32-UsiqyLk=?CategoryName=de_DE-so%2eka%2e15%2e40&pg=0&sz=16&lnav=sport/inc/sport_navi_left&bnr=232_so_outdoor.jpg&ziel=sportnavi&mc=ove_095',
'http://www.mytoys.de/is-bin/INTERSHOP.enfinity/eCS/Store/de/-/DEU/Mt_DisplaySearchResult-Start;sid=2MQSlDiqwbIRlH521oJxnDmgyoH4USDlFB0=?key=hudora&cat=de_DE&sort=sd&pg=0',
'http://www.mytoys.de/is-bin/INTERSHOP.enfinity/eCS/Store/de/-/DEU/Mt_DisplaySearchResult-Start;sid=sq5c9rxWmrNe9vq3MtU8_r1cO32-UsiqyLk=?key=hudora&cat=de_DE&sort=sd&pg=0',
'http://www.neckermann.de/index.mb1?mb_f020_id=zl7HChS_xjfIJ9gnnUk1X0DjzDsHDsW9&vkh=0461&linktracking_nr=BUo96xmJvGWLXM7vhhiXX-WjazPLaW8&tgs_group=&ct=1&mb_v301_ch=ab2ea',
'http://www.otto.de/is-bin/INTERSHOP.enfinity/WFS/Otto-OttoDe-Site/de_DE/-/EUR/OV_ViewFHSearch-Search;sid=Rkrckgssg0eUk03wQuT8UF58jGc6Kb-ez6a6CvqGFFV53Fkz4wR3_gb05L1l-Q==?ls=0&commit=true&fh_search=hudora&fh_search_initial=hudora&stype=N',
'http://www.otto.de/is-bin/INTERSHOP.enfinity/WFS/Otto-OttoDe-Site/de_DE/-/EUR/OV_ViewFHSearch-Search;sid=xj6UoeETQG8RoafyRkS9gfq_DBNyGlWhT9IR-3JilCEx77MMY3A_zezLtysjww==?ls=0&commit=true&fh_search=hudora&fh_search_initial=hudora&stype=N',
'http://www.paperazzi.de/cgi-bin/pap_engine_v8.pl?suche=hudora&image.x=0&image.y=0',
'http://www.paperball.de/index.html?send=true&query=hudora&x=0&y=0&cat=loc',
'http://www.preis.de/index.htm',
'http://www.preisroboter.de/ergebnis102830.html',
'http://www.preissuchmaschine.de/psm_frontend/main.asp?kid=3-563-3342',
'http://www.preissuchmaschine.de/psm_frontend/main.asp?suche=hudora',
'http://www.preistrend.de/suchen.php?q=hudora&s=0&a=&z=&x=0&y=0',
'http://www.quelle.de/is-bin/INTERSHOP.enfinity/WFS/Quelle-quelle_de-Site/de_DE/-/EUR/Q_FreeSearch-Start;sid=FoQD8ABd2egO8Ea8lv2BphTxbZruGzuZrOl47u22?search_input=hudora&search_free=hudora&fh_view_size=10&fh_sort_by=&enfaction=msearch&action=search&Linktype=E&fh_location=%2F%2Fquelle_de%2Fde_DE',
'http://www.rollsport.de/',
'http://www.rollsport.de/advanced_search_result.php?keywords=hudora&osCsid=1fdd16378f3e607dd03a4476bb8b9f2e&x=0&y=0',
'http://www.sharelook.de/sldb/SLDB_db.php?keyword=hudora&suche_starten=suchen&seite=400001&template=template_suchen&next_results=0&ad=1',
'http://www.shopping-profis.de/preisvergleich/suche-n1.html?q=hudora&mc=&x=0&y=0',
'http://www.spock.com/q/dornseif',
'http://www.sportscheck.com/is-bin/INTERSHOP.enfinity/WFS/Sportscheck-SportscheckDe-Site/de_DE/-/EUR/SPM_ParametricSearch-Progress;sid=_PHZNufT-andNqEyfHHE9LKDsZ3e4tpMMVFC3iHH5VyeqkU8eXGtKZBqqnx8Tw==',
'http://www.supabillig.com/a/result.jsp?cr=f&query=Hudora',
'http://www.tchibo.de/is-bin/INTERSHOP.enfinity/eCS/Store/de/-/EUR/TdTchParametricSearch-Start?search_query_keyword=hudora',
'http://www.topxplorer.de/cgi-bin/search.cgi?query=hudora&where=de',
'http://www.topxplorer.de/cgi-bin/search.cgi?query=hudora&where=web',
'http://www.web-archiv.de/index.php?qry=hudora&cms=suche_internet&imageField.x=0&imageField.y=0',
'http://www.webcrawler.com/webcrawler/ws/results/Web/hudora/1/417/TopNavigation/Relevance/zoom=off/_iceUrlFlag=7?_IceUrl=true',
'http://www.wisenut.com/search/query.dll?q=hudora',
'http://www.witch.de/search-result.php?cn=0&search=hudora',
'http://www.xing.com/app/search?op=universal&universal=hudora',
'http://www.yatego.com/index.htm?&cl=mallsearch&tab=shopping&std=1&startCat=&query=hudora&catonly=false&x=0&y=0',
'http://www.yopi.de/index.php?template=search_result&search_mode=basic&search_string=hudora&cat_id=0',
'http://www.yopi.de/index.php?template=search_result&w=hudora&l=a&search_mode=category&cat_id=343',
'http://www.yopi.de/index.php?template=search_result&w=hudora&l=a&search_mode=category&cat_id=516',
'http://www.yopi.de/index.php?template=search_result&w=hudora&l=a&search_mode=category&cat_id=744',
'http://search.dooyoo.de/search/both/hudora/0/?suche=hudora',
]

random.shuffle(searchterms)
for searchterm in searchterms:
    starturls.extend(list(urls_for_searchengines(searchterm))[:2])
print "<html><body>"
print '\n'.join(['<a href="%s">hier</a>' % x for x in starturls])
print "</body></html>"
