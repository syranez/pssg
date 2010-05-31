#!/usr/bin/perl

use strict;
#use CGI::Carp qw(fatalsToBrowser);

#
# Einstellungen
#



# Im Browser ausgeben oder in HTML-Datei schreiben
# [0]: Browser
# [1]: HTML-Datei ($OutputFile)
my $OutputDirection = 0;

# Name und Verzeichnis der HTML-Datei
# Format: ">FILE"
my $OutputFile = ">http://www.minaga-church.de/pssg/example/cgi-bin/stats.htm";

# Titel der HTML Datei
my $OutputFileTitle = "Megapix Soldat Server";

# Name und Verzeichnis der CSS-Datei
my $OutputFileCSSFile = "pssg.css";

# Webverzeichnis der Killlogs
my $KilllogDir = ".";

# Servername
my $ServerName = "Megapix Soldat Server";

# Server-IP und -Port
my $ServerIPPort = "62.75.222.207:23073";

# Soll Serverinformationen ausgegeben werden?
# [0]: nein
# [1]: ja
my $EnableServer = 1;

# Soll Spielerinformationen ausgegeben werden?
# [0]: nein
# [1]: ja
my $EnablePlayer = 1;

# Soll die Player-Ausgabe sortiert werden?
# [0]: nicht sortieren
# [1]: sortieren
my $EnablePlayerSort = 1;

# Wie soll die Player-Ausgabe sortiert werden?
# [1]: nach Kills
# [2]: nach Deaths
# [3]: nach Selfkills
my $PlayerSort = 1;

# Soll der Lieblingsgegner/Angstgegner angezeigt werden?
# [0]: nein
# [1]: nur Lieblingsgegner
# [2]: nur Angstgegner
# [3]: beide
my $PlayerEnableEnemy = 2;

# Soll die Lieblingswaffe/Angstwaffe angezeigt werden?
# [0]: nein
# [1]: nur Lieblingswaffe
# [2]: nur Angstwaffe
# [3]: beide
my $PlayerEnableWeapon = 0;

# Wieviele Spieler sollen in der ausführlichen Player-Ausgabe erscheinen?
# [0]: alle
# [X]: jeder andere Wert für Anzahl Spieler
my $PlayerExtended = 10;

# Soll eine Waffenaufschlüsselung der Personen erfolgen, mit denen sie getötet haben?
# [0]: nein
# [1]: nur Primärwaffen
# [2]: nur Sekundärwaffen
# [3]: alle Waffen
my $EnableWeaponKill = 1;

# Soll eine Waffenaufschlüsselung der Personen erfolgen, mit denen sie getötet _wurden_?
# [0]: nein
# [1]: nur Primärwaffen
# [2]: nur Sekundärwaffen
# [3]: alle Waffen
my $EnableWeaponKilled = 1;

# Für wieviele Spieler soll die Waffenaufschlüsselung gemacht werden?
# (empfehlenswert: selber Wert wie in $PlayerExtended)
# [0]: alle
# [X]: jeder andere Wert für Anzahl Spieler
my $WeaponPlayers = $PlayerExtended;

# Soll eine Aufstellung der Kills/Deaths gemacht werden?
# [0]: nein
# [1]: ja
my $EnableWhoKilledWho = 1;

# Wieviele Spieler sollen in der Kills/Deaths-Aufstellung erscheinen?
# (empfehlenswert: selber Wert wie in $PlayerExtended)
# [0]: alle
# [X]: jeder andere Wert für Anzahl Spieler
my $WhoKilledWhoPlayers = $PlayerExtended;

# Soll <Sonstige Stats> erstellt werden?
# [0]: nein
# [1]: ja
my $EnableOther = 1;



#
# Ab hier nix mehr ändern, ausser Du kennst dich aus ^^
#
	


#
# Variablen
#



# Im Skript benutzte Zeichenketten
# Für Lokalisierung des Skriptes nur hier Zeichenketten ändern.
my @PSSG_TextCommon = ("Statistik erstellt am");
my @PSSG_TextServer = ("Server","Allgemeine Serverinformationen","Server-Name","Server-IP/Port",
	"Killlogs","Statistikzeitraum","Spieler","Frags","Selbstmorde");
my @PSSG_TextPlayers = ("Top $PlayerExtended Spieler","Spieler","(nach Kills sortiert)",
	"(nach Deaths sortiert)","(nach Selfkills sortiert)","Rang","Spieler","Frags",
	"Tode","Selbstmorde","K:D","Lieblingsgegner","Angstgegner","Lieblingswaffe",
	"Angstwaffe","Sie haben es nicht an die Spitze geschafft:");
my @PSSG_TextWeapons = ("Top $WeaponPlayers Spieler","(genutzte Waffen)","Spieler-Waffenaufschlüsselung",
	"(getötet durch)","(nach Kills sortiert)","(nach Deaths sortiert)","(nach Selfkills sortiert)",
	"Hauptwaffen","Zweitwaffen");
my @PSSG_TextWhoKilledWho = ("Top $WhoKilledWhoPlayers", "Who Killed Who", "(nach Kills sortiert)",
	"(nach Deaths sortiert)","(nach Selfkills sortiert)","Spieler");
my @PSSG_TextOther = ("Sonstige Stats","Die fabelhafte Welt der Zahlen",
	"{NAME} ist der Schrecken seiner Gegner: {VALUE} Kills.",
	"{NAME} erfreut sich am Sterben. Insgesamt starb er {VALUE} mal.",
	"{NAME} mag sich lieber selbst töten. Insgesamt {VALUE} Selfkill(s).",
	"Die Primärwaffe {NAME} wurde mit insgesamt {VALUE} Kills am Liebsten zum Töten benutzt.",
	"Bei den Zweitwaffen wurde die {NAME} am meisten verwendet. Insgesamt {VALUE} mal.");

# Speichert wie oft mit welcher Waffe getötet wurde
# [0-9]:   Primary Weapons
# [10-13]: Secondary Weapons
# See PrimaryWeaponsN & SecondaryWeaponsN
my @PSSG_Weapons = (0,0,0,0,0,0,0,0,0,0,0,0,0,0);

# PlayerInfoIndex
# --    --      -
my $plinxName		 = 0;
my $plinxKills		 = 1;
my $plinxDeaths		 = 2;
my $plinxSelfkills	 = 3;
my $plinxKilledEnemys	 = 4;
my $plinxWeaponKill	 = 5;
my $plinxWeaponKilled	 = 6;
my $plinxFavouriteWeapon = 7;
my $plinxFearedWeapon	 = 8;

# [0]: Anzahl Kills
my @PSSG_KilledEnemys;

# Player Info
# Every Element of Players is an Array with this Information:
# [0]: Player-Name
# [1]: Kills
# [2]: Deaths (no selfkills)
# [3]: Selfkills
# [4]: Killed Enemys
# [5]: Killed by Enemys
# [6]: How often used which weapon to kill
# [7]: How often killed by using weapon
# [8]: Favourite Weapon
# [9]: Feared Weapon
#@PlayerInfo = ("PlayerName",0,0,0,[@PSSG_KilledEnemys],[@PSSG_Weapons],[@PSSG_Weapons],0,0);



#
# Im Skript genutzte Variablen
#



# PSSG Version
my $PSSG_Version = "v1.0";

# Counter für
# [0]: Players
# [1]: Kills
# [2]: Selfkills
# [3]: Anzahl Killlogs
my @PSSG_Counter = (0,0,0,0);

# Date & Time
# [0]: Erster Eintrag in der Killlogfile (z.B. 04-12-30 13:21:47    Kill Log Started)
# [1]: Letztes Datum in der Killlogfile (z.B. 04-12-30 13:44:31)
# [2]: Killlogfile-Name
my @PSSG_TimeKilllog = ("","","NONE");

# Enthält $PSSG_Counter[3]x @PSSG_TimeKilllog
my @PSSG_TimeDate;

