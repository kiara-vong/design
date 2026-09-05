# -*- coding: utf-8 -*-
"""The four case studies' content. Structure lives in gen-cases.py.

SOURCING AND CONFIDENTIALITY. The work described here is real and the details are
taken from the owner's own project material. What is NOT here, deliberately: the
internal product name, internal URLs, private repository or pull-request links,
and the employer's brand hex values. Those appear only in an internally-classified,
DLP-marked deck, and a public portfolio is not the place for any of them.

The line drawn is the one the owner already drew herself in the public demo
repository that these screenshots come from: describe the engineering decisions
and their outcomes, name the employer, never the internal system. Every metric
below is about her own work -- files touched, PRs cut, review order -- rather than
about the company's data, customers or infrastructure.
"""
from gen.case_template import build, section, sub, NOTE
from gen.case_blocks import stats, rules, figure_raw, before_after, plate

CO = "Capital One"

# =====================================================================
build("resource-dashboard", dict(
    out="work/resource-dashboard.html", root="../",
    kicker=CO,
    title="Resource Dashboard",
    hero="case/cs-dash-seams.svg",
    hero_alt="A cloud resource dashboard with filters, a drill-down graph view and an export action",
    intro=("Engineers responsible for cloud resources had no single place to see "
           "them. Answering “what do I own, and what needs attention” meant "
           "three tools and a spreadsheet. I designed and built the dashboard that "
           "replaced that: one surface, two ways through it, and an export at every "
           "level."),
    meta=[("Role", "Design engineer,<br>front end"),
          ("Stack", "React, TypeScript,<br>MUI, AG Grid"),
          ("Scope", "IA, components,<br>end-to-end flows"),
          ("Status", "Shipped to<br>enterprise users"),
          ("Note", NOTE)],
    nav=[("overview", "Overview", False),
         ("context", "Context", False),
         ("decisions", "Key decisions", False),
         ("two-views", "Two views over one dataset", True),
         ("drill", "Drilling without getting lost", True),
         ("export", "An export at every level", True),
         ("impact", "What changed", False)],
    sections=(
        section("context", "Context",
                "Everything was somewhere, nothing was anywhere",
                ["The data already existed. Ownership lived in one system, compliance "
                 "jobs in another, the resource inventory in a third, and the way you "
                 "answered a question about your own infrastructure was to open all "
                 "three and reconcile them by hand.",
                 "That is a shape of problem I keep running into: nothing is broken, "
                 "every individual tool works, and the entire cost sits in the seams "
                 "between them. It never gets filed as a bug because no single step is "
                 "wrong. It just quietly taxes everyone who has to do it."],
                plate("video", "workflow demo, looping",
                      "The three-tool reconciliation, before the dashboard existed",
                      "A screen recording of the old workflow, so the reader feels the "
                      "cost instead of being told about it. Cut it tight: the point is "
                      "how many windows it takes to answer one question.",
                      ["Window 1: ownership lookup, paste an identifier",
                       "Window 2: the compliance job list, find the same resource",
                       "Window 3: the inventory, confirm what it actually is",
                       "End on all three open at once"],
                      [("Size", "799x391"), ("Format", "muted mp4 + webm, or animated webp"),
                       ("Length", "8-12s, seamless loop"), ("Cursor", "visible")])),

        '    <div id="decisions" class="cs-group">\n\n' +
        sub("two-views", "Key decisions", "Two views over one dataset",
            ["Two groups of people arrive at a tool like this with genuinely different "
             "questions. One has a job to do today and wants the shortest path to it. "
             "The other is exploring, and needs to understand the shape of what they own.",
             "Rather than average them into one compromised view, the dashboard has "
             "two and makes the default the urgent one. The job-focused view opens "
             "first, sorted by due date, because someone arriving without a plan is "
             "usually arriving because something is due. The hierarchy explorer is one "
             "toggle away for everyone else."],
            plate("anno", "dots-to-lines callouts",
                      "The default view, annotated",
                      "One clean capture of the job-focused view with four callouts "
                      "drawn onto it: a dot on the element, a hairline out to a short "
                      "label in the margin. Same device the reference build uses to "
                      "explain a screen.",
                      ["Callout: the urgency sort, and why it is the default",
                       "Callout: the view toggle",
                       "Callout: filters that persist across both views",
                       "Callout: the export, scoped to what is on screen"],
                      [("Size", "799x391 @2x"), ("Format", "PNG, no OS chrome"),
                       ("Note", "leave ~120px clear on the right for labels")]),
            first=True),

        sub("drill", "Key decisions", "Drilling without getting lost",
            ["The explorer goes environment, then region, then type, then the resource "
             "itself. Four levels is enough to get lost in, so every level carries its "
             "own counts and a breadcrumb back out.",
             "The counts are the part that earns its place. A level that only lists "
             "categories tells you where you can go; a level that lists categories with "
             "how much is in each tells you where you should go. It is a small addition "
             "that changes the drill-down from navigation into triage."],
            plate("seq", "zoom-in sequence, four steps",
                      "Drilling environment to region to type to resource",
                      "Four frames of the same explorer, one per level, so the reader "
                      "sees the descent rather than one arbitrary level. Keep the "
                      "breadcrumb visible in every frame; it is what makes the sequence "
                      "read as a single movement.",
                      ["Frame 1: environments, with counts",
                       "Frame 2: regions inside the chosen environment",
                       "Frame 3: resource types",
                       "Frame 4: the resources themselves"],
                      [("Size", "799x391 @2x each"),
                       ("Format", "4 PNGs, or one cross-fading loop"),
                       ("Note", "same window size and scroll position in all four")])),

        sub("export", "Key decisions", "An export at every level",
            ["Every table exports, and what it exports is exactly what you are looking "
             "at: current filters, current level, nothing else.",
             "This sounds like a checkbox feature and was one of the most-used things "
             "in the tool. People do not live in dashboards. They come in, narrow down "
             "to the thing they care about, and then need it somewhere else — a "
             "ticket, a spreadsheet, a message to the team that owns it. A dashboard "
             "that cannot hand off its own answer sends everyone back to the "
             "reconciling-by-hand it was built to remove."]) +
        '    </div>\n\n',

        section("impact", "Impact", "From three tools to one",
                ["The reconciliation step is gone. What used to be a cross-tool search "
                 "is a paste-an-identifier lookup, and what used to be invisible — "
                 "which of your resources have work outstanding — is the screen "
                 "that opens by default.",
                 "The dashboard shipped to enterprise users. Figures below describe the "
                 "shape of the work rather than usage numbers, which are not mine to "
                 "publish."],
                fig=before_after([
                    ("No single view of your resources", "One surface, two ways through it"),
                    ("Search across several tools", "Paste an identifier, get the resource"),
                    ("Outstanding work invisible", "Default view, sorted by urgency"),
                    ("Manual, fragmented exports", "One-click export at any level"),
                    ("Metadata hard to parse", "Organised for scanning"),
                    ("No compliance history", "Event timeline and table"),
                ])),
    )))

