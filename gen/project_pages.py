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
from gen import media
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
              ("how", "How it works", False), ("grid", "Triangles", True),
              ("pipeline", "The tile set", True),
              ("taught", "What it taught me", False)],
         sections=[
             ("context", "Context", "Reading about an algorithm is not knowing it",
              ["I had read the wave function collapse write-ups and could have described "
               "the idea accurately at a whiteboard. Then I tried to implement it and "
               "found I understood the idea and none of the engineering, which is a gap "
               "that only appears when you build the thing.",
               "The collapse step is easy. Propagation is not: when a cell settles, every "
               "neighbour's option set narrows, and theirs after that. Getting that to "
               "terminate, stay correct, and run fast enough to watch is the actual "
               "problem, and no description had made that clear."],
              media.clip("island-generator-building",
                         "The solver filling an empty grid tile by tile",
                         "Empty to finished. Every tile placed is the most constrained cell that was left, which is the heuristic the whole thing rests on.")),
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
                "a choice. Most of the work is choosing where to look next.")],
              media.deal(["plate/island-generator-stage1-empty.webp",
                          "plate/island-generator-stage2-quarter.webp",
                          "plate/island-generator-stage3-threequarter.webp",
                          "plate/island-generator-stage4-complete.webp"],
                         "One generation at four stages, from an empty grid to a finished island",
                         "Same camera in all four, so what changes is only how much has been decided. This is the still version of the clip above, and what reduced motion gets.")),
             ("grid", "How it works", "Three edges, not four",
              ["The island is a triangular grid rather than a square one, which is the "
               "decision the whole tile set rests on. Three edges instead of four means "
               "far fewer unique pieces are needed to cover a surface without a visible "
               "seam, and hand-modelling every piece is the expensive part of this kind "
               "of project.",
               "The cost is a coordinate system that is genuinely harder to reason "
               "about. Each tile has three rotations rather than four, neighbours "
               "alternate orientation across a row, and every adjacency rule has to be "
               "stated against the right edge of the right rotation. That bookkeeping is "
               "where the bugs lived.",
               "Generation is also steerable rather than purely automatic. Clicking any "
               "cell forces a specific tile there and re-propagates outward from it, so "
               "the solver can be pushed toward a coastline or a cliff and then left to "
               "resolve everything the choice implies."],
              media.clip("island-generator-steering",
                         "Forcing a tile mid-generation and watching the constraint propagate outward",
                         "One click fixes a cell, and everything that choice implies resolves around it.")),
             ("pipeline", "How it works", "Blender to browser",
              ["The pieces are modelled in Blender and exported as glTF, then loaded and "
               "instanced through react-three-fiber, which lets the scene graph be "
               "declarative JSX instead of imperative Three.js calls. That matters more "
               "than it sounds for a generator: the solver produces a list of placements "
               "and React renders it, so the algorithm never touches the renderer.",
               "Rock and foliage colour is done in custom GLSL vertex shaders rather "
               "than baked into the models, which is what keeps a few hand-modelled "
               "pieces from reading as the same object repeated across the island."],
              media.push("plate/island-generator-finished.webp",
                         "A finished island: cliffs, water, beaches and scattered conifers",
                         "Nothing here is placed by hand. The rock and foliage colour is shader work, which is what stops a few modelled pieces reading as one object repeated.",
                         z=1.4, fx="52%", fy="46%")),
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
              ("does", "What it does", False), ("how", "How it works", False),
              ("plans", "Floor plans", True), ("photos", "Photographs", True),
              ("taught", "What it taught me", False)],
         sections=[
             ("context", "Context", "Everyone was guessing, including Res Life",
              ["The information existed. It was just scattered across a university "
               "housing page, a few years of forum posts, and whoever you happened to "
               "know who had lived somewhere. There was no single place to see what a "
               "room actually looks like or hear what the people in it thought.",
               "The cost landed on students as a bad decision they lived with for a "
               "year, and on Residential Life as a steady stream of one-off questions "
               "that better upfront information would have answered."]),
             ("does", "What it does", "Everything in one place, then a shortlist",
              ["Thirty dorms, filterable down to the few worth walking to. The filters "
               "are the ones people actually argue about in March: room type, location "
               "on campus, whether the bathroom is shared and how, kitchen access, class "
               "year, amenities, with live search by name over the top of all of it.",
               "A dorm's own page then has to answer the question the filters cannot, "
               "which is what the place is like. Photo gallery, floor plans, room "
               "features, an embedded campus map, an average rating, and reviews from "
               "people who lived there."],
              [("Browse and filter",
                "Six filter dimensions and live name search, applied to the whole "
                "campus at once."),
               ("Dorm pages",
                "Photos, plans, features, map and rating, which is more than the "
                "official housing page has ever shown in one place."),
               ("Peer reviews",
                "Read what other students said, or sign in and leave your own with an "
                "optional photo."),
               ("The quiz",
                "A few questions about what you care about, and thirty dorms come back "
                "as a ranked shortlist."),
               ("Sign-in",
                "Google, restricted to brown.edu, so the reviews come from people who "
                "actually live there.")],
              media.clip("dorms-browse-filter",
                         "Filtering the dorm list, then searching it by name",
                         "Six filter dimensions over the whole campus with live search on top. The narrowing is the feature."),
              media.push("plate/dorms-reviews.webp",
                         "A dorm's review list with star ratings",
                         "Named in the intro of every version of this project and, until now, shown nowhere. Author names are blurred; these are real students.",
                         z=1.4, fx="40%", fy="52%")),
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
                "static hosts: the window opens, closes, and never completes.")],
              media.push("plate/dorms-signin-gate.webp",
                         "Google sign-in, restricted to brown.edu accounts",
                         "The gate is what makes a review worth reading: it comes from somebody who actually lives there. Signed out, because a real account has no business in a portfolio screenshot.",
                         z=1.5, fx="50%", fy="44%")),
             ("plans", "How it works", "Some dorms are more than one building",
              ["Keeney, Greg, Grad Center, New Pembroke and Young Orchard are not "
               "buildings, they are several, each with its own floors and its own set "
               "of plans. A flat list of floor plans is wrong for those five and "
               "quietly misleading for anyone who does not already know that.",
               "So the plans render as grouped card grids, one group per building. It "
               "is a small structural decision that only exists because the data was "
               "looked at rather than assumed, and it is invisible on the other "
               "twenty-five dorms, which is the correct outcome."],
              media.push("plate/dorms-floorplans-multibuilding.webp",
                         "Floor plans grouped into one card grid per building",
                         "Five of the thirty dorms are several buildings. A flat list of plans is wrong for those and quietly misleading to anyone who does not already know it.",
                         z=1.35, fx="30%", fy="50%")),
             ("photos", "How it works", "Photographs nobody framed",
              ["Dorm photos are phone snapshots in every orientation and resolution. "
               "Hard-cropping a tall photo into a fixed frame cuts off half the room, "
               "which is the half you wanted.",
               "The gallery letterboxes the full photo over a blurred, darkened copy of "
               "itself filling the rest of the frame. Nothing is cropped, the frame "
               "stays a consistent size, and the fill reads as intentional rather than "
               "as empty space."],
              media.push("plate/dorms-gallery-letterbox.webp",
                         "A tall phone photo letterboxed over a blurred copy of itself",
                         "Nothing is cropped and the frame keeps its size. What fills the rest is the same photograph, blurred and darkened.",
                         z=1.45, fx="50%", fy="50%")),
             ("taught", "What it taught me", "The deployment is part of the design",
              ["I had thought of hosting as something that happens after the build. It "
               "is not: the static-host constraint decided the architecture, the "
               "auth flow and the routing, and every one of those is visible to the "
               "person using it.",
               "Client-side routing on a project path needed an explicit basename and "
               "the redirect trick for deep links, because there is no server to "
               "rewrite a URL. That is a design decision that arrived from the "
               "infrastructure, and I would now go looking for those earlier."],
              media.clip("dorms-quiz",
                         "Answering the quiz and landing on a ranked shortlist",
                         "Thirty dorms in, a shortlist worth touring out, over a container on a free tier that sleeps between visits.")),
         ]),

    dict(slug="p-stardew", title="Stardew Companion", kicker="Personal",
         hero="tile/stardew.jpg",
         hero_alt="A pixel-art farm title screen with mountains, a barn and a night sky",
         live="https://kiara-vong.github.io/stardew/",
         intro=("A single-page fan guide: look up any of the 34 villagers' favourite "
                "gifts, click around town to learn what each building is for, and play "
                "one of four arcade cabinets built into the page. No framework and no "
                "build step, styled closely enough that it feels like it belongs in "
                "the game."),
         meta=[("Role", "Everything"),
               ("Stack", "HTML, CSS, vanilla JS,<br>canvas, Web Audio"),
               ("Year", "2024"), ("Live", live("https://kiara-vong.github.io/stardew/", "Open it")),
               ("Note", NOTE)],
         nav=[("overview", "Overview", False), ("context", "Context", False),
              ("how", "How it works", False), ("data", "Facts and assets", True),
              ("arcade", "The arcade", False), ("rhythm", "The rhythm game", True),
              ("taught", "What it taught me", False)],
         sections=[
             ("context", "Context", "The wiki is complete and unpleasant",
              ["Everything about this game is documented somewhere. The problem is that "
               "the documentation is a wiki, and a wiki is optimised for completeness "
               "rather than for the question you actually have, which is almost always "
               "“what does this one person want”, asked while the game is paused.",
               "So the whole design brief was: one page, no navigation, answer that "
               "question in under three seconds."],
              media.clip("stardew-gift-lookup",
                         "Searching a villager and opening their gift card",
                         "Type a name, open the card, read the two lists. This is the question the wiki answers in four clicks and a lot of scrolling."),
              media.deal(["plate/stardew-didyouknow-1.webp",
                          "plate/stardew-didyouknow-2.webp",
                          "plate/stardew-didyouknow-3.webp"],
                         "The Did You Know card, showing three different facts",
                         "What replaced a contact form that went nowhere. A fan guide does not need a get in touch box; it needs one more thing worth knowing.")),
             ("how", "How it works", "Borrowing a visual language without stealing assets",
              ["The thing that makes it feel like the game is not any single asset. It "
               "is the palette, the chunky border radii, the drop shadows on the panels "
               "and the specific weight of the type. Get those right and hand-drawn "
               "elements read as belonging; get them wrong and a real asset still looks "
               "pasted in.",
               "No build step is a constraint I set on purpose. A fan guide that needs "
               "npm install to change a gift list is a fan guide that stops being "
               "updated."],
              media.strip("plate/stardew-locations-both-tiers.webp",
                          "The six main buildings as full boxes, the smaller spots as an icon row beneath",
                          "Both tiers in one frame, which is the only way the tiering reads as a decision rather than as inconsistency.",
                          travel="63.99%"),
              media.strip("plate/stardew-explore-valley-popup.webp",
                          "The Explore the Valley popup, scrolled through its full height",
                          "The outdoor areas are one long scrollable panel rather than a box each, because they are places to wander through rather than buildings to visit.",
                          travel="39.39%")),
             ("data", "How it works", "Facts, sprites and code are not the same thing",
              ["The gift lists are game data, so a one-time Node script parsed them out "
               "of a mirrored fan site rather than my typing 34 characters' worth of "
               "preferences by hand. Portraits, item icons and location photos come from "
               "the same source and the official wiki, used the way a fan guide "
               "typically uses them.",
               "Game code is a different category, and the arcade below draws the line "
               "in both directions. Prairie King's shooter logic is an original "
               "recreation, because the original is somebody's work in a way a gift "
               "list is not. The fishing catch-bar, on the other hand, is a deliberate "
               "port of a specific open reference implementation at its own constants, "
               "because approximating it did not feel right and matching it exactly was "
               "the entire point."],
              [("Facts are facts",
                "What a character likes is not authored; it is looked up. Scraping it "
                "once beats retyping it 34 times."),
               ("Sprites are borrowed, and credited",
                "Non-commercial fan use, the same footing as any fan wiki, and named "
                "as such."),
               ("Logic is written, or ported on purpose",
                "Recreated where it belongs to someone, ported exactly where the "
                "reference is open and the fidelity IS the feature.")],
              media.strip("plate/stardew-villagers-grid.webp",
                          "All 34 villager portraits",
                          "Thirty-four of them. A number in a sentence is an assertion, and this is why the gift lists were parsed once rather than typed out.",
                          travel="62.72%"),
              media.push("plate/stardew-villager-abigail.webp",
                         "A villager card: bracketed portrait, birthday, biography, loved and liked gifts",
                         "The hearts beside Loves and Likes are the game's own friendship sprites rather than emoji, which is the sort of detail the whole pastiche rests on.",
                         z=1.5, fx="62%", fy="68%")),
             ("arcade", "The arcade", "Four cabinets and no game engine",
              ["Half of this project is not a guide at all. Four playable cabinets sit "
               "on the same page, each a plain canvas element with its own loop, and "
               "none of them uses a framework or an engine.",
               "They are also the reason the page does not cost anything while you are "
               "reading it. All four pause their render loop through an "
               "IntersectionObserver the moment they scroll out of view, and the rhythm "
               "game suspends its audio context at the same instant, so closing the "
               "modal actually stops the music rather than leaving it playing under "
               "everything else."],
              [("Junimo Kart",
                "A runner. Jump the spikes and the gaps, collect stars, and beat a best "
                "score that survives a reload."),
               ("Fishing",
                "Cast, bite and result on canvas, with the catch-bar minigame itself "
                "built as a DOM overlay so its physics can run at the source's native "
                "20ms tick rather than once a frame."),
               ("Journey of the Prairie King",
                "A top-down shooter over five waves. Arrows or WASD to move, hold space "
                "to fire."),
               ("Junimo Jamboree",
                "A four-lane rhythm game at three difficulties, with a song that does "
                "not exist as a file.")],
              media.push("plate/stardew-arcade-row.webp",
                         "Four arcade cabinets side by side",
                         "Junimo Kart, Fishing, Prairie King and Junimo Jamboree. Each is a plain canvas with its own loop and no engine under it.",
                         z=1.5, fx="22%", fy="50%")),
             ("rhythm", "The arcade", "One source for the song and the chart",
              ["Junimo Jamboree has no audio track. A short hand-written motif is "
               "arranged into a sixteen-measure structure at load, and that same "
               "generated chart drives both the falling notes and the oscillators, so "
               "the beatmap and the music are the same object rather than a track with "
               "a chart hand-placed on top of it. They cannot drift apart because there "
               "is nothing to drift.",
               "Note judgment and the falling-note animation are both timed off the "
               "audio context's own clock rather than animation-frame timestamps, which "
               "is the difference between a rhythm game that feels tight and one that "
               "feels slightly wrong in a way players cannot name. Because the whole "
               "chart is known up front, every oscillator is scheduled in one pass at "
               "load instead of through the lookahead scheduler that Web Audio "
               "sequencing usually needs.",
               "Difficulty changes note density and timing windows. It does not change "
               "the song."],
              media.strip("plate/stardew-jamboree-difficulty.webp",
                          "The difficulty select, with a best score kept per difficulty",
                          "Three difficulties over one generated song. What changes is note density and the timing windows, not the music.",
                          travel="36.64%")),
             ("taught", "What it taught me", "Ports have tick rates",
              ["Matching an existing visual language closely is much harder than "
               "designing freely, and much better practice. You cannot fall back on "
               "taste; you have to measure what is actually there and reproduce it, "
               "which is the same skill an audit of a design system needs.",
               "The sharpest version of that lesson was numeric. The first pass at the "
               "catch-bar ran its physics once per animation frame, which at 60fps came "
               "out about 20% faster than intended, and every constant I then re-tuned "
               "by feel took it further from the thing I was trying to match. The fix "
               "was not a better constant, it was running the loop at the tick rate the "
               "original used.",
               "The other one was structural. The popups rendered off-screen for a day "
               "because the page's parallax puts a perspective on the main element, "
               "which quietly makes it the containing block for any fixed-position "
               "child instead of the viewport. The modals had to live outside it in the "
               "DOM. Nothing about the symptom pointed at the cause."],
              media.clip("stardew-fishing",
                         "The cast, the bite, and the catch bar",
                         "The catch bar is the ported one, and the thing that ran about 20 per cent fast until its physics moved to the tick rate the original used.")),
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
              ("studies", "The four", False), ("how", "How it works", False),
              ("build", "Shared markup", True),
              ("taught", "What it taught me", False)],
         sections=[
             ("context", "Context", "A grid of final screens says nothing",
              ["Most student portfolios are a grid of finished screens. They show that "
               "you can make something look good, which is the least interesting thing "
               "about design work and the easiest to fake.",
               "What a reviewer actually wants is the middle: what you tried, what you "
               "threw away, and why. That is the part nobody publishes because it is "
               "the part that is unflattering."],
              media.strip("plate/uxfolio-casestudies-index.webp",
                          "The case-study index at full height",
                          "Four studies, and the page spends its length on them rather than on a grid of finished screens.",
                          travel="77.49%")),
             ("studies", "The four", "Four problems, deliberately unalike",
              ["Four case studies, chosen so they do not all demonstrate the same "
               "skill. One is quantitative, one is competitive research turned into a "
               "build, one is a redesign with a sense of humour about itself, and one "
               "is a domain nobody designs for."],
              [("A/B Testing",
                "Two appointment-booking flows, a hypothesis, a statistical test, and "
                "a result that had to be reported whichever way it went."),
               ("Development",
                "Competitive analysis into UI design for a React film-discovery app: "
                "search, genre filtering, bookmarking."),
               ("The Room",
                "A website redesign for the cult film, played straight enough to be "
                "useful and knowing enough to be funny."),
               ("Fonda Wallet",
                "A mobile finance tool for restaurant owners, centralising revenue and "
                "expenses. The least glamorous brief and the most interesting one.")],
              media.deal(["plate/uxfolio-fondawallet-1-problem.webp",
                          "plate/uxfolio-fondawallet-2-tried.webp",
                          "plate/uxfolio-fondawallet-3-iteration.webp",
                          "plate/uxfolio-fondawallet-4-shipped.webp"],
                         "Fonda Wallet from the problem through what was tried to what shipped",
                         "Four frames of one case study, in order. This arc is what the whole format rests on.")),
             ("how", "How it works", "Process as the artefact",
              ["Every case study leads with the problem and spends most of its length "
               "on the decisions, with the final screens arriving last and briefly. "
               "The explorations that were abandoned get as much room as the one that "
               "shipped, which is the only honest way to show a decision was made "
               "rather than stumbled into."]),
             ("build", "How it works", "Framework-free output, non-repetitive source",
              ["The shipped site is plain HTML, CSS and JavaScript with no framework "
               "and no pipeline, which is the right answer for five static pages. The "
               "trouble with five static pages is that the nav, the footer and the "
               "about card exist five times each, and hand-editing one text change in "
               "five files is how they drift apart.",
               "So the source is not what deploys. The shared pieces live once in a "
               "partials folder, the page sources reference them with include markers, "
               "and a small Node script assembles the flat static files that actually "
               "ship. The output stays framework-free; the source stops being "
               "repetitive.",
               "This site does the same thing for the same reason, with Python instead "
               "of Node and considerably more generated. That is not a coincidence, it "
               "is this project's idea kept."],
              media.clip("uxfolio-loader-transition",
                         "The loading sequence, then a page transition into a case study",
                         "The navy screen is a designed loader. It is also what made every headless capture of this site come back as a flat rectangle.")),
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


def _parts(sec):
    """(anchor, label, h2, escaped paragraphs, rules table, figure).

    A section is (anchor, label, h2, paragraphs) with two optional tails: a list of
    (title, description) pairs that becomes the bordered rules table, and a block of
    figure markup from gen/media.py.

    Read by SHAPE rather than by position. A rules table is a list of pairs and a
    figure is a string of markup, so either can be given, in either order, and a
    section that wants only a figure does not have to pass None for rules it does
    not have. Parsing these by position put a figure in the rules slot, and the
    failure was rules() trying to enumerate a string of HTML.

    A section may carry two figures. The first sits above the rules table and the
    second below it, which is the order they read in: the figure that shows what the
    section is about, then the constraints, then a figure showing a consequence.
    """
    after, figs = None, []
    for extra in sec[4:]:
        if not extra:
            continue
        elif isinstance(extra, (list, tuple)):
            after = rules(extra)
        else:
            figs.append(extra)
    if len(figs) > 1:
        after = (after or "") + "".join(figs[1:])
    return sec[0], sec[1], sec[2], [esc(x) for x in sec[3]], after, (figs or [None])[0]


def build(p):
    """Assemble one project page.

    A section is (anchor, label, h2, paragraphs) and optionally a fifth element, a
    list of (title, description) pairs that becomes the bordered rules table. That
    shape is the only thing PROJECTS has to know about the case-study template.

    Consecutive sections that share a LABEL are one group rather than several
    sections. The label is the small eyebrow above the heading, and it names the part
    of the document you are in, so printing "How it works" three times in a row turns
    one part into three loose ones and stops meaning anything. Inside a group only the
    first sub carries the eyebrow; the rest carry their heading alone, which is what
    the work case studies already do with their key decisions.

    Nav anchors keep working either way: the spy resolves them with getElementById and
    sub() puts the id on the .cs-sub. Marking those entries as sub in `nav` is what
    indents them to match.
    """
    blocks, secs, i = [], p["sections"], 0
    while i < len(secs):
        run = [secs[i]]
        while i + len(run) < len(secs) and secs[i + len(run)][1] == secs[i][1]:
            run.append(secs[i + len(run)])
        if len(run) == 1:
            anchor, label, h2, paras, after, fig = _parts(run[0])
            blocks.append(section(anchor, label, h2, paras, fig=fig, after=after))
        else:
            group = ['    <div class="cs-group">\n\n']
            for n, sec in enumerate(run):
                anchor, label, h2, paras, after, fig = _parts(sec)
                group.append(sub(anchor, label, h2, paras, fig=fig,
                                 first=(n == 0), after=after))
            group.append('    </div>\n\n')
            blocks.append("".join(group))
        i += len(run)
    # p-stardew.html was a prefix standing in for a folder. It is a folder now.
    _gc.build(p["slug"], dict(
        out="pages/projects/%s.html" % p["slug"].replace("p-", ""), root="../../",
        title=p["title"], kicker=p["kicker"], intro=p["intro"],
        flowers="foot-projects.png",
        hero=p["hero"], hero_alt=p["hero_alt"],
        nav=p["nav"], meta=p["meta"], sections=blocks))


for p in PROJECTS:
    build(p)
print("%d project pages" % len(PROJECTS))