# Zeitraum des Statistikzeitraums
# [0]: Anfangsdatum
# [1]: Enddatum
my @PSSG_TimeStats = ("","");

# Primary Weapons Name
# [0]: Desert Eagles
# [1]: HK MP5
# [2]: Ak-74
# [3]: Steyr AUG
# [4]: Spas-12
# [5]: Ruger 77
# [6]: M79
# [7]: Barret M82A1
# [8]: FN Minimi
# [9]: XM214 Minigun
my @PSSG_PrimaryWeaponsN = ("Desert Eagles","HK MP5","Ak-74","Steyr AUG",
	"Spas-12","Ruger 77","M79","Barret M82A1","FN Minimi","XM214 Minigun");

# Secondary Weapons Name
# [0]: USSOCOM
# [1]: Combat Knife
# [2]: Chainsaw
# [3]: M72 Law
my @PSSG_SecondaryWeaponsN = ("USSOCOM","Combat Knife","Chainsaw","M72 Law");

# Enthält die PlayerInfos
my @Players;

# Enthält die IDs der sortierten PlayerInfos
my @SortedPlayers;



#
# Skriptablauf
#



# Argument einlesen
my $file = $ENV{'QUERY_STRING'};
$file = substr($file,5,length($file));

if ( $OutputDirection == 1 ){open(OUTPUT,$OutputFile);select (OUTPUT);}else{select (STDOUT);}

# wenn das ganze verzeichnis ausgewertet werden soll
if ( $file eq "all" )
{
	my $file = "";

	opendir(DIR,$KilllogDir) || die "hoa $KilllogDir: $!";
	my @Entrys = readdir(DIR);
	closedir(DIR);
	foreach(@Entrys)
	{		
		$file = substr($_,0,7);
		if ( $file eq "killlog" ){PSSG_MakeDataFromFile($_);}		
	}	
}

# ansonsten nur die datei
else{PSSG_MakeDataFromFile($file);}

# Stats erstellen
MakeStats();

# Schreibt die ermittelte Statistik
PSSG_WriteStats();

if ( $OutputDirection == 1){close(OUTPUT);}



#
# Sortierfunktion
#