# =====================================================================
build("events-timeline", dict(
    out="work/events-timeline.html", root="../",
    kicker=CO,
    title="Events Timeline",
    hero="case/cs-tl-carry.svg",
    hero_alt="A compliance event timeline with coloured state segments and dated event dots",
    intro=("A resource's compliance history was a table of rows sorted by date, which "
           "is technically the whole story and practically unreadable. I designed the "
           "timeline that sits above it: a single track where you can see, at a glance, "
           "how long something has been in trouble and when it stopped being."),
    meta=[("Role", "Design engineer,<br>front end"),
          ("Stack", "React, TypeScript"),
          ("Scope", "Timeline, events table,<br>accessibility pass"),
          ("Status", "Shipped in beta"),
          ("Note", NOTE)],
    nav=[("overview", "Overview", False),
         ("context", "Context", False),
         ("decisions", "Key decisions", False),
         ("carry", "Colouring the gaps", True),
         ("collapse", "When two things happen at once", True),
         ("keys", "Making it work without a mouse", True),
         ("impact", "What changed", False)],
    sections=(
        section("context", "Context",
                "A table is a list of events, not a history",
                ["The events were all there, sorted by timestamp, each one accurate. "
                 "But the question people actually had was never “what happened on "
                 "the third of August”. It was “how long has this been "
                 "broken”, and a table answers that only if you are willing to read "
                 "it and do arithmetic.",
                 "A timeline answers it by being looked at. That is the whole argument "
                 "for the feature: the data did not change, the shape of it did."],
                plate("still", "explored / shipped",
                      "The table on its own, before the timeline sat above it",
                      "A capture of the events table with no timeline, so the reader "
                      "meets the problem in its original form. Label it EXPLORED and "
                      "pair it with the shipped version further down.",
                      ["Enough rows to make the date arithmetic look tedious",
                       "At least one violated-then-fixed pair several days apart"],
                      [("Size", "799x391 @2x"), ("Format", "PNG"),
                       ("Label", "EXPLORED, top left, mono caps")])),

        '    <div id="decisions" class="cs-group">\n\n' +
        sub("carry", "Key decisions", "Colouring the gaps",
            ["Events are discrete and compliance is continuous, and that mismatch is "
             "the whole engineering problem. A resource that was violated on the 3rd "
             "and fixed on the 8th generates two events and five days of nothing, and "
             "those five days are the part that matters most.",
             "So state carries forward: the segment between two events is coloured by "
             "the state the earlier one left behind, not by the absence of data. Drawn "
             "the naive way, the track shows two dots and a gap, which reads as "
             "“nothing was wrong” for precisely the stretch when something was."],
            plate("seq", "explored vs shipped, stacked",
                      "The naive track above the carry-forward track",
                      "Two renders of the same event data, stacked, so the difference "
                      "IS the figure. This is the most important image in the study: it "
                      "shows the engineering decision rather than describing it.",
                      ["Top: dots on a plain rule, gaps uncoloured (EXPLORED)",
                       "Bottom: the same dots with state carried across the gaps (SHIPPED)",
                       "Identical dates and width in both, so they read as one comparison"],
                      [("Size", "799x391 @2x"),
                       ("Format", "PNG, or a loop that wipes the coloured version in"),
                       ("Label", "EXPLORED / SHIPPED")]),
            first=True),

        sub("collapse", "Key decisions", "When two things happen at once",
            ["Events cluster. An automated fix fires, fails, retries and succeeds, and "
             "at any sensible zoom those are four dots occupying the same pixel.",
             "Adjacent same-day events collapse into one dot that opens a popover with "
             "all of them. The alternative was letting them overlap, which looks like a "
             "rendering bug, or spacing them evenly, which lies about when they "
             "happened. Collapsing keeps the position honest and moves the detail one "
             "interaction away, where there is room for it."]),

        sub("keys", "Key decisions", "Making it work without a mouse",
            ["The first version of the dots and the sortable table headers were "
             "mouse-only. Everything worked, and none of it could be reached from a "
             "keyboard.",
             "They take focus now, activate on Enter or Space, close on Escape, and "
             "announce themselves properly. I am putting this in a case study rather "
             "than quietly fixing it because the reason it shipped that way is worth "
             "saying out loud: it was built with a mouse in hand and never tested any "
             "other way. Nobody decided to exclude anyone. That is exactly how it "
             "usually happens."],
            fig=plate("video", "keyboard walkthrough",
                      "Tabbing through the timeline with no mouse",
                      "A recording with the cursor hidden and the focus ring visible, "
                      "moving dot to dot and into the sortable header. Nothing "
                      "demonstrates an accessibility fix like watching it work with no "
                      "pointer on screen.",
                      ["Tab onto the first dot, ring visible",
                       "Enter to open the popover",
                       "Escape to close it",
                       "Tab to the Timestamp header, Enter to re-sort"],
                      [("Size", "799x391"), ("Format", "muted mp4 + webm"),
                       ("Length", "10-14s"), ("Cursor", "hidden")]),
            after=rules([
                ("Reachable", "Every dot and sortable header is in the tab order."),
                ("Operable", "Enter or Space activates; Escape closes the popover."),
                ("Announced", "State is exposed, so the sort direction and the "
                              "open/closed state are not purely visual."),
            ])) +
        '    </div>\n\n',

        section("impact", "Impact", "The same data, now legible",
                ["The question the feature exists to answer — how long, and is it "
                 "fixed — went from a read-and-calculate to a glance. The table is "
                 "still there underneath for the cases where you need the specifics.",
                 "It shipped in beta for feedback, which was the right call for "
                 "something whose value is entirely in whether people read it the way "
                 "it was meant to be read."],
                fig=stats("Shipped in beta · figures describe scope, not usage", [
                    ("3", "0", "interaction states made keyboard-operable",
                     "timeline dots, popovers, sortable headers"),
                    ("2", "0", "views over one event stream",
                     "the summary track and the detail table"),
                    ("0", "0", "events dropped when they collide",
                     "same-day events collapse rather than overlap"),
                ], note="Most-used control&nbsp; <b>Timeframe filter</b>")),
    )))

