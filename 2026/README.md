# Modul Suchmaschinentechnologie BIM-25

# Installation der erforderlichen Infrastruktur

## git

**git** ist ein Versionskontrollsystem, das wir für die Verwaltung von Quellcode im Modul Suchmaschinentechnologie
verwenden werden. Der Quellcode sämtlicher Programme sowie die benötigten Konfigurationsdateien werden über ein
git-Repository auf GitHub verteilt. Hierzu existiert bei GitHub das öffentliches Projekt **suma-tech**
(https://github.com/saschaszott/suma-tech). git erlaubt es Ihnen zudem lokal ausgeführte Änderungen an Quelltexten und
Konfigurationsdateien zu versionieren, so dass Sie den Änderungsverlauf der Dateien später einfach nachvollziehen
können. Auch im Hinblick auf eine spätere Masterarbeit mit Implementierungsanteil ist die Beschäftigung mit git sehr zu
empfehlen. In der Vorlesung werde ich Ihnen noch im Detail die Arbeit mit dem Versionskontrollsystem git erklären.

Die Installation von git unterscheidet sich je nach Betriebssystem:

*	Windows: git-Installer von der offiziellen Website https://git-scm.com/install/windows herunterladen und ausführen
    (Standardoptionen des Installationsassistenten sind in der Regel ausreichend).
*	macOS: sofern git noch nicht installiert ist (Prüfung im Terminal mittels `git --version`) kann git über
    den Paketmanager Homebrew (mittels `brew install git`) installiert werden.
*	Linux (z. B. Ubuntu, Debian): Terminal öffnen und git mittels APT-Paketmanager installieren:
    `sudo apt update && sudo apt install git`.

Nach der Installation von git kann mit dem Befehl `git --version` auf der Kommandozeile geprüft werden, ob git korrekt
installiert wurde. Beachten Sie bitte, dass Sie eine aktuelle git-Version (Versionsnummer 2.50 oder höher) besitzen.

Sie können git mit dem Kommandozeilenbefehl `git <command>` bedienen (oder später mit der graphischen Oberfläche von
Visual Studio Code). Sofern Sie zusätzlich eine graphische Benutzeroberfläche bevorzugen, können Sie optional einen
graphischen git-Client installieren. Eine Liste der verfügbaren git-Clients finden Sie beispielsweise unter
https://git-scm.com/downloads/guis

## Visual Studio Code

**Visual Studio Code** (auch **VS Code**) ist ein Quelltexteditor aus dem Hause Microsoft. Er bietet Syntax-Highlighting,
Autovervollständigung, integrierte git-Unterstützung, Debugging-Tools und eine große Auswahl an Erweiterungen für viele
Programmiersprachen und Entwicklungsumgebungen.

Die Installationsdatei von VS Code kann kostenfrei unter https://code.visualstudio.com/Download heruntergeladen werden.
Für Windows und macOS empfiehlt sich der Installationsassistent. Unter Linux können Sie VS Code auch über die
Kommandozeile installieren. Für Ubuntu gibt es sogar ein Snap-Paket.

## Python

**Python** ist eine weit verbreitete, leicht verständliche Programmiersprache, die sich besonders gut für Einsteiger
eignet. Sie wird häufig in der Data Science / Datenanalyse, Künstlichen Intelligenz, Webentwicklung oder der
Automatisierung eingesetzt. Python ist bekannt für seine klare Syntax, eine große Standardbibliothek und eine aktive
Community. Bitte beachten Sie, dass wir Python in einer aktuellen Version (Versionsnummer 3.13 oder höher) verwenden.

Den Python-Installer für Windows können Sie unter https://www.python.org/downloads/windows/ herunterladen (Sie benötigen
Windows 10 oder höher). Unter macOS bietet sich - analog zu git - die Installation mittels Homebrew an (mittels
`brew install python`). Linux-Nutzende können ebenfalls Python mittels Paket-Manager installieren, z.B. unter Ubuntu
mittels `sudo apt update && sudo apt install python3 python3-pip`.

Nach der Installation können Sie mit dem Befehl `python3 --version` prüfen, ob Sie eine aktuelle Version auf Ihrem
System installiert haben. Es wird empfohlen die Python-Version mit der Versionsnummer 3.13 oder höher zu verwenden.

Wir werden im Verlauf der Vorlesung verschiedene Python-Programmbibliotheken benötigen. Für die Installation der
erforderlichen Python-Pakete werden wir den Python-Paketmanager `pip` nutzen. Optional kann auch der Paketmanager
`conda` verwendet werden, der z.B. bei der Installation von Anaconda automatisch installiert wird.

