# YouTube → pianonoter

Et program som henter ut pianonoter fra et valgt utsnitt av en YouTube-video —
laget for lange konsertopptak der du bare vil ha noter for én låt.

Programmet:

1. **Laster ned lyden** for tidsintervallet du velger (med `yt-dlp`).
   Det prøver først å laste ned bare utsnittet; hvis det ikke går, lastes hele
   lydsporet ned og klippes lokalt med `ffmpeg`.
2. **Isolerer pianoet** fra resten av bandet (valgfritt, med Demucs).
3. **Transkriberer lyden til MIDI** med ByteDance sin
   [High-Resolution Piano Transcription](https://github.com/bytedance/piano_transcription)
   — en av de beste åpne modellene for pianotranskripsjon.
4. **Lager noter**: MIDI-fil, MusicXML-noteark (åpnes i MuseScore) og en
   lesbar tekstliste over alle notene. Har du MuseScore installert, lages
   også en ferdig PDF.

## Installasjon

Du trenger Python 3.10+ og [ffmpeg](https://ffmpeg.org) på PATH
(macOS: `brew install ffmpeg`, Ubuntu: `sudo apt install ffmpeg`).
`yt-dlp` trenger også node eller deno for YouTubes JS-utfordringer.

```bash
cd youtube-piano-noter
pip install -r requirements.txt

# Uten NVIDIA-GPU? Spar flere GB med CPU-versjonen av PyTorch:
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

Første gang programmet kjører lastes transkripsjonsmodellen (~170 MB) ned
automatisk.

## Bruk

Utsnittet 53:40–59:00 av konsertopptaket (standardverdiene i programmet):

```bash
python youtube_piano_noter.py "https://youtu.be/6xVbSU7WyHk" --start 53:40 --slutt 59:00
```

Siden dette er et konsertopptak med helt band (vokal, gitar, trommer …)
anbefales det å isolere pianoet først — det gir mye renere noter:

```bash
pip install demucs   # engangsinstallasjon
python youtube_piano_noter.py "https://youtu.be/6xVbSU7WyHk" --start 53:40 --slutt 59:00 --isoler-piano
```

Resultatene havner i mappa `noter_5340-5900/`:

| Fil | Innhold |
|---|---|
| `piano.mid` | MIDI — åpnes i MuseScore, GarageBand, Logic … |
| `piano.musicxml` | Noteark — åpnes i [MuseScore](https://musescore.org) (gratis) |
| `piano_noter.txt` | Lesbar liste: tidspunkt, note, varighet, anslag |
| `piano.pdf` | Ferdig noteark (bare hvis MuseScore er installert) |

I notelista brukes internasjonale notenavn: `B` = norsk «H», `A#` = «B».

### Alle valg

```text
python youtube_piano_noter.py [URL] [valg]

--start 53:40                starttidspunkt (MM:SS eller H:MM:SS)
--slutt 59:00                sluttidspunkt
--utmappe MAPPE              hvor resultatene skal lagres
--navn piano                 grunnavn på resultatfilene
--motor piano|basic-pitch    transkripsjonsmotor (standard: piano)
--isoler-piano               kjør Demucs-kildeseparasjon først (krever demucs)
--min-varighet 0.05          fjern noter kortere enn dette (0 = behold alt)
--behold-lyd                 lagre lydutsnittet som WAV i utmappa
--lydfil FIL.wav             hopp over nedlasting, bruk lokal lydfil
--cookies FIL                cookies.txt for YouTube
--cookies-fra-nettleser chrome   gjenbruk nettleserens YouTube-innlogging
```

## Feilsøking

**«HTTP Error 403: Forbidden» ved nedlasting** — YouTube blokkerer
IP-adresser den ikke stoler på (VPN, skyservere o.l.). Kjør programmet fra
din egen maskin, eller bruk `--cookies-fra-nettleser chrome` (evt. `firefox`,
`safari`, `edge`) slik at yt-dlp gjenbruker YouTube-innloggingen din.

**Notene ser rotete ut** — automatisk transkripsjon av et liveopptak blir
aldri perfekt. Prøv `--isoler-piano`, og åpne `.musicxml`-fila i MuseScore
for å rydde manuelt. MIDI-fila er ofte det nyttigste utgangspunktet.

**Transkripsjonen tar lang tid** — på CPU tar den gjerne 1–3× sanntid
(et 5-minutters utsnitt kan ta 5–15 minutter). Med NVIDIA-GPU går det mye
raskere.

## Merk

Last bare ned innhold du har rett til å bruke. Transkripsjonene er til
privat bruk (øving/planking).
