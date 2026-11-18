# jaimegomesparente.github.io

Portfolio en ligne : https://jaimegomesparente.github.io

Site statique servi tel quel par GitHub Pages (HTML et CSS, sans JavaScript ni étape de build).

## Structure

```
index.html          la page
style.css           styles, couleurs, mode sombre
favicon.svg
.nojekyll           sert les fichiers tels quels, sans Jekyll
fonts/              Archivo Black et IBM Plex Mono (licence OFL)
img/                images tramées, générées par tools/dither.py
tools/
  dither.py         trame les images de tools/raw/ vers img/
  illustrations.py  illustrations provisoires dessinées en code
  raw/              images sources (captures, illustrations)
```

## Changer une image

1. Mettre une capture dans `tools/raw/`, avec le nom de l'image à remplacer (`claylings.png`, `wooly.png`, `gravity.png`, `facemask.png`), ou un nouveau nom.
2. Lancer :

   ```bash
   pip install pillow numpy
   python3 tools/dither.py                                  # toutes les images
   python3 tools/dither.py tools/raw/claylings.png --method atkinson --gamma 0.8
   ```

3. Committer le PNG produit dans `img/`.

Options utiles : `--method bayer|atkinson|floyd` (Bayer pour les schémas, Atkinson pour les captures), `--gamma` (< 1 éclaircit les captures sombres), `--contrast`, `--invert`.

Les images font 288 × 180 px et la page les affiche exactement à 2× (1× sur mobile), avec `image-rendering: pixelated`. Une échelle non entière rendrait la trame floue ou ferait du moiré : si la largeur change dans `dither.py`, il faut changer `.px` dans `style.css`.

## Ajouter un projet

Copier un bloc `<article class="card">` dans `index.html`, puis changer le lien, l'image, le texte et le numéro de figure.

## Publication

Settings → Pages → Build and deployment → Source : *Deploy from a branch*, branche `main`, dossier `/ (root)`. Chaque push sur `main` met le site à jour.