## Docker

Wir werden uns im Modul Suchmaschinentechnologie intensiv mit der Open Source Software **Apache Solr** auseinandersetzen.

Zur (einfachen) Installation und Ausführung von Solr werden wir **Docker** verwenden.

Docker ist eine Plattform zur Container-Virtualisierung, die es ermöglicht, Softwareanwendungen samt ihrer
Abhängigkeiten in einer isolierten Umgebung – einem sogenannten **Container** – auszuführen. Im Gegensatz zu klassischen
virtuellen Maschinen (VMs) sind Container deutlich leichtgewichtiger. Ein Docker Container ist eine abgeschlossene
Umgebung, die auf jedem System (Docker Host) identisch funktioniert, unabhängig davon, welches Betriebssystem oder
welche Software auf dem Docker Host installiert ist.

Wir werden Docker verwenden, um einen Solr-Server in einem Docker Container auszuführen. Der Docker Container stellt
hierbei sicher, dass alle für die Ausführung des Solr-Servers erforderlichen Komponenten (z.B. Java Laufzeitumgebung,
Konfigurationsdateien) zur Verfügung stehen. Für Sie wird dadurch der Installationsaufwand deutlich reduziert.

Ein **Docker Image** ist eine Art Vorlage oder Bauplan für einen Docker-Container. Das Image enthält alle benötigten
Dateien, Programme und Programmbibliotheken sowie Konfigurationen, um eine gewünschte Anwendung ausführen zu können.

Ein **Docker Container** ist eine laufende Instanz eines Images, vergleichbar mit einem Programm, das aus einer
ausführbaren Datei gestartet wird.

Normalerweise müsste Solr manuell installiert, konfiguriert und mit den richtigen Abhängigkeiten versehen werden. Mit
Docker genügt ein einziger Befehl, um Solr in einer standardisierten Umgebung zu starten – unabhängig vom
Betriebssystem des Hosts. Das macht die Nutzung für alle Studierenden einheitlich und vermeidet typische
Installationsprobleme.

## Docker Desktop

Die **Docker Engine** ist das Herzstück von Docker. Sie führt die Container aus und verwaltet sie.
Auf Linux-Systemen wird die Docker Engine direkt im Betriebssystem installiert. Da Windows und macOS jedoch anders
funktionieren, stellt **Docker Desktop** eine benutzerfreundliche Oberfläche zur Verfügung, die die Docker Engine in
einer speziellen Umgebung (z. B. per WSL2 oder virtueller Maschine) integriert. Docker Desktop ermöglicht es uns,
Container einfach zu starten, zu stoppen und zu verwalten, entweder per grafischer Oberfläche (GUI) oder über die
Kommandozeile (über docker Befehle).

Für Docker Desktop stehen Installationsdateien für alle gängigen (aktuellen) Betriebssysteme zur Verfügung:

* Docker Desktop für **Windows** (10 und 11) unter https://docs.docker.com/desktop/setup/install/windows-install/
* Docker Desktop für **MacOS** unter https://docs.docker.com/desktop/setup/install/mac-install/
* Docker Desktop für **Linux** unter https://docs.docker.com/desktop/setup/install/linux/

Bitte stellen Sie sicher, dass Sie eine aktuelle Version (4.75.0 oder höher) von Docker Desktop installieren.
Sofern Sie Docker Desktop installiert haben, können Sie die Versionsnummer in der graphischen Oberfläche von
Docker Desktop ermitteln (die Versionsnummer steht unten rechts in der Statuszeile).

Wichtige Hinweise zur Installation von Docker Desktop unter **Windows** finden Sie in der Dokumentation unter:

https://docs.docker.com/desktop/setup/install/windows-install/

Beachten Sie insbesondere folgenden Hinweis:

> If your admin account is different to your user account, you must add the user to the `docker-users` group:

```
net localgroup docker-users <user> /add
```

Für Linux sollten Sie Ihren Benutzeraccount zur Gruppe `docker` hinzufügen:

```sh
sudo usermod -aG docker $USER
```

Wir benötigen zudem die Software **Docker Compose**. Docker Compose ist in der aktuellen Version von Docker Desktop
bereits enthalten, so dass keine zusätzliche Installation erforderlich ist.

## Git-Repository suma-tech in VS Code klonen

Starten Sie nun das zuvor installierte Programm Visual Studio Code. Wählen Sie im Menü _Anzeigen_ den Eintrag
_Quellcodeverwaltung_.

Auf der linken Seite erscheint der Bereich _Quellcodeverwaltung_. Klicken Sie auf den Button _Repository klonen_. 
Geben Sie nun die Repository-URL ein: https://github.com/saschaszott/suma-tech.git

