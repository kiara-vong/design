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


# The arrow. Drawn rather than typed, because the two characters that mean this --
# an arrow glyph and a box-with-arrow -- render at a different weight in every
# font on the list and one of them is an emoji on Windows.
ARROW = ('<svg viewBox="0 0 14 14" aria-hidden="true" focusable="false">'
         '<path d="M4 10L10 4M10 4H5.2M10 4v4.8"/></svg>')


def cta(href, label):
    """The live link, as the thing it actually is.

    It used to be the fourth of five columns in the meta box, set at 14px between
    the year and a footnote -- which is where you put a fact, not where you put
    the only place on the page a reader can go and use the thing. Everything above
    it argues that the work exists; this is the sentence that offers to prove it.

    The URL rides alongside rather than inside. A reader deciding whether to
    follow a link wants to know where it goes, and github.io is itself part of the
    claim: these are live and they are hosted, not screenshots of something that
    once ran.
    """
    host = href.split("//", 1)[-1].rstrip("/")
    return ('        <div class="cs-cta">\n'
            '          <a href="%s" target="_blank" rel="noopener">'
            '<span>%s</span>%s</a>\n'
            '          <span class="cs-cta-url">%s</span>\n'
            '        </div>\n' % (href, esc(label), ARROW, esc(host)))