# =====================================================================
build("ui-consistency", dict(
    out="work/ui-consistency.html", root="../",
    kicker=CO,
    title="UI Consistency",
    hero="case/cs-ui-drift.svg",
    hero_alt="Nine slightly different buttons on the left, the same nine identical on the right",
    intro=("The app had grown a dozen local dialects of the same interface: inline "
           "styles instead of tokens, four table layouts, three ways to say “no "
           "data”. I audited it, designed the shared layer underneath, and cut the "
           "208-file change into ten pull requests a human could actually review."),
    meta=[("Role", "Design engineer,<br>system owner"),
          ("Stack", "React, TypeScript,<br>MUI theming"),
          ("Scope", "208 files,<br>9 commits, 10 PRs"),
          ("Status", "Shipped"),
          ("Note", NOTE)],
    nav=[("overview", "Overview", False),
         ("context", "Context", False),
         ("decisions", "Key decisions", False),
         ("audit", "Counting what was actually there", True),
         ("theme", "One theme, no inline styles", True),
         ("prs", "Ten pull requests, in dependency order", True),
         ("impact", "What changed", False)],
    sections=(
        section("context", "Context",
                "Nobody set out to build four table layouts",
                ["Each one was a reasonable local decision. A team needed a table, the "
                 "existing one was close but not right, and copying it was ten minutes "
                 "against a week of negotiation. Enough reasonable local decisions "
                 "later, nobody could tell you what the product's table looked like, "
                 "because the honest answer was that it depended on the page.",
                 "The cost was not really aesthetic. It was that every change had to be "
                 "made in every copy, and the last copy was always the one somebody "
                 "forgot. A shared layer is worth building at the point where keeping "
                 "things in sync by hand costs more than the abstraction does, and we "
                 "were well past it."],
                plate("still", "contact sheet",
                      "Every live variant of one component, side by side",
                      "The real inventory, cropped from the actual pages and laid out "
                      "on one sheet. Buttons are the clearest case: nine near-identical "
                      "things next to each other make the argument in a way no count "
                      "ever does.",
                      ["Crop each variant at the same zoom, on a neutral ground",
                       "Keep their real spacing and radii; do not tidy them",
                       "Caption each with the surface it came from"],
                      [("Size", "799x391 @2x"), ("Format", "PNG"),
                       ("Note", "component chrome only, no data")])),

        '    <div id="decisions" class="cs-group">\n\n' +
        sub("audit", "Key decisions", "Counting what was actually there",
            ["The instinct is to design the target state and then go find everything "
             "that does not match it. I did the opposite: inventoried every variant "
             "already shipping, with no judgement attached, before proposing anything.",
             "That order mattered more than it sounds. Two of the variants I would have "
             "deleted on sight turned out to be load-bearing, solving a real constraint "
             "the canonical component could not. They became part of that component's "
             "API rather than exceptions to it. Designing first and reconciling later "
             "produces a system that is correct in isolation and wrong in the product, "
             "which is the usual way these fail."],
            first=True),

        sub("theme", "Key decisions", "One theme, no inline styles",
            ["The foundation is a single theme provider wrapping the app, with tokens "
             "for colour, typography, spacing and radius. Components inherit from it "
             "instead of carrying their own inline values.",
             "Underneath that, the shared pieces: one toolbar with search, filter chips "
             "and actions in a single row; one footer with the count on the left and "
             "export on the right; real empty and not-found states instead of the "
             "inline “no data” text that had been written separately on every "
             "page. Tables lost twenty pixels of row height, gained proper header "
             "treatment and zebra striping, and dropped to a subtler border.",
             "The filter chips are the detail I am most pleased with. They show at full "
             "width rather than truncating, overflow collapses into a +N chip, the "
             "dropdown stays open while you are still choosing, and typing hides the "
             "chips so you get a clean search field. Four small decisions, all of them "
             "about not interrupting someone mid-thought."],
            plate("still", "before / after, one component",
                      "One table, before and after the shared layer",
                      "The same table on the same page, captured either side of the "
                      "change. Row height, header treatment, striping and border weight "
                      "all move at once, which is why one component carries the story "
                      "better than a token diagram.",
                      ["Identical data and window width in both",
                       "Same scroll position, so only the styling differs",
                       "Label BEFORE / AFTER rather than old / new"],
                      [("Size", "799x391 @2x"), ("Format", "two PNGs, or one slider"),
                       ("Note", "the 72px to 52px row height should be obvious")])),

        sub("prs", "Key decisions", "Ten pull requests, in dependency order",
            ["208 files across 9 commits is not a reviewable change. It is a change "
             "that gets approved without being read, which is the same as not being "
             "reviewed, on a diff touching every page in the app.",
             "So it went out as ten pull requests of fifteen files or fewer, ordered so "
             "each could merge on its own. The theme provider had to land first because "
             "everything else assumes it. The shared table and filter components went "
             "second because the page-level work consumes them. After that the "
             "remaining seven were independent and could go in parallel, in any order, "
             "by whoever had time.",
             "The foundation PR contained no behavioural changes at all — visual "
             "consistency only. That was deliberate: the riskiest change in the "
             "sequence is the one everything depends on, so it should also be the one "
             "with the least in it."],
            fig=plate("still", "variants grid",
                      "The filter chip, in all four of its states",
                      "The chip work is the detail worth showing close up: full-width "
                      "labels, the +N overflow chip, the dropdown staying open, and "
                      "typing hiding the chips for a clean search field. Four small "
                      "decisions, one grid.",
                      ["State 1: one chip selected, label at full width",
                       "State 2: overflow, showing the +N chip",
                       "State 3: dropdown open mid-selection",
                       "State 4: typing, chips hidden"],
                      [("Size", "799x391 @2x"), ("Format", "PNG, 2x2 grid"),
                       ("Note", "crop tight to the control, not the page")]),
            after=rules([
                ("PR 1", "The theme provider and global defaults. No behavioural "
                         "change. Everything downstream assumes it."),
                ("PR 2", "Shared table, toolbar and filter components, consumed by "
                         "every page-level PR that follows."),
                ("PRs 3–10", "Page-level adoption. Independent of each other, "
                                  "reviewable in parallel, mergeable in any order."),
            ])) +
        '    </div>\n\n',

        section("impact", "Impact", "One product, one language",
                ["Every page now renders from one theme, and a change to a shared "
                 "component is one edit rather than a search-and-replace across the "
                 "app.",
                 "The result I care about most is quieter than the file count: design "
                 "review stopped spending its first ten minutes establishing which "
                 "version of a component we were looking at. The system's real output "
                 "is the argument it makes unnecessary."],
                fig=stats("208 files · 9 commits · 10 pull requests", [
                    ("208", "0", "files changed", "across the whole application"),
                    ("10", "0", "reviewable pull requests",
                     "15 files or fewer, dependency-ordered"),
                    ("1", "0", "theme provider",
                     "replacing inline styles throughout"),
                ], note="Riskiest PR&nbsp; <b>The one with no behaviour in it</b>")),
    )))

