EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Connector_Generic:Conn_02x03_Odd_Even J1
U 1 1 5DC2C4F5
P 2650 1750
F 0 "J1" V 2654 1930 50  0000 L CNN
F 1 "SAO" V 2745 1930 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_2x03_P2.54mm_Vertical" H 2650 1750 50  0001 C CNN
F 3 "~" H 2650 1750 50  0001 C CNN
	1    2650 1750
	0    1    1    0   
$EndComp
Wire Wire Line
	2750 1550 2750 1450
Wire Wire Line
	2650 1550 2650 1450
Wire Wire Line
	2550 1550 2550 1450
Wire Wire Line
	2550 2050 2550 2150
Wire Wire Line
	2650 2050 2650 2150
Wire Wire Line
	2750 2050 2750 2150
Text Label 2750 1450 1    50   ~ 0
VCC
Text Label 2750 2150 3    50   ~ 0
GND
Text Label 2650 2150 3    50   ~ 0
SCL
Text Label 2650 1450 1    50   ~ 0
SDA
Text Label 2550 1450 1    50   ~ 0
GPIO1
Text Label 2550 2150 3    50   ~ 0
GPIO2
Wire Wire Line
	4350 1550 4350 1450
Wire Wire Line
	4250 1550 4250 1450
Wire Wire Line
	4150 1550 4150 1450
Wire Wire Line
	4150 2050 4150 2150
Wire Wire Line
	4250 2050 4250 2150
Wire Wire Line
	4350 2050 4350 2150
Text Label 4350 1450 1    50   ~ 0
VCC
Text Label 4350 2150 3    50   ~ 0
GND
Text Label 4250 2150 3    50   ~ 0
SCL
Text Label 4250 1450 1    50   ~ 0
SDA
Text Label 4150 1450 1    50   ~ 0
GPIO1
Text Label 4150 2150 3    50   ~ 0
GPIO2
$Comp
L Connector_Generic:Conn_02x03_Odd_Even J2
U 1 1 5DC316E3
P 4250 1750
F 0 "J2" V 4254 1930 50  0000 L CNN
F 1 "Badge" V 4345 1930 50  0000 L CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_2x03_P2.54mm_Vertical" H 4250 1750 50  0001 C CNN
F 3 "~" H 4250 1750 50  0001 C CNN
	1    4250 1750
	0    1    1    0   
$EndComp
$EndSCHEMATC
