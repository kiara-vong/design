# -*- coding: utf-8 -*-
"""Detail pages for the six archive projects.

Built on the case-study shell rather than a new layout: these are the same KIND of
document as the work write-ups, just shorter and with the stakes turned down. A
side-effect worth having is that a reader arriving from the archive gets the same
reading experience as one arriving from the work grid.

The difference from a work case study is the section set. These do not have an
Impact section, because nobody's compliance posture improved because a game felt
solid. They have "What it taught me" instead, which is the honest version, and a
live link at the top, because unlike the work these can actually be opened.

Content comes from each project's own README, so it is accurate about the
architecture rather than reconstructed from memory.
"""
import io

from gen import nav as _nv
from gen import case_template as _gc
from gen.case_blocks import rules

section, sub, esc = _gc.section, _gc.sub, _gc.esc
NOTE = _gc.NOTE


def live(href, label):
    return ('<a class="touch" href="%s" target="_blank" rel="noopener">%s</a>'
            % (href, esc(label)))


PROJECTS = [
    dict(slug="p-animal-crossing", title="Island Generator", kicker="Personal",
         hero="tile/ac.jpg",
         hero_alt="A low-poly 3D island with cliffs, water and scattered conifers",
         live="https://kiara-vong.github.io/animal-crossing/",
         intro=("A procedural island built tile by tile with wave function collapse. "
                "No map is authored and no layout is stored: the entire input is a "
                "set of hand-modelled pieces and the rules about which may sit next "
                "to which."),
         meta=[("Role", "Everything"), ("Stack", "React, Three.js,<br>WFC solver"),
               ("Year", "2024"), ("Live", live("https://kiara-vong.github.io/animal-crossing/", "Open it")),
               ("Note", NOTE)],
         nav=[("overview", "Overview", False), ("context", "Context", False),
              ("how", "How it works", False), ("taught", "What it taught me", False)],
         sections=[
             ("context", "Context", "Reading about an algorithm is not knowing it",
              ["I had read the wave function collapse write-ups and could have described "
               "the idea accurately at a whiteboard. Then I tried to implement it and "
               "found I understood the idea and none of the engineering, which is a gap "
               "that only appears when you build the thing.",
               "The collapse step is easy. Propagation is not: when a cell settles, every "
               "neighbour's option set narrows, and theirs after that. Getting that to "
               "terminate, stay correct, and run fast enough to watch is the actual "
               "problem, and no description had made that clear."]),
             ("how", "How it works", "Adjacency is the whole ruleset",
              ["The solver takes no map. Its entire input is a set of tiles and, for "
               "each, what is allowed on each of its edges. Everything the output looks "
               "like is emergent from those constraints.",
               "That is what makes it worth building rather than reading about. The "
               "design surface is not the picture, it is the ruleset, and the "
               "relationship between the two is not obvious in either direction. "
               "Tightening one edge rule changes the character of the whole island, and "
               "wanting a particular look means reasoning backwards to the constraints "
               "that would produce it."],
              [("Lowest entropy first",
                "Always collapse the most constrained cell. Pick randomly instead and "
                "the solver spends its time backtracking out of contradictions it "
                "walked into with its eyes open."),
               ("Propagate, then stop",
                "A settled cell narrows its neighbours, and theirs. The queue has to "
                "drain to a fixed point before the next collapse."),
               ("Backtrack cheaply",
                "When a cell runs out of options, rewind to the last one that still had "
                "a choice. Most of the work is choosing where to look next.")]),
             ("taught", "What it taught me", "Constraint propagation, everywhere after",
              ["The thing I did not expect is how often this shape turns up once you "
               "have built it once. A design system's token layers are a constraint "
               "propagation problem wearing different clothes: change a primitive, and "
               "the change has to reach every component that depends on it, exactly "
               "once, without cycling.",
               "I recognised that faster at work for having written a solver first."]),
         ]),

    dict(slug="p-dorms", title="Dorms @ Brown", kicker="Personal",
         hero="tile/dorms.jpg",
         hero_alt="The Dorms @ Brown landing page: find where you will actually want to live",
         live="https://kiara-vong.github.io/dab/",
         intro=("Before the annual housing lottery, students piece dorm information "
                "together from old forum posts, secondhand accounts and a housing page "
                "with floor plans but no photos. D@B puts it in one place: photos, "
                "plans, features and peer reviews, plus a quiz that narrows thirty "
                "dorms to a shortlist worth touring."),
         meta=[("Role", "Full stack"),
               ("Stack", "React, Java (Spark),<br>Firebase, Docker"),
               ("Year", "2023"), ("Live", live("https://kiara-vong.github.io/dab/", "Open it")),
               ("Note", NOTE)],
         nav=[("overview", "Overview", False), ("context", "Context", False),
              ("how", "How it works", False), ("taught", "What it taught me", False)],
         sections=[
             ("context", "Context", "Everyone was guessing, including Res Life",
              ["The information existed. It was just scattered across a university "
               "housing page, a few years of forum posts, and whoever you happened to "
               "know who had lived somewhere. There was no single place to see what a "
               "room actually looks like or hear what the people in it thought.",
               "The cost landed on students as a bad decision they lived with for a "
               "year, and on Residential Life as a steady stream of one-off questions "
               "that better upfront information would have answered."]),
             ("how", "How it works", "Why there is a backend at all",
              ["The frontend never talks to the database. Every read and write goes "
               "through a Java server, which is the only thing holding admin "
               "credentials; the client holds a public config good for sign-in and "
               "photo upload and nothing else.",
               "That split is what forced the deployment shape. GitHub Pages serves "
               "static files only, so the server needed a real host and runs as a "
               "container elsewhere, with the service-account key passed in as an "
               "environment variable rather than a file, because most container "
               "platforms have no friendly way to drop in a raw secret."],
              [("One credential holder",
                "Admin keys live on the server. The client gets a public config and "
                "no more."),
               ("Static front, hosted back",
                "A static host cannot run a server, so the two deploy separately and "
                "meet over HTTP."),
               ("Sign-in by redirect",
                "Popup sign-in is silently killed by default cross-origin policy on "
                "static hosts: the window opens, closes, and never completes.")]),
             ("photos", "How it works", "Photographs nobody framed",
              ["Dorm photos are phone snapshots in every orientation and resolution. "
               "Hard-cropping a tall photo into a fixed frame cuts off half the room, "
               "which is the half you wanted.",
               "The gallery letterboxes the full photo over a blurred, darkened copy of "
               "itself filling the rest of the frame. Nothing is cropped, the frame "
               "stays a consistent size, and the fill reads as intentional rather than "
               "as empty space."]),
             ("taught", "What it taught me", "The deployment is part of the design",
              ["I had thought of hosting as something that happens after the build. It "
               "is not: the static-host constraint decided the architecture, the "
               "auth flow and the routing, and every one of those is visible to the "
               "person using it.",
               "Client-side routing on a project path needed an explicit basename and "
               "the redirect trick for deep links, because there is no server to "
               "rewrite a URL. That is a design decision that arrived from the "
               "infrastructure, and I would now go looking for those earlier."]),
         ]),

    dict(slug="p-stardew", title="Stardew Companion", kicker="Personal",
         hero="tile/stardew.jpg",
         hero_alt="A pixel-art farm title screen with mountains, a barn and a night sky",
         live="https://kiara-vong.github.io/stardew/",
         intro=("A single-page fan guide: look up any villager's favourite gifts, click "
                "around town to learn what each building is for, and pick up a fact on "
                "the way past. No framework and no build step, styled closely enough "
                "that it feels like it belongs in the game."),
         meta=[("Role", "Everything"), ("Stack", "HTML, CSS,<br>vanilla JS"),
               ("Year", "2024"), ("Live", live("https://kiara-vong.github.io/stardew/", "Open it")),
               ("Note", NOTE)],
         nav=[("overview", "Overview", False), ("context", "Context", False),
              ("how", "How it works", False), ("taught", "What it taught me", False)],
         sections=[
             ("context", "Context", "The wiki is complete and unpleasant",
              ["Everything about this game is documented somewhere. The problem is that "
               "the documentation is a wiki, and a wiki is optimised for completeness "
               "rather than for the question you actually have, which is almost always "
               "“what does this one person want”, asked while the game is paused.",
               "So the whole design brief was: one page, no navigation, answer that "
               "question in under three seconds."]),
             ("how", "How it works", "Borrowing a visual language without stealing assets",
              ["The thing that makes it feel like the game is not any single asset. It "
               "is the palette, the chunky border radii, the drop shadows on the panels "
               "and the specific weight of the type. Get those right and hand-drawn "
               "elements read as belonging; get them wrong and a real asset still looks "
               "pasted in.",
               "No build step is a constraint I set on purpose. A fan guide that needs "
               "npm install to change a gift list is a fan guide that stops being "
               "updated."]),
             ("taught", "What it taught me", "Pastiche is a discipline",
              ["Matching an existing visual language closely is much harder than "
               "designing freely, and much better practice. You cannot fall back on "
               "taste; you have to measure what is actually there and reproduce it, "
               "which is the same skill an audit of a design system needs."]),
         ]),

    dict(slug="p-uxfolio", title="UI/UX Case Studies", kicker="Personal",
         hero="tile/uxfolio.jpg",
         hero_alt="A dark portfolio home page with a large introduction and case study cards",
         live="https://kiara-vong.github.io/portfolio/",
         intro=("An earlier portfolio, built around research and process rather than "
                "final screenshots. Each piece walks through the problem, what was "
                "tried, and what actually shipped, which is the format I still think "
                "is right and the reason this site looks the way it does."),
         meta=[("Role", "Everything"), ("Stack", "HTML, CSS, JS,<br>static build"),
               ("Year", "2023"), ("Live", live("https://kiara-vong.github.io/portfolio/", "Open it")),
               ("Note", NOTE)],
         nav=[("overview", "Overview", False), ("context", "Context", False),
              ("how", "How it works", False), ("taught", "What it taught me", False)],
         sections=[
             ("context", "Context", "A grid of final screens says nothing",
              ["Most student portfolios are a grid of finished screens. They show that "
               "you can make something look good, which is the least interesting thing "
               "about design work and the easiest to fake.",
               "What a reviewer actually wants is the middle: what you tried, what you "
               "threw away, and why. That is the part nobody publishes because it is "
               "the part that is unflattering."]),
             ("how", "How it works", "Process as the artefact",
              ["Every case study leads with the problem and spends most of its length "
               "on the decisions, with the final screens arriving last and briefly. "
               "The explorations that were abandoned get as much room as the one that "
               "shipped, which is the only honest way to show a decision was made "
               "rather than stumbled into."]),
             ("taught", "What it taught me", "The format that survived",
              ["This is the direct ancestor of the case studies on this site: problem, "
               "then the two or three choices that were genuinely hard, then what "
               "changed. Two portfolios later I have not found a better shape."]),
         ]),

    dict(slug="p-chess", title="Chess Engine", kicker="Personal",
         hero="tile/chess.jpg",
         hero_alt="A chess board at the starting position with move and perspective controls",
         live="https://kiara-vong.github.io/site/projects/chess/",
         intro=("A playable board with an opponent behind it: move generation, "
                "alpha-beta search, and an evaluation function that is honest about "
                "how little it knows. It beats me, which was the acceptance criterion "
                "and remains mildly annoying."),
         meta=[("Role", "Everything"), ("Stack", "JavaScript, canvas"),
               ("Year", "2023"), ("Live", live("https://kiara-vong.github.io/site/projects/chess/", "Play it")),
               ("Note", NOTE)],
         nav=[("overview", "Overview", False), ("context", "Context", False),
              ("how", "How it works", False), ("taught", "What it taught me", False)],
         sections=[
             ("context", "Context", "Move generation is the boring, load-bearing part",
              ["Everyone starts a chess engine wanting to write the clever search. The "
               "search is a week; move generation is a month, because the rules have "
               "more exceptions than anyone remembers. En passant, castling through "
               "check, pinned pieces, promotion, the fifty-move rule.",
               "None of it is interesting and all of it has to be exactly right, "
               "because a search built on top of a subtly wrong move generator produces "
               "confident nonsense."]),
             ("how", "How it works", "Searching without wasting the search",
              ["Alpha-beta is minimax that stops looking down a line as soon as it "
               "proves it cannot beat one already found. How much it saves depends "
               "entirely on move ordering: search the best move first and most of the "
               "tree never gets visited at all.",
               "So the ordering heuristics matter more than the depth. Captures first, "
               "then checks, then everything else, and the improvement is dramatic "
               "enough that it changes what depth is affordable."],
              [("Order first, search second",
                "Alpha-beta only pays off if the good moves come first. The ordering "
                "is the optimisation."),
               ("Quiesce at the leaves",
                "Stopping mid-capture makes the engine hallucinate material. Search "
                "captures until the position is quiet."),
               ("Evaluate honestly",
                "Material, position, mobility. It has no opening book and no endgame "
                "tables, and it should not pretend otherwise.")]),
             ("taught", "What it taught me", "Correctness before cleverness",
              ["I wrote the search first and spent a fortnight debugging an engine that "
               "was fine. The bug was in castling. Building the unglamorous layer "
               "properly and testing it against known positions would have cost two "
               "days and saved twelve."]),
         ]),

    dict(slug="p-pacman", title="Pac-Man", kicker="Personal",
         hero="tile/pacman.jpg",
         hero_alt="A Pac-Man maze in blue on black, dots laid through every corridor",
         live="https://kiara-vong.github.io/site/projects/pacman/",
         intro=("Pac-Man rebuilt in the browser: the maze, the pellets, four ghosts "
                "with their own pursuit behaviour, and the frightened state that "
                "briefly reverses all of it. Canvas and plain JavaScript, no engine."),
         meta=[("Role", "Everything"), ("Stack", "JavaScript, canvas"),
               ("Year", "2023"),
               ("Live", live("https://kiara-vong.github.io/site/projects/pacman/",
                             "Play it")),
               ("Note", NOTE)],
         nav=[("overview", "Overview", False), ("context", "Context", False),
              ("how", "How it works", False), ("taught", "What it taught me", False)],
         sections=[
             ("context", "Context", "The game is the ghosts",
              ["Pac-Man is easy to describe and hard to reproduce, and almost all of "
               "the difficulty is in four characters who could have been identical and "
               "deliberately are not. The maze is a fixed grid, the pellets are a "
               "counter, and the player has one input. Everything anybody remembers "
               "about the game comes from how the ghosts behave.",
               "So the interesting version of this project was never getting a yellow "
               "circle to move. It was giving four pursuers distinct personalities out "
               "of one shared movement system."]),
             ("how", "How it works", "Four chase rules, one movement system",
              ["Each ghost runs the same loop: pick a target tile, then at every "
               "junction take the direction that most reduces the distance to it, "
               "without reversing. All four share that. What separates them is only "
               "which tile they choose, which is a remarkably cheap way to buy "
               "character.",
               "Frightened mode then inverts the rule rather than replacing it: the "
               "same code picks the direction that INCREASES the distance. The state "
               "everyone remembers is four lines, because the movement system was built "
               "to be pointed at any target."],
              [("Targets, not paths",
                "No pathfinding anywhere. A ghost only ever compares the distance from "
                "each legal exit of a junction, which is why it can be wrong in the "
                "specific ways that make it fun to dodge."),
               ("No reversing",
                "One rule, and it is what stops a ghost oscillating in a corridor. It "
                "is also why cornering works as an escape."),
               ("Grid first, pixels second",
                "Movement resolves on tile centres and is interpolated for drawing. "
                "Doing it the other way round makes turns feel mushy and lets a "
                "character clip a corner it should not.")]),
             ("taught", "What it taught me", "Behaviour is cheaper than content",
              ["Four ghosts with four target rules produce more variety than four "
               "hand-authored patrol routes would have, and they keep producing it "
               "after the player has learned them. The system generates the content.",
               "That has come up in interface work more than once. A rule that "
               "describes how something should behave outlasts a screen that shows "
               "what it should look like, and it survives the case nobody drew."]),
         ]),
]


def build(p):
    """Assemble one project page.

    A section is (anchor, label, h2, paragraphs) and optionally a fifth element, a
    list of (title, description) pairs that becomes the bordered rules table. That
    shape is the only thing PROJECTS has to know about the case-study template.
    """
    blocks = []
    for sec in p["sections"]:
        anchor, label, h2, paras = sec[0], sec[1], sec[2], sec[3]
        after = rules(sec[4]) if len(sec) > 4 else None
        blocks.append(section(anchor, label, h2, [esc(x) for x in paras], after=after))
    # p-stardew.html was a prefix standing in for a folder. It is a folder now.
    _gc.build(p["slug"], dict(
        out="projects/%s.html" % p["slug"].replace("p-", ""), root="../",
        title=p["title"], kicker=p["kicker"], intro=p["intro"],
        hero=p["hero"], hero_alt=p["hero_alt"],
        nav=p["nav"], meta=p["meta"], sections=blocks))


for p in PROJECTS:
    build(p)
print("%d project pages" % len(PROJECTS))
