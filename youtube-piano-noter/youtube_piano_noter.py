#!/usr/bin/env python3
"""
youtube_piano_noter.py — hent pianonoter fra et utsnitt av en YouTube-video.

Pipeline:
  1. Last ned lyden for valgt tidsintervall med yt-dlp.
     Prøver først å laste ned bare utsnittet; faller tilbake til å laste ned
     hele lydsporet og klippe lokalt med ffmpeg (mer robust for lange opptak).
  2. (Valgfritt, --isoler-piano) Isoler pianoet fra resten av bandet med
     Demucs (modellen htdemucs_6s har eget piano-stem). Anbefales for
     konsertopptak der pianoet konkurrerer med vokal, gitar og trommer.
  3. Transkriber lyd -> MIDI.
     Standardmotor er ByteDance "High-Resolution Piano Transcription"
     (best for piano). Alternativ: Spotify basic-pitch (--motor basic-pitch).
  4. Skriv ut resultatene:
       <navn>.mid        MIDI-fil (kan åpnes i MuseScore, GarageBand, ...)
       <navn>.musicxml   Noteark (åpnes i MuseScore/Sibelius/Finale)
       <navn>_noter.txt  Lesbar liste over alle noter med tidspunkt
       <navn>.pdf        Ferdig noteark, hvis MuseScore er installert

Eksempel (utsnittet 53:40–59:00 av et konsertopptak):

    python youtube_piano_noter.py "https://youtu.be/6xVbSU7WyHk" \
        --start 53:40 --slutt 59:00

Krever: ffmpeg på PATH, samt pakkene i requirements.txt.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# ---------------------------------------------------------------------------
# Tidshåndtering
# ---------------------------------------------------------------------------


def parse_tid(tekst: str) -> float:
    """Tolk et tidspunkt som '59:00', '1:02:03', '53m40s' eller '3220' -> sekunder."""
    tekst = tekst.strip().lower()
    if not tekst:
        raise ValueError("tomt tidspunkt")
    if tekst.endswith("s") or "m" in tekst or "h" in tekst:
        # Formater som 53m40s / 1h02m03s / 90s
        total = 0.0
        tall = ""
        for tegn in tekst:
            if tegn.isdigit() or tegn == ".":
                tall += tegn
            elif tegn in "hms":
                if not tall:
                    raise ValueError(f"ugyldig tidspunkt: {tekst!r}")
                total += float(tall) * {"h": 3600, "m": 60, "s": 1}[tegn]
                tall = ""
            else:
                raise ValueError(f"ugyldig tidspunkt: {tekst!r}")
        if tall:
            total += float(tall)
        return total
    deler = tekst.split(":")
    if len(deler) > 3:
        raise ValueError(f"ugyldig tidspunkt: {tekst!r}")
    total = 0.0
    for del_ in deler:
        total = total * 60 + float(del_)
    return total


def formater_tid(sekunder: float) -> str:
    """Sekunder -> 'H:MM:SS' eller 'MM:SS'."""
    s = int(round(sekunder))
    h, rest = divmod(s, 3600)
    m, sek = divmod(rest, 60)
    if h:
        return f"{h}:{m:02d}:{sek:02d}"
    return f"{m:02d}:{sek:02d}"


# ---------------------------------------------------------------------------
# Nedlasting fra YouTube
# ---------------------------------------------------------------------------


def _ffmpeg_til_wav(kilde: Path, mål: Path, start: float | None = None,
                    slutt: float | None = None, sr: int = 44100) -> None:
    """Konverter (og eventuelt klipp) en lydfil til WAV med ffmpeg."""
    kmd = ["ffmpeg", "-y", "-loglevel", "error"]
    if start is not None:
        kmd += ["-ss", f"{start:.3f}"]
    if slutt is not None:
        kmd += ["-to", f"{slutt:.3f}"]
    kmd += ["-i", str(kilde), "-vn", "-acodec", "pcm_s16le", "-ar", str(sr), str(mål)]
    subprocess.run(kmd, check=True)


def last_ned_utsnitt(url: str, start: float, slutt: float, arbeidsmappe: Path,
                     cookies: str | None = None,
                     cookies_fra_nettleser: str | None = None) -> Path:
    """Last ned lyden for [start, slutt] av videoen og returner sti til WAV-fil.

    Strategi 1: be yt-dlp laste ned bare utsnittet (raskt for lange opptak).
    Strategi 2: last ned hele lydsporet og klipp lokalt med ffmpeg.
    """
    try:
        import yt_dlp
        from yt_dlp.utils import download_range_func
    except ImportError:
        sys.exit("Mangler yt-dlp. Installer med:  pip install -r requirements.txt")

    wav = arbeidsmappe / "utsnitt.wav"

    def grunnvalg(mal: str) -> dict:
        valg: dict = {
            "format": "bestaudio/best",
            "outtmpl": str(arbeidsmappe / (mal + ".%(ext)s")),
            "noplaylist": True,
            "retries": 4,
            # Godta alle JS-motorer yt-dlp støtter (standard er bare deno);
            # trengs for YouTubes signatur-utfordringer.
            "js_runtimes": {"deno": {}, "node": {}, "bun": {}, "quickjs": {}},
        }
        if cookies:
            valg["cookiefile"] = cookies
        if cookies_fra_nettleser:
            valg["cookiesfrombrowser"] = (cookies_fra_nettleser,)
        return valg

    def finn_nedlastet(mal: str) -> Path | None:
        treff = sorted(arbeidsmappe.glob(mal + ".*"))
        treff = [t for t in treff if t.suffix not in {".part", ".ytdl"}]
        return treff[0] if treff else None

    # --- Strategi 1: seksjonsnedlasting -----------------------------------
    print(f"[1/4] Laster ned utsnittet {formater_tid(start)}–{formater_tid(slutt)} ...")
    valg = grunnvalg("seksjon")
    valg["download_ranges"] = download_range_func(None, [(start, slutt)])
    try:
        with yt_dlp.YoutubeDL(valg) as ydl:
            ydl.download([url])
        fil = finn_nedlastet("seksjon")
        if fil is not None:
            _ffmpeg_til_wav(fil, wav)
            return wav
    except Exception as feil:  # noqa: BLE001 - vi vil alltid prøve strategi 2
        print(f"      Seksjonsnedlasting feilet ({feil}).")

    # --- Strategi 2: full nedlasting + lokal klipping ----------------------
    print("      Prøver i stedet å laste ned hele lydsporet og klippe lokalt ...")
    valg = grunnvalg("fullt")
    try:
        with yt_dlp.YoutubeDL(valg) as ydl:
            ydl.download([url])
    except Exception as feil:  # noqa: BLE001
        sys.exit(
            f"Nedlastingen feilet: {feil}\n\n"
            "Tips: Får du '403 Forbidden' eller beskjed om å logge inn, kjører du\n"
            "sannsynligvis fra en IP-adresse YouTube ikke stoler på. Prøv:\n"
            "  * å kjøre programmet fra din egen maskin/nettverk, eller\n"
            "  * --cookies-fra-nettleser chrome  (eller firefox/safari/edge)\n"
            "    slik at yt-dlp gjenbruker YouTube-innloggingen din, eller\n"
            "  * --cookies cookies.txt  med eksporterte YouTube-cookies."
        )
    fil = finn_nedlastet("fullt")
    if fil is None:
        sys.exit("Fant ikke den nedlastede lydfilen – ukjent feil i yt-dlp.")
    _ffmpeg_til_wav(fil, wav, start=start, slutt=slutt)
    fil.unlink(missing_ok=True)  # spar plass; hele konserten kan være stor
    return wav


# ---------------------------------------------------------------------------
# Kildeseparasjon (valgfritt): isoler pianoet fra resten av bandet
# ---------------------------------------------------------------------------


def isoler_piano(wav: Path, arbeidsmappe: Path) -> Path:
    """Kjør Demucs (htdemucs_6s) og returner sti til piano-stemmen."""
    try:
        import demucs  # noqa: F401
    except ImportError:
        sys.exit(
            "Valget --isoler-piano krever Demucs. Installer med:\n"
            "  pip install demucs"
        )
    print("[2/4] Isolerer pianoet fra resten av miksen (Demucs htdemucs_6s) ...")
    utmappe = arbeidsmappe / "demucs"
    subprocess.run(
        [sys.executable, "-m", "demucs.separate",
         "-n", "htdemucs_6s", "--two-stems", "piano",
         "-o", str(utmappe), str(wav)],
        check=True,
    )
    kandidater = list(utmappe.glob("htdemucs_6s/*/piano.wav"))
    if not kandidater:
        sys.exit("Demucs fullførte, men piano-stemmen ble ikke funnet.")
    return kandidater[0]


# ---------------------------------------------------------------------------
# Transkripsjon lyd -> MIDI
# ---------------------------------------------------------------------------


def _les_lyd_16k_mono(wav: Path, arbeidsmappe: Path):
    """Les en lydfil som 16 kHz mono float32-array (formatet piano-modellen vil ha)."""
    import numpy as np
    import soundfile as sf

    wav16 = arbeidsmappe / "utsnitt_16k_mono.wav"
    _ffmpeg_til_wav(wav, wav16, sr=16000)
    lyd, _ = sf.read(wav16, dtype="float32", always_2d=True)
    return np.ascontiguousarray(lyd.mean(axis=1))


def transkriber_piano(wav: Path, midi_ut: Path, arbeidsmappe: Path) -> None:
    """ByteDance High-Resolution Piano Transcription (beste valg for piano)."""
    try:
        import torch
        from piano_transcription_inference import PianoTranscription
    except ImportError:
        sys.exit(
            "Motoren 'piano' krever torch og piano_transcription_inference.\n"
            "Installer med:  pip install -r requirements.txt"
        )
    print("[3/4] Transkriberer piano -> MIDI (kan ta noen minutter på CPU) ...")
    lyd = _les_lyd_16k_mono(wav, arbeidsmappe)
    enhet = "cuda" if torch.cuda.is_available() else "cpu"
    transkriptor = PianoTranscription(device=enhet)
    transkriptor.transcribe(lyd, str(midi_ut))


def transkriber_basic_pitch(wav: Path, midi_ut: Path) -> None:
    """Spotify basic-pitch (lettere, mer generell modell)."""
    try:
        from basic_pitch import ICASSP_2022_MODEL_PATH
        from basic_pitch.inference import predict
    except ImportError:
        sys.exit(
            "Motoren 'basic-pitch' krever pakken basic-pitch. Installer med:\n"
            "  pip install basic-pitch"
        )
    print("[3/4] Transkriberer lyd -> MIDI med basic-pitch ...")
    _, midi_data, _ = predict(str(wav), ICASSP_2022_MODEL_PATH)
    midi_data.write(str(midi_ut))


# ---------------------------------------------------------------------------
# MIDI -> noteark og noteliste
# ---------------------------------------------------------------------------

_NOTENAVN = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def _notenavn(midi_nr: int) -> str:
    """MIDI-nummer -> notenavn, f.eks. 60 -> 'C4'. (Merk: B = norsk H.)"""
    return f"{_NOTENAVN[midi_nr % 12]}{midi_nr // 12 - 1}"


def rydd_midi(midi_fil: Path, min_varighet: float) -> None:
    """Fjern svært korte «spøkelsesnoter» (typisk overtoner/støy) fra MIDI-fila."""
    if min_varighet <= 0:
        return
    import pretty_midi

    pm = pretty_midi.PrettyMIDI(str(midi_fil))
    før = sum(len(i.notes) for i in pm.instruments)
    for inst in pm.instruments:
        inst.notes = [n for n in inst.notes if n.end - n.start >= min_varighet]
    etter = sum(len(i.notes) for i in pm.instruments)
    if etter < før:
        print(f"      Fjernet {før - etter} spøkelsesnoter kortere enn "
              f"{min_varighet:.2f}s.")
        pm.write(str(midi_fil))


def skriv_noteliste(midi_fil: Path, tekst_ut: Path, start_offset: float) -> int:
    """Skriv en lesbar liste over alle noter. Returnerer antall noter."""
    import pretty_midi

    pm = pretty_midi.PrettyMIDI(str(midi_fil))
    noter = sorted(
        (n for inst in pm.instruments for n in inst.notes),
        key=lambda n: (n.start, n.pitch),
    )
    with tekst_ut.open("w", encoding="utf-8") as f:
        f.write("Tid i utsnitt  Tid i video  Note  Varighet  Anslag(0-127)\n")
        f.write("-" * 60 + "\n")
        for n in noter:
            f.write(
                f"{n.start:>10.2f}s  {formater_tid(start_offset + n.start):>9}  "
                f"{_notenavn(n.pitch):<5} {n.end - n.start:>7.2f}s  {n.velocity:>5}\n"
            )
    return len(noter)


def skriv_noteark(midi_fil: Path, musicxml_ut: Path, tittel: str) -> None:
    """Konverter MIDI til MusicXML-noteark med music21 (kvantisert)."""
    import music21

    partitur = music21.converter.parse(str(midi_fil), quantizePost=True,
                                       quarterLengthDivisors=(4, 3))
    partitur.metadata = music21.metadata.Metadata()
    partitur.metadata.title = tittel
    partitur.metadata.composer = "Transkribert automatisk"
    partitur.write("musicxml", fp=str(musicxml_ut))


def prøv_pdf(musicxml: Path, pdf_ut: Path) -> bool:
    """Lag PDF-noteark hvis MuseScore er installert. Returnerer True ved suksess."""
    for kandidat in ("mscore", "musescore", "mscore4portable", "musescore4",
                     "mscore3", "musescore3", "MuseScore4"):
        binær = shutil.which(kandidat)
        if binær:
            try:
                subprocess.run([binær, "-o", str(pdf_ut), str(musicxml)],
                               check=True, capture_output=True, timeout=300)
                return pdf_ut.exists()
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                return False
    return False


# ---------------------------------------------------------------------------
# Hovedprogram
# ---------------------------------------------------------------------------


def main() -> None:
    p = argparse.ArgumentParser(
        description="Hent pianonoter fra et utsnitt av en YouTube-video.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("url", nargs="?",
                   default="https://youtu.be/6xVbSU7WyHk",
                   help="YouTube-lenke")
    p.add_argument("--start", default="53:40",
                   help="starttidspunkt i videoen (MM:SS eller H:MM:SS)")
    p.add_argument("--slutt", "--end", dest="slutt", default="59:00",
                   help="sluttidspunkt i videoen (MM:SS eller H:MM:SS)")
    p.add_argument("--utmappe", "--outdir", dest="utmappe", default=None,
                   help="mappe for resultatfilene (standard: noter_<start>-<slutt>)")
    p.add_argument("--navn", default="piano",
                   help="grunnavn på resultatfilene")
    p.add_argument("--motor", "--engine", dest="motor",
                   choices=["piano", "basic-pitch"], default="piano",
                   help="transkripsjonsmotor: 'piano' (ByteDance, best for piano) "
                        "eller 'basic-pitch' (Spotify, lettere)")
    p.add_argument("--isoler-piano", "--separate", dest="isoler",
                   action="store_true",
                   help="isoler pianoet fra resten av bandet med Demucs først "
                        "(anbefales for konsertopptak, krever 'pip install demucs')")
    p.add_argument("--behold-lyd", action="store_true",
                   help="behold WAV-filen med lydutsnittet i utmappa")
    p.add_argument("--cookies", default=None,
                   help="sti til cookies.txt for YouTube (om nedlasting nektes)")
    p.add_argument("--cookies-fra-nettleser", "--cookies-from-browser",
                   dest="cookies_nettleser", default=None,
                   help="hent YouTube-cookies fra nettleseren din, "
                        "f.eks. chrome, firefox, safari eller edge")
    p.add_argument("--lydfil", default=None,
                   help="hopp over nedlastingen og bruk en lokal lydfil i stedet")
    p.add_argument("--min-varighet", type=float, default=0.05,
                   help="fjern noter kortere enn dette (sekunder) fra resultatet; "
                        "0 skrur av filteret")
    args = p.parse_args()

    start = parse_tid(args.start)
    slutt = parse_tid(args.slutt)
    if slutt <= start:
        sys.exit("Sluttidspunktet må være etter starttidspunktet.")

    utmappe = Path(args.utmappe or
                   f"noter_{args.start.replace(':', '')}-{args.slutt.replace(':', '')}")
    utmappe.mkdir(parents=True, exist_ok=True)

    if shutil.which("ffmpeg") is None:
        sys.exit("ffmpeg må være installert og på PATH (https://ffmpeg.org).")

    with tempfile.TemporaryDirectory(prefix="yt-piano-") as tmp:
        arbeidsmappe = Path(tmp)

        # 1) Skaff lydutsnittet
        if args.lydfil:
            print(f"[1/4] Bruker lokal lydfil: {args.lydfil}")
            wav = arbeidsmappe / "utsnitt.wav"
            _ffmpeg_til_wav(Path(args.lydfil), wav)
        else:
            wav = last_ned_utsnitt(args.url, start, slutt, arbeidsmappe,
                                   cookies=args.cookies,
                                   cookies_fra_nettleser=args.cookies_nettleser)

        # 2) Eventuelt: isoler pianoet
        if args.isoler:
            wav = isoler_piano(wav, arbeidsmappe)
        else:
            print("[2/4] Hopper over kildeseparasjon "
                  "(tips: --isoler-piano gir renere resultat for konsertopptak).")

        # 3) Transkriber til MIDI
        midi_fil = utmappe / f"{args.navn}.mid"
        if args.motor == "piano":
            transkriber_piano(wav, midi_fil, arbeidsmappe)
        else:
            transkriber_basic_pitch(wav, midi_fil)

        rydd_midi(midi_fil, args.min_varighet)

        if args.behold_lyd:
            shutil.copy2(wav, utmappe / f"{args.navn}.wav")

        # 4) Noteark og noteliste
        print("[4/4] Lager noteark og noteliste ...")
        antall = skriv_noteliste(midi_fil, utmappe / f"{args.navn}_noter.txt", start)
        musicxml = utmappe / f"{args.navn}.musicxml"
        skriv_noteark(midi_fil, musicxml,
                      tittel=f"Piano {args.start}–{args.slutt}")
        pdf = utmappe / f"{args.navn}.pdf"
        fikk_pdf = prøv_pdf(musicxml, pdf)

    print()
    print(f"Ferdig! {antall} noter funnet i utsnittet "
          f"{formater_tid(start)}–{formater_tid(slutt)}.")
    print(f"Resultater i {utmappe.resolve()}:")
    print(f"  {args.navn}.mid        - MIDI (åpnes i MuseScore, GarageBand, ...)")
    print(f"  {args.navn}.musicxml   - noteark (åpnes i MuseScore: musescore.org)")
    print(f"  {args.navn}_noter.txt  - lesbar liste over notene")
    if fikk_pdf:
        print(f"  {args.navn}.pdf        - ferdig noteark")
    else:
        print("  (Ingen PDF: installer MuseScore og kjør på nytt, eller åpne "
              ".musicxml-fila i MuseScore og eksporter derfra.)")


if __name__ == "__main__":
    main()