PROJECTS = [
    dict(slug="p-animal-crossing", title="Island Generator", kicker="Personal",
         hero="hero/cover-ac.webp",
         hero_alt="A low-poly 3D island with cliffs, water and scattered conifers",
         live="https://kiara-vong.github.io/animal-crossing/",
         cta=cta("https://kiara-vong.github.io/animal-crossing/", "Open the generator"),
         intro=("A procedural island built tile by tile with wave function collapse. "
                "No map is authored and no layout is stored: the entire input is a "
                "set of hand-modelled pieces and the rules about which may sit next "
                "to which."),
         meta=[("Role", "Everything"), ("Stack", "React, Three.js,<br>WFC solver"),
               ("Year", "2024"),
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
              # A real recording, finally, and in the window the rest of the
              # site's screenshots sit in. No camera over it: the scene is
              # already turning and the grid is already filling, and a third
              # movement on top of two would be motion for its own sake.
              media.stage("video/island-generator-building.mp4",
                          "The solver filling an empty triangular grid tile by "
                          "tile while the island turns",
                          "Empty to finished, in one take. Every tile placed is "
                          "the most constrained cell that was left, which is the "
                          "heuristic the whole thing rests on.",
                          plate=(1280, 670))),
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
              # Interactive rather than looping, and that is the point rather
              # than a flourish. This section's claim is that the island is not
              # drawn but decided -- one cell, then the next, each following from
              # what was already settled. A loop makes that something you watch.
              # A click makes it something you do, which is the only version that
              # puts the reader where the solver is.
              #
              # Twelve frames out of one recorded run, chosen at equal increments
              # of filled area so every click is worth the same amount. Out of the
              # STILL-CAMERA run: the first take was auto-rotating, and a stepper
              # whose view swings between clicks makes the reader work out what
              # moved before they can see what changed. It starts on the bare
              # board, which is also the best evidence this section has for three
              # edges rather than four and had never been shown on its own.
              media.stepper(["plate/island-step-%02d.webp" % i
                             for i in range(1, 13)],
                            "The generator stepped forward by hand, from an empty "
                            "triangulated board to a finished island",
                            "Twelve steps out of one run, and yours to walk. The "
                            "board is the argument on its own: three edges per "
                            "cell rather than four is why ten pieces cover a "
                            "surface with no visible seam.",
                            label="Place the next tiles",
                            again="Back to the empty board",
                            note="In the app a click does more than advance it: "
                                 "it forces a specific tile into that cell and "
                                 "re-propagates outward from the choice.",
                            plate=(1440, 758))),
             ("pipeline", "How it works", "Blender to browser",
              ["The pieces are modelled in Blender and exported as glTF, then loaded and "
               "instanced through react-three-fiber, which lets the scene graph be "
               "declarative JSX instead of imperative Three.js calls. That matters more "
               "than it sounds for a generator: the solver produces a list of placements "
               "and React renders it, so the algorithm never touches the renderer.",
               "Rock and foliage colour is done in custom GLSL vertex shaders rather "
               "than baked into the models, which is what keeps a few hand-modelled "
               "pieces from reading as the same object repeated across the island."],
              # The pieces, by name, out of the app's own controls panel. This
              # section has always claimed the input is "a set of hand-modelled
              # pieces" and never shown the set. It is ten, and they are listed
              # on screen, which is a better proof than any number in a caption.
              media.stage("plate/island-generator-tiles.webp",
                          "The controls panel open on the tile list: Grass, four "
                          "cliffs, water, two beaches and two triangles",
                          "The entire input, on screen and named. Everything "
                          "above was built out of these and the rules about which "
                          "may touch which.",
                          look=(1723, 14, 458, 605),
                          call=("ten pieces",
                                "Grass, four cliffs, water, two beaches, two "
                                "triangles. That is the whole set.")),
              # What the ten add up to, against what they started from. Only
              # possible because the second run was recorded with the camera
              # still: these are two frames of one take, in exact register, so
              # the only thing that changes across the seam is the thing being
              # compared.
              media.wipe("plate/island-wipe-before.webp",
                         "plate/island-wipe-after.webp",
                         "The same board before and after one full generation, "
                         "split by a line the reader can drag",
                         "Drag the line. Left is the board with nothing decided; "
                         "right is what the ten pieces and their adjacency rules "
                         "made of it, in one run, with nothing placed by hand.",
                         tags=("nothing decided", "every cell settled"),
                         plate=(1440, 758))),
             ("taught", "What it taught me", "Constraint propagation, everywhere after",
              ["The thing I did not expect is how often this shape turns up once you "
               "have built it once. A design system's token layers are a constraint "
               "propagation problem wearing different clothes: change a primitive, and "
               "the change has to reach every component that depends on it, exactly "
               "once, without cycling.",
               "I recognised that faster at work for having written a solver first."]),
         ]),

    dict(slug="p-dorms", title="Dorms @ Brown", kicker="Personal",
         hero="hero/cover-dorms.webp",
         hero_alt="The Dorms @ Brown landing page: find where you will actually want to live",
         live="https://kiara-vong.github.io/dab/",
         cta=cta("https://kiara-vong.github.io/dab/", "Open Dorms @ Brown"),
         intro=("Before the annual housing lottery, students piece dorm information "
                "together from old forum posts, secondhand accounts and a housing page "
                "with floor plans but no photos. D@B puts it in one place: photos, "
                "plans, features and peer reviews, plus a quiz that narrows thirty "
                "dorms to a shortlist worth touring."),
         meta=[("Role", "Full stack"),
               ("Stack", "React, Java (Spark),<br>Firebase, Docker"),
               ("Year", "2023"),
               ("Note", NOTE)],
         nav=[("overview", "Overview", False), ("context", "Context", False),
              ("does", "What it does", False),
              ("page", "A dorm page", True), ("quiz", "The quiz", True),
              ("how", "How it works", False),
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
              # The narrowing, as one figure rather than two. It used to be a
              # clip of the filters plus a still of the list, which stated the
              # same claim twice and proved it neither time: the clip was too
              # small to read a checkbox in and the still could not show length.
              #
              # So: the whole list scrolls to its own footer -- thirty halls is a
              # scroll, not a number in a caption -- and then three switches land
              # in order and the grid falls from thirty to seventeen to four to
              # one underneath them. The camera holds wide through all of it,
              # because the collapse is the evidence and a close framing would
              # crop it, and only afterwards goes in on the rail that did it.
              #
              # The `scroll` there is doing real work: at the framing that shows
              # the grid, the third switch (Private, under BATHROOM) is below the
              # fold. The camera cannot reach past the window, so the page is
              # carried up 228px first and all three checks land in one frame.
              media.page(["plate/dorms-filter-0.webp",
                          "plate/dorms-filter-1.webp",
                          "plate/dorms-filter-2.webp",
                          "plate/dorms-filter-3.webp"],
                         "The dorm index, filtered: thirty residence halls, then "
                         "seventeen with singles, then four of those on Center "
                         "Campus, then the one with a private bathroom",
                         "The narrowing is the feature: six dimensions and a live "
                         "search, over the whole campus. Three of the six take "
                         "thirty halls down to Minden.",
                         view=(1280, 600), scroll=228,
                         look=(0, 80, 820, 412))),

             ("page", "What it does", "A dorm page, top to bottom",
              ["The page answers the questions in the order you would ask them. A "
               "photograph of the actual room first, because that is what nobody "
               "could find anywhere else. Then the description and the six features "
               "the filters run on. Then where it is on campus, then the plan of the "
               "floor you might live on, then what somebody who lived there said.",
               "Two of those parts took a decision rather than a layout. Dorm photos "
               "are phone snapshots in every orientation and resolution, and "
               "hard-cropping a tall one into a fixed frame cuts off the half of the "
               "room you wanted. The gallery letterboxes the whole photo over a "
               "blurred, darkened copy of itself: nothing is cropped, the frame keeps "
               "its size, and the fill reads as intentional rather than as empty "
               "space.",
               "The other is the plans. Keeney, Greg, Grad Center, New Pembroke and "
               "Young Orchard are not buildings, they are several, each with its own "
               "floors and its own set of plans, so the plans render as grouped card "
               "grids, one group per building. That only exists because the data was "
               "looked at rather than assumed, and it is invisible on the other "
               "twenty-five dorms, which is the correct outcome."],
              [("Gallery",
                "Every photo at full height, letterboxed rather than cropped."),
               ("Description and features",
                "Room type, bathroom, kitchen, floor, common room, elevator: the "
                "filter rail restated for one dorm."),
               ("Location",
                "An embedded campus map, because South Campus means nothing until "
                "you have seen the walk."),
               ("Floor plans",
                "Grouped per building for the five dorms that are more than one."),
               ("Reviews",
                "An average rating, and what the people who lived there wrote.")],
              # The dorm page itself, and the reason it is one figure rather than
              # a set of crops: the claim is that everything is in ONE PLACE, and
              # you cannot make that claim with five pictures of five places. So
              # the whole page runs past: photographs of the actual room, the
              # description, the feature table, the map, six floors of four
              # buildings, and a review at the bottom.
              #
              # It closes on the feature table because that is the row-for-row
              # answer to the filter rail above. Room type, bathroom, kitchen,
              # floor, common room, elevator: the same six dimensions the index
              # narrows on, stated for one dorm. Everything else in this page is
              # shown closer somewhere further down; the table is not.
              media.page("plate/dorms-detail.webp",
                         "A dorm page for Grad Center: photo gallery, description, "
                         "a feature table, a campus map, floor plans for four "
                         "buildings, and a student review",
                         "One page per dorm, answering what the filters cannot. "
                         "Photographs of the actual room rather than the building "
                         "from outside, a plan for every floor of every building, "
                         "where it sits on the map, and someone who lived there "
                         "saying what it was like. The table it ends on is the "
                         "filter rail again, stated for one dorm.",
                         view=(1280, 600), scroll=490,
                         look=(740, 125, 540, 350), dur="18s"),
              media.stage("plate/dorms-reviews.webp",
                          "The reviews section of a dorm page: the rating summary, "
                          "the form for writing one, and a posted review",
                          "The part named in the intro of every version of this "
                          "project. A rating, a box asking what it is actually like, "
                          "and the one review that came back.",
                          # The whole section at rest, then the review itself. No
                          # label on this one: the card runs the width of the page,
                          # so reserving a column for one would shrink the words
                          # below reading size, and the words are the point.
                          plate=(2400, 1480), look=(380, 1120, 1640, 320))),
             ("quiz", "What it does", "Thirty dorms in, three out",
              ["The filters assume you already know what you want. Plenty of people "
               "do not. They know they would like to cook sometimes, that a private "
               "bathroom matters more to them than being on Center Campus, and that "
               "they would rather not spend a year alone on a Tuesday night, which is "
               "not a filter query.",
               "So the quiz asks about those instead: room styles that would work, "
               "where you would rather live, how much the bathroom matters, and a few "
               "more. What comes back is not a filtered list with everything else "
               "hidden, it is a ranked shortlist of three, which is a number of "
               "buildings you can actually go and walk through before the lottery."],
              # The form fills itself in, then submits itself. The answers are
              # not in the capture as a state that can be cross-faded to -- the
              # capture IS the answered form -- so what moves is the other way
              # round: an unselected pill sits over each answer and is taken away
              # in turn, and every one of those pills carries the glyphs lifted
              # out of the crimson it is covering. See gen/quiz_picks.py.
              #
              # Not two states of one screen: two pages, and the click that
              # goes from one to the other. The form scrolls to its own foot so
              # the button arrives in frame rather than being cut to, the camera
              # goes in far enough that a press is a press rather than a couple
              # of pixels, and the load is a cut -- a page arriving is instant and
              # a cross-fade would say it was not.
              #
              # The button that moves is a crop of the button in the capture,
              # laid over itself on a patch of the page's own background, so
              # there is no second asset to keep in register with the first.
              media.flow(["plate/dorms-quiz-page.webp",
                          "plate/dorms-quiz-results.webp"],
                         "The recommendation quiz with all six questions "
                         "answered, the Get Recommendations button pressed, and "
                         "the results page ranking Hegeman, Hope and Caswell one "
                         "to three",
                         "Six questions, one button, three buildings. Not a "
                         "shorter list of the same kind: an answer to a question "
                         "the filters cannot be asked.",
                         view=(1280, 600),
                         picks="quiz-picks.json",
                         press=(510, 1166, 260, 55),
                         look=(400, 1090, 500, 200))),
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
              media.stage("plate/dorms-signin-gate.webp",
                          "Google sign-in, restricted to brown.edu accounts",
                          "The gate is what makes a review worth reading: it comes from somebody who actually lives there. Signed out, because a real account has no business in a portfolio screenshot.",
                          plate=(1568, 751), look=(430, 175, 710, 200),
                          call=("brown.edu only",
                                "The whole gate, and the reason a review here is "
                                "worth more than one anywhere else."))),
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
         hero="hero/cover-stardew.webp",
         hero_alt="A pixel-art farm title screen with mountains, a barn and a night sky",
         live="https://kiara-vong.github.io/stardew/",
         cta=cta("https://kiara-vong.github.io/stardew/", "Open the companion"),
         intro=("A single-page fan guide: look up any of the 34 villagers' favourite "
                "gifts, click around town to learn what each building is for, and play "
                "one of four arcade cabinets built into the page. No framework and no "
                "build step, styled closely enough that it feels like it belongs in "
                "the game."),
         meta=[("Role", "Everything"),
               ("Stack", "HTML, CSS, vanilla JS,<br>canvas, Web Audio"),
               ("Year", "2024"),
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
                          travel="39.39%"),
              media.strip("plate/stardew-location-popup-saloon.webp",
                          "The Saloon popup, scrolled through its full height",
                          "One of the six full-box buildings, given the same treatment as the others: hours, what's inside, who you'll find there.",
                          travel="25.98%")),
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
              media.stage("plate/stardew-villager-abigail.webp",
                          "A villager card: bracketed portrait, birthday, biography, loved and liked gifts",
                          "The hearts beside Loves and Likes are the game's own friendship sprites rather than emoji, which is the sort of detail the whole pastiche rests on.",
                          plate=(2200, 1100), look=(620, 610, 1000, 320),
                          call=("the game's own heart",
                                "A friendship sprite lifted from the game, not "
                                "an emoji standing in for one."))),
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
              media.stage("plate/stardew-arcade-row.webp",
                          "Four arcade cabinets side by side",
                          "Junimo Kart, Fishing, Prairie King and Junimo Jamboree. Each is a plain canvas with its own loop and no engine under it.",
                          plate=(2200, 498), look=(420, 175, 1360, 300),
                          call=("four cabinets",
                                "One canvas each, one loop each, and no engine "
                                "under any of them.")),
              media.clip("stardew-junimo-kart",
                         "Junimo Kart: the start line, a cleared gap, a spike hit, and the score screen",
                         "Start, a cleared jump, a spike taken wrong, the score screen it resets from. Four states standing in for the run until this one gets a real recording."),
              media.clip("stardew-prairie-king",
                         "Journey of the Prairie King: spawn, a wave cleared, a hit taken, the wave counter climbing",
                         "Five waves as five stills. The counter and the health both move considerably faster than this in the actual game.")),
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
                          travel="36.64%"),
              media.clip("stardew-junimo-jamboree",
                         "Junimo Jamboree: difficulty select, notes falling in the four lanes, a cleared song",
                         "Difficulty select, notes falling, a cleared song: three states where the actual note timing belongs once there's a real capture of it.")),
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
         hero="hero/cover-uxfolio.webp",
         hero_alt="A dark portfolio home page with a large introduction and case study cards",
         live="https://kiara-vong.github.io/portfolio/",
         cta=cta("https://kiara-vong.github.io/portfolio/", "Open the case studies"),
         intro=("An earlier portfolio, built around research and process rather than "
                "final screenshots. Each piece walks through the problem, what was "
                "tried, and what actually shipped, which is the format I still think "
                "is right and the reason this site looks the way it does."),
         meta=[("Role", "Everything"), ("Stack", "HTML, CSS, JS,<br>static build"),
               ("Year", "2023"),
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
         hero="hero/cover-chess.webp",
         hero_alt="A chess board at the starting position with move and perspective controls",
         live="https://kiara-vong.github.io/site/projects/chess/",
         cta=cta("https://kiara-vong.github.io/site/projects/chess/", "Play the engine"),
         intro=("A playable board with an opponent behind it: move generation, "
                "alpha-beta search, and an evaluation function that is honest about "
                "how little it knows. It beats me, which was the acceptance criterion "
                "and remains mildly annoying."),
         meta=[("Role", "Everything"), ("Stack", "JavaScript, canvas"),
               ("Year", "2023"),
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
                "tables, and it should not pretend otherwise.")],
              media.clip("chess-autoplay",
                         "Two copies of the engine playing each other with no human "
                         "moves, the board degrading from the starting position into "
                         "an unrecognizable mess within seconds",
                         "Both sides set to the live site's own (BAD) AI CHESS, taking "
                         "the engine's first choice every move. No opening book to "
                         "paper over the early game and no endgame tables to recover "
                         "with, so the position is unrecognizable by move six.")),
             ("taught", "What it taught me", "Correctness before cleverness",
              ["I wrote the search first and spent a fortnight debugging an engine that "
               "was fine. The bug was in castling. Building the unglamorous layer "
               "properly and testing it against known positions would have cost two "
               "days and saved twelve."]),
         ]),

    dict(slug="p-pacman", title="Pac-Man", kicker="Personal",
         hero="hero/cover-pacman.webp",
         hero_alt="A Pac-Man maze in blue on black, dots laid through every corridor",
         live="https://kiara-vong.github.io/site/projects/pacman/",
         cta=cta("https://kiara-vong.github.io/site/projects/pacman/", "Play it"),
         intro=("Pac-Man rebuilt in the browser: the maze, the pellets, four ghosts "
                "with their own pursuit behaviour, and the frightened state that "
                "briefly reverses all of it. Canvas and plain JavaScript, no engine."),
         meta=[("Role", "Everything"), ("Stack", "JavaScript, canvas"),
               ("Year", "2023"),
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
                "character clip a corner it should not.")],
              media.clip("pacman-gameplay",
                         "A round of Pac-Man from the ready countdown through a ghost "
                         "collision, death and restart",
                         "The countdown, a clean run past two ghosts, then a cornering "
                         "none of the three chase rules were built to survive, and the "
                         "restart that follows automatically.")
              + media.flat(
                  "case/cs-pac-targets.svg",
                  "Four boards side by side: the same player in each, one ghost "
                  "each, and a different highlighted target tile every time",
                  "The part no screenshot of this game can show. Every frame of "
                  "the clip above is four ghosts moving; the reason they move "
                  "differently is four target tiles, and that only exists in the "
                  "code until something draws it.")),
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
        out="projects/%s/index.html" % p["slug"].replace("p-", ""), root="../../",
        title=p["title"], kicker=p["kicker"], intro=p["intro"],
        flowers="foot-projects.png",
        hero=p["hero"], hero_alt=p["hero_alt"],
        nav=p["nav"], meta=p["meta"], cta=p.get("cta", ""), sections=blocks))


for p in PROJECTS:
    build(p)
print("%d project pages" % len(PROJECTS))
