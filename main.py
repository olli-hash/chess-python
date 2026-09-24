import pygame

pygame.init()

# Schachbrett-Konfiguration
ANZAHL_FELDER = 8
FELD_GROESSE = 80

breite = ANZAHL_FELDER * FELD_GROESSE
hoehe = ANZAHL_FELDER * FELD_GROESSE

fenster = pygame.display.set_mode((breite, hoehe))
pygame.display.set_caption("Quadrat auf einem Schachbrett")

# Farben
HELL = (240, 217, 181)
DUNKEL = (181, 136, 99)
ROT = (220, 50, 50)

# Spieler – exakt so groß wie ein Feld
spieler = pygame.Rect(0, 0, FELD_GROESSE, FELD_GROESSE)
geschwindigkeit = 5

# Werte für die Zentrierungsanimation
zentrierung_aktiv = False
start_x = 0
start_y = 0
ziel_x = 0
ziel_y = 0
animationszeit = 0.0
ANIMATIONSDAUER = 0.35

uhr = pygame.time.Clock()
laeuft = True
war_in_bewegung = False


def feld_mit_meister_ueberdeckung(rechteck):
    """Findet das Feld, das vom Quadrat am stärksten überdeckt wird."""
    bestes_feld = (0, 0)
    groesste_ueberdeckung = -1

    for zeile in range(ANZAHL_FELDER):
        for spalte in range(ANZAHL_FELDER):
            feld = pygame.Rect(
                spalte * FELD_GROESSE,
                zeile * FELD_GROESSE,
                FELD_GROESSE,
                FELD_GROESSE,
            )

            schnittflaeche = rechteck.clip(feld)
            ueberdeckung = schnittflaeche.width * schnittflaeche.height

            if ueberdeckung > groesste_ueberdeckung:
                groesste_ueberdeckung = ueberdeckung
                bestes_feld = (spalte, zeile)

    return bestes_feld


def zentrierung_starten():
    """Startet die Animation zum am stärksten überdeckten Feld."""
    global zentrierung_aktiv
    global start_x, start_y, ziel_x, ziel_y, animationszeit

    spalte, zeile = feld_mit_meister_ueberdeckung(spieler)

    start_x = spieler.x
    start_y = spieler.y
    ziel_x = spalte * FELD_GROESSE
    ziel_y = zeile * FELD_GROESSE
    animationszeit = 0.0
    zentrierung_aktiv = True


while laeuft:
    delta_zeit = uhr.tick(60) / 1000.0

    for ereignis in pygame.event.get():
        if ereignis.type == pygame.QUIT:
            laeuft = False

    tasten = pygame.key.get_pressed()

    bewegt_sich = (
        tasten[pygame.K_LEFT]
        or tasten[pygame.K_RIGHT]
        or tasten[pygame.K_UP]
        or tasten[pygame.K_DOWN]
    )

    # Wenn während der Animation erneut eine Taste gedrückt wird,
    # wird die Animation abgebrochen.
    if bewegt_sich and zentrierung_aktiv:
        zentrierung_aktiv = False

    # Quadrat bewegen, solange eine Pfeiltaste gedrückt wird
    if bewegt_sich and not zentrierung_aktiv:
        if tasten[pygame.K_LEFT]:
            spieler.x -= geschwindigkeit
        if tasten[pygame.K_RIGHT]:
            spieler.x += geschwindigkeit
        if tasten[pygame.K_UP]:
            spieler.y -= geschwindigkeit
        if tasten[pygame.K_DOWN]:
            spieler.y += geschwindigkeit

        # Innerhalb des Schachbretts bleiben
        spieler.clamp_ip(fenster.get_rect())

    # Übergang von "bewegt sich" zu "steht still":
    # Der Benutzer hat die Taste losgelassen.
    if war_in_bewegung and not bewegt_sich and not zentrierung_aktiv:
        zentrierung_starten()

    war_in_bewegung = bewegt_sich

    # Zentrierungsanimation ausführen
    if zentrierung_aktiv:
        animationszeit += delta_zeit
        fortschritt = min(animationszeit / ANIMATIONSDAUER, 1.0)

        # Ease-in: erst langsam, dann schneller
        fortschritt = fortschritt ** 2

        spieler.x = round(start_x + (ziel_x - start_x) * fortschritt)
        spieler.y = round(start_y + (ziel_y - start_y) * fortschritt)

        if animationszeit >= ANIMATIONSDAUER:
            spieler.x = ziel_x
            spieler.y = ziel_y
            zentrierung_aktiv = False

    # Schachbrett zeichnen
    for zeile in range(ANZAHL_FELDER):
        for spalte in range(ANZAHL_FELDER):
            if (zeile + spalte) % 2 == 0:
                farbe = HELL
            else:
                farbe = DUNKEL

            x = spalte * FELD_GROESSE
            y = zeile * FELD_GROESSE

            pygame.draw.rect(
                fenster,
                farbe,
                (x, y, FELD_GROESSE, FELD_GROESSE),
            )

    # Quadrat zeichnen
    pygame.draw.rect(fenster, ROT, spieler)

    pygame.display.flip()

pygame.quit()
