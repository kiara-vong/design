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
from gen.case_template import build, section, sub, NOTE, esc
from gen.case_blocks import stats, rules, figure_raw, before_after, plate
from gen import media

CO = "Capital One"

# A public rebuild of the surface three of these four case studies describe. Written
# from scratch in React and TypeScript, with every name, ARN, account ID and owner
# email invented and no proprietary code in it, so it can be linked where the work
# itself cannot. Each case points at the route that shows its own part.
#
# The column is labelled Rebuilt rather than Live, because calling a scrubbed
# recreation the live product would be a small lie in the one place a reader is most
# entitled to take a claim at face value.
DEMO = "https://kiara-vong.github.io/resource-dashboard/"


def demo(route, label="Open it"):
    return ('<a class="touch" href="%s%s" target="_blank" rel="noopener">%s</a>'
            % (DEMO, route, esc(label)))


ARROW = ('<svg viewBox="0 0 14 14" aria-hidden="true" focusable="false">'
         '<path d="M4 10L10 4M10 4H5.2M10 4v4.8"/></svg>')


# The one repository all three rebuilds are served from. Named here rather than
# derived from DEMO: the Pages URL and the repository do not share a name for
# this one, so a rule would be a guess dressed as a convention.
DEMO_SRC = "https://github.com/kiara-vong/resource-dashboard"


def demo_cta(route, label="Open the rebuild"):
    """The rebuild, as a thing you can hit rather than a cell in a table.

    Same button the project pages carry, and deliberately NOT the same word. The
    projects say "live" because they are; this is a scrubbed recreation of an
    internal tool, and calling it live would be a small lie in the one place a
    reader is most entitled to take a claim at face value. So the button says
    rebuild, and the line under it says what that means -- once, here, instead of
    a caveat the reader has to go looking for.
    """
    href = DEMO + route
    return ('        <div class="cs-cta">\n'
            '          <a href="%s" target="_blank" rel="noopener">'
            '<span>%s</span>%s</a>\n'
            '          <span class="cs-cta-url">A public rebuild of the internal '
            'tool, with the data scrubbed &middot; '
            '<a href="%s" target="_blank" rel="noopener">source</a></span>\n'
            '        </div>\n' % (href, esc(label), ARROW, DEMO_SRC))

def repo_cta(url, label, note, src=None):
    """Same button, pointed at a rebuild that is deployed on its own.

    The other rebuilds are routes inside one deployed app, so demo_cta can build
    their links from a base and a fragment. This one is its own repository with
    its own Pages deployment, so it takes a whole URL, and the line under the
    button carries the source as well: it is the only rebuild on this site a
    reader can read the code of, and burying that would be throwing away the
    better half of the claim.
    """
    tail = ('%s &middot; <a href="%s" target="_blank" rel="noopener">source</a>'
            % (esc(note), src)) if src else esc(note)
    return ('        <div class="cs-cta">\n'
            '          <a href="%s" target="_blank" rel="noopener">'
            '<span>%s</span>%s</a>\n'
            '          <span class="cs-cta-url">%s</span>\n'
            '        </div>\n' % (url, esc(label), ARROW, tail))


