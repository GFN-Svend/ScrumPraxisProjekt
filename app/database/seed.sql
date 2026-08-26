-- 66 fiktive Katzenmeldungen für die Demo-Datenbank.
-- Fehlende Meldungen werden bei jedem App-Start ergänzt; vorhandene bleiben erhalten.

BEGIN TRANSACTION;

INSERT INTO anliegen
    (titel, beschreibung, kategorie, ort, foto_pfad, datum, status)
SELECT column1, column2, column3, column4, column5, column6, column7
FROM (
    VALUES
        -- Nachrichtenkette: Kater Karlo und die nächtliche Irrfahrt
        ('Betrunkene Katze fährt in ein KFC', 'Kater Karlo entwendete einen Lieferwagen, verwechselte offenbar Gas und Bremse und beendete seine Fahrt im Eingangsbereich des KFC. Menschen und Katzen blieben unverletzt.', 'Verkehr', 'Hähnchenring 7', 'img/news/01-kfc-unfall.png', '2026-02-01 23:48:00', 'in_bearbeitung'),
        ('Polizei findet Katzenminze in Karlos Lieferwagen', 'Bei der Untersuchung des Lieferwagens entdeckte die Katzenpolizei drei offene Beutel besonders kräftiger Katzenminze. Kater Karlo bestreitet, während der Fahrt daran geschnuppert zu haben.', 'Polizeimeldung', 'Polizeirevier Nord', 'img/news/02-katzenminze-ermittlung.png', '2026-02-02 10:15:00', 'in_bearbeitung'),
        ('KFC-Filiale eröffnet provisorischen Katzenschalter', 'Nach dem Unfall verkauft die beschädigte Filiale vorübergehend ausschließlich durch ein Seitenfenster. Katzen erhalten dort als Entschuldigung ein kleines Schälchen Wasser.', 'Gastronomie', 'Hähnchenring 7', 'img/news/03-katzenschalter.png', '2026-02-03 12:30:00', 'offen'),
        ('Kater Karlo übernimmt Verantwortung für KFC-Unfall', 'Karlo entschuldigte sich öffentlich und versprach, den Lieferwagen künftig nur noch mit gültigem Katzenführerschein zu bewegen.', 'Gemeinschaft', 'Rathausplatz', 'img/news/04-karlo-entschuldigung.png', '2026-02-05 16:00:00', 'erledigt'),
        ('KFC nach Katzenunfall wieder vollständig geöffnet', 'Die Eingangstür wurde repariert. Kater Karlo durchschnitt gemeinsam mit Filialkatze Nugget das rote Band zur Wiedereröffnung.', 'Gastronomie', 'Hähnchenring 7', 'img/news/05-kfc-wiedereroeffnung.png', '2026-02-12 11:00:00', 'erledigt'),

        -- Nachrichtenkette: Bürgermeisterkatze verschwunden
        ('Bürgermeisterkatze Minka spurlos verschwunden', 'Minka wurde zuletzt am Morgen auf dem Balkon des Rathauses gesehen. Die Stadt bittet alle Katzen um Hinweise und raschelnde Leckerlibeutel.', 'Vermisst', 'Rathausplatz 1', 'img/news/06-minka-vermisst.png', '2026-03-04 09:20:00', 'in_bearbeitung'),
        ('Pfotenabdrücke führen zum alten Glockenturm', 'Die Suche nach Bürgermeisterkatze Minka konzentriert sich auf den Glockenturm. Frische Pfotenabdrücke und ein halb gegessener Thunfischsnack wurden gefunden.', 'Vermisst', 'Kirchplatz', NULL, '2026-03-04 18:45:00', 'in_bearbeitung'),
        ('Feuerwehr rettet Minka aus dem Glockenturm', 'Die vermisste Bürgermeisterkatze saß wohlbehalten neben der großen Glocke und weigerte sich zunächst, ohne ihre Lieblingsdecke herunterzukommen.', 'Rettung', 'Kirchplatz', NULL, '2026-03-05 07:35:00', 'erledigt'),
        ('Minka dankt ihren Retterkatzen mit Rathausfest', 'Beim spontanen Fest wurden Thunfischhäppchen verteilt. Minka kündigte außerdem ein neues Sicherheitsgitter für den Rathausbalkon an.', 'Veranstaltung', 'Rathausplatz 1', NULL, '2026-03-07 14:00:00', 'erledigt'),

        -- Nachrichtenkette: geheimnisvoller Tunnel unter dem Marktplatz
        ('Kätzchen entdeckt geheimen Tunnel unter dem Marktplatz', 'Beim Spielen mit einem Wollknäuel fand die junge Katze Pixel einen lockeren Pflasterstein und darunter den Eingang zu einem bislang unbekannten Tunnel.', 'Entdeckung', 'Marktplatz', NULL, '2026-03-18 15:10:00', 'in_bearbeitung'),
        ('Katzenarchäologen untersuchen Marktplatztunnel', 'Ein Team der Universität fand alte Futternäpfe, Wandzeichnungen und eine erstaunlich gut erhaltene Spielzeugmaus.', 'Forschung', 'Marktplatz', NULL, '2026-03-20 10:40:00', 'in_bearbeitung'),
        ('Tunnel war historische Katzenpost-Route', 'Die Fundstücke belegen, dass Stadtkatzen vor über hundert Jahren Nachrichten durch den Tunnel transportierten, ohne nasse Pfoten zu bekommen.', 'Stadtgeschichte', 'Stadtmuseum', NULL, '2026-03-26 13:00:00', 'erledigt'),
        ('Historischer Katzentunnel wird sonntags geöffnet', 'Nach Abschluss der Sicherungsarbeiten können Katzen den alten Posttunnel in kleinen Gruppen besichtigen. Wollknäuel müssen am Eingang abgegeben werden.', 'Tourismus', 'Marktplatz', NULL, '2026-04-02 09:00:00', 'erledigt'),

        -- Nachrichtenkette: Bibliothekskater und das verschwundene Buch
        ('Seltenes Katzenkochbuch aus Bibliothek verschwunden', 'Das einzige Exemplar von „Hundert Arten, einen Thunfisch zu öffnen“ fehlt seit Dienstag. Bibliothekskater Goethe leitete die Suche ein.', 'Kultur', 'Stadtbibliothek', NULL, '2026-04-09 17:25:00', 'in_bearbeitung'),
        ('Bibliothekskater Goethe entdeckt verdächtige Krümelspur', 'Eine Spur aus Fischkekskrümeln führt vom Kochbuchregal bis zur Kinderleseecke. Dort wurde außerdem ein fremdes rotes Halsband gefunden.', 'Kultur', 'Stadtbibliothek', NULL, '2026-04-10 08:50:00', 'in_bearbeitung'),
        ('Katzenkochbuch hinter Sitzkissen wiedergefunden', 'Lesekatze Lotti hatte das Buch versehentlich als Unterlage für ihr Nickerchen verwendet. Das Werk blieb bis auf ein umgeknicktes Eselsohr unbeschädigt.', 'Kultur', 'Stadtbibliothek', NULL, '2026-04-10 14:35:00', 'erledigt'),
        ('Goethe startet Lesekreis für kochbegeisterte Katzen', 'Als versöhnlichen Abschluss lädt Bibliothekskater Goethe jeden Mittwoch zum gemeinsamen Lesen und anschließenden Thunfischtesten ein.', 'Veranstaltung', 'Stadtbibliothek', NULL, '2026-04-15 16:30:00', 'erledigt'),

        -- Nachrichtenkette: Katzenbahn Linie 3
        ('Katzenbahn Linie 3 wegen Wollknäueln verspätet', 'Mehrere Wollknäuel blockierten am Morgen die Schienen. Fahrgäste wurden gebeten, auf die Ersatzbuskatze umzusteigen.', 'Nahverkehr', 'Haltestelle Schnurrallee', NULL, '2026-05-02 07:12:00', 'in_bearbeitung'),
        ('Wollknäuel auf Linie 3 waren Teil eines Kunstprojekts', 'Künstlerkater Banksy-Pfote bekannte sich zur Aktion. Die Verkehrsbetriebe lobten die Farben, kritisierten aber den Berufsverkehr als Ausstellungsort.', 'Kultur', 'Schnurrallee', NULL, '2026-05-02 12:20:00', 'offen'),
        ('Katzenbahn testet wollknäuelsichere Schienenräumer', 'Neue weiche Bürsten sollen Spielzeug von den Gleisen schieben, ohne es zu beschädigen. Der Probebetrieb startet auf Linie 3.', 'Nahverkehr', 'Betriebshof Süd', NULL, '2026-05-08 09:45:00', 'in_bearbeitung'),
        ('Katzenbahn Linie 3 fährt wieder pünktlich und wollknäuelfrei', 'Der Test der neuen Schienenräumer war erfolgreich. Die Katzenverkehrsbetriebe übergaben Banksy-Pfotes Wollknäuelkunst an das Stadtmuseum.', 'Nahverkehr', 'Schnurrallee', NULL, '2026-05-20 08:00:00', 'erledigt'),

        -- Nachrichtenkette: Gemeinschaftsgarten
        ('Katzen eröffnen ersten Gemeinschaftsgarten', 'Auf einer ehemaligen Brachfläche pflanzten Nachbarschaftskatzen Katzengras, Minze und schattenspendende Sonnenblumen.', 'Umwelt', 'Pfotenweg 12', NULL, '2026-05-25 11:00:00', 'erledigt'),
        ('Mysteriöser Diebstahl von Katzenminze im Gemeinschaftsgarten', 'Über Nacht verschwanden zwölf Pflanzen. Zurück blieben nur kleine Pfotenabdrücke und ein auffällig entspannter Kater.', 'Nachbarschaft', 'Pfotenweg 12', NULL, '2026-05-29 06:55:00', 'in_bearbeitung'),
        ('Minzspur führt zu illegalem Katzenpicknick', 'Die vermissten Pflanzen wurden auf einer Wiese gefunden. Eine Gruppe Jungkatzen hatte dort ohne Genehmigung ein ausgelassenes Picknick veranstaltet.', 'Nachbarschaft', 'Mauswiese', NULL, '2026-05-29 19:10:00', 'in_bearbeitung'),
        ('Jungkatzen leisten Gartenstunden als Wiedergutmachung', 'Die beteiligten Katzen pflanzten neue Minze und bauten zusätzlich ein Insektenhotel. Das Verfahren wurde daraufhin eingestellt.', 'Gemeinschaft', 'Pfotenweg 12', NULL, '2026-06-03 15:30:00', 'erledigt'),

        -- Einzelmeldungen und kleinere Zweiteiler
        ('Kater blockiert Kreisverkehr mit ausgedehntem Sonnenbad', 'Kater Bruno legte sich exakt in die Mitte des Kreisverkehrs und ignorierte sämtliche Umleitungsangebote. Nach einem Snack räumte er die Fahrbahn freiwillig.', 'Verkehr', 'Kreisverkehr West', NULL, '2026-06-07 13:22:00', 'erledigt'),
        ('Katze gewinnt regionalen Schnurrwettbewerb', 'Die dreifarbige Katze Susi erreichte mit gleichmäßigen 27 Hertz den ersten Platz und erhielt den goldenen Futternapf.', 'Sport', 'Stadthalle', NULL, '2026-06-09 18:00:00', 'erledigt'),
        ('Neue Katzenklappe am Bürgerbüro war zu klein', 'Großkater Norbert blieb bei der Eröffnung kurzzeitig stecken. Das Bauamt kündigte eine breitere und barrierearme Ausführung an.', 'Verwaltung', 'Bürgerbüro', NULL, '2026-06-11 09:05:00', 'in_bearbeitung'),
        ('Bürgerbüro eröffnet vergrößerte Katzenklappe', 'Die neue Katzenklappe bietet nun auch Norbert ausreichend Platz. Er durchquerte sie bei der Abnahme dreimal ohne Beanstandung.', 'Verwaltung', 'Bürgerbüro', NULL, '2026-06-18 10:00:00', 'erledigt'),
        ('Kätzchen melden Schlagloch mit Kreidezeichnung', 'Drei junge Katzen umrandeten ein tiefes Schlagloch mit bunten Kreidepfoten. Der Bauhof sicherte die Stelle noch am selben Nachmittag.', 'Infrastruktur', 'Miauergasse 4', NULL, '2026-06-20 14:18:00', 'in_bearbeitung'),
        ('Schlagloch in der Miauergasse wurde repariert', 'Der Bauhof schloss die von den Kätzchen markierte Stelle. Als Dank durften die drei Nachwuchsmelder ihre Pfoten im frischen Randstein verewigen.', 'Infrastruktur', 'Miauergasse 4', NULL, '2026-06-23 16:40:00', 'erledigt'),
        ('Seniorenkater eröffnet kostenlose Mäuseberatung', 'Kater Herbert erklärt jungen Wohnungskatzen jeden Dienstag, wie man Spielzeugmäuse erkennt, anschleicht und anschließend unter dem Sofa verliert.', 'Bildung', 'Seniorentreff Samtpfote', NULL, '2026-06-25 12:00:00', 'erledigt'),
        ('Katze schläft seit neun Stunden auf wichtigem Bauplan', 'Die Sanierung des Brunnens verzögerte sich, weil Baukatze Frieda nicht geweckt werden sollte. Die Verwaltung sprach von höherer Gewalt.', 'Verwaltung', 'Bauamt', NULL, '2026-06-27 15:45:00', 'offen'),
        ('Frieda gibt Bauplan nach erfolgreichem Nickerchen frei', 'Die Baukatze verließ den Plan am Morgen aus eigenem Antrieb. Die Brunnenarbeiten konnten mit nur einem Tag Verzögerung beginnen.', 'Verwaltung', 'Bauamt', NULL, '2026-06-28 08:10:00', 'erledigt'),
        ('Stadtpark erhält fünf neue Kratzbäume', 'Die robusten Naturholzmodelle wurden entlang der großen Wiese aufgestellt und von 23 Katzen gleichzeitig getestet.', 'Freizeit', 'Stadtpark', NULL, '2026-07-01 11:30:00', 'erledigt'),
        ('Eichhörnchen protestieren gegen Katzenkratzbäume', 'Eine Gruppe Eichhörnchen warf Zapfen auf die Einweihungsfeier. Katzen und Eichhörnchen wollen nun über getrennte Kletterzeiten verhandeln.', 'Nachbarschaft', 'Stadtpark', NULL, '2026-07-02 10:05:00', 'in_bearbeitung'),
        ('Katzen und Eichhörnchen einigen sich auf Kletterplan', 'Kratzbäume gehören vormittags den Katzen und nachmittags den Eichhörnchen. Die Dämmerung bleibt für spontane Begegnungen reserviert.', 'Gemeinschaft', 'Stadtpark', NULL, '2026-07-05 17:15:00', 'erledigt'),
        ('Kater bestellt versehentlich 800 Dosen Thunfisch', 'Bürokater Klaus lief über die Tastatur der Einkaufsabteilung und bestätigte eine Großbestellung. Die Stadt sucht nun gemeinnützige Abnehmerkatzen.', 'Verwaltung', 'Rathauslager', NULL, '2026-07-07 08:42:00', 'in_bearbeitung'),
        ('Thunfisch-Großbestellung an Tierheime verteilt', 'Alle 800 Dosen wurden an Katzenstationen der Region gespendet. Bürokater Klaus erhielt vorsorglich eine Tastatursperre.', 'Soziales', 'Rathauslager', NULL, '2026-07-08 16:20:00', 'erledigt'),
        ('Nachtbus nimmt erstmals Katzen ohne Begleitmenschen mit', 'Die neue Regelung gilt freitags und samstags. Voraussetzung sind ein gültiges Pfotenticket und ein sicherer Transportkorb für das Lieblingsspielzeug.', 'Nahverkehr', 'Zentraler Busbahnhof', NULL, '2026-07-10 20:00:00', 'erledigt'),
        ('Katze meldet tropfenden Hydranten per Bürgerportal', 'Molly fotografierte den Schaden und schickte die genaue Position. Der Wasserversorger stoppte das Leck innerhalb von zwei Stunden.', 'Infrastruktur', 'Fischmarkt 3', NULL, '2026-07-12 09:33:00', 'erledigt'),
        ('Katzenchor sucht tiefe Stimmen', 'Dem städtischen Chor fehlen Basskater für das Sommerkonzert. Vorsingen ist auch mit nervösem Schnurren möglich.', 'Kultur', 'Musikschule', NULL, '2026-07-14 14:00:00', 'offen'),
        ('Vier Basskater verstärken den Katzenchor', 'Nach dem Aufruf meldeten sich überraschend viele tiefe Stimmen. Das Sommerkonzert kann nun mit vollständigem Schnurrsatz stattfinden.', 'Kultur', 'Musikschule', NULL, '2026-07-17 18:10:00', 'erledigt'),
        ('Unbekannte Katze verteilt Komplimente an Bushaltestelle', 'Pendlerkatzen berichten von einer freundlichen Fremden, die jedem Fahrgast ein schönes Fell oder besonders elegante Schnurrhaare bescheinigte.', 'Gemeinschaft', 'Haltestelle Rathaus', NULL, '2026-07-19 07:50:00', 'erledigt'),
        ('Kater verwechselt Blumenbeet mit riesigem Katzenklo', 'Das frisch bepflanzte Beet vor dem Theater musste kurzzeitig gesperrt werden. Stadtgärtner stellten diskrete Hinweisschilder für Katzen auf.', 'Umwelt', 'Theaterplatz', NULL, '2026-07-20 06:40:00', 'in_bearbeitung'),
        ('Theaterbeet nach Katzenmissverständnis wiederhergestellt', 'Freiwillige Katzen halfen beim Nachpflanzen und installierten nebenan eine große Sandkiste. Seitdem blieb das Beet unberührt.', 'Umwelt', 'Theaterplatz', NULL, '2026-07-22 13:35:00', 'erledigt'),
        ('Erste Katzenampel reagiert auf Miauen', 'Die neue Ampel erkennt ein deutliches Miauen und verlängert die Grünphase für langsam laufende Katzen. Leises Schnurren reicht technisch noch nicht aus.', 'Infrastruktur', 'Samtpfotenallee', NULL, '2026-07-24 10:10:00', 'erledigt'),
        ('Papagei imitiert Miauen und legt Katzenampel lahm', 'Ein entflogener Papagei löste 47 Grünphasen hintereinander aus. Die Ampelsoftware soll künftig echte Katzenstimmen genauer erkennen.', 'Infrastruktur', 'Samtpfotenallee', NULL, '2026-07-25 11:28:00', 'in_bearbeitung'),
        ('Katzenampel erkennt nach Update keine Papageien mehr', 'Ein Softwareupdate unterscheidet nun Miauen, Schnurren und Papageienimitationen. Testkater Emil überquerte die Straße erfolgreich.', 'Infrastruktur', 'Samtpfotenallee', NULL, '2026-07-28 09:55:00', 'erledigt'),
        ('Katze findet Geldbörse und fordert Finderlohn in Lachs', 'Fundkatze Paula gab die Börse vollständig im Fundbüro ab. Die Besitzerkatze erfüllte den ungewöhnlichen, aber angemessenen Wunsch.', 'Fundbüro', 'Bahnhofsvorplatz', NULL, '2026-07-30 16:05:00', 'erledigt'),
        ('Freibad führt stille Stunde für wasserscheue Katzen ein', 'Jeden Donnerstag bleiben Sprungturm und Fontänen eine Stunde ausgeschaltet, damit auch vorsichtige Katzen den Beckenrand erkunden können.', 'Freizeit', 'Freibad Süd', NULL, '2026-08-01 09:00:00', 'erledigt'),
        ('Mutige Katze schwimmt eine komplette Bahn', 'Während der stillen Stunde überwand Katze Nala ihre Wasserscheu und schwamm unter großem Applaus vom flachen Ende bis zur Leiter.', 'Sport', 'Freibad Süd', NULL, '2026-08-01 10:20:00', 'erledigt'),
        ('Kater eröffnet Reparaturdienst für zerkratzte Sofas', 'Handwerkerkater Uwe kaschiert Kratzspuren mit dekorativen Sisaleinsätzen. Die ersten Kundinnen loben das robuste Ergebnis.', 'Wirtschaft', 'Werkstatt am Hafen', NULL, '2026-08-03 12:45:00', 'erledigt'),
        ('Katze hängt Beschwerde über zu laute Staubsauger aus', 'Hauskatze Erna fordert eine tägliche staubsaugerfreie Mittagsruhe zwischen 13 und 15 Uhr. Bereits 41 Katzen haben den Aushang mit Pfotenabdruck unterstützt.', 'Lärmschutz', 'Wohngebiet Am Napf', NULL, '2026-08-07 13:15:00', 'offen'),
        ('Wohngebiet beschließt Staubsauger-Mittagsruhe für Katzen', 'Die Hausgemeinschaft nahm Ernas Vorschlag einstimmig an. Ausnahmen gelten nur bei umgekippten Trockenfutterbeuteln.', 'Lärmschutz', 'Wohngebiet Am Napf', NULL, '2026-08-10 18:00:00', 'erledigt'),
        ('Kätzchen programmiert App zur Kartonsuche', 'Die Anwendung zeigt freie Kartons in der Umgebung und bewertet Größe, Geruch und Knisterfaktor. Innerhalb eines Tages registrierten sich 300 Katzen.', 'Digitales', 'Technologiezentrum', NULL, '2026-08-12 10:30:00', 'erledigt'),
        ('Kartonsuch-App meldet versehentlich Umzugslaster als frei', 'Dutzende Katzen besetzten einen abgestellten Möbelwagen. Das Entwicklerkätzchen ergänzte daraufhin eine Prüfung für bewegliche Kartons.', 'Digitales', 'Umzugsplatz', NULL, '2026-08-13 14:48:00', 'in_bearbeitung'),
        ('Kartonsuch-App erhielt Sicherheitsupdate', 'Nach dem Update werden Fahrzeuge und bereits bewohnte Kartons zuverlässig erkannt. Die Katzen aus dem Möbelwagen sind sicher ausgestiegen.', 'Digitales', 'Technologiezentrum', NULL, '2026-08-15 09:25:00', 'erledigt'),
        ('Stadt sucht ehrenamtliche Vorlesekatzen', 'Ruhige Katzen können sich für wöchentliche Vorlesenachmittage mit Kitten anmelden. Erfahrung im deutlichen Schnurren ist erwünscht.', 'Ehrenamt', 'Familienzentrum', NULL, '2026-08-17 11:00:00', 'offen'),
        ('Kater gewinnt Schachturnier durch Umwerfen aller Figuren', 'Schiedsrichter werteten den ungewöhnlichen Zug zunächst als Aufgabe. Nach langer Beratung erhielt Kater Kasimir einen Sonderpreis für Kreativität.', 'Sport', 'Vereinshaus', NULL, '2026-08-18 20:10:00', 'erledigt'),
        ('Marktkatze warnt vor gefälschtem Premium-Thunfisch', 'Mehrere Dosen enthielten lediglich gewöhnlichen Thunfisch mit aufgemaltem Monokel. Das Ordnungsamt für Katzenfutter ermittelt.', 'Verbraucherschutz', 'Wochenmarkt', NULL, '2026-08-20 08:35:00', 'in_bearbeitung'),
        ('Gefälschter Premium-Thunfisch aus dem Verkehr gezogen', 'Kontrollkatzen beschlagnahmten 90 Dosen. Käuferkatzen können die Ware gegen echten Thunfisch ohne Monokel eintauschen.', 'Verbraucherschutz', 'Wochenmarkt', NULL, '2026-08-21 15:50:00', 'erledigt'),
        ('Katzenfeuerwehr befreit Roboterstaubsauger aus Vorhang', 'Das Gerät hatte sich beim Fluchtversuch im Stoff verfangen. Drei Katzen beobachteten die Rettung aus sicherer Entfernung vom Schrank.', 'Rettung', 'Wohnpark Süd', NULL, '2026-08-23 17:42:00', 'erledigt'),
        ('Kostenlose Sonnenplätze auf Rathausdach eingerichtet', 'Zwölf gepolsterte Liegeflächen stehen Katzen täglich von 10 bis 18 Uhr zur Verfügung. Reservierungen mit Handtüchern sind nicht erlaubt.', 'Freizeit', 'Rathausplatz 1', NULL, '2026-08-24 10:00:00', 'erledigt'),
        ('Kater meldet verdächtig leeren Futternapf', 'Die Katzenpolizei stellte fest, dass Kater Oskar sein Abendessen bereits gefressen und den Vorgang offenbar vergessen hatte.', 'Polizeimeldung', 'Flauschweg 8', NULL, '2026-08-25 19:05:00', 'erledigt'),
        ('Großes Katzenkino zeigt Klassiker mit Untertiteln', 'Beim Open-Air-Abend laufen drei Naturfilme über Vögel, Fische und besonders schnelle rote Punkte. Eigene Decken dürfen mitgebracht werden.', 'Veranstaltung', 'Mauswiese', NULL, '2026-08-26 20:00:00', 'offen')
) AS seed_rows
WHERE NOT EXISTS (
    SELECT 1
    FROM anliegen
    WHERE anliegen.titel = seed_rows.column1
);