sub PSSG_SortPlayers
{
	my $Option = shift;
	my $i = 0;
	my $ii = 0;
	my $Place = 0;
	
	# Initialisierung
	for ( $i = 0; $i < $PSSG_Counter[0]; $i++ ){$SortedPlayers[$i]=$i;}
	# Sortieren
	for ( $i = 0; $i < $PSSG_Counter[0]; $i++ )
	{
		$Place = 0;
		for ( $ii = 0; $ii < $PSSG_Counter[0]; $ii++ )
		{
			if ( $Players[$i][$Option] > $Players[$ii][$Option] ){$Place++;}
		}
		$SortedPlayers[$#SortedPlayers-$Place] = $i;
	}
}



#
# Funktionen zum Ermitteln einzelner Daten
#



sub PSSG_getWeaponID
{
	my $Weapon = shift;
	# maybe i will kill some people. working hours for hours cos $PSSG_PrimaryWeaponsN[$i] is not
	# $Weapon. I've changed everything in this skript but nothing helped. Hour for hour, i worked
	# on this problem. And then: I print out $Weapon and $PSSG_PrimaryWeaponsN[$i] (they should equal)
	# and recognized following:
	# 		Ak-74
	#		Ak-74
	# Ive used this command: print "$Weapon $PSSG_PrimaryWeaponsN[$i]
	# Do you see why $Weapon is never $PSSG_PrimaryWeaponsN[$i]? Yes? So...you are dead.
	my $TrueWeapon = substr($Weapon,0,length($Weapon)-1);
	my $i = 0;
	
	# Primary Weapons
	for ( $i = 0; $i < 10; $i++ )
	{
		if ( $PSSG_PrimaryWeaponsN[$i] eq $TrueWeapon ){return $i;}
	}
	
	# Secondary Weapons
	for ( $i = 0; $i < 4; $i++ )
	{
		if ( $PSSG_SecondaryWeaponsN[$i] eq $TrueWeapon ){$i+=9;return $i;}
	}
	
	# if there is no weapon
	return "NONE";
}

sub PSSG_getPlayerID
{
	my $Player = shift;
	my $i = 0;
	
	for ( $i = 0; $i < $PSSG_Counter[0]; $i++ )
	{
		if ( $Players[$i][$plinxName] eq $Player ){return $i;}
	}
	
	return "NONE";
}

sub PSSG_getWeaponName
{
	my $WeaponID = shift;
	my $i = 0;
	
	if ( $WeaponID < 9 ){print "$PSSG_PrimaryWeaponsN[$WeaponID]";}
	else {$i-=9;print "$PSSG_SecondaryWeaponsN[$WeaponID]";}
}

sub PSSG_getEnemyNo1ID
{
	my $PlayerID = shift;
	my $i = 0;
	my $EnemyNo1ID = 0;
	my $EnemyNo1Kills = 0;
	for ( $i = 0; $i < $PSSG_Counter[0]; $i++ )
	{
		if ( $Players[$i][$plinxKilledEnemys][$PlayerID] > $EnemyNo1Kills )
		{
			$EnemyNo1ID = $i;
			$EnemyNo1Kills = $Players[$i][$plinxKilledEnemys][$PlayerID];
		}
	}
	return $EnemyNo1ID;
}

sub PSSG_getFavouriteEnemyID
{
	my $PlayerID = shift;
	my $i = 0;
	my $FavouriteEnemyID = 0;
	my $FavouriteEnemyKills = 0;
	
	for ( $i = 0; $i < $PSSG_Counter[0]; $i++ )
	{
		if ( $Players[$PlayerID][$plinxKilledEnemys][$i] > $FavouriteEnemyKills )
		{
			$FavouriteEnemyID = $i;
			$FavouriteEnemyKills = $Players[$PlayerID][$plinxKilledEnemys][$i];
		}
	}	
	return $FavouriteEnemyID;
}

sub PSSG_getPlayerName
{
	my $PlayerID = shift;
	return "$Players[$PlayerID][$plinxName]";
}

sub PSSG_getPlayerIDOf
{
	# switch: plinxKills, plinxDeaths, plinxSelfkills
	my $Switch = shift;
	my $PlayerID = 0;	
	my $Object = 0;
	my $i = 0;
	
	for ( $i = 0; $i < $PSSG_Counter[0]; $i++ )
	{
		if ( $Players[$i][$Switch] > $Object )
		{$Object=$Players[$i][$Switch];$PlayerID = $i;}
	}
	
	return $PlayerID;
}

sub PSSG_getLogStartTime
{
	my $i = 0;
	my $ii = 0;
	my $iii = 0;
	
	my @KilllogIndex;
	
	for ( $i = 0; $i < $PSSG_Counter[3]; $i++ )
	{	
		$KilllogIndex[$i] = substr($PSSG_TimeDate[$i][2],8,length($PSSG_TimeDate[$i][2])-8);
		chop($KilllogIndex[$i]);chop($KilllogIndex[$i]);chop($KilllogIndex[$i]);chop($KilllogIndex[$i]);
	}
	
	# Älteste Killlogfile finden
	$ii = $KilllogIndex[0];
	for ( $i = 1; $i < $PSSG_Counter[3]; $i++ )
	{
		if ( $KilllogIndex[$i] < $ii ){$ii=$KilllogIndex[$i];$iii=$i;}	
	}
	
	$PSSG_TimeStats[0] = $PSSG_TimeDate[$iii][0];
	# Datum in TT.MM.JJJJ konvertieren
	PSSG_ConvertDate(0);	
}

sub PSSG_getLogEndTime
{
	my $i = 0;
	my $ii = 0;
	my $iii = 0;
	
	my @KilllogIndex;
	
	for ( $i = 0; $i < $PSSG_Counter[3]; $i++ )
	{	
		$KilllogIndex[$i] = substr($PSSG_TimeDate[$i][2],8,length($PSSG_TimeDate[$i][2])-8);
		chop($KilllogIndex[$i]);chop($KilllogIndex[$i]);chop($KilllogIndex[$i]);chop($KilllogIndex[$i]);
	}
	
	# Jüngste Killlogfile finden
	$ii = $KilllogIndex[0];
	for ( $i = 1; $i < $PSSG_Counter[3]; $i++ )
	{
		if ( $KilllogIndex[$i] > $ii ){$ii=$KilllogIndex[$i];$iii=$i;}	
	}
	
	$PSSG_TimeStats[1] = $PSSG_TimeDate[$iii][0];
	# Datum in TT.MM.JJJJ konvertieren
	PSSG_ConvertDate(1);
}



sub PSSG_getMostUsedPrimaryWeaponKill
{
	my $PlayerCounter = 0;
	my $WeaponCounter = 0;
	my $WeaponID = 0;
	my $i = 0;
	my $ii = 0;
	
	for ( $WeaponCounter = 0; $WeaponCounter < 10; $WeaponCounter++ )
	{
		$i = 0;
		for ( $PlayerCounter = 0; $PlayerCounter < $PSSG_Counter[0]; $PlayerCounter++ )
		{$i += $Players[$PlayerCounter][$plinxWeaponKill][$WeaponCounter];}
		if ( $i > $ii ){$ii=$i;$WeaponID=$WeaponCounter;}
	}
	
	return $WeaponID;	
}

sub PSSG_getMostUsedSecondaryWeaponKill
{
	my $PlayerCounter = 0;
	my $WeaponCounter = 0;
	my $WeaponID = 0;
	my $i = 0;
	my $ii = 0;
	
	for ( $WeaponCounter = 10; $WeaponCounter <= 13; $WeaponCounter++ )
	{
		$i = 0;
		for ( $PlayerCounter = 0; $PlayerCounter < $PSSG_Counter[0]; $PlayerCounter++ )
		{$i += $Players[$PlayerCounter][$plinxWeaponKill][$WeaponCounter];}
		if ( $i > $ii ){$ii=$i;$WeaponID=$WeaponCounter;}
	}
	
	return ($WeaponID-10);
}


#
# Konvertierungsfunktionen
#



sub PSSG_ConvertDate
{
	my $Time = shift;
	my $Day;
	my $Month;
	# falls Logs vor 2000 sind, hier ändern in "19"
	my $Year = "20";
	
	$PSSG_TimeStats[$Time] = substr($PSSG_TimeStats[$Time],0,8);
	
	$Day = substr($PSSG_TimeStats[$Time],6,2);
	$Month = substr($PSSG_TimeStats[$Time],3,2);
	$Year .= substr($PSSG_TimeStats[$Time],0,2);
	
	$PSSG_TimeStats[$Time] = $Day;
	$PSSG_TimeStats[$Time] .= ".";
	$PSSG_TimeStats[$Time] .= $Month;
	$PSSG_TimeStats[$Time] .= ".";
	$PSSG_TimeStats[$Time] .= $Year;
}
	


#
# Funktionen zum Erstellen der Stats
#



sub PSSG_MakeDataFromFile
{
	my $File = shift;
	my @Killlog;
	my @TimeKilllog;
	my $Killer; my $Victim; my $Weapon; my $i;
	my @FileInfo = stat($File);
	if ( $FileInfo[7] == 0 ){return;}
	
	open (INPUT,$File) || die "Datei $File nicht gefunden.";
	@Killlog = <INPUT>;
	close(INPUT);

	# Killlogdatum ermitteln
	$TimeKilllog[0] = $Killlog[0];
	$TimeKilllog[2] = $File;
		
	for ( $i = 2; $i <= $#Killlog; $i+=4 )
	{	
		$Killer = $Killlog[$i];
		$Victim = $Killlog[$i+1];
		$Weapon = $Killlog[$i+2];
		$TimeKilllog[1] = $Killlog[$i+3];
		PSSG_MakeData($Killer,$Victim,$Weapon);	
	}
	push(@PSSG_TimeDate,[@TimeKilllog]);
	$PSSG_Counter[3]++;
}

# Makes Data from input
# $Killer $Victim and $Weapon
#
# 1: Player: wie oft getötet
# 2: Player: wie oft hat er getötet
# 3: Player: wie oft selbst getötet
# 4: Player: Lieblingswaffe (wie oft hat er welche waffe benutzt)
# 5: Player: Angstgegner => wer hat ihn am meisten getötet (wie oft von wem getötet)
# 6: Player: Lieblingsgegner => wen hat er am meisten getötet (wen hat er wie oft getötet)
# (7: wie lang hat wer gespielt)

sub PSSG_MakeData
{
	my $Killer = shift;
	my $Victim = shift;
	my $Weapon = shift;
	
	# Killer	
	PSSG_MakeKillerData($Killer,$Victim,$Weapon);
	
	# Victim
	PSSG_MakeVictimData($Killer,$Victim,$Weapon);
}

sub PSSG_MakeKillerData
{
	my $Killer = shift;
	my $Victim = shift;
	my $Weapon = shift;	
	my $i = 0;
	my $KilledEnemyID = 0;
	my $WeaponID = 0;
	my @PlayerInfo = ("PlayerName",0,0,0,[@PSSG_KilledEnemys],[@PSSG_Weapons],[@PSSG_Weapons],0,0);
	
	# dies ist verantwortlich dafür, falls Kills fehlen
	# musste ich einfügen, als leere Namen in den Stats erschienen. möglicherweise Logfehler
	if ( $Killer eq "" ){return;}
	if ( $Victim eq "" ){return;}
	
	# nachgucken, ob $Killer bereits in $Players vorhanden ist
	$i = PSSG_getPlayerID($Killer);
	
	# wenn noch kein $Killer existiert
	if ( $i eq "NONE" )	
	{
		for ( $i = 0; $i <= 13; $i++ ){$PlayerInfo[$plinxWeaponKill][$i]=0;}
	
		$PlayerInfo[$plinxName] = $Killer;
		
		# wenn selfkill
		if ( $Killer eq $Victim ){$PlayerInfo[$plinxSelfkills]++;}
		
		# ansonsten frag
		else{$PlayerInfo[$plinxKills]++;}
				
		# welche waffe benutzt?
		$WeaponID = PSSG_getWeaponID($Weapon);
		
		if ( $WeaponID eq "NONE" ){}
		else{$PlayerInfo[$plinxWeaponKill][$WeaponID]++;}
		
		$PlayerInfo[$plinxKilledEnemys][$PSSG_Counter[0]] = 0;
		
		# wie oft hat $Killer $Victim getötet?
		$KilledEnemyID = PSSG_getPlayerID($Victim);
		if ( $KilledEnemyID eq "NONE" )
		{$KilledEnemyID = $PSSG_Counter[0];$KilledEnemyID++;$PlayerInfo[$plinxKilledEnemys][$KilledEnemyID] = 0;}
		$PlayerInfo[$plinxKilledEnemys][$KilledEnemyID]++;
		# alle anderen $plinxKilledEnemys mit 0 belegen
		for ( $i = 0; $i < $KilledEnemyID; $i++ ){$PlayerInfo[$plinxKilledEnemys][$i]=0;}		
		$i = $KilledEnemyID;
		for ( $i++; $i <= $PSSG_Counter[0]; $i++ ){$PlayerInfo[$plinxKilledEnemys][$i]=0;}
		
		for ( $i = 0; $i < $PSSG_Counter[0]; $i++ )
		{
			$Players[$i][$plinxKilledEnemys][$PSSG_Counter[0]] = 0;
		}
		
		push(@Players,[@PlayerInfo]);		
		$PSSG_Counter[0]++;
	}
	
	# $Killer existiert bereits
	else
	{
		# selfkill
		if ( $Killer eq $Victim ){$Players[$i][$plinxSelfkills]++;}
		
		# frag
		else{$Players[$i][$plinxKills]++;}
				
		# welche waffe hat $Killer benutzt
		$WeaponID = PSSG_getWeaponID($Weapon);
		if ( $WeaponID eq "NONE" ){}
		else{$Players[$i][$plinxWeaponKill][$WeaponID]++;}		
	
		# wie oft hat $Killer $Victim getötet?
		$KilledEnemyID = PSSG_getPlayerID($Victim);
		if ( $KilledEnemyID eq "NONE" )
		{$KilledEnemyID = $PSSG_Counter[0];$PlayerInfo[$plinxKilledEnemys][$KilledEnemyID] = 0;}
		$Players[$i][$plinxKilledEnemys][$KilledEnemyID]++;
	}
}

sub PSSG_MakeVictimData
{
	my $Killer = shift;
	my $Victim = shift;
	my $Weapon = shift;
	my $i = 0;
	my $PlayerID = 0;
	my $WeaponID = 0;
	my @VictimInfo = ("x",0,0,0,[@PSSG_KilledEnemys],[@PSSG_Weapons],[@PSSG_Weapons],0,0);
	
	# siehe oben in PSSG_MakeKillerData
	if ( $Victim eq "" ){return;}
	if ( $Killer eq "" ){return;}
	
	# existiert $Victim bereits?
	$i = PSSG_getPlayerID($Victim);
	
	# $Victim existiert noch nicht => anlegen
	if ( $i eq "NONE" )	
	{
		for ( $i = 0; $i <= 13; $i++ ){$VictimInfo[$plinxWeaponKill][$i]=0;}
		
		$VictimInfo[$plinxName] = $Victim;
		if ( $Killer ne $Victim ){$VictimInfo[$plinxDeaths]++;}
		
		# welche waffe hat ihn getötet?
		$WeaponID = PSSG_getWeaponID($Weapon);
		if ( $WeaponID eq "NONE" ){}
		else{$VictimInfo[$plinxWeaponKilled][$WeaponID]++;}

		# alle $plinxKilledEnemys mit 0 belegen
		for ( $i = 0; $i <= $PSSG_Counter[0]; $i++ ){$VictimInfo[$plinxKilledEnemys][$i]=0;}
		# allen ausser dem Killer sagen, dass $Victim existiert
		$PlayerID = PSSG_getPlayerID($Killer);
		for ( $i = 0; $i < $PSSG_Counter[0]; $i++ )
		{
			if ( $i == $PlayerID ){}
			else{$Players[$i][$plinxKilledEnemys][$PSSG_Counter[0]] = 0;}
		}
		
		push(@Players,[@VictimInfo]);
		$PSSG_Counter[0]++;
	}
	
	# $Victim existiert schon
	else
	{	
		# Death
		if ( $Killer ne $Victim ){$Players[$i][$plinxDeaths]++;}
				
		# welche waffe hat ihn getötet?
		$WeaponID = PSSG_getWeaponID($Weapon);
		if ( $WeaponID eq "NONE" ){}
		else{$Players[$i][$plinxWeaponKilled][$WeaponID]++;}		
	}
}

sub MakeStats
{
	my $i = 0;
	
	# Favourite Weapon
	for ( $i = 0; $i < $PSSG_Counter[0]; $i++ )
	{
		$Players[$i][$plinxFavouriteWeapon] = MakeStatsWeapons($i,$plinxWeaponKill);
	}
	
	# Feared Weapon
	for ( $i = 0; $i < $PSSG_Counter[0]; $i++ )
	{
		$Players[$i][$plinxFearedWeapon] = MakeStatsWeapons($i,$plinxWeaponKilled);
	}
	
	# Kills
	for ( $i = 0; $i < $PSSG_Counter[0]; $i++ )
	{
		$PSSG_Counter[1] += $Players[$i][$plinxKills];
	}
	
	# Selfkills
	for ( $i = 0; $i < $PSSG_Counter[0]; $i++ )
	{
		$PSSG_Counter[2] += $Players[$i][$plinxSelfkills];
	}
	
	# Zeitraum des Statistikzeitraumes ermitteln
	PSSG_getLogStartTime();	
	PSSG_getLogEndTime();

}

sub MakeStatsWeapons
{
	my $PlayerCounter = shift;
	my $WeaponSwitch = shift;
	
	my $i = 0;	
	my $WeaponCount = 0;
	my $Weapon = 0;
	
	for ( $i = 0; $i <= 13; $i++ )
	{
		if ( $Players[$PlayerCounter][$WeaponSwitch][$i] > $WeaponCount )
		{$WeaponCount=$Players[$PlayerCounter][$WeaponSwitch][$i];$Weapon=$i;}		
	}
	return $Weapon;
}



#
# Ausgabefunktionen
#



sub PSSG_WriteHeader
{
	my $CTIME_String = localtime(time);
	if ( $OutputDirection == 0 ){print "Content-type: text/html\n\n";}
	print '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">', "\n";
	print "<html><head>";
	print "<title>$OutputFileTitle</title>";
	if ( $OutputDirection == 0 )
	{
		open(CSSFILE,$OutputFileCSSFile);
		my @CSSFile = <CSSFILE>;
		close(CSSFILE);
		print "<style type=\"text/css\"><!--";
		foreach(@CSSFile){print "$_";}
		print "--></style>";
	}
	else{print "<link rel=\"stylesheet\" type=\"text/css\" href=";print "\"$OutputFileCSSFile\"";print "/ >";}
	print "</head><body>";
	print "<div align=\"center\">";
	print "<span id=\"PSSG_Header_Title\">$OutputFileTitle</span>";
	print "<br /><br /><br />";
	print "<span id=\"PSSG_Header_StatsCreated\">$PSSG_TextCommon[0] $CTIME_String.</span>";
	print "</div>";
}

sub PSSG_WriteServerStats
{
	print "<div align=\"center\">";
	print "<span id=\"PSSG_Server_TextTitle\">$PSSG_TextServer[0]</span>";
	print "<br /><br />";
	print "<table id=\"PSSG_Server_Table\">";
	print "<tr id=\"PSSG_Server_HeadRow\">";
	print "<td colspan=\"2\"><span id=\"PSSG_Server_HeadTextRow\">$PSSG_TextServer[1]</span></td>";
	print "</tr>";
	# Server Name
	print "<tr class=\"PSSG_Server_Row0\">";
	print "<td id=\"PSSG_Server_HeadName\">";
	print "<span id=\"PSSG_Server_HeadTextName\">$PSSG_TextServer[2]</span>";
	print "</td>";
	print "<td id=\"PSSG_Server_ContentName\">";
	print "<span id=\"PSSG_Server_ContentTextName\">$ServerName</span>";
	print "</td></tr>";
	# Server IP / Port
	print "<tr class=\"PSSG_Server_Row1\">";
	print "<td id=\"PSSG_Server_HeadIPPort\">";
	print "<span id=\"PSSG_Server_HeadTextIPPort\">$PSSG_TextServer[3]</span>";
	print "</td>";
	print "<td id=\"PSSG_Server_ContentIPPort\">";
	print "<span id=\"PSSG_Server_ContentTextIPPort\">$ServerIPPort</span>";
	print "</td></tr>";
	# Anzahl Killlogs
	print "<tr class=\"PSSG_Server_Row0\">";
	print "<td id=\"PSSG_Server_HeadKilllogs\">";
	print "<span id=\"PSSG_Server_HeadTextKilllogs\">$PSSG_TextServer[4]</span>";
	print "</td>";
	print "<td id=\"PSSG_Server_ContentKilllogs\">";
	print "<span id=\"PSSG_Server_ContentTextKilllogs\">$PSSG_Counter[3]";
	if ( $PSSG_Counter[3] == 1 ){print " ($file)";}
	print "</span>";
	print "</td></tr>";
	# Log Period
	print "<tr class=\"PSSG_Server_Row1\">";
	print "<td id=\"PSSG_Server_HeadLogPeriod\">";
	print "<span id=\"PSSG_Server_HeadTextLogPeriod\">$PSSG_TextServer[5]</span>";
	print "</td>";
	print "<td id=\"PSSG_Server_ContentLogPeriod\">";
	print "<span id=\"PSSG_Server_ContentTextLogPeriod\">$PSSG_TimeStats[0] - $PSSG_TimeStats[1]</span>";
	print "</td></tr>";
	# Total Players
	print "<tr class=\"PSSG_Server_Row0\">";
	print "<td id=\"PSSG_Server_HeadTotalPlayers\">";
	print "<span id=\"PSSG_Server_HeadTextTotalPlayers\">$PSSG_TextServer[6]</span>";
	print "</td>";
	print "<td id=\"PSSG_Server_ContentTotalPlayers\">";
	print "<span id=\"PSSG_Server_ContentTextTotalPlayers\">$PSSG_Counter[0]</span>";
	print "</td></tr>";
	# Total Kills
	print "<tr class=\"PSSG_Server_Row1\">";
	print "<td id=\"PSSG_Server_HeadTotalKills\">";
	print "<span id=\"PSSG_Server_HeadTextTotalKills\">$PSSG_TextServer[7]</span>";
	print "</td>";
	print "<td id=\"PSSG_Server_ContentTotalKills\">";
	print "<span id=\"PSSG_Server_ContentTextTotalKills\">$PSSG_Counter[1]</span>";
	print "</td></tr>";	
	# Total Suicides
	print "<tr class=\"PSSG_Server_Row0\">";
	print "<td id=\"PSSG_Server_HeadTotalSuicides\">";
	print "<span id=\"PSSG_Server_HeadTextTotalSuicides\">$PSSG_TextServer[8]</span>";
	print "</td>";
	print "<td id=\"PSSG_Server_ContentTotalSuicides\">";
	print "<span id=\"PSSG_Server_ContentTextTotalSuicides\">$PSSG_Counter[2]</span>";
	print "</td></tr></table>";
	print "</div>";
}

sub PSSG_WritePlayerStats
{
	my $i = 0;
	my $ii = 0;
	my $RowColor = 0;
	my $KD = 0;
	my $EnemyNo1ID = 0;
	my $PlayersToPrint = $PSSG_Counter[0];
	my $FavouriteEnemyID = 0;
	
	if ( $PlayerExtended != 0 )
	{
		if ( $PlayerExtended > $PSSG_Counter[0] ){}
		else{$PlayersToPrint = $PlayerExtended;}
	}

	if ( $EnablePlayerSort == 1 ){PSSG_SortPlayers($PlayerSort);}
	
	print "<div align=\"center\">";
	print "<span id=\"PSSG_Player_TextTitle\">";
	if ( $PlayerExtended != 0 and $EnablePlayerSort == 1 ){print "$PSSG_TextPlayers[0] ";}
	else{print "$PSSG_TextPlayers[1]";}
	if ( $EnablePlayerSort == 1 )
	{
		if ( $PlayerSort == 1 ){print "$PSSG_TextPlayers[2]";}
		if ( $PlayerSort == 2 ){print "$PSSG_TextPlayers[3]";}
		if ( $PlayerSort == 3 ){print "$PSSG_TextPlayers[4]";}
	}
	print "</span>";
	print "<br /><br />";
	print "<table id=\"PSSG_Player_Table\">";
	print "<tr id=\"PSSG_Player_HeadRow\">";
	print "<td id=\"PSSG_Player_HeadRank\"><span id=\"PSSG_Player_HeadTextRank\">$PSSG_TextPlayers[5]</span></td>";
	print "<td id=\"PSSG_Player_HeadPlayer\"><span id=\"PSSG_Player_HeadTextPlayer\">$PSSG_TextPlayers[6]</span></td>";
	print "<td id=\"PSSG_Player_HeadKills\"><span id=\"PSSG_Player_HeadTextKills\">$PSSG_TextPlayers[7]</span></td>";
	print "<td id=\"PSSG_Player_HeadDeaths\"><span id=\"PSSG_Player_HeadTextDeaths\">$PSSG_TextPlayers[8]</span></td>";	
	print "<td id=\"PSSG_Player_HeadSelfKills\"><span id=\"PSSG_Player_HeadTextSelfKills\">$PSSG_TextPlayers[9]</span></td>";
	print "<td id=\"PSSG_Player_HeadKD\"><span id=\"PSSG_Player_HeadTextKD\">$PSSG_TextPlayers[10]</span></td>";
	if ( $PlayerEnableEnemy == 1 or $PlayerEnableEnemy == 3 )
	{print "<td id=\"PSSG_Player_HeadFavouriteEnemy\"><span id=\"PSSG_Player_HeadTextFavouriteEnemy\">$PSSG_TextPlayers[11]</span></td>";}
	if ( $PlayerEnableEnemy == 2 or $PlayerEnableEnemy == 3 )
	{print "<td id=\"PSSG_Player_HeadEnemyNo1\"><span id=\"PSSG_Player_HeadTextEnemyNo1\">$PSSG_TextPlayers[12]</span></td>";}
	if ( $PlayerEnableWeapon == 1 or $PlayerEnableWeapon == 3 )
	{print "<td id=\"PSSG_Player_HeadFavouriteWeapon\"><span id=\"PSSG_Player_HeadTextFavouriteWeapon\">$PSSG_TextPlayers[13]</span></td>";}
	if ( $PlayerEnableWeapon == 2 or $PlayerEnableWeapon == 3 )
	{print "<td id=\"PSSG_Player_HeadFearedWeapon\"><span id=\"PSSG_Player_HeadTextFearedWeapon\">$PSSG_TextPlayers[14]</span></td>";}
	print "</tr>";
	for ( $ii = 0; $ii < $PlayersToPrint; $ii++ )
	{
		if ( $EnablePlayerSort == 1 ){$i = $SortedPlayers[$ii];}
		else{$i=$ii;}
		print "<tr class=\"PSSG_Player_ContentRow$RowColor\">";
		$ii++;
		print "<td class=\"PSSG_Player_ContentRank\">\#$ii</td>";
		$ii--;
		print "<td class=\"PSSG_Player_ContentPlayer\">$Players[$i][$plinxName]</td>";		
		print "<td class=\"PSSG_Player_ContentKills\">$Players[$i][$plinxKills]</td>";		
		print "<td class=\"PSSG_Player_ContentDeaths\">$Players[$i][$plinxDeaths]</td>";
		print "<td class=\"PSSG_Player_ContentSelfkills\">$Players[$i][$plinxSelfkills]</td>";
		
		# Kills-Deaths Verhältnis
		if ($Players[$i][$plinxKills] == 0 ){$KD="n00b";}
		if ($Players[$i][$plinxDeaths] == 0 ){$KD="hrhrhr";}
		else{$KD = $Players[$i][$plinxKills]/($Players[$i][$plinxDeaths]+$Players[$i][$plinxSelfkills]);$KD=substr($KD,0,4);}
		print "<td class=\"PSSG_Player_ContentKD\">$KD</td>";
		
		# Lieblingsgegner
		if ( $PlayerEnableEnemy == 1 or $PlayerEnableEnemy == 3 )
		{
			$FavouriteEnemyID = PSSG_getFavouriteEnemyID($i);
			print "<td class=\"PSSG_Player_ContentFavouriteEnemy\">";
			if ( $Players[$i][$plinxKilledEnemys][$FavouriteEnemyID] == 0 ){print "-";}
			else{print "$Players[$FavouriteEnemyID][$plinxName] ($Players[$i][$plinxKilledEnemys][$FavouriteEnemyID])";}
			print "</td>";
		}
		
		# Angstgegner
		if ( $PlayerEnableEnemy == 2 or $PlayerEnableEnemy == 3 )
		{
			$EnemyNo1ID = PSSG_getEnemyNo1ID($i);
			print "<td class=\"PSSG_Player_ContentEnemyNo1\">";
			if ( $Players[$EnemyNo1ID][$plinxKilledEnemys][$i] == 0 ){print "-";}
			else{print "$Players[$EnemyNo1ID][$plinxName] ($Players[$EnemyNo1ID][$plinxKilledEnemys][$i])";}
			print "</td>";
		}
	
		# Lieblingswaffe
		if ( $PlayerEnableWeapon == 1 or $PlayerEnableWeapon == 3 )
		{
			print "<td class=\"PSSG_Player_ContentFavouriteWeapon\">";
			PSSG_getWeaponName($Players[$i][$plinxFavouriteWeapon]);		
			print " ($Players[$i][$plinxWeaponKill][$Players[$i][$plinxFavouriteWeapon]])</td>";
		}
		
		# Angstwaffe
		if ( $PlayerEnableWeapon == 2 or $PlayerEnableWeapon == 3 )
		{
			print "<td class=\"PSSG_Player_ContentFearedWeapon\">";
			PSSG_getWeaponName($Players[$i][$plinxFearedWeapon]);		
			print " ($Players[$i][$plinxWeaponKilled][$Players[$i][$plinxFearedWeapon]])</td>";
		}
		print "</tr>";
		if ( $RowColor == 0 ){$RowColor=1;}else{$RowColor=0;}
	}
	print "</table>";
	
	# falls nicht alle Spieler in den ausführlichen Player-Stats erscheinen sollen, folgt hier der Rest
	# hier wird $RowColor missbraucht. :>	
	if ( $PlayerExtended != 0 && $PlayerExtended < $PSSG_Counter[0] )
	{
		$RowColor = 0;
		print "<br /><br /><span id=\"PSSG_Player_NotTop_TextTitle\">$PSSG_TextPlayers[15]</span>";
		print "<table id=\"PSSG_Player_NotTop_Table\"><tr class=\"PSSG_Player_NotTop_Row\">";
		for ( $ii = $PlayerExtended; $ii < $PSSG_Counter[0]; $ii++ )
		{
			if ( $EnablePlayerSort == 1 ){$i = $SortedPlayers[$ii];}else{$i=$ii;}
			if ( $RowColor == 5 ){print "</tr><tr class=\"PSSG_Player_NotTop_Row\">";$RowColor=0;}
			if ( $i != $PSSG_Counter[0] ){print "<td>$Players[$i][$plinxName] ($Players[$i][$plinxKills])</td>";}
			else
			{
				for (;$RowColor < 5;$RowColor++)
				{print "<td></td>";}
			}
			$RowColor++;
		}
		print "</table>";
	}	
	print "</div>";
}

sub PSSG_WriteWeaponKillStats
{
	my $i = 0;
	my $ii = 0;
	my $iii = 0;
	my $RowColor = 0;
	my $PlayersToPrint = $PSSG_Counter[0];
	
	if ( $WeaponPlayers != 0 )
	{
		if ( $WeaponPlayers > $PSSG_Counter[0] ){}
		else{$PlayersToPrint = $WeaponPlayers;}
	}
	
	# Player kills by weapon	
	print "<div align=\"center\">";
	print "<span class=\"PSSG_Weapon_TextTitle\">";
	if ( $WeaponPlayers != 0 and $EnablePlayerSort == 1 ){print "$PSSG_TextWeapons[0] $PSSG_TextWeapons[1] ";}
	else{print "$PSSG_TextWeapons[2]";}
	if ( $EnablePlayerSort == 1 )
	{
		if ( $PlayerSort == 1 ){print "$PSSG_TextWeapons[4]";}
		if ( $PlayerSort == 2 ){print "$PSSG_TextWeapons[5]";}
		if ( $PlayerSort == 3 ){print "$PSSG_TextWeapons[6]";}
	}
	print "</span>";	
	print "<br /><br />";		
	
	# primary weapons used for kills
	if ( $EnableWeaponKill == 1 or $EnableWeaponKill == 3 )
	{
		print "<table class=\"PSSG_Weapon_Table\">";
		print "<tr class=\"PSSG_Weapon_Primary_RowWeaponNames\">";
		print "<td><span class=\"PSSG_Weapon_Primary_TextWeapons\">$PSSG_TextWeapons[7]</span></td>";
		for ( $i = 0; $i <= 9; $i++ )
		{
			print "<td><span class=\"PSSG_Weapon_Primary_TextWeaponNames\">$PSSG_PrimaryWeaponsN[$i]</span></td>";
		}	
		print "</tr>";
		for ( $iii = 0; $iii < $PlayersToPrint; $iii++ )
		{
			if ( $EnablePlayerSort == 1 ){$i = $SortedPlayers[$iii];}
			else{$i=$iii;}			
			print "<tr class=\"PSSG_Weapon_Primary_ContentRow$RowColor\">";
			print "<td><span class=\"PSSG_Weapon_Primary_TextPlayerNames\">$Players[$i][$plinxName]</span></td>";
			for ( $ii = 0; $ii <= 9; $ii++ )
			{
				print "<td><span class=\"PSSG_Weapon_Primary_TextWeaponCount\">$Players[$i][$plinxWeaponKill][$ii]</span></td>";
			}
			print "</tr>";
			if ($RowColor==0){$RowColor=1;}else{$RowColor=0;}
		}
		print "</table><br />";
	}
	
	# secondary weapons used for kills
	if ( $EnableWeaponKill == 2 or $EnableWeaponKill == 3 )
	{
		$RowColor = 0;
		print "<table class=\"PSSG_Weapon_Table\">";
		print "<tr class=\"PSSG_Weapon_Secondary_RowWeaponNames\">";
		print "<td><span class=\"PSSG_Weapon_Secondary_TextWeapons\">$PSSG_TextWeapons[8]</span></td>";
		for ( $i = 0; $i <= 3; $i++ )
		{
			print "<td colspan=\"2\">";
			print "<span class=\"PSSG_Weapon_Secondary_TextWeaponNames\">$PSSG_SecondaryWeaponsN[$i]</span>";
			print "</td>";
		}	
		print "<td colspan=\"2\"></td></tr>";
		for ( $iii = 0; $iii < $PlayersToPrint; $iii++ )
		{
			if ( $EnablePlayerSort == 1 ){$i = $SortedPlayers[$iii];}
			else{$i=$iii;}	
			print "<tr class=\"PSSG_Weapon_Secondary_ContentRow$RowColor\"><td>";
			print "<span class=\"PSSG_Weapon_Secondary_TextPlayerNames\">$Players[$i][$plinxName]</span>";
			print "</td>";
			for ( $ii = 10; $ii <= 13; $ii++ )
			{
				print "<td colspan=\"2\">";
				print "<span class=\"PSSG_Weapon_Secondary_TextWeaponCount\">";
				# Notlösung :/
				if ( $Players[$i][$plinxWeaponKill][$ii] == 0 )
				{ print "$Players[$i][$plinxWeaponKill][$ii]</span>";}
				else{print "<b>$Players[$i][$plinxWeaponKill][$ii]</b></span>";}
				print "</td>";
			}
			if ($RowColor==0){$RowColor=1;}else{$RowColor=0;}
			print "<td colspan=\"2\"></td></tr>";
		}
		print "</table>";
	}
	print "</div>";
}

sub PSSG_WriteWeaponDeathStats
{
	my $i = 0;
	my $ii = 0;
	my $iii = 0;
	my $RowColor = 0;
	my $PlayersToPrint = $PSSG_Counter[0];
	
	if ( $WeaponPlayers != 0 )
	{
		if ( $WeaponPlayers > $PSSG_Counter[0] ){}
		else{$PlayersToPrint = $WeaponPlayers;}
	}
	
	# Player deaths by weapon
	print "<div align=\"center\">";
	print "<span class=\"PSSG_Weapon_TextTitle\">";	
	if ( $WeaponPlayers != 0 and $EnablePlayerSort == 1 ){print "$PSSG_TextWeapons[0] $PSSG_TextWeapons[3] ";}
	else{print "$PSSG_TextWeapons[2]";}
	if ( $EnablePlayerSort == 1 )
	{
		if ( $PlayerSort == 1 ){print "$PSSG_TextWeapons[4]";}
		if ( $PlayerSort == 2 ){print "$PSSG_TextWeapons[5]";}
		if ( $PlayerSort == 3 ){print "$PSSG_TextWeapons[6]";}
	}
	print "</span>";
	print "<br /><br />";
	
	# primary weapons
	if ( $EnableWeaponKilled == 1 or $EnableWeaponKilled == 3 )
	{
		print "<table class=\"PSSG_Weapon_Table\">";
		print "<tr class=\"PSSG_Weapon_Primary_RowWeaponNames\">";
		print "<td><span class=\"PSSG_Weapon_Primary_TextWeapons\">$PSSG_TextWeapons[7]</span></td>";
		for ( $i = 0; $i <= 9; $i++ )
		{
			print "<td><span class=\"PSSG_Weapon_Primary_TextWeaponNames\">$PSSG_PrimaryWeaponsN[$i]</span></td>";
		}	
		print "</tr>";
		for ( $iii = 0; $iii < $PlayersToPrint; $iii++ )
		{
			if ( $EnablePlayerSort == 1 ){$i = $SortedPlayers[$iii];}
			else{$i=$iii;}	
			print "<tr class=\"PSSG_Weapon_Primary_ContentRow$RowColor\">";
			print "<td><span class=\"PSSG_Weapon_Primary_TextPlayerNames\">$Players[$i][$plinxName]</span></td>";
			for ( $ii = 0; $ii <= 9; $ii++ )
			{
				print "<td><span class=\"PSSG_Weapon_Primary_TextWeaponCount\">$Players[$i][$plinxWeaponKilled][$ii]</span></td>";
			}
			if ($RowColor==0){$RowColor=1;}else{$RowColor=0;}
			print "</tr>";
		}
		print "</table><br />";
	}
	
	# secondary weapons used for kills
	if ( $EnableWeaponKilled == 2 or $EnableWeaponKilled == 3 )
	{
		$RowColor = 0;
		print "<table class=\"PSSG_Weapon_Table\">";
		print "<tr class=\"PSSG_Weapon_Secondary_RowWeaponNames\"><td>";
		print "<span class=\"PSSG_Weapon_Secondary_TextWeapons\">$PSSG_TextWeapons[8]</span>";
		print "</td>";
		for ( $i = 0; $i <= 3; $i++ )
		{
			print "<td colspan=\"2\">";
			print "<span class=\"PSSG_Weapon_Secondary_TextWeaponNames\">$PSSG_SecondaryWeaponsN[$i]</span>";
			print "</td>";
		}	
		print "<td colspan=\"2\"></td></tr>";
		for ( $iii = 0; $iii < $PlayersToPrint; $iii++ )
		{
			if ( $EnablePlayerSort == 1 ){$i = $SortedPlayers[$iii];}
			else{$i=$iii;}	
			print "<tr class=\"PSSG_Weapon_Secondary_ContentRow$RowColor\"><td>";
			print "<span class=\"PSSG_Weapon_Secondary_TextPlayerNames\">$Players[$i][$plinxName]</span></td>";
			for ( $ii = 10; $ii <= 13; $ii++ )
			{
				print "<td colspan=\"2\">";
				print "<span class=\"PSSG_Weapon_Secondary_TextWeaponCount\">";
				# Notlösung :/
				if ( $Players[$i][$plinxWeaponKill][$ii] == 0 )
				{ print "$Players[$i][$plinxWeaponKill][$ii]</span>";}
				else{print "<b>$Players[$i][$plinxWeaponKill][$ii]</b></span>";}			
				print "</td>";
			}
			if ($RowColor==0){$RowColor=1;}else{$RowColor=0;}
			print "<td colspan=\"2\"></td></tr>";
		}
		print "</table>";
	}
	print "</div>";
}

# Schreibt eine Tabelle, die Aufschluss darüber gibt, wer wen gekillt hat
sub PSSG_WriteWhoKilledWho
{
	my $i = 0;
	my $ii = 0;
	my $iii = 0;
	my $RowColor = 0;
	my $PlayersToPrint = $PSSG_Counter[0];
	
	if ( $WhoKilledWhoPlayers != 0 )
	{
		if ( $WhoKilledWhoPlayers > $PSSG_Counter[0] ){}
		else{$PlayersToPrint = $WhoKilledWhoPlayers;}
	}

	print "<div align=\"center\">";
	print "<span id=\"PSSG_WhoKilledWho_TextTitle\">";
	if ( $WhoKilledWhoPlayers != 0 and $EnablePlayerSort == 1 ){print "$PSSG_TextWhoKilledWho[0] $PSSG_TextWhoKilledWho[1] ";}
	else{print "$PSSG_TextPlayers[1]";}
	if ( $EnablePlayerSort == 1 )
	{
		if ( $PlayerSort == 1 ){print "$PSSG_TextWhoKilledWho[2]";}
		if ( $PlayerSort == 2 ){print "$PSSG_TextWhoKilledWho[3]";}
		if ( $PlayerSort == 3 ){print "$PSSG_TextWhoKilledWho[4]";}
	}
	print "</span>";
	print "<br /><br />";
	print "<table id=\"PSSG_WhoKilledWho_Table\">";
	print "<tr id=\"PSSG_WhoKilledWho_RowPlayerNames\">";
	print "<td id=\"PSSG_WhoKilledWho_TextPlayers\">$PSSG_TextWhoKilledWho[5]</td>";	
	for ( $ii = 0; $ii < $PlayersToPrint; $ii++ )
	{
		#if ( $EnablePlayerSort == 1 ){$i = $SortedPlayers[$ii];}
		#else{$i=$ii;}
		print "<td>";
		$ii++;
		print "<span class=\"PSSG_WhoKilledWho_TextPlayerNames\">#$ii</span>";
		$ii--;
		print "</td>";
	}
	print "</tr>";	
	for ( $ii = 0; $ii < $PlayersToPrint; $ii++ )
	{
		if ( $EnablePlayerSort == 1 ){$i = $SortedPlayers[$ii];}
		else{$i=$ii;}
		print "<tr>";
		print "<td class=\"PSSG_WhoKilledWho_ColumnPlayerNames\">";
		$ii++;		
		print "<span class=\"PSSG_WhoKilledWho_TextPlayerNames\">(#$ii) $Players[$i][$plinxName]</span>";
		$ii--;
		print "</td>";
		for ( $iii = 0; $iii < $PlayersToPrint; $iii++ )
		{
			print "<td class=\"PSSG_WhoKilledWho_Field$RowColor\">";
			print "<span class=\"PSSG_WhoKilledWho_TextKillCount\">$Players[$i][$plinxKilledEnemys][$iii]</span>";
			print "</td>";
		}
		print "</tr>";
		if($RowColor==0){$RowColor=1;}else{$RowColor=0;}
	}	
	print "</table>";
	print "</div>";
}

sub PSSG_WriteOtherStats
{
	my $i = 0;
	my $ii = 0;
	my $Value = 0;
	my $Name = "";
	my $Text = "";
	my $TextPosition1 = 0;
	my $TextPosition2 = 0;

	print "<div align=\"center\">";
	print "<span id=\"PSSG_Other_TextTitle\">$PSSG_TextOther[0]</span>";
	print "<br /><br />";	
	print "<table id=\"PSSG_Other_Table\">";
	print "<tr><td id=\"PSSG_Other_HeadRow\"><span id=\"PSSG_Other_HeadTextRow\">$PSSG_TextOther[1]</span></td></tr>";
	
	# meisten kills
	print "<tr class=\"PSSG_Other_Row$i\"><td>";
	print "<span class=\"PSSG_Other_Text\">";
	$i = PSSG_getPlayerIDOf($plinxKills);$Name="<span class=\"bold\">";$Name.=PSSG_getPlayerName($i);$Name.="</span>";
	$Value = $Players[$i][$plinxKills];
	# muhahahahaha kill mich dafür ^^ aber KOMFORT ist alles :/
	# liest die $PSSG_TextOther aus und interpretiert {NAME} und {VALUE}
	$TextPosition1 = index($PSSG_TextOther[2],"{NAME}");
	if ( $TextPosition1 == 0 ){print $Name;}
	else{$Text = substr($PSSG_TextOther[2],0,$TextPosition1);print $Text;print $Name;}
	$TextPosition1+=6;$TextPosition2 = index($PSSG_TextOther[2],"{VALUE}");
	if ( $TextPosition2 == 0 ){print $Value;}
	else{$Text = substr($PSSG_TextOther[2],$TextPosition1,($TextPosition2-$TextPosition1));print $Text;}
	print $Value;$TextPosition2+=7;
	$Text = substr($PSSG_TextOther[2],$TextPosition2,length($PSSG_TextOther[2])-$TextPosition1);
	print "$Text</span></td></tr>";
	# erst hier ist ENDE ^^
	
	# meisten deaths
	$i = 1;
	print "<tr class=\"PSSG_Other_Row$i\"><td>";
	print "<span class=\"PSSG_Other_Text\">";
	$i = PSSG_getPlayerIDOf($plinxDeaths);$Name="<span class=\"bold\">";$Name.=PSSG_getPlayerName($i);$Name.="</span>";
	$Value = $Players[$i][$plinxDeaths];
	# Ausgabe
	$TextPosition1 = index($PSSG_TextOther[3],"{NAME}");
	if ( $TextPosition1 == 0 ){print $Name;}
	else{$Text = substr($PSSG_TextOther[3],0,$TextPosition1);print $Text;print $Name;}
	$TextPosition1+=6;$TextPosition2 = index($PSSG_TextOther[3],"{VALUE}");
	if ( $TextPosition2 == 0 ){print $Value;}
	else{$Text = substr($PSSG_TextOther[3],$TextPosition1,($TextPosition2-$TextPosition1));print $Text;}
	print $Value;$TextPosition2+=7;
	$Text = substr($PSSG_TextOther[3],$TextPosition2,length($PSSG_TextOther[3])-$TextPosition1);
	print "$Text</span></td></tr>";
	
	# meisten selfkills
	$i = 0;
	print "<tr class=\"PSSG_Other_Row$i\"><td>";
	print "<span class=\"PSSG_Other_Text\">";
	$i = PSSG_getPlayerIDOf($plinxSelfkills);
	$Name = "<span class=\"bold\">";$Name .= PSSG_getPlayerName($i);$Name.="</span>";		
	$Value = $Players[$i][$plinxSelfkills];
	# Ausgabe
	$TextPosition1 = index($PSSG_TextOther[4],"{NAME}");
	if ( $TextPosition1 == 0 ){print $Name;}
	else{$Text = substr($PSSG_TextOther[4],0,$TextPosition1);print $Text;print $Name;}
	$TextPosition1+=6;$TextPosition2 = index($PSSG_TextOther[4],"{VALUE}");
	if ( $TextPosition2 == 0 ){print $Value;}
	else{$Text = substr($PSSG_TextOther[4],$TextPosition1,($TextPosition2-$TextPosition1));print $Text;}
	print $Value;$TextPosition2+=7;
	$Text = substr($PSSG_TextOther[4],$TextPosition2,length($PSSG_TextOther[4])-$TextPosition1);
	print "$Text</span></td></tr>";
		
	# welche Primärwaffe wurde am meisten zum Töten benutzt
	$i = 1;
	print "<tr class=\"PSSG_Other_Row$i\"><td>";
	print "<span class=\"PSSG_Other_Text\">";
	$i = PSSG_getMostUsedPrimaryWeaponKill();
	for ( $ii = 0; $ii < $PSSG_Counter[0]; $ii++ ){$Value+=$Players[$ii][$plinxWeaponKill][$i];}
	$Name = "<span class=\"bold\">";$Name .= $PSSG_PrimaryWeaponsN[$i];$Name.="</span>";
	# Ausgabe
	$TextPosition1 = index($PSSG_TextOther[5],"{NAME}");
	if ( $TextPosition1 == 0 ){print $Name;}
	else{$Text = substr($PSSG_TextOther[5],0,$TextPosition1);print $Text;print $Name;}
	$TextPosition1+=6;$TextPosition2 = index($PSSG_TextOther[5],"{VALUE}");
	if ( $TextPosition2 == 0 ){print $Value;}
	else{$Text = substr($PSSG_TextOther[5],$TextPosition1,($TextPosition2-$TextPosition1));print $Text;}
	print $Value;$TextPosition2+=7;
	$Text = substr($PSSG_TextOther[5],$TextPosition2,length($PSSG_TextOther[5])-$TextPosition2);
	print "$Text</span></td></tr>";
	
	# welche Sekundärwaffe wurde am meisten zum Töten benutzt
	$i = 0;
	print "<tr class=\"PSSG_Other_Row$i\"><td>";
	print "<span class=\"PSSG_Other_Text\">";
	$i = PSSG_getMostUsedSecondaryWeaponKill();
	$i+=10;$Value = 0;
	for ( $ii = 0; $ii < $PSSG_Counter[0]; $ii++ ){$Value+=$Players[$ii][$plinxWeaponKill][$i];}
	$i-=10;
	$Name = "<span class=\"bold\">";$Name .= $PSSG_SecondaryWeaponsN[$i];$Name.="</span>";	
	# Ausgabe
	$TextPosition1 = index($PSSG_TextOther[6],"{NAME}");
	if ( $TextPosition1 == 0 ){print $Name;}
	else{$Text = substr($PSSG_TextOther[6],0,$TextPosition1);print $Text;print $Name;}
	$TextPosition1+=6;$TextPosition2 = index($PSSG_TextOther[6],"{VALUE}");
	if ( $TextPosition2 == 0 ){print $Value;}
	else{$Text = substr($PSSG_TextOther[6],$TextPosition1,($TextPosition2-$TextPosition1));print $Text;}
	print $Value;$TextPosition2+=7;
	$Text = substr($PSSG_TextOther[6],$TextPosition2,length($PSSG_TextOther[6])-$TextPosition2);
	print "$Text</span></td></tr>";	
	
	# welche waffen wurden überhaupt genutzt
	# welche waffen wurde nicht genutzt
	# wer war angstgegner von wem
	
	print "</table>";
	print "</div>";
}

sub PSSG_WriteStats
{
	# Header
	PSSG_WriteHeader();
	print "<br /><br /><br />";
	
	# Server Stats
	if ( $EnableServer != 0 ){PSSG_WriteServerStats();}
	print "<br /><br /><br />";
	
	# Player Stats
	if ( $EnablePlayer != 0 ){PSSG_WritePlayerStats();}
	print "<br /><br /><br />";
	
	# Weapon-Stats: Wer killte wie oft mit welcher Waffe
	if ( $EnableWeaponKill != 0 ){PSSG_WriteWeaponKillStats();}
	print "<br /><br /><br />";

	# Weapon-Stats: Wer starb wie oft durch welche Waffe
	if ( $EnableWeaponKilled != 0 ){PSSG_WriteWeaponDeathStats();}
	print "<br /><br /><br />";
	
	# Who Killed Who
	if ( $EnableWhoKilledWho != 0 ){PSSG_WriteWhoKilledWho();}
	print "<br /><br /><br />";
	
	# Other Stats
	if ( $EnableOther != 0 ){PSSG_WriteOtherStats();}
	print "<br /><br /><br />";

	# Write Footer
	print "<br /><br /><br />";
	print "<div align=\"center\"><span id=\"PSSG_Footer\">Stats generated by pssg $PSSG_Version<br />";
	print "<b>P</b>erl <b>S</b>oldat <b>S</b>tats <b>G</b>enerator by siranus</span></div>";
	print "</body></html>";
}