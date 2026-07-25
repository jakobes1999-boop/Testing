#!/usr/bin/env python3
"""Genererer MP3-filer av podkastmanuset med norsk nevral talesyntese (Piper).

Filene spiller som vanlige lydfiler, og kan dermed sendes til AirPlay,
Bluetooth-høyttalere og Chromecast — i motsetning til nettleserens
innebygde talesyntese, som ikke kan rutes til eksterne lydutganger.

Bruk:
    pip install piper-tts imageio-ffmpeg
    python3 -m piper.download_voices --data-dir voices no_NO-talesyntese-medium
    python3 lag-lydfiler.py

Resultat: lyd/01-den-mikrookonomiske-verktoykassa.mp3 osv.
"""
import os
import re
import subprocess
import sys
import unicodedata
import wave

MANUS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'okonomisk-teori-refresher.md')
UTKATALOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lyd')
STEMME = os.environ.get('PIPER_VOICE', 'voices/no_NO-talesyntese-medium.onnx')
ALBUM = 'Økonomisk teori før høsten'

# Fagforkortelser skrevet om til norsk uttale. Uten dette leser talesyntesen
# «QALY» og «HHI» som ord, ikke som fagtermer.
UTTALE = {
    'EØS': 'e-ø-ess', 'EU': 'e-u', 'USA': 'u-s-a',
    'QALY': 'kvali', 'SSNIP': 'snipp', 'GUPPI': 'guppi', 'SIEC': 'sikk',
    'DEA': 'de-e-a', 'HHI': 'hå-hå-i', 'UPP': 'u-pe-pe', 'BLP': 'be-el-pe',
    'AVC': 'a-ve-se', 'AAC': 'a-a-se', 'LRAIC': 'el-er-a-i-se',
    'ECPR': 'e-se-pe-er', 'RPI': 'er-pe-i', 'DRG': 'de-er-ge',
    'WTP': 'dobbelt-ve-te-pe', 'WTA': 'dobbelt-ve-te-a',
    'CO2': 'se-o-to', 'TFEU': 'te-ef-e-u', 'FTC': 'ef-te-se',
    'NHH': 'en-hå-hå', 'UiB': 'Universitetet i Bergen', 'DFØ': 'de-ef-ø',
    'SSB': 'ess-ess-be', 'NVE': 'en-ve-e', 'UCLA': 'u-se-el-a',
    'BECCLE': 'bekkle', 'KILE': 'kile', 'ESA': 'Esa', 'RAND': 'rand',
    'R-109': 'err 109',
}


def les_manus():
    """Deler manuset i episoder med overskrifter og avsnitt."""
    episoder = []
    gjeldende = None
    for rå in open(MANUS, encoding='utf-8'):
        linje = rå.strip()
        if not linje:
            continue
        if linje.startswith('### '):
            if gjeldende:
                gjeldende['blokker'].append(('h3', linje[4:]))
        elif linje.startswith('## '):
            treff = re.match(r'Episode (\d+): (.*)', linje[3:])
            if treff:
                gjeldende = {'nr': int(treff.group(1)), 'tittel': treff.group(2), 'blokker': []}
                episoder.append(gjeldende)
        elif linje.startswith('# '):
            continue
        elif gjeldende:
            gjeldende['blokker'].append(('p', linje))
    return episoder


def for_opplesning(tekst):
    """Gjør teksten uttalbar: forkortelser, tankestreker og sitattegn."""
    for forkortelse, uttale in UTTALE.items():
        tekst = re.sub(r'\b%s\b' % re.escape(forkortelse), uttale, tekst)
    tekst = tekst.replace('—', ',').replace('–', ',')
    tekst = tekst.replace('«', '').replace('»', '')
    tekst = re.sub(r',\s*,', ',', tekst)
    return re.sub(r'\s+', ' ', tekst).strip()


def filnavn(nr, tittel):
    grunn = unicodedata.normalize('NFKD', tittel.lower())
    grunn = grunn.replace('ø', 'o').replace('æ', 'ae').replace('å', 'a')
    grunn = ''.join(c for c in grunn if not unicodedata.combining(c))
    grunn = re.sub(r'[^a-z0-9]+', '-', grunn).strip('-')
    return '%02d-%s' % (nr, grunn)


RAMMERATE = 22050


def skriv_stillhet(wav, sekunder):
    wav.writeframes(b'\x00\x00' * int(RAMMERATE * sekunder))


def skriv_tale(wav, stemme, tekst):
    for bit in stemme.synthesize(for_opplesning(tekst)):
        wav.writeframes(bit.audio_int16_bytes)


def main():
    if not os.path.exists(STEMME):
        sys.exit('Fant ikke stemmemodellen %s — se bruksanvisningen øverst i filen.' % STEMME)
    from piper import PiperVoice
    import imageio_ffmpeg

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    stemme = PiperVoice.load(STEMME)
    os.makedirs(UTKATALOG, exist_ok=True)
    episoder = les_manus()

    # Global avsnittsteller, samme rekkefølge som avsnittene i HTML-versjonen,
    # slik at teksten kan markeres synkront under avspilling av lydfilene.
    avsnitt_nr = 0
    indeks = {}

    for episode in episoder:
        navn = filnavn(episode['nr'], episode['tittel'])
        wav_sti = os.path.join(UTKATALOG, navn + '.wav')
        mp3_sti = os.path.join(UTKATALOG, navn + '.mp3')
        merker = []

        with wave.open(wav_sti, 'wb') as ut:
            ut.setnchannels(1)
            ut.setsampwidth(2)
            ut.setframerate(RAMMERATE)
            skriv_tale(ut, stemme, 'Episode %d. %s.' % (episode['nr'], episode['tittel']))
            skriv_stillhet(ut, 0.9)
            for slag, tekst in episode['blokker']:
                if slag == 'h3':
                    skriv_stillhet(ut, 0.5)
                    skriv_tale(ut, stemme, tekst + '.')
                    skriv_stillhet(ut, 0.45)
                else:
                    merker.append([avsnitt_nr, round(ut.tell() / RAMMERATE, 2)])
                    avsnitt_nr += 1
                    skriv_tale(ut, stemme, tekst)
                    skriv_stillhet(ut, 0.35)
            lengde = ut.tell() / RAMMERATE

        indeks[str(episode['nr'])] = {
            'fil': navn + '.mp3',
            'lengde': round(lengde, 2),
            'avsnitt': merker,
        }

        subprocess.run([
            ffmpeg, '-y', '-loglevel', 'error', '-i', wav_sti,
            '-codec:a', 'libmp3lame', '-b:a', '64k', '-ac', '1',
            '-metadata', 'title=Episode %d: %s' % (episode['nr'], episode['tittel']),
            '-metadata', 'album=%s' % ALBUM,
            '-metadata', 'artist=%s' % ALBUM,
            '-metadata', 'track=%d' % (episode['nr'] + 1),
            '-metadata', 'genre=Speech',
            mp3_sti,
        ], check=True)
        os.remove(wav_sti)

        print('%s.mp3 — %d:%02d' % (navn, lengde // 60, lengde % 60), flush=True)

    import json
    with open(os.path.join(UTKATALOG, 'lydindeks.json'), 'w', encoding='utf-8') as f:
        json.dump(indeks, f, ensure_ascii=False, indent=1)

    print('Ferdig: %d filer i %s' % (len(episoder), UTKATALOG))


if __name__ == '__main__':
    main()
