STREAKWISE — updated weekly schedule

Open streakwise-single.html in a modern browser, or run a local server from this folder:
  python -m http.server 8000
Then visit http://localhost:8000/streakwise-single.html

Changes in this update:
- English classes are scheduled Sunday, Tuesday and Thursday, 16:10–17:40.
- Existing saved default class times are migrated automatically on load, while manually customized times are preserved.
- Uncompleted future class instances are updated; completed historical records are preserved.
- Homework, JavaScript review/practice, Thursday project, English practice and exercise blocks are adjusted to avoid overlapping the new class time.
- Persian RTL layout is hardened for cards, images, navigation, and narrow screens.

Persian font:
The HTML references assets/fonts/Iranian-Sans.ttf. The font file itself was not present among the project files available in this edit, so place your supplied TTF file at that exact path. Until then, the browser uses the configured Persian fallback fonts.

Data is stored locally in the browser under the Streakwise localStorage key. Export a backup before clearing browser data.