-- Ergänzt die Bildpfade auch in bereits gesäten Entwicklungsdatenbanken.
UPDATE anliegen
SET foto_pfad = CASE titel
    WHEN 'Betrunkene Katze fährt in ein KFC' THEN 'img/news/01-kfc-unfall.png'
    WHEN 'Polizei findet Katzenminze in Karlos Lieferwagen' THEN 'img/news/02-katzenminze-ermittlung.png'
    WHEN 'KFC-Filiale eröffnet provisorischen Katzenschalter' THEN 'img/news/03-katzenschalter.png'
    WHEN 'Kater Karlo übernimmt Verantwortung für KFC-Unfall' THEN 'img/news/04-karlo-entschuldigung.png'
    WHEN 'KFC nach Katzenunfall wieder vollständig geöffnet' THEN 'img/news/05-kfc-wiedereroeffnung.png'
    WHEN 'Bürgermeisterkatze Minka spurlos verschwunden' THEN 'img/news/06-minka-vermisst.png'
END
WHERE titel IN (
    'Betrunkene Katze fährt in ein KFC',
    'Polizei findet Katzenminze in Karlos Lieferwagen',
    'KFC-Filiale eröffnet provisorischen Katzenschalter',
    'Kater Karlo übernimmt Verantwortung für KFC-Unfall',
    'KFC nach Katzenunfall wieder vollständig geöffnet',
    'Bürgermeisterkatze Minka spurlos verschwunden'
);