Sie können nun ein beliebiges Arbeitsverzeichnis auf Ihrem Rechner festlegen, in dem das git-Repository `suma-tech`
heruntergeladen wird. Nehmen wir an, dass Sie als Arbeitsverzeichnis `sumatech2026` auswählen, dann existiert in diesem
Verzeichnis nach dem Klonen das Unterverzeichnis `suma-tech`. Alle Pfadangaben, die im Folgenden angegeben werden, sind
relativ zum Arbeitsverzeichnis.

Wählen Sie nach dem Klonen im Dialog _Möchten Sie das geklonte Repository öffnen?_ den Button _Öffnen_.

Auf der linken Seite wird nun der Inhalt des Verzeichnis `suma-tech` angezeigt. Wählen Sie das Unterverzeichnis `2026`
und anschließend das Unterverzeichnis `solr`. Klicken Sie im Kontextmenü (rechte Maustaste) den Eintrag
_In integriertem Terminal öffnen_.


## Test der Docker-Installation: Ausführung eines Docker Containers

Sie können testweise einen Container starten, der `Hello from Docker!` auf der Kommandozeile ausgibt. Geben Sie dazu
im soeben geöffneten Terminal folgenden Befehl ein:

```sh
docker run hello-world
```

Die erfolgreiche Ausführung des Befehls sollte folgende Ausgabe ergeben (die Ausgabe kann je nach Host-Betriebssytem
leicht variieren):

```
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
58dee6a49ef1: Pull complete
Digest: sha256:0e760fdfbc48ba8041e7c6db999bb40bfca508b4be580ac75d32c4e29d202ce1
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (arm64v8)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

Nun erklären wir kurz, was nach der Eingabe des Befehls `docker run hello-world` passiert ist.

Zunächst überprüft Docker, ob das benötigte Docker Image mit dem Namen `hello-world` bereits auf dem Rechner vorhanden
ist. Ist das nicht der Fall, so wird das Docker Image automatisch aus **Docker Hub** heruntergeladen. Docker Hub ist ein
öffentliches Repository für Container-Images. Aus Sicherheitsgründen sollten Sie darauf achten, nur vertrauenswürdige
Docker Images aus dem Docker Hub herunterzuladen. Vertrauenswürdige Images erkennen Sie z.B. an dem Zusatz
_Docker Official Image_.

Nachdem das Docker Image heruntergeladen wurde, startet Docker anschließend einen Container, d.h. eine isolierte
Umgebung, in der das Image ausgeführt wird.

Das Docker Image `hello-world` enthält ein kleines Programm, das lediglich eine Begrüßungsnachricht ausgibt. Sobald der
Container gestartet ist, führt er dieses Programm aus und zeigt die Meldung `Hello from Docker!` an. Damit bestätigt
Docker, dass die Installation erfolgreich ist und korrekt funktioniert. Nachdem die Nachricht ausgegeben wurde, beendet
sich der Container automatisch, da er seine Aufgabe erfüllt hat.

## Installation von Apache Solr in einem Docker Container

Führen Sie nun den folgenden Befehl aus, um einen Docker Container mit dem Namen `solr-server` zu erzeugen, in dem
schließlich ein Solr Server gestartet wird:

```sh
# wir gehen davon aus, dass Sie sich im Verzeichnis suma-tech/2026/solr befinden
docker compose up -d
```

Der `docker compose` Befehl liest die Datei `docker-compose.yml` ein (aus dem Verzeichnis `suma-tech/2026/solr`). In
dieser Datei sind die Dienste (Services) definiert, die beim Start (`up`) in einzelnen Docker Containern gestartet
werden. In unserem Fall steht in der Datei nur ein Service mit dem Namen `solr`. Dazu wird zuerst das offizielle Docker
Image `solr:10.0.0` aus dem Docker Hub heruntergeladen. Anschließend wird ein Docker Container mit dem Namen
`solr-server` erzeugt, in dem schließlich ein Solr-Server gestartet wird. Die Option `-d` im obigen Befehl führt dazu,
dass der Container im Hintergrund ausgeführt wird und nach der Beendigung des Befehls weiterhin ausgeführt wird.

Damit haben wir unser Ziel erreicht.

Nachdem die Befehlsausführung beendet wurde, sollten Sie folgende Meldung sehen:

```sh
 ✔ Container solr-server  Started
 ```

Anschließend können Sie auf ihrem Rechner die Web-Admin-Oberfläche des Solr-Servers im Browser unter der URL

```
http://localhost:8983
```

aufrufen. Schauen Sie sich in der Admin-Oberfläche etwas um. Wir werden in der Vorlesung intensiv mit der Oberfläche
arbeiten.

## Basisbefehle für das Arbeiten mit Docker Containern

Nun möchte ich Ihnen noch einige Befehle vorstellen, die Sie für die Verwaltung des Docker Containers nutzen können.

Zum **Stoppen** des Docker Containers `solr-server` können Sie folgenden Befehl verwenden:

```sh
docker stop solr-server
```

Anschließend lässt sich der Container wieder hochfahren mittels:

```sh
docker start solr-server
```

Um zu prüfen, ob der Container `solr-server` bereits ausgeführt wird, kann folgender Befehl genutzt werden:

```sh
docker ps -f "name=solr-server"
```

Wenn der Container nicht ausgeführt wird, so kann folgender Befehl genutzt werden (um zu prüfen, ob der Container
gestoppt wurde):

```sh
docker ps -a -f "name=solr-server"
```

Nach der Änderung von Konfigurationsdateien im Solr-Server muss der Solr-Server ggf. neu gestartet werden. Dies kann in
einem Befehl erreicht werden:

```sh
docker restart solr-server
```

Der Docker Container `solr-server` kann entfernt werden mittels

```sh
docker compose down
```

Das lokale Verzeichnis `suma-tech/2026/solr/solrdata` wird beim Entfernen des Docker Containers **nicht** gelöscht, da
es als Bind Mount eingebunden ist (siehe unten).

Ein neuer Docker Container kann erzeugt werden mittels

```sh
docker compose up -d
```

### Bind Mounts: Dateien zwischen Docker Host und Container teilen

Docker-Container sind isolierte Umgebungen, und standardmäßig gehen alle darin gespeicherten Daten verloren, sobald der
Docker Container gelöscht wird. Um Daten persistent zu speichern, nutzt man **Docker Volumes** oder **Bind Mounts**
(Volumes eher für Produktivszenarien; Bind Mounts für lokale Entwicklungsumgebungen).

Ein **Bind Mount** ermöglicht es, ein Verzeichnis oder eine Datei vom Docker Host direkt in einen Docker-Container
einzubinden. Anders als **Docker Volumes**, die von Docker verwaltet werden, nutzt ein Bind Mount einen festen Pfad im
Dateisystem des Docker Host. Alle Änderungen in diesem Verzeichnis wirken sich sowohl im Docker Container als auch auf
dem Docker Host aus. Ein Bind Mount ist praktisch für die lokale Entwicklung, da Änderungen an Dateien (Quellcode,
Konfigurationsdateien), die auf dem Docker Host erfolgen, sofort im Container verfügbar sind. Ferner erlaubt ein Bind
Mount den Zugriff auf Konfigurationsdateien oder Protokolldateien (Log-Files) von Diensten, die im Docker Container
ausgeführt wird, außerhalb des Containers.

In der Datei `docker-compose.yml` ist ein Bind Mount definiert:


```yml
    volumes:
      - ./solrdata:/var/solr