# =====================================================================
build("resource-dashboard", dict(
    cta=demo_cta("#/resources", "Open the rebuild"),
    out="work/resource-dashboard/index.html", root="../../",
    kicker=CO,
    title="Resource Dashboard",
    hero="case/cs-dash-seams.svg",
    hero_alt="A cloud resource dashboard with filters, a drill-down graph view and an export action",
    intro=("Engineers responsible for cloud resources had no single place to see "
           "them. Answering “what do I own, and what needs attention” meant "
           "three tools and a spreadsheet. I owned the dashboard that replaced "
           "that end to end, from research and requirements through design, build "
           "and enterprise release: one surface, two ways through it, and an "
           "export at every level. The demo linked above is a simplified, "
           "scrubbed recreation of it, rebuilt in public with invented data."),
    meta=[("Role", "Design engineer,<br>front end"),
          ("Stack", "React, TypeScript,<br>MUI, AG Grid"),
          ("Scope", "IA, components,<br>end-to-end flows"),
          ("Status", "Released to all<br>enterprise users"),
          ("Note", NOTE)],
    nav=[("overview", "Overview", False),
         ("context", "Context", False),
         ("decisions", "Key decisions", False),
         ("two-views", "Two views over one dataset", True),
         ("drill", "Drilling without getting lost", True),
         ("export", "An export at every level", True),
         ("data", "A real boundary", True),
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
""),

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
            # Two views over one dataset, shown as the thing that connects them:
            # the click. It opens on the graph, goes in close enough that a press
            # is a press rather than two pixels, presses the toggle, and cuts --
            # a page swap is instantaneous and a cross-fade would say it was not
            # -- to the table, which then scrolls its full height.
            #
            # The graph page fits its window with nothing below the fold, so the
            # ordinary flow timeline would spend a third of its loop scrolling
            # something that does not scroll. `still` gives that time to the two
            # beats this version actually has.
            media.flow(
                ["plate/dashboard-graph-page.webp",
                 "plate/dashboard-table-page.webp"],
                "The dashboard in graph view, the Table toggle pressed, and the "
                "same filtered set as a table scrolled through all eight rows",
                "One dataset, two readings, and the toggle between them. Same "
                "search, same filters, same eight resources: what changes is "
                "whether you are looking at the shape of what you own or at the "
                "list of what it wants from you.",
                view=(1280, 673), still=True,
                press=(1100, 90, 158, 34), press_pad=6, press_bg="#F5F5F5",
                look=(400, 60, 880, 180)),
            first=True,
            after=media.annotated(
                "plate/dashboard-default-annotated.webp",
                "The dashboard's default view, with its filters, view toggle, jobs "
                "filter and export called out",
                "Point at a label and the picture goes there. Four controls, and the "
                "argument for each is that it survives the switch between views.",
                [("filters", "Filters",
                  "Category, region and environment. They persist across the view "
                  "toggle, so switching does not cost you the narrowing you just did.",
                  "35%", "26%", "2.1", "5%"),
                 ("jobs", "Resources with jobs",
                  "A second source joined in rather than a filter over the first: "
                  "which of your resources have work outstanding.",
                  "72%", "17%", "2.4", "26%"),
                 ("views", "Table and Graph",
                  "Two readings of one dataset. The urgent one opens first, because "
                  "someone arriving without a plan is usually arriving because "
                  "something is due.",
                  "88%", "17%", "2.4", "47%"),
                 ("export", "Export",
                  "Scoped to what is on screen: current filters, current "
                  "level, nothing else.",
                  "86%", "91%", "2.2", "68%")])),


        sub("drill", "Key decisions", "Drilling without getting lost",
            ["The explorer goes environment, then region, then type, then the resource "
             "itself. Four levels is enough to get lost in, so every level carries its "
             "own counts and a breadcrumb back out.",
             "The counts are the part that earns its place. A level that only lists "
             "categories tells you where you can go; a level that lists categories with "
             "how much is in each tells you where you should go. It is a small addition "
             "that changes the drill-down from navigation into triage."],
            # The route, clicked out rather than laid out. Four stills in a row
            # would leave the reader working out what was pressed between them,
            # which is the one thing this figure exists to supply.
            #
            # No camera moves. The route is the figure, and going in and out of
            # it four times turns a path into a series of destinations -- what
            # the reader is meant to follow is the line through the levels, not
            # each level in isolation. So the clicks carry it, and they squash
            # harder and leave a ring because at this framing a card is forty-five
            # pixels and a subtle press would be invisible.
            #
            # Each press box is a rectangle in its screen's own pixels, read off
            # the capture. The categories screen is the one that runs past its
            # window, so it scrolls to its foot first: ELB is at the bottom of it,
            # and cutting straight there would skip the counts on the way down.
            media.walk(
                [dict(page="plate/dashboard-drill-1-envs.webp",
                      press=(550, 329, 107, 107)),
                 dict(page="plate/dashboard-drill-2-regions.webp",
                      press=(550, 335, 107, 107)),
                 dict(page="plate/dashboard-drill-3-categories.webp", scroll=True,
                      press=(621, 1215, 107, 107)),
                 dict(page="plate/dashboard-drill-4-resource.webp")],
                "Drilling from environments to prod, to us-east-1, past four "
                "categories to ELB, and into the load balancer itself",
                "Four levels, three clicks, and the breadcrumb in every frame. "
                "The counts are what turn this from navigation into triage: a "
                "level that lists categories tells you where you can go, and a "
                "level that lists them with how much is in each tells you where "
                "you should.",
                view=(1280, 673), press_bg="#F9FAFC", press_pad=14)),

        sub("export", "Key decisions", "An export at every level",
            ["Every table exports, and what it exports is exactly what you are looking "
             "at: current filters, current level, nothing else.",
             "This sounds like a checkbox feature and was one of the most-used things "
             "in the tool. People do not live in dashboards. They come in, narrow down "
             "to the thing they care about, and then need it somewhere else. A "
             "ticket, a spreadsheet, a message to the team that owns it. A dashboard "
             "that cannot hand off its own answer sends everyone back to the "
             "reconciling-by-hand it was built to remove."],
            # One framing, not a pan. The pan was wrong for a reason worth
            # writing down: it went in on the rows, then travelled to the file,
            # and at no point were the two things it is comparing on screen
            # together. A comparison you have to hold in memory between two shots
            # is not a comparison, it is two shots -- and the ends of both frames
            # were cut mid-line, which is what made it look broken rather than
            # tight.
            #
            # So the rectangle is drawn around the ARGUMENT instead: the two rows
            # at the top, the sentence, the filename, and the three lines of the
            # file, from the card's own left edge down. Everything the claim needs
            # is in one frame at once, and both ARNs can be read off against each
            # other without the figure moving at all.
            #
            # Delivered at the capture's own 3232 rather than the usual 2200,
            # since a resampled monospace glyph is exactly the thing that cannot
            # be recovered later.
            media.stage("plate/dashboard-export-scoped.webp",
                        "Two filtered rows on screen, and the downloaded file "
                        "below containing those same two rows",
                        "What comes out is what is on screen: current filters, "
                        "current level, nothing else. Both ARNs are in the frame "
                        "twice, once in the table and once in the file, which is "
                        "the only way that claim gets checked rather than taken "
                        "on trust.",
                        plate=(1616, 664),
                        look=(20, 155, 860, 470))) +
        # The rebuild's strongest engineering claim, and the one the write-up had no
        # slot for. The data layer is a real network boundary rather than an imported
        # array: typed fetch functions behind small hooks, a mocked REST surface
        # intercepted at the service-worker level, artificial latency, loading
        # skeletons, and an error path that retries. The same handlers run in Node for
        # the tests, so the suite drives the boundary the browser drives.
        #
        # It sits after the export rather than among the product decisions above it,
        # because it is not a decision about what the tool should do. It is what makes
        # the loading and error states in every screen above built and tested rather
        # than assumed.
        sub("data", "Key decisions", "A real boundary, not a prop",
            ["Every screen here fetches. The data layer is typed fetch functions behind "
             "small hooks that track loading, error and refetch, with a mocked REST "
             "surface behind them at the service-worker level rather than an imported "
             "array pretending to be a response.",
             "That distinction is why the loading skeletons and the retry banner exist "
             "at all. A component handed its data synchronously has no in-flight state "
             "to design, no failure to recover from, and no way to find out it was "
             "wrong until it meets a real server. The same handlers run in Node for the "
             "tests, so those drive the actual fetch, loading, render, error and retry "
             "cycle instead of asserting against props."],
            # The five detail tabs ARE the boundary's output: one resource, five
            # views of what came back for it. The brief below still stands, because
            # a still of the result cannot show the request that produced it.

            # strip() before, which scrolled it behind a fixed frame at half
            # size: a page whose whole subject is how much it answers, shown at a
            # size where none of the answers can be read. It is a page, so it gets
            # the page machine -- the window holds still, the page scrolls behind
            # it the way a page does, and at the end the camera goes to 1:1 on the
            # metadata block, where each field is one value that came back over
            # the boundary this section is about.
            media.page(
                "plate/resource-detail-full.webp",
                "One resource detail page scrolled through its full height: "
                "identifiers and metadata, ownership, five tabs, a compliance "
                "timeline and the jobs outstanding against it",
                "One resource, top to bottom, at the length it actually is. "
                "Every field on the way down is a value that arrived over the "
                "boundary described above, with a skeleton in its place while it "
                "was in flight. The page is long because that is the answer: this "
                "is what it takes to stop somebody opening a second tool.",
                view=(1600, 820), look=(115, 50, 720, 340), dur="20s")
) +
        '    </div>\n\n',

        section("impact", "Impact", "From three tools to one",
                ["The reconciliation step is gone. What used to be a cross-tool search "
                 "is a paste-an-identifier lookup. Which of your resources have work "
                 "outstanding used to be invisible, and is now the screen that "
                 "opens by default.",
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
    cta=demo_cta("#/resources/res-05", "Open the rebuild"),
    out="work/events-timeline/index.html", root="../../",
    kicker=CO,
    title="Events Timeline",
    hero="case/cs-tl-carry.svg",
    hero_alt="A compliance event timeline with coloured state segments and dated event dots",
    intro=("A resource's compliance history was a table of rows sorted by date, "
           "which is technically the whole story and practically unreadable. I "
           "built the feature that sits above it end to end, the GraphQL API and "
           "the interface both: a time-scaled track where a glance tells you what "
           "state a resource is in, how long it has been in it, and what the "
           "automated remediation did along the way. The demo linked above is a "
           "simplified, scrubbed recreation of it."),
    meta=[("Role", "Design engineer,<br>API and interface"),
          ("Stack", "React, TypeScript,<br>GraphQL"),
          ("Scope", "Schema, resolvers,<br>timeline, events table"),
          ("Status", "Released in beta,<br>expanding to more<br>dashboards"),
          ("Note", NOTE)],
    nav=[("overview", "Overview", False),
         ("context", "Context", False),
         ("decisions", "Key decisions", False),
         ("carry", "Colouring the gaps", True),
         ("collapse", "When two things happen at once", True),
         ("table", "What a column can be", True),
         ("impact", "What changed", False)],
    sections=(
        section("context", "Context",
                "A table is a list of events, not a history",
                ["The events were all there, sorted by timestamp, each one accurate. "
                 "But the question people actually had was never “what happened on "
                 "the third of August”. It was “how long has this been "
                 "broken”, and a table answers that only if you are willing to read "
                 "it and do arithmetic.",
                 "A timeline answers it by being looked at. That is the whole "
                 "argument for the feature: the data did not change, the shape of "
                 "it did.",
                 "What it answers now is a different question from the one the "
                 "table answered. Not “is this compliant right now”, which a chip "
                 "can say in four words, but “how did it get into this state, and "
                 "what did the automation do about it”. The chip at the top right "
                 "gives the state and how long it has held: conformant since a "
                 "date, or in violation for four days, with the timer resetting "
                 "the moment a fix lands so there is no ambiguity about whether "
                 "it did."],
                media.stage(
                    "plate/dashboard-events-table-explored.webp",
                    "A compliance event table sorted by timestamp",
                    "The whole history, and technically complete. Working out how "
                    "long anything was in trouble means reading two rows and doing "
                    "the arithmetic yourself.",
                    # The callout names two rows and the old rectangle framed
                    # neither of them together: it ran from y 250 to 510, which
                    # holds Aug 23 and Aug 20 and cuts Aug 18 clean off. A label
                    # pointing at something outside the frame is worse than no
                    # label, because the reader trusts it and goes looking.
                    plate=(2200, 682), look=(40, 310, 760, 270),
                    call=("Aug 18, then Aug 23",
                          "Violated here, fixed there. The gap between them is "
                          "the answer, and the table makes you work it out."))),

        '    <div id="decisions" class="cs-group">\n\n' +
        sub("carry", "Key decisions", "Colouring the gaps",
            ["Events are discrete and compliance is continuous, and that mismatch is "
             "the whole engineering problem. A resource that was violated on the 3rd "
             "and fixed on the 8th generates two events and five days of nothing, and "
             "those five days are the part that matters most.",
             "So state carries forward: the segment between two events is coloured by "
             "the state the earlier one left behind, not by the absence of data. Drawn "
             "the naive way, the track shows two dots and a gap, which reads as "
             "“nothing was wrong” for precisely the stretch when something was.",
             "The track is time-scaled, so where a dot sits horizontally is when "
             "it happened, and the colours are semantic rather than per-event: "
             "red while the resource was in violation, green while it was "
             "conformant, amber across an automated change of any kind. Three "
             "colours covering a dozen event types is a decision that has to be "
             "made once and defended afterwards, and the defence is that a reader "
             "scanning a track is asking about state, not about which of six "
             "words the change was called."],
            # A drag rather than a travelling seam, and framed whole rather than
            # cropped. The old machine filled the card with object-fit:cover, and
            # this widget is 6.7 times wider than it is tall -- so what a reader
            # actually saw was the middle third of a timeline whose whole point is
            # its ends. Now the window holds the entire track, and the line the
            # reader drags is the one they can stop wherever they doubt it.
            media.slider(
                "plate/dashboard-timeline-naive.webp",
                "plate/dashboard-timeline-carryforward.webp",
                "The same events with the gaps left uncoloured, and the same "
                "events with the state of the earlier one carried across them",
                "Identical dates, identical width, the same six events. The only "
                "difference is whether the line between two of them knows what "
                "happened at the first one.",
                tags=("gaps left empty", "state carried forward"),
                plate=(2200, 328)),
            first=True),

        sub("collapse", "Key decisions", "When two things happen at once",
            ["Events cluster. An automated fix fires, fails, retries and succeeds, and "
             "at any sensible zoom those are four dots occupying the same pixel.",
             "Adjacent same-day events collapse into one dot that opens a popover with "
             "all of them. The alternative was letting them overlap, which looks like a "
             "rendering bug, or spacing them evenly, which lies about when they "
             "happened. Collapsing keeps the position honest and moves the detail one "
             "interaction away, where there is room for it.",
             "The badge is a count, and it opens a card listing every event that "
             "landed at that moment. Clicking one of them scrolls to its row in "
             "the table below, which is the part that makes the two halves one "
             "feature rather than a chart with a table under it. Clusters are "
             "usually a fleet-wide change arriving everywhere at once, so the "
             "count is information in itself."],
            # Drawn rather than captured, because two of the three options never
            # shipped: there is no screenshot of the overlap bug and there never
            # should be. A section that weighs three answers and picks one needs
            # the reader to have seen the ones it turned down.
            media.flat("case/cs-tl-collapse.svg",
                       "Four events on one day drawn where they happened, "
                       "overlapping into a single smear, beside the same four "
                       "collapsed into one dot that opens a list of them",
                       "Left is honest and unreadable. Right keeps the position "
                       "exactly as honest and moves the four events one "
                       "interaction away, which is the only version where both "
                       "the when and the what survive.")),

        sub("table", "Key decisions", "What a column can be asked to do",
            ["The table under the track is not a fallback. It is where the "
             "specifics live, and two of its columns do more than report a field.",
             "The quantification column renders financial events as money. The "
             "underlying value is a metric string, and every reader of it was "
             "doing the same conversion in their head to answer the same "
             "question, which is what a remediation actually saved. Doing that "
             "conversion once, in the column, is a smaller change than it sounds "
             "and it is the difference between a number and an answer.",
             "The requirement column is a link out to the control the event was "
             "raised against. It exists because the alternative was a reader "
             "copying an identifier into a second system, which is the exact "
             "behaviour this whole dashboard was built to remove. Every column "
             "sorts, and the filters above narrow by event type, status and "
             "timeframe."]) +
        section("impact", "Impact", "The same data, now legible",
                ["The question the feature exists to answer, how long and is it fixed, "
                 "went from a read-and-calculate to a glance. The table is "
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
    cta=demo_cta("#/showcase", "Open the showcase"),
    out="work/ui-consistency/index.html", root="../../",
    kicker=CO,
    title="UI Consistency",
    hero="case/cs-ui-drift.svg",
    hero_alt="Nine slightly different buttons on the left, the same nine identical on the right",
    intro=("The app had grown a dozen local dialects of the same interface: inline "
           "styles instead of tokens, four table layouts, three different ways to "
           "say \u201cno data\u201d. I inventoried it, designed the shared layer "
           "underneath, and cut a 231-file, 12,600-line change across twelve pages "
           "into twenty-four pull requests a human could actually review, with "
           "a Cypress suite under it so review was not the only thing standing "
           "between a refactor this size and a regression."),
    meta=[("Role", "Design engineer,<br>system owner"),
          ("Stack", "React, TypeScript,<br>MUI, Cypress"),
          ("Scope", "231 files, 12,600 lines,<br>12+ pages"),
          ("Status", "Shipped,<br>no regressions"),
          ("Note", NOTE)],
    nav=[("overview", "Overview", False),
         ("context", "Context", False),
         ("decisions", "Key decisions", False),
         ("audit", "Counting what was actually there", True),
         ("theme", "One theme, no inline styles", True),
         ("prs", "Twenty-four pull requests, in order", True),
         ("tests", "The net under the refactor", True),
         ("impact", "What changed", False)],
    sections=(
        section("context", "Context",
                "Nobody set out to build four table layouts",
                ["Each one was a reasonable local decision. A team needed a table, the "
                 "existing one was close but not right, and copying it was ten minutes "
                 "against a week of negotiation. Enough reasonable local decisions "
                 "later, nobody could tell you what the product\u2019s table looked "
                 "like, because the honest answer was that it depended on the page.",
                 "The cost was not really aesthetic. It was that every change had to be "
                 "made in every copy, and the last copy was always the one somebody "
                 "forgot. A shared layer is worth building at the point where keeping "
                 "things in sync by hand costs more than the abstraction does, and we "
                 "were well past it."],
                media.stage(
                    "plate/dashboard-button-contact-sheet.webp",
                    "Every live button variant side by side on a neutral ground",
                    "One component, as many versions of it as the app actually "
                    "had. Nothing here is tidied: the spacing and the radii are "
                    "what shipped, and the mess is the argument.",
                    plate=(2200, 832), look=(90, 100, 1000, 380),
                    call=("two of seven",
                          "Same control, different radius, different weight, "
                          "different idea of what a button is."))),

        '    <div id="decisions" class="cs-group">\n\n' +
        sub("audit", "Key decisions", "Counting what was actually there",
            ["The instinct is to design the target state and then go find everything "
             "that does not match it. I did the opposite: inventoried every variant "
             "already shipping, with no judgement attached, before proposing anything.",
             "That order mattered more than it sounds. Two of the variants I would have "
             "deleted on sight turned out to be load-bearing, solving a real constraint "
             "the canonical component could not. They became part of that component\u2019s "
             "API rather than exceptions to it. Designing first and reconciling later "
             "produces a system that is correct in isolation and wrong in the product, "
             "which is the usual way these fail.",
             "The inventory became a page. Every component that had drifted got a card: "
             "what was wrong, what replaced it, how many files it touched, what it "
             "blocked. Reviewers read that page before they read a diff, and so "
             "did the people who had written the variants I was proposing to delete."],
            media.page(
                "plate/showcase-full-height.webp",
                "The refactor showcase, scrolled: eight components, each with the "
                "version that shipped before and the version that replaced it",
                "The inventory, written down before anything was designed. Each card "
                "carries the problem, the resolution, and the line that says what it "
                "costs to review. The length of the page is the finding. (This is the "
                "public rebuild, which condenses the change to eight representative "
                "components; the real one ran to twenty-four pull requests.)",
                view=(1200, 580), scroll=900, look=(100, 158, 1064, 319),
                dur="34s"),
            first=True),

        sub("theme", "Key decisions", "One theme, no inline styles",
            ["The foundation is a single theme provider wrapping the app, with tokens "
             "for colour, typography, spacing and radius. Components inherit from it "
             "instead of carrying their own inline values, and the fifty-odd hardcoded "
             "hex literals scattered through the tree stopped being editable one file "
             "at a time.",
             "Underneath that, the shared pieces: one toolbar with search, filter chips "
             "and actions in a single row; one footer with the count on the left and "
             "export on the right; real empty, error and not-found states instead of "
             "the inline \u201cno data\u201d text that had been written separately on "
             "every page. Tables lost twenty pixels of row height, gained proper header "
             "treatment and zebra striping, and dropped to a subtler border.",
             "The filter chips are the detail I am most pleased with. They show at full "
             "width rather than truncating, overflow collapses into a +N chip, the "
             "dropdown stays open while you are still choosing, and typing hides the "
             "chips so you get a clean search field. Four small decisions, all of them "
             "about not interrupting someone mid-thought."],
            media.slider(
                "plate/ui-tables-before.webp", "plate/ui-tables-after.webp",
                "One table before and after the shared layer, the two frames "
                "stacked in register with a seam the reader drags",
                "Drag the seam. Same three rows, same three columns, same width, "
                "cut from the showcase so the headers land on the same line. "
                "Twenty pixels off the row height, a header that stopped "
                "shouting, and a footer that finally says how many there are and "
                "where to get the rest.",
                tags=("before", "after"), start=46,
                handle="Reveal the table after the shared layer",
                plate=(966, 560)),
            after=media.page(
                "plate/style-guide-full.webp",
                "The full style guide: colour, typography, spacing and radius "
                "tokens, then every shared component built on them",
                "Every token on one page, in order, and then every component that "
                "reads them. A change to a value becomes one edit against "
                "something you can point a reviewer at, instead of an inline "
                "style hunted down file by file.",
                view=(1200, 580), scroll=633, look=(100, 147, 700, 192),
                dur="30s")),

        sub("prs", "Key decisions", "Twenty-four pull requests, in dependency order",
            ["231 files and 12,600 lines is not a reviewable change. It is a change "
             "that gets approved without being read, which is the same as not being "
             "reviewed, on a diff touching every page in the app.",
             "So it went out as twenty-four pull requests of fifteen files or fewer, "
             "ordered so each could merge on its own. The theme provider had to land "
             "first because everything else assumes it. The shared table and filter "
             "components went second because the page-level work consumes them. After "
             "that the rest were independent and could go in parallel, in any order, "
             "by whoever had time.",
             "The foundation PR contained no behavioural changes at all. Visual "
             "consistency only. That was deliberate: the riskiest change in the "
             "sequence is the one everything depends on, so it should also be the one "
             "with the least in it."],
            fig=media.stage(
                "plate/ui-pr-anatomy.webp",
                "One card from the showcase: the change, the reason, and a line "
                "giving its file count, its risk and what it blocks",
                "Every pull request was written up before it was opened. The line "
                "under the resolution is the part reviewers actually used: how big "
                "it is, how much it can break, and what is waiting on it.",
                plate=(2228, 795), look=(44, 268, 720, 44),
                call=("what a reviewer needs",
                      "Size, risk and dependency, on one line, next to the "
                      "change rather than in a ticket.")),
            after=rules([
                ("PR 1", "The theme provider and global defaults. No behavioural "
                         "change. Everything downstream assumes it."),
                ("PR 2", "Shared table, toolbar and filter components, consumed by "
                         "every page-level PR that follows."),
                ("PRs 3\u201324", "Page-level adoption, plus the new primitives. "
                                   "Independent of each other, reviewable in "
                                   "parallel, mergeable in any order."),
            ])) +

        sub("tests", "Key decisions", "The net under the refactor",
            ["A refactor makes a promise that is hard to check: nothing behaves "
             "differently. On a diff this wide, nobody can hold that in their head, "
             "and \u201cit looked fine when I clicked around\u201d is not evidence. "
             "It is the absence of it.",
             "So the Cypress suite grew alongside the change rather than after it, to "
             "roughly 85% of the critical flows: the paths people take every day, "
             "asserted before the shared components went in and re-run after each "
             "pull request. Where a spec had to change, that was the signal to stop "
             "and look, because a passing test that needed rewriting is a behaviour "
             "change wearing a costume.",
             "It shipped with no regressions, which is the claim I would otherwise "
             "have had no honest way to make."]) +
        '    </div>\n\n',

        section("impact", "Impact", "One product, one language",
                ["Every page now renders from one theme, and a change to a shared "
                 "component is one edit rather than a search-and-replace across the "
                 "app.",
                 "The result I care about most is quieter than the file count: design "
                 "review stopped spending its first ten minutes establishing which "
                 "version of a component we were looking at. The system\u2019s real "
                 "output is the argument it makes unnecessary."],
                fig=stats("231 files \u00b7 12,600 lines \u00b7 24 pull requests", [
                    ("231", "0", "files changed",
                     "twelve pages and the shared layer under them"),
                    ("24", "0", "reviewable pull requests",
                     "15 files or fewer, dependency-ordered"),
                    ("85", "0", "% of critical flows covered",
                     "Cypress specs written alongside the change"),
                ], note="Regressions after release&nbsp; <b>None</b>")),
    )))

# =====================================================================
build("persona-homepage", dict(
    out="work/persona-homepage/index.html", root="../../",
    kicker=CO,
    title="Persona Homepage",
    cta=repo_cta("https://kiara-vong.github.io/persona-homepage/",
                 "Open the recreation",
                 "kiara-vong.github.io/persona-homepage",
                 "https://github.com/kiara-vong/persona-homepage"),
    hero="case/cs-persona-reorder.svg",
    hero_alt="The same homepage twice, its five widgets joined by curves showing "
             "where each one lands for the other persona",
    intro=("A homepage serving several kinds of user, each of whom needs a "
           "different half of it. I picked up a proposal two teammates had "
           "shelved, researched how three other products had solved it, drew "
           "five personas, ran the workshop that cut them to two, and am now "
           "building the model, the API and the interface. This is the whole "
           "arc, in the order it happened."),
    meta=[("Role", "Design engineer,<br>research through build"),
          ("Stack", "React, TypeScript,<br>GraphQL"),
          ("Scope", "Research, wireframes,<br>workshop, build"),
          ("Status", "In build behind<br>a feature flag"),
          ("Note", NOTE)],
    nav=[("overview", "Overview", False),
         ("context", "Context", False),
         ("research", "Research", False),
         ("decisions", "Key decisions", False),
         ("draft", "Everything that could go on a page", True),
         ("workshop", "A workshop is a decision list", True),
         ("personas", "Five became two", True),
         ("scope", "Scope is the persona", True),
         ("ship", "Shipping it invisibly", True),
         ("mockups", "Mockups", False),
         ("built", "In build", False),
         ("recreation", "The recreation", False),
         ("thinking", "Where my head is", False)],
    sections=(
        section("context", "Context",
                "A landing page nobody landed on",
                ["The people arriving at this page do not want the same things. "
                 "Some own one application and want the shortest path to what it "
                 "needs today. Some run a division and want the shape of all of "
                 "it. They all got the same mostly-empty page, so everyone "
                 "landed and immediately started filtering.",
                 "Two teammates had already written a proposal for it: "
                 "configurable widget slots you pick from a dropdown, a tabbed "
                 "nav in place of the dropdown menu, saved against your user id. "
                 "It was shelved before it was fleshed out. Picking it up meant "
                 "saying what it was missing, and I think the answer is this: it "
                 "personalised by WHO you are, and the thing that actually "
                 "predicts what you need is what you are responsible for.",
                 "So the direction kept their selection model and added a "
                 "detected scope underneath it. The page works out what you own, "
                 "shows you what it worked out, and lets you correct it before "
                 "anything is saved."],
                media.flat("case/cs-persona-flow.svg",
                           "The flow from opening the page for the first time to "
                           "using it daily: detect scope, confirm it, tour, "
                           "render, customise, save a preset",
                           "The whole feature in one line. The branch at the "
                           "front is the part I care about: somebody who has been "
                           "here before skips every step of the onboarding, "
                           "because a page that greets you the same way on the "
                           "fortieth visit is a page that has not been paying "
                           "attention.")),

        section("research", "Research",
                "Three products had already solved half of it",
                ["Before designing anything I went and used three products that "
                 "already do customisable dashboards: two other internal ones and "
                 "a third-party observability platform. Not for inspiration, but for "
                 "the list of things that go wrong, which is much harder to "
                 "get from a blank page than from somebody else\u2019s shipped "
                 "one.",
                 "The most useful finding was an anti-pattern. One of the two "
                 "internal products fetches a rich user profile on load, with the "
                 "role and the org and the team all in it, and then renders the "
                 "same layout for everybody. All the signal, none of the "
                 "branching. That is the failure this project exists to avoid, "
                 "and it was already sitting there in production to be looked at."],
                fig=rules([
                    ("Borrow", "One catalog source, no fallbacks. An explicit edit "
                               "mode you opt into. Curated presets plus a personal "
                               "override. Hiding widgets a user is not entitled to "
                               "see."),
                    ("Skip", "Multi-dashboard create-share-clone. A write on every "
                             "drag. A three-way catalog fallback. A full-page "
                             "editor route where a side panel would do."),
                    ("Open", "Neither internal product has a persona concept at "
                             "all. If this is right, it is new here, and being "
                             "first is a reason to be careful rather than a "
                             "reason to be pleased."),
                ])),

        '    <div id="decisions" class="cs-group">\n\n' +
        sub("draft", "Key decisions", "Everything that could go on a page",
            ["The first artefact was not a layout. It was an inventory: every "
             "widget the product already had, grouped under the headings the "
             "picker would eventually use. Twenty-four of them, six categories, "
             "and not one of them new.",
             "That constraint was deliberate and it survived the workshop intact. "
             "A first release that also invents widgets is a release where you "
             "cannot tell whether people dislike the customisation or the new "
             "content. Everything here already exists on a page somebody uses "
             "today; all this feature does is let them choose which ones and in "
             "what order.",
             "Five wireframes came out of that list, one each for developer, manager, "
             "director, division lead and executive: a different opening "
             "hand from the same deck, with the reasoning written in the margin "
             "next to every block."],
            media.inline_svg("case/cs-persona-catalog.svg",
                       "The widget catalog: twenty-four widgets under six "
                       "headings, from maturity and compliance through to layout "
                       "primitives",
                       "The deck every persona is dealt from. Grouping it this "
                       "way was not documentation. The headings are what the "
                       "picker is grouped by, so the inventory and the interface "
                       "are the same list."),
            first=True),

        sub("workshop", "Key decisions", "A workshop is a decision list, not a meeting",
            ["Eight of us, an hour, and a written agenda where every item was a "
             "question with its options and the argument for each already laid "
             "out. Not slides. The pre-read had the questions; the follow-up doc "
             "had the answers, in the same order, so you could see which ones "
             "moved.",
             "The framing mattered more than the facilitation. \u201cAre these the "
             "right five personas?\u201d is a decision somebody can disagree with "
             "in one sentence. \u201cHere is my design\u201d is not. It is a "
             "thing people nod at and then quietly ignore, and the proposal I "
             "inherited had been nodded at once already.",
             "It also set what we would NOT decide: no final visual design, no "
             "aggregation logic per widget, no production wiring. A workshop that "
             "tries to settle everything settles nothing."],
            after=rules([
                ("Personas", "How many, detected from what, and what scope each "
                             "one fills in by default."),
                ("Widgets", "Whether the catalog is right, what each persona "
                            "opens with, and which existing pages this replaces."),
                ("Affordances", "Editable, stackable and resizable widgets, and "
                                "which edit-mode control we ship."),
                ("Persistence", "Where preferences live, and what happens to a "
                                "custom layout when somebody\u2019s role changes."),
            ])),

        sub("personas", "Key decisions", "Five personas became two",
            ["The proposal I inherited had five roles and the version before it "
             "had three. The workshop collapsed them to two, and the reasoning is "
             "the part worth keeping: the first release ships widgets that already "
             "exist, and five roles cannot be told apart by widgets none of them "
             "have yet. A five-way split is a promise the product cannot cash.",
             "So there are two. Somebody scoped to one application or account, and "
             "somebody scoped to many, a division, or all of them. The finer split "
             "is written down and waiting for the role-specific widgets that would "
             "make it mean something, which is a different thing from being "
             "dropped.",
             "The persona is also not read off a job title. It follows from a "
             "scope the user has confirmed: on a first visit the page shows what "
             "it detected and asks them to correct it before anything is saved. "
             "Applying it silently was on the table and the room turned it down, "
             "which I think was right. A page that quietly rearranges itself "
             "around a guess about you is a page you cannot argue with."],
            media.inline_svg("case/cs-persona-five-to-two.svg",
                       "Five proposed persona layouts above, joined by curves to "
                       "the two that shipped: contributor and leader",
                       "Nothing was thrown away. Two of the five folded into one "
                       "default and three into the other, and the split waits for "
                       "the widgets that would justify it. A picture of that is "
                       "more honest than a list of two, which reads as though the "
                       "other three were never considered.")),

        sub("scope", "Key decisions", "Scope is the persona",
            ["Every widget declares which scope dimensions it can answer for. "
             "Effective scope resolves widget-first, then the page, then a default "
             "from the profile, so one widget can be pinned to a single "
             "application while the rest of the page follows the division.",
             "The interesting case is the mismatch: the page is scoped by "
             "something a widget does not accept. Two easy answers were available "
             "and both are wrong. Applying it silently makes the widget lie about "
             "what it is showing; dropping it silently makes it lie about what it "
             "was asked. So it ignores the dimension and says so on its own chip. "
             "A visible inconsistency the reader can reason about beats an "
             "invisible one they cannot.",
             "Sizes are bounded for the same reason. At most three per widget, at "
             "most two layouts, and the compact size always shows a real number "
             "plus one piece of context: a trend, a threshold, a delta. Never "
             "a bare number, because a bare number is a thing you have to go "
             "somewhere else to understand."],
            media.stage("plate/persona-widget-jobs.webp",
                        "One widget on the homepage: a jobs table with its own "
                        "scope chip, three filters and an export, stacked behind "
                        "a numbered tab with a second widget",
                        "One entry in that catalog, on the page. It carries its "
                        "own scope chip, its own filters and its own export, and "
                        "it is stacked behind a numbered tab with a second "
                        "widget, which is how a column holds more than it "
                        "has room for.",
                        look=(146, 70, 440, 228),
                        call=("two widgets, one column",
                              "Stacked behind numbered tabs, each carrying its "
                              "own scope, because a column has less room than a "
                              "page has widgets."))),

        sub("ship", "Key decisions", "Shipping it where nobody can see it",
            ["The new homepage is a separate route behind a flag that is off in "
             "production, and the existing homepage is untouched, byte for byte. "
             "That is deliberate: this arrives as roughly forty small pull "
             "requests over a quarter, and the cost of a regression on the page "
             "everybody already uses is far higher than the cost of running two "
             "routes for three months. The team opts in by visiting the route; "
             "the architect and the tech lead review from the same place.",
             "If the flag resolves off, or the client that evaluates it fails "
             "outright, the new route redirects to the old one. The failure mode "
             "of a half-finished homepage should be the homepage that already "
             "works, and that has to be designed rather than hoped for.",
             "Preferences go to a table in the database that already serves this "
             "product rather than to a new service, keyed by user, holding the "
             "persona, the layout, the saved presets and whether the tour has been "
             "seen. Local storage stays as an offline cache. Syncing across "
             "devices was a requirement rather than a nicety, which is what ruled "
             "out the browser-only version that would have shipped a month "
             "sooner."]) +
        '    </div>\n\n',

        section("mockups", "Mockups", "What it looks like when it opens",
                ["Three moments got mocked before any of them got built, because "
                 "all three are moments where the page is about to do something "
                 "on your behalf and the only question is whether you can see it "
                 "coming.",
                 "The first is onboarding: what we detected, where each piece came "
                 "from, and a control to remove or add any of it. The second is a "
                 "five-step tour that runs once and is remembered. The third is "
                 "the one nobody asks for and everybody needs: what happens "
                 "when your role changes and you have unsaved edits. That one "
                 "stops and makes you name what you have before it loads anything "
                 "else. Discarding is allowed; discarding silently is not."],
                fig=media.flat("case/cs-persona-onboard.svg",
                               "The onboarding modal: an auto-detected banner, "
                               "then rows of application, account and division "
                               "chips, each removable, with a confirm button",
                               "The banner is the whole argument. It says what was "
                               "detected and where it came from, and everything "
                               "under it can be taken off before a single "
                               "preference is written."),
                after=media.stage("plate/persona-home-leader.webp",
                                  "The homepage as it opens for someone "
                                  "responsible for a whole division: a maturity "
                                  "score, its trend, and what the automation has "
                                  "done lately",
                                  "And the mockup, built. What a division lead "
                                  "opens to. Nothing here was chosen by them; "
                                  "it is what the page decided to show somebody "
                                  "with their scope.",
                                  look=(163, 152, 830, 64),
                                  call=("the page\u2019s scope",
                                        "Not a job title. The page asks what you "
                                        "are responsible for, and the opening "
                                        "layout follows from the answer."))),

        section("built", "In build", "The half that is on screen today",
                ["Editing is a mode you enter rather than a state you fall into. "
                 "Edit layout adds a grip to every widget, an action menu on each "
                 "one, and drag handles on the right and bottom edges; nothing "
                 "else about the page changes. The page you were reading is the "
                 "page you are rearranging, which is the difference between "
                 "customising something and being handed a configuration screen.",
                 "Underneath, the widget catalog is a typed array in code, one "
                 "file per widget, validating itself at module load: duplicate "
                 "identifiers and malformed scope declarations throw before "
                 "anything renders. A JSON file and a server-fetched catalog were "
                 "both considered and both rejected, because both turn a compile "
                 "error into a runtime one and then need a fallback for the case "
                 "where the catalog is missing, and a fallback catalog is a "
                 "second source of truth pretending to be a safety net."],
                fig=media.stage("plate/persona-home-edit.webp",
                                "The same homepage in edit mode, its widgets "
                                "showing drag handles and the page scope set to a "
                                "single application",
                                "Edit mode, and the scope chips along the top. "
                                "Those chips are the persona: the page does not "
                                "ask who you are, it asks what you are "
                                "responsible for, and the layout follows from the "
                                "answer.",
                                look=(172, 280, 605, 82),
                                call=("what moves",
                                      "Edit mode adds a grip to each widget and "
                                      "changes nothing else. The page you were "
                                      "reading is the page you are rearranging.")),
                after=media.stage("plate/persona-home-contributor.webp",
                                  "The homepage as it opens for someone who owns "
                                  "a single application: alerts first, then cost, "
                                  "then the jobs outstanding against it",
                                  "The other default. Same page, same widgets "
                                  "available, different opening hand: what is "
                                  "broken, what it costs, what it wants from you "
                                  "today.")),

        section("recreation", "The recreation",
                "Rebuilt so it can be shown",
                ["The internal captures on this page are stills, and stills are "
                 "all they can be. The recording of the real thing carries a "
                 "division, an application identifier and a colleague\u2019s name "
                 "in half a dozen places on every frame, several of which pass "
                 "under an open menu as it moves. A figure whose safety depends "
                 "on a rectangle staying put is a figure waiting to leak.",
                 "So the page is rebuilt in the open instead: same rail, same "
                 "scope bar, same card grid, same edit mode, running on accounts "
                 "and divisions I made up. Rebuilding it removes the question "
                 "rather than managing it, and it is a better artefact anyway, "
                 "because a reader can open it and drive it themselves rather "
                 "than take a screenshot\u2019s word for it. It is deployed at "
                 "kiara-vong.github.io/persona-homepage and the source is on "
                 "GitHub beside it.",
                 "It carries the decisions this page argues for, not just the "
                 "look: each widget declares which scope dimensions it accepts, "
                 "the effective scope resolves widget then page then default, and "
                 "a widget the page scope cannot reach says so on its own card "
                 "instead of showing numbers for a scope nobody asked for.",
                 "It is close but not complete. Real data, entitlements, "
                 "server-side preferences and the wider persona split are "
                 "described here rather than implemented there."],
                fig=media.clip("persona-edit-options",
                               "Edit mode, a widget\u2019s action menu open on "
                               "expand, replace, delete, move, merge, unstack and "
                               "three sizes, then the change undone",
                               "Edit mode and one widget\u2019s menu. Every "
                               "action on it is reversible, which is what lets "
                               "the page be rearranged by someone who is not sure "
                               "yet what they want.",
                               root="../../"),
                after=media.clip("persona-scope-switch",
                                 "The page scope changing from a single account "
                                 "to a division, and the whole layout, the grade "
                                 "and every widget\u2019s subtitle following it",
                                 "The same page under a different scope. Nothing "
                                 "was configured between these two states: the "
                                 "scope changed and the layout followed, which is "
                                 "the entire argument.",
                                 root="../../")
                      + media.clip("persona-widget-scope",
                                   "One card pinned to a different account, then a "
                                   "divisional widget added to a page scoped to a "
                                   "single account, showing a warning on its own "
                                   "scope line",
                                   "Scope resolves widget, then page, then default. "
                                   "The rollup at the bottom cannot be scoped by an "
                                   "account, so it falls back to its own dimension "
                                   "and says which scope it is not using. Silently "
                                   "applying the wrong one, or silently dropping "
                                   "it, are the two failures this replaces.",
                                   root="../../")),

        section("thinking", "Where my head is",
                "The defaults are the product",
                ["The thing I keep coming back to is that customisation is not "
                 "the feature. The default is the feature, and customisation is "
                 "what you offer the people the default cannot serve. If the "
                 "starting layout is right for most people, very few will change "
                 "it, and that is the success case rather than a sign the feature "
                 "failed.",
                 "Which is why most of the work so far has been research, "
                 "personas and defaults rather than settings screens. Which "
                 "layout does the page open as, and how does it decide? What "
                 "moves, and what is fixed because moving it would break the "
                 "orientation of everyone who has learned where it is? A second "
                 "workshop and two rounds of structured feedback are in the plan "
                 "for exactly that, because the answer is not something I can "
                 "reason my way to alone.",
                 "Write-up to follow once it ships."],
                fig=rules([
                    ("Default first", "The starting layout has to be right for the "
                                      "majority before any control is offered."),
                    ("Bounded", "A page that can become anything is a page nobody "
                                "can support or design for."),
                    ("Legible", "When the page reorders, it should be obvious that "
                                "it did and why."),
                ])),
    )))