# =====================================================================
build("persona-homepage", dict(
    out="work/persona-homepage.html", root="../",
    kicker=CO,
    title="Persona Homepage",
    hero="case/cs-persona-reorder.svg",
    hero_alt="A homepage rearranging itself as the selected persona changes",
    intro=("A homepage serving several kinds of user, each of whom needs a different "
           "half of it. I am designing the customisation model: what it means for a "
           "page to reorder itself around who is looking, which defaults have to be "
           "right before anyone touches a setting, and how a page earns the right to "
           "move."),
    meta=[("Role", "Design engineer"),
          ("Stack", "React, TypeScript"),
          ("Scope", "In progress"),
          ("Status", "Coming soon"),
          ("Note", NOTE)],
    nav=[("overview", "Overview", False),
         ("context", "Context", False),
         ("thinking", "Where my head is", False)],
    sections=(
        section("context", "Context",
                "One homepage, several jobs",
                ["The people arriving at this page do not want the same things. Some "
                 "have a task and want the shortest path to it. Some are checking on "
                 "something they own. Some are new and do not yet know what the tool is "
                 "for. Today they all get the same page, which means it is sized for "
                 "the average of them and ideal for none.",
                 "The obvious answer is to let people customise it. The obvious answer "
                 "is also how you end up with a page most users never touch and a small "
                 "minority configure into something unsupportable."]),

        section("thinking", "Where my head is",
                "The defaults are the product",
                ["The thing I keep coming back to is that customisation is not the "
                 "feature. The default is the feature, and customisation is what you "
                 "offer the people the default cannot serve. If the starting layout is "
                 "right for most people, very few will change it — and that is the "
                 "success case, not a sign the feature failed.",
                 "So the work is mostly research and defaults, not settings screens. "
                 "Which persona does the page open as, and how does it decide? What "
                 "moves, and what is fixed because moving it would break the "
                 "orientation of everyone who has learned where it is? How does the "
                 "page change without the change itself being disorienting?",
                 "Write-up to follow once it ships."],
                fig=plate("seq", "variants, three personas",
                      "The same homepage, three orderings",
                      "Once there is something to capture: the same page rendered for "
                      "three personas, side by side, with one block colour-tracked "
                      "across all three so the reader can follow it moving.",
                      ["Operator, Owner and Newcomer, same window width",
                       "One block tinted identically in all three",
                       "The persona switcher visible and in its selected state"],
                      [("Size", "799x391 @2x"), ("Format", "PNG, or a 3-state loop"),
                       ("When", "after the first build ships")]),
                after=rules([
                    ("Default first", "The starting layout has to be right for the "
                                      "majority before any control is offered."),
                    ("Bounded", "A page that can become anything is a page nobody can "
                                "support or design for."),
                    ("Legible", "When the page reorders, it should be obvious that it "
                                "did and why."),
                ])),
    )))