```

Dadurch wird das Verzeichnis `solrdata` (innerhalb des Verzeichnisses, in dem die Datei `docker-compose.yml` gespeichert
ist, d.h. innerhalb von `suma-tech/2026/solr/solrdata`) des Docker Host mit dem Verzeichnis `/var/solr` im Docker
Container verbunden. Alle Änderungen, die innerhalb dieses Verzeichnisses (auch in Unterverzeichnissen) ausgeführt
werden, sind im Docker Host und Container sichtbar. Werden z.B. vom Solr-Server (der im Container ausgeführt wird)
Dateien in diesem Verzeichnis gespeichert, so können Sie im Docker Host ebenfalls auf diese Dateien zugreifen.

Im Unterverzeichnis `suma-tech/2026/solr/solrdata/logs` werden die Protkolldateien (Log-Files) des Solr-Servers
gespeichert. Die wichtigste Logdatei eines Solr-Servers heißt `solr.log`. Falls unerwartete Probleme beim Betrieb eines
Solr-Servers bzw. bei Indexierung oder Suche auftreten, kann man dort nach möglichen Fehlerursachen suchen.

Die Logdatei wird automatisch rotiert (`solr.log.1` usw.).

Die Logausgabe des Solr-Servers kann auch mit folgenden Befehl (ausgeführt auf dem Docker Host) fortlaufend ausgegeben
werden:

```sh
docker logs -f solr-server
```

Alternativ kann die Datei `suma-tech/2026/solr/solrdata/logs/solr.log` im Dateisystem des Docker Hosts aufgerufen
werden, um die Lognachrichten des Solr-Servers einzusehen.
