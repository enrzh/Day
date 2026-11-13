# Changelog

The same notes as a page, which Day's Settings → What's New opens: <https://enrzh.github.io/Day/changelog/>. That page is built from `changelog/releases.json` with `python3 scripts/changelog.py`.

What changed in each version of Day, newest first. Day comes from the [App Store](https://apps.apple.com/app/day-calendar/id6822896434), which delivers updates itself, so there is no separate update feed; these are the notes from the store's "What's New", with what each version added on top of the one before.

## 2.1.6 · iPhone and iPad

- Habits: any repeating reminder can be a habit. Set a weekly goal (for example 4 times a week) and Day tracks the current streak, the longest streak, how many days you did it and missed, and in how many weeks you met the goal.
- Forgiving streak: a day you skip on purpose is excused. It counts as neither done nor missed, so it does not break the streak.
- At the End of the Day: choose per reminder what Day does when the day is over — leave it open, mark it completed, or (for repeating reminders) skip it. Day applies this as of the day the reminder was due, when you open the app and in the refresh iOS allows after midnight. A day that ended while neither ran is settled the next time. Ticking a settled reminder back on is never undone again. The rules stay on this device.
- Values: log an amount per day on a habit's card (8 km, 20 min) with a unit, and see a line of the last 30 days.
- Weekly habit graph (Settings > Reminders > Habit Graph, off by default): replaces the 70-day square grid on a repeating reminder's card with one bar per week showing how much of it was done. Streak, done and missed figures stay.
- Today's habits sit at the top of the day's list.
- New Habits widget (small and medium): lists today's open habits, each with a button that ticks it off, as in the app.
- Find Free Time (Calendar menu, ⇧⌘F with a keyboard): a sheet lists the free stretches of the next five days, 8:00 to 20:00 and from now on today, for a length of 15 minutes to 2 hours. Tap a gap to start a new event at its beginning. Only this device's calendars count.
- Settings > What's New now opens the notes from Day's public site in the app, so a new version's notes show up without an app update. Offline, the notes bundled with the app show instead. Nothing about you is sent; the site only sees a normal web request.
- Habits and Find Free Time are translated into all ten languages.

Fixes:

- Up Next, Reminders and Invitations: a card picked from the list now opens in front. On the Mac it opened hidden behind the sheet.

## 2.1.6 · Mac

- Everything in iPhone and iPad 2.1.6: Habits, the Habits widget, Find Free Time (⇧⌘F) and What's New from the public site.
- Since Mac 2.1.3, also: pull down on a timeline or press ⌘R to refresh calendars and reminders (Refresh is in the View menu), and the Mac now keeps every view you have opened and warms the others after launch, so switching between Day, 3 Days, Week, Month and Year is a show, not a rebuild (median switch hitch measured 110 ms before, 39 ms now).

Fixes:

- Search: the field takes everything you type. It used to collapse to a magnifier after the first letter. Escape still leaves search, and ⌘F focuses it.
- Month: the '+n more' list is a floating panel like the event card, so a click outside closes it and still reaches what is under it. Escape or a second click on the button also closes it, and a click on a row opens that event's card.
- The event card, the Month's '+n more' list and cards picked from Up Next, Reminders or Invitations open in front of the window and of sheets, not behind them.
- A swipe on a day's list no longer taps New Event. The top bar is one line that shrinks, with a single Today stepper, and clicks land where you aim.

## 2.1.5 · iPhone and iPad

- Pull down on a timeline to refresh your calendars and reminders.
- Swiping through a day's list in Month no longer taps New Event by mistake.

## 2.1.4 · iPhone and iPad

- Up Next: an overdue all-day reminder now shows its own title on the pill, instead of a blank label.

## 2.1.3 · iPhone and iPad

- Reminders: delete a list from its menu, groups with no list to show are hidden, and your list groups now follow your iCloud to your other devices.
- Turn Scheduled or another card back on and it returns to its place, not the end.
- Edit's list rows are tighter, so titles keep their room.
- Touch and hold an event or reminder in a list, then tap the popup to open it, with VoiceOver actions for the menu.
- The optional on-device model for Quick Add can now be downloaded in more regions.

## 2.1.2 · Mac

- Mac: Settings opens in its own window, and Day remembers window size and calendar position.
- Mac: Month view fits more event text, shows details next to the event, and supports dragging events and scheduling reminders.
- Reminders: choose the list order and which lists show as cards, plus automatic list emoji.
- Settings: Calendars and Reminders have their own pages, and permissions are shown the same way everywhere.
- iPad: Settings is in the top bar, and ⌘1–5 switch views.

macOS 2.1.3 is in App Review and will be listed here once it is out.
