# plaits-palette-navigator

travelers guide for decoding the voice index: load a Rubato Audio Plaits Palette configuration (`.plaits-palette.json`, from **Save configuration** on https://rubato.audio/plaits-palette/) and the page builds a guide to that exact firmware: every model in every bank with its four controls, out / aux / trig, the options menu with the build's starting settings, chord tables and 6-op fm patch names.

live page: https://mellotom.github.io/plaits-palette-navigator/

- the file is read in the browser; nothing is uploaded. the browser remembers the last palette, and the share link carries the whole guide in the address.
- model names and descriptions come from the Rubato Audio Plaits Palette catalog (github.com/lylepmills/eurorack, `alt_firmwares/plaits_lab_catalog/public_catalog.json`), pulled 2026.11.14. a model newer than that shows by id only until the catalog is pulled again.
- stock fm patch names come from the Mutable Instruments Plaits source banks.

## rebuilding

`python3 build/gen.py <plaits-navigator/index.html> index.html` — the plaits guide's page is the style template; `build/models.json` is the catalog extract, `build/app.js` the page logic.

design homage to the house of x / powers of x data pages by tom muller with jonathan hickman. not affiliated with rubato audio, mutable instruments or marvel.
