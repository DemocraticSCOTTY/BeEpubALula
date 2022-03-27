#!/usr/bin/env python3

from os import getcwd as cwd, scandir as scd, system as run
from PIL import Image as img

src = f"{ cwd() + '/' + 'corpora' }"
dst = f"{ cwd() + '/' + 'processed.txt' }"


def main(src, dst, exe, ext, lng, dpi, psm):

  ext = [str(item) for item in args.ext.split(',')]
  dpi = lambda img, dpi=dpi: f"{img.open(img).info['dpi'][0]}" if (
   dpi == None) else f"{dpi}"
  corpora = [
   f"{e.path}" for e in scd(src) for each in ext if e.name.endswith(each)
  ]
  cmdlist = [
   f"{exe} {f} {f} -l {lng} --psm {psm} {'--dpi ' + dpi(f) if (dpi==None) else ''}"
   for f in corpora
  ]

  for cmd in cmdlist:
   run(cmd)
  run(f"cat {src}/*.txt > ocr.txt && rm -f {src}/*.txt")

  open(dst, encoding='utf8', mode='w').write(
    '\n'.join([l.rstrip() for l in open('ocr.txt')]) \
    .replace('\n\n','ø\n') \
    .replace('\n',' ') \
    .replace('ø','\n') \
    .replace('- ', '') \
    .replace('\n ', '\n')
  )

  run(f"rm -f ocr.txt")


import argparse
parser = argparse.ArgumentParser(description='Images to OCR', prog='t5')
parser.add_argument(
  '-s',
  '--src',
  help=
  f"{ 'Chemin dossier contenant les images à océriser (default: ' + src + ')' }",
  type=str,
  default=src)
parser.add_argument(
  '-d',
  '--dst',
  help=
  f"{ 'Chemin dossier contenant la sortie océrisée (default: ' + dst + ')' }",
  type=str,
  default=dst)
parser.add_argument(
  '-e',
  '--exe',
  help=
  "Chemin exécutable tesseract par défault tesseract (default: tesseract)",
  type=str,
  default='tesseract')
parser.add_argument(
  '-x',
  '--ext',
  help="Liste des extensions (default: '.jpg,.jpeg,.tif,.png')",
  type=str,
  default=".jpg,.jpeg,.tif,.png")
parser.add_argument(
  '-l',
  '--lng',
  help="Langue (default: fra)",
  type=str,
  default='fra')
parser.add_argument(
  '-i',
  '--dpi',
  help="dpi si connue (default: None)",
  type=str,
  default=None)
parser.add_argument(
  '-p',
  '--psm',
  help="Prévu pour un futur usage (lstm fine tuning) (default: 1)",
  type=int,
  default=1)
args = parser.parse_args()

main(**vars(args))