-- Bildlose Seed-Meldungen verwenden ein gemeinsames gemeinfreies Standardmotiv.
UPDATE anliegen
SET foto_pfad = 'img/news/web-01.webp'
WHERE foto_pfad IS NULL
   OR foto_pfad LIKE 'img/news/web-%';

-- Vorhandene, eigens für bestimmte Meldungen erstellte Illustrationen.
UPDATE anliegen
SET foto_pfad = CASE titel
    WHEN 'Pfotenabdrücke führen zum alten Glockenturm' THEN 'img/news/codex-clipboard-78030a55-1409-49dd-97a3-b78b9ba2a12c.png'
    WHEN 'Feuerwehr rettet Minka aus dem Glockenturm' THEN 'img/news/codex-clipboard-924843c7-ec03-4588-b9bc-fa389a320967.png'
    WHEN 'Minka dankt ihren Retterkatzen mit Rathausfest' THEN 'img/news/codex-clipboard-6324df55-0983-436b-8ec9-09f06c502d9f.png'
    WHEN 'Kätzchen entdeckt geheimen Tunnel unter dem Marktplatz' THEN 'img/news/codex-clipboard-a8e23707-52d0-417c-beb5-73bd05e411d7.png'
    WHEN 'Katzenarchäologen untersuchen Marktplatztunnel' THEN 'img/news/codex-clipboard-ac82dcb2-d42f-4730-b030-b90e8124c24e.png'
    WHEN 'Tunnel war historische Katzenpost-Route' THEN 'img/news/codex-clipboard-94478d2f-d0fc-4aea-8430-82b726283ed0.png'
    WHEN 'Historischer Katzentunnel wird sonntags geöffnet' THEN 'img/news/codex-clipboard-08f2ced3-7424-4549-a6ac-0333245d9caf.png'
    WHEN 'Seltenes Katzenkochbuch aus Bibliothek verschwunden' THEN 'img/news/codex-clipboard-0cbb3681-c956-4d8e-a081-cb54bcb666d3.png'
    WHEN 'Bibliothekskater Goethe entdeckt verdächtige Krümelspur' THEN 'img/news/codex-clipboard-7f4b0fd2-d8a5-41c0-b70a-cd0c4e6badf7.png'
    WHEN 'Katzenkochbuch hinter Sitzkissen wiedergefunden' THEN 'img/news/codex-clipboard-2c69eb82-9365-4647-a8af-e141455d052f.png'
    WHEN 'Kater meldet verdächtig leeren Futternapf' THEN 'img/news/codex-clipboard-111e8683-1e99-494b-937d-4b8837082db3.png'
END
WHERE titel IN (
    'Pfotenabdrücke führen zum alten Glockenturm',
    'Feuerwehr rettet Minka aus dem Glockenturm',
    'Minka dankt ihren Retterkatzen mit Rathausfest',
    'Kätzchen entdeckt geheimen Tunnel unter dem Marktplatz',
    'Katzenarchäologen untersuchen Marktplatztunnel',
    'Tunnel war historische Katzenpost-Route',
    'Historischer Katzentunnel wird sonntags geöffnet',
    'Seltenes Katzenkochbuch aus Bibliothek verschwunden',
    'Bibliothekskater Goethe entdeckt verdächtige Krümelspur',
    'Katzenkochbuch hinter Sitzkissen wiedergefunden',
    'Kater meldet verdächtig leeren Futternapf'
);

INSERT INTO app_meta (key, value)
VALUES ('cat_news_seed_version', '1')
ON CONFLICT(key) DO UPDATE SET value = excluded.value;

COMMIT;
