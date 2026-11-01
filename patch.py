from pathlib import Path
p=Path('/mnt/data/streakwise-update/streakwise-single.html')
s=p.read_text()
# New class schedule
s=s.replace("english: {\n    sat: null, sun: ['19:30', '21:00'], mon: null, tue: ['19:30', '21:00'],\n    wed: null, thu: ['19:30', '21:00'], fri: null\n  }", "english: {\n    sat: null, sun: ['16:10', '17:40'], mon: null, tue: ['16:10', '17:40'],\n    wed: null, thu: ['16:10', '17:40'], fri: null\n  }")
# Routine timing adjustments to prevent overlap with new class times
s=s.replace("{ id: 'r-homework', title: 'Homework & school review', description: 'Finish assignments first, then review today’s lessons', category: 'school', days: SCHOOL_DAYS, order: 20, startTime: '15:00', endTime: '16:00' },", "{ id: 'r-homework', title: 'Homework & school review', description: 'Finish assignments first, then review today’s lessons', category: 'school', days: ['sat','mon','wed'], order: 20, startTime: '14:45', endTime: '15:45' },\n  { id: 'r-homework-sun', title: 'Homework & school review', description: 'Finish assignments first, then review today’s lessons', category: 'school', days: ['sun'], order: 20, startTime: '13:30', endTime: '14:30' },\n  { id: 'r-homework-tue', title: 'Homework & school review', description: 'Finish assignments first, then review today’s lessons', category: 'school', days: ['tue'], order: 20, startTime: '14:30', endTime: '15:30' },")
s=s.replace("{ id: 'r-js-practice', title: 'JavaScript exercises & practice', description: 'Solve problems without the video running', category: 'programming', days: ['sun'], order: 30, startTime: '15:00', endTime: '16:00', jsStage: 'practice' },", "{ id: 'r-js-practice', title: 'JavaScript exercises & practice', description: 'Solve problems without the video running', category: 'programming', days: ['sun'], order: 40, startTime: '14:45', endTime: '15:30', jsStage: 'practice' },")
s=s.replace("{ id: 'r-js-review', title: 'JavaScript review & practice', description: 'Revisit older topics, fix weak spots', category: 'programming', days: ['tue'], order: 30, startTime: '16:30', endTime: '17:15', jsStage: 'review' },", "{ id: 'r-js-review', title: 'JavaScript review & practice', description: 'Revisit older topics, fix weak spots', category: 'programming', days: ['tue'], order: 50, startTime: '18:15', endTime: '19:00', jsStage: 'review' },")
s=s.replace("{ id: 'r-rest', title: 'Meals, rest & free time', description: 'Eat properly and take a real break', category: 'health', days: SCHOOL_DAYS, order: 30, startTime: '16:00', endTime: '16:30' },", "{ id: 'r-rest', title: 'Meals, rest & free time', description: 'Eat properly and take a real break', category: 'health', days: ['sat','mon','wed'], order: 30, startTime: '15:45', endTime: '16:15' },\n  { id: 'r-rest-sun', title: 'Meals, rest & free time', description: 'Eat properly and take a real break', category: 'health', days: ['sun'], order: 30, startTime: '14:30', endTime: '15:10' },\n  { id: 'r-rest-tue', title: 'Meals, rest & free time', description: 'Eat properly and take a real break', category: 'health', days: ['tue'], order: 30, startTime: '15:30', endTime: '16:00' },")
s=s.replace("{ id: 'r-project-thu', title: 'Personal programming project', description: 'Move your own project forward', category: 'programming', days: ['thu'], order: 30, startTime: '14:00', endTime: '15:30', jsStage: 'project' },", "{ id: 'r-project-thu', title: 'Personal programming project', description: 'Move your own project forward', category: 'programming', days: ['thu'], order: 30, startTime: '13:30', endTime: '14:45', jsStage: 'project' },")
s=s.replace("{ id: 'r-en-thu', title: 'English practice', description: 'Speaking, writing or listening', category: 'english', days: ['thu'], order: 40, startTime: '16:00', endTime: '16:30' },", "{ id: 'r-en-thu', title: 'English practice', description: 'Speaking, writing or listening', category: 'english', days: ['thu'], order: 40, startTime: '15:00', endTime: '15:30' },")
s=s.replace("{ id: 'r-exercise', title: 'Exercise & rest', description: 'Move your body, then switch off', category: 'health', days: ['thu'], order: 80, startTime: '17:00', endTime: '18:00' },", "{ id: 'r-exercise', title: 'Exercise & rest', description: 'Move your body, then switch off', category: 'health', days: ['thu'], order: 80, startTime: '18:00', endTime: '19:00' },")
# Migration: update old saved English class times without overwriting user's custom schedule
needle="""  if (raw.schedule && typeof raw.schedule === 'object') {
    ['school', 'english'].forEach(kind => DAYS.forEach(day => {
      const v = raw.schedule[kind] && raw.schedule[kind][day];
      o.schedule[kind][day] = Array.isArray(v) && okTime(v[0]) && okTime(v[1]) ? [v[0], v[1]] : null;
    }));
  }
"""
replacement=needle+"""  // One-time migration: move the previous default English class slots to 16:10–17:40.
  // Preserve any schedule times the user has manually customized.
  const oldEnglish = { sun: ['19:30','21:00'], tue: ['19:30','21:00'], thu: ['19:30','21:00'] };
  Object.entries(oldEnglish).forEach(([day, oldSlot]) => {
    const current = o.schedule.english[day];
    if (Array.isArray(current) && current[0] === oldSlot[0] && current[1] === oldSlot[1]) {
      o.schedule.english[day] = ['16:10','17:40'];
    }
  });
"""
if needle not in s: raise SystemExit('schedule normalization block not found')
s=s.replace(needle,replacement)
# Update uncompleted future generated class entries during normalization; completed history stays untouched
needle2="""  // Backfill scheduled times for tasks created by earlier versions of this app.
  o.tasks.forEach(t => {
"""
replacement2="""  // Migrate uncompleted class entries in today/future from the old default time.
  o.tasks.forEach(t => {
    if (t.routineId === 'sys:english' && !t.completed && !t.edited && t.date >= todayKey()) {
      const wd = weekdayId(t.date), slot = o.schedule.english[wd];
      if (slot) { t.startTime = slot[0]; t.endTime = slot[1]; }
    }
  });
  // Backfill scheduled times for tasks created by earlier versions of this app.
  o.tasks.forEach(t => {
"""
if needle2 not in s: raise SystemExit('task migration block not found')
s=s.replace(needle2,replacement2)
# CSS improvements for Persian layout and mixed direction content
css="""
/* Persian RTL layout hardening: prevent text/image collisions in cards and responsive rows. */
html[lang="fa"] body { direction: rtl; text-align: right; font-family: 'Iranian Sans','Vazirmatn','Noto Sans Arabic',Tahoma,sans-serif; }
html[lang="fa"] .wrap, html[lang="fa"] .page { direction: rtl; }
html[lang="fa"] .top-bar, html[lang="fa"] .stats3, html[lang="fa"] .week,
html[lang="fa"] .home-grid, html[lang="fa"] .row-cards, html[lang="fa"] .info-grid,
html[lang="fa"] .profile, html[lang="fa"] .sec { direction: rtl; }
html[lang="fa"] .st + .st::before { left: auto; right: 0; }
html[lang="fa"] .banner { direction: rtl; text-align: right; padding: 14px 6px 14px 18px; gap: 10px; }
html[lang="fa"] .banner-art { margin-left: 0; margin-right: -4px; flex: 0 0 clamp(76px, 27%, 112px); width: clamp(76px, 27%, 112px); min-width: 0; }
html[lang="fa"] .banner-art svg, html[lang="fa"] .banner-art img { width: 100%; height: auto; }
html[lang="fa"] .banner-txt { direction: rtl; text-align: right; flex: 1 1 0; min-width: 0; max-width: none; overflow-wrap: anywhere; position: relative; z-index: 1; }
html[lang="fa"] .banner-txt strong { line-height: 1.5; letter-spacing: 0; }
html[lang="fa"] .keep { direction: rtl; }
html[lang="fa"] .keep-txt { text-align: right; max-width: 66%; min-width: 0; }
html[lang="fa"] .trophy { right: auto; left: -10px; }
html[lang="fa"] .crew-av { direction: ltr; }
html[lang="fa"] .info, html[lang="fa"] .road { direction: rtl; text-align: right; }
html[lang="fa"] .info-k { direction: rtl; }
html[lang="fa"] .nav { direction: rtl; }
html[lang="fa"] .nav button { direction: rtl; }
html[lang="fa"] .nav button[aria-current="page"] { padding: 0 18px 0 22px; }
html[lang="fa"] .nav .lbl { margin-left: 0; }
html[lang="fa"] .nav button[aria-current="page"] .lbl { margin-left: 0; margin-right: 9px; }
html[lang="fa"] .nav .lbl > span { transform: translateX(6px); }
html[lang="fa"] .nav button[aria-current="page"] .lbl > span { transform: none; }
html[lang="fa"] .task, html[lang="fa"] .task-main, html[lang="fa"] .task-main .t-title { direction: rtl; text-align: right; }
html[lang="fa"] .hero-top, html[lang="fa"] .hero-right { direction: ltr; }
html[lang="fa"] .t-time { direction: ltr; unicode-bidi: isolate; font-family: ui-monospace,monospace; }
html[lang="fa"] .calendar, html[lang="fa"] .cal-layout, html[lang="fa"] .cal-grid { direction: rtl; }
html[lang="fa"] .month-head, html[lang="fa"] .panel-head, html[lang="fa"] .panel-sub { direction: rtl; text-align: right; }
html[lang="fa"] .form, html[lang="fa"] .field { direction: rtl; text-align: right; }
html[lang="fa"] .btn-row { direction: rtl; }
html[lang="fa"] .row, html[lang="fa"] .rt-row { direction: rtl; }
html[lang="fa"] .row > *, html[lang="fa"] .rt-row > * { min-width: 0; }
@media (max-width: 520px) {
  html[lang="fa"] .row-cards { grid-template-columns: minmax(0, .9fr) minmax(0, 1.1fr); gap: 8px; }
  html[lang="fa"] .banner { gap: 8px; }
  html[lang="fa"] .banner-txt strong { font-size: 15px; }
  html[lang="fa"] .banner-txt .sm { font-size: 11px; line-height: 1.65; }
  html[lang="fa"] .keep-txt { max-width: 70%; }
}
@media (max-width: 360px) {
  html[lang="fa"] .row-cards { grid-template-columns: 1fr; }
  html[lang="fa"] .crew, html[lang="fa"] .keep { min-height: 124px; }
}
"""
s=s.replace("@media(max-width:420px){.t-time{font-size:10.5px}}\n\n</style>", "@media(max-width:420px){.t-time{font-size:10.5px}}\n"+css+"\n</style>")
p.write_text(s)
print('patched',len(s))
