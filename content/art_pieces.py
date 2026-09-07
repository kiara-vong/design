# -*- coding: utf-8 -*-
"""The Art section's content: every category, every piece, every title.

Separated from gen-gallery.py deliberately. That file is image processing -- open,
transpose, resize, encode -- and this is writing. They were one 480-line file, and
the consequence was not untidiness: a caption is prose, and prose buried two
hundred lines inside a resize loop does not get read as prose. Several piece titles
in here were wrong for months (the still lifes are cut-paper flowers and had been
captioned as fruit-bowl drawing practice) because nobody, including me, ever looked
at this as a page of text.

So it is a page of text now. No imports, no logic, no executable statements: paths
are strings, and the only thing this file can do is be read.

WHERE THE CONTENT COMES FROM

Titles are hers. ../website/art/<folder>/index.html carried a title for most pieces
and those are transcribed verbatim; the grouping, the category labels and each
category's cover come from ../website/art/art.js, which is the old site's own art
index. Where a piece had no title on that site, the title here was written off the
image itself. Do not invent one. If you cannot tell what a picture is, open it.

  kind "project"  a written page: context, method, results
  kind "studio"   a salon hang, grouped by GROUPS in gen-art-pages.py

  pieces          (slug, source path, title, blurb)
                  slug is the output filename in assets/art and must be unique
                  across every category; blurb is shown only on project pages.
"""

# Source roots. The hang and the covers are cut from these by gen-gallery.py.
ART = "../website/art/"          # her own art folders, one per category
SRC = "assets/art/_src/"         # frames pulled from video, figures out of a .docx

# =====================================================================
# The categories.
#
# kind "project"  -> gets a written page: context, method, results, then the set
# kind "studio"   -> gets a salon hang and a short standfirst
# =====================================================================
CATEGORIES = [

    dict(slug="water-drop", name="Splash", kind="project", cover="mycology",
         tag="High-speed photography",
         course="ENGN 1350: Art Fluid Mechanics, Brown University",
         team="Sofia Gilroy, Kiara Vong, Himanssh Pettie, Lucian Sharpe",
         lead="Prof. Roberto Zenit",
         blurb="Worthington-Edgerton splashes: a droplet hitting still liquid, "
               "frozen by a flash a few hundred microseconds wide.",
         pieces=[
             ("dark-matter", ART + "water drop/crown bubble.png",
              "Dark Matter",
              "A single-drop crown caught inside an intact bubble. The crown and "
              "the bubble are the only two things in the frame and neither gives "
              "the eye anywhere to rest, which is where the name came from."),
             ("mycology", ART + "water drop/_mushroom.png",
              "Mycology",
              "A rising jet struck by a second drop, which caps it. Glow-stick "
              "fluid and glycerol on a water-and-cream surface: the pink and blue "
              "split down the jet is two fluids refusing to mix."),
             ("cerulean", ART + "water drop/_splash (one).png",
              "Cerulean",
              "One large blue drop held above a chaotic yellow splash. The "
              "filaments connecting the fragmenting droplets are the fluid's "
              "viscoelasticity made visible."),
             ("wd-crown", ART + "water drop/crown (drop).png", "Crown",
              "The textbook Worthington crown, lit from behind so the rim reads "
              "as separate points rather than one ring."),
             ("wd-bubble", ART + "water drop/bubble.png", "Bubble",
              "Same setup, a few milliseconds later, before the surface closed."),
             ("wd-neon", ART + "water drop/neon.png", "Neon",
              "A magenta drop above a splash still climbing toward it."),
             ("wd-catch", ART + "water drop/catch.png", "Catch",
              "The moment before the second drop lands: the surface is already "
              "deforming to meet it."),
             ("wd-clam", ART + "water drop/clam (sharp).png", "Clam",
              "A sheet thrown sideways rather than up, which happens when the "
              "drop arrives off-centre."),
             ("wd-clam-y", ART + "water drop/clam (yellow).png", "Clam, yellow",
              "The same shape on a yellow bath. Colour here is entirely the "
              "fluid, not the light."),
             ("wd-photog", ART + "water drop/splash (photographer).png",
              "Splash", "A cleaner, colder version, on white."),
         ]),

    dict(slug="smoke", name="Vortex Rings", kind="project", cover="ring-of-fire",
         tag="Flow visualisation",
         course="ENGN 1350: Art Fluid Mechanics, Brown University",
         team="Sofia Gilroy, Kiara Vong, Himanssh Pettie, Lucian Sharpe",
         lead="Prof. Roberto Zenit",
         blurb="Smoke vortex rings, laminar and turbulent, lit hard against black "
               "so the structure survives the exposure.",
         pieces=[
             ("ring-of-fire", ART + "smoke/ring of fire.png", "Ring of Fire",
              "A ring caught just as it begins to break down. The torus is still "
              "intact on the left and already shedding on the right."),
             ("inferno", ART + "smoke/inferno.png", "Inferno",
              "The turbulent regime. Past a critical Reynolds number a laminar "
              "ring stops holding together, and this is what that looks like."),
             ("chains", ART + "smoke/DSC_0900.remini-enhanced-1.png", "Chains",
              "Successive rings, each one catching the wake of the last."),
             ("sm-cosmo", ART + "smoke/cosmo.png", "Cosmo",
              "A ring that has fully transitioned, drawn out into a plume."),
             ("sm-fire", ART + "smoke/fire.png", "Fire",
              "Two rings colliding, which is the fastest way to destroy both."),
             ("sm-flower", ART + "smoke/flower.jpeg", "Flower",
              "Head-on. The rotation of the torus is legible from this angle and "
              "from almost no other."),
             ("sm-0921", ART + "smoke/DSC_0921.remini-enhanced.png", "Trailing",
              "A ring with its tail still attached to the orifice."),
             ("sm-0918", ART + "smoke/DSC_0918.remini-enhanced.png", "Travelling",
              "The same ring further along, thinner and faster."),
             ("sm-0892", ART + "smoke/DSC_0892.remini-enhanced-2.png", "Bloom",
              "Breakdown, lit magenta. The instability is symmetric at first and "
              "then very much is not."),
             ("sm-0923", ART + "smoke/DSC_0923.remini-enhanced.png", "Long",
              "A wide crop, for the length of the structure rather than its core."),
         ]),

    dict(slug="rheoscopic", name="Rheoscopic Gear Train", kind="project",
         cover="rh-final", tag="Kinetic sculpture",
         course="ENGN 1350: Art Fluid Mechanics, Brown University",
         team="Sofia Gilroy, Kiara Vong, Himanssh Pettie, Lucian Sharpe",
         lead="Prof. Roberto Zenit",
         blurb="A self-sustaining sculpture: rheoscopic fluid in rotating "
               "cylinders, driven by a 3D-printed gear train, after Paul "
               "Matisse's Kalliroscope.",
         pieces=[
             # rh-run and rh-clip are the two films' posters; rh-final is the
             # index cover. Everything else is a Selected still, each labelled for
             # what it actually shows -- the set had drifted (a printed gear filed
             # as a cylinder, a flow pattern filed as CAD, a Moody chart filed as a
             # bench photo), which is what this pass fixes.
             ("rh-run", SRC + "rheo/run.jpg", "The piece, running",
              "The gear train running under its own drive."),
             ("rh-clip", SRC + "rheo/clip.jpg", "The piece, up close",
              "The same train from the table, the cylinders in blue and pink."),
             ("rh-final", SRC + "rheo/image5.jpg", "The piece, running",
              "The whole piece from above, one cylinder full of moving fluid."),
             ("rh-hand", SRC + "rheo/hand.jpg", "A cylinder in hand",
              "One cylinder out of the train. Rheoscopic fluid is water with "
              "microscopic mica flakes that line up with the flow, so the currents "
              "show without any dye."),
             ("rh-cad", SRC + "rheo/image13.png", "CAD",
              "The assembly before it was anything physical. Tooth counts were "
              "worked backwards from the flow we wanted to see."),
             ("rh-gears", SRC + "rheo/image6.jpg", "Gear housing",
              "3D-printed drive, printed in place. The gearing sets the rotation "
              "rate, which sets whether the flow reads as laminar or turbulent."),
             ("rh-detail", SRC + "rheo/image3.jpg", "The printed gear",
              "One of the gears before assembly, printed clear so the mesh is easy "
              "to check."),
             ("rh-flow2", SRC + "rheo/image8.png", "Flow study, I",
              "The slower state. The bands are broad and hold their shape."),
             ("rh-flow", SRC + "rheo/image7.png", "Flow study, II",
              "Faster. The transition toward turbulence is sharp and repeatable."),
             ("rh-bench", SRC + "rheo/image9.png", "Moody diagram",
              "Where the flow tips from laminar to turbulent against Reynolds "
              "number. The rotation rate we chose sits on the laminar side of "
              "that line."),
         ]),

    dict(slug="sandsketch", name="SandSketch", kind="project", cover="ss-1",
         tag="Robotics",
         course="CSCI 1952Z, Brown University",
         team="Christian Labrador, Kiara Vong, Michael Donoso",
         lead=None,
         blurb="A robo-zen garden: a quadrotor with a pencil attachment, drawing "
               "geometric patterns into a sand table from the air.",
         pieces=[
             ("ss-3", SRC + "sandsketch-3.jpg", "Drawing",
              "The quad over the table mid-pattern, with the target shape inset. "
              "The guard around the nib is there to keep rotor downwash from "
              "erasing the line as fast as it is drawn."),
             ("ss-1", SRC + "sandsketch-1.jpg", "Setup",
              "Sand table, lit from below through tempered glass."),
             ("ss-4", SRC + "sandsketch-4.jpg", "Pattern",
              "Trajectories beyond parametric curves: the interesting shapes are "
              "the ones a plotter would not choose."),
         ]),

    dict(slug="films", name="iPhone Films", kind="project", cover="fm-goose-1",
         tag="Short film",
         course=None, team=None, lead=None,
         blurb="Three short films shot and cut entirely on a phone, where the "
               "constraint is the point: no rig, no second take, no colourist.",
         pieces=[
             ("fm-goose-1", SRC + "film-goose-1.jpg", "A Goose's Life",
              "Fifty seconds at goose height, handheld, following rather than "
              "framing. Shooting from down there is the only choice that makes the "
              "bird the protagonist instead of the scenery, and it costs you every "
              "steady frame in the film."),
             ("fm-grocery-1", SRC + "film-grocery-1.jpg", "Grocery Shopping",
              "Eighteen seconds, and all of it is cut rhythm. No single shot in it "
              "is interesting; the order and the length of them is the piece. "
              "Fluorescent light, uncorrected, on purpose."),
             ("fm-torah-1", SRC + "film-torah-1.jpg", "Torah",
              "The longest of the three and the most still. The shots hold well "
              "past where a cut would normally come, and the holding is what turns "
              "them from coverage into observation. Available light throughout."),
         ]),

    # ------------------------------------------------------------- studio work
    # One category per folder in ../website/art. They used to be grouped by
    # medium, which merged five sports and two unrelated series into two
    # catch-all pages -- so a card routine sat inside "Illustration" and the
    # swim meet inside a category called "Photography" with the plumeria.
    # Titles are the ones her own site gave each piece wherever it gave one.
    dict(slug="canvas", name="Canvas", kind="studio", cover="cv-cover", group="Painting",
         tag="Paint",
         blurb="Canvas, mostly small, mostly evenings.",
         pieces=[
             ("cv-starry", ART + "canvas/img/starry.jpg", "Starry Night", ""),
             ("cv-mountain", ART + "canvas/img/mountain.jpg", "Bob Ross Mountains", ""),
             ("cv-girl", ART + "canvas/img/girl.jpg", "Girl", ""),
             ("cv-smoke", ART + "canvas/img/smoke.jpg", "Smoke", ""),
             ("cv-cat", ART + "canvas/img/cat.jpg", "Cat", ""),
             ("cv-cats", ART + "canvas/img/cats.jpg", "Cats", ""),
             ("cv-anya", ART + "canvas/img/anya.jpg", "Anya", ""),
             ("cv-pulp", ART + "canvas/img/pulp.jpg", "Pulp", ""),
             ("cv-soju", ART + "canvas/img/soju.jpg", "Soju", ""),
             ("cv-cover", ART + "canvas/img/cover.jpg", "Portrait, in leaves", ""),
         ]),

    dict(slug="pens", name="Pens", kind="studio", cover="pn-cover", group="Painting",
         tag="Ink and wash",
         blurb="Sketchbook-sized, one sitting each.",
         pieces=[
             ("pn-grapes", ART + "pens/img/grapes.jpg", "Grapes", ""),
             ("pn-avocado", ART + "pens/img/avocado.jpg", "Avocado", ""),
             ("pn-tangerine", ART + "pens/img/tangerine.jpg", "Tangerine", ""),
             ("pn-cake", ART + "pens/img/cake.jpg", "Cake", ""),
             ("pn-trees", ART + "pens/img/trees.jpg", "Trees", ""),
             ("pn-cover", ART + "pens/img/cover.jpg", "Grapes, in the sketchbook", ""),
         ]),

    dict(slug="sketches", name="Sketches", kind="studio", cover="sk-stiles", group="Drawing",
         tag="Graphite and ink",
         blurb="Sketchbook pages, none of them precious.",
         pieces=[
             ("sk-owl", ART + "sketches/img/owl.jpg", "Owl", ""),
             ("sk-dreamcatcher", ART + "sketches/img/dreamcatcher.jpg", "Dreamcatcher", ""),
             ("sk-arthur", ART + "sketches/img/arthur.jpg", "King Arthur", ""),
             ("sk-captain", ART + "sketches/img/captain.jpg", "Captain America", ""),
             ("sk-four", ART + "sketches/img/four.jpg", "Divergent - Four", ""),
             ("sk-divergent", ART + "sketches/img/divergent.png", "Divergent - Tris", ""),
             ("sk-dead", ART + "sketches/img/dead.jpg", "Sugar Skull", ""),
             ("sk-sterek", ART + "sketches/img/sterek.jpg", "Teen Wolf - Fanart", ""),
             ("sk-voidstiles", ART + "sketches/img/voidstiles.jpg", "Teen Wolf - Stiles", ""),
             ("sk-stiles", ART + "sketches/img/stiles.jpg", "Teen Wolf - Stiles, in text", ""),
         ]),

    dict(slug="hatch", name="Hatching", kind="studio", cover="ht-cover", group="Drawing",
         tag="Line and cross-hatch",
         blurb="Line work, where the only tone available is how close the "
               "lines are.",
         pieces=[
             ("ht-cherry", ART + "hatch/img/cherry.jpg", "Cherry Blossoms", ""),
             ("ht-cherry2", ART + "hatch/img/cherry2.jpg", "Cherry Blossoms, II", ""),
             ("ht-face", ART + "hatch/img/face.jpg", "Portrait study", ""),
             ("ht-face2", ART + "hatch/img/face2.jpg", "Portrait study, II", ""),
             ("ht-face3", ART + "hatch/img/face3.jpg", "Portrait study, III", ""),
             ("ht-face4", ART + "hatch/img/face4.jpg", "Portrait study, IV", ""),
             ("ht-yeji", ART + "hatch/img/yeji.jpg", "ITZY - Yeji", ""),
             ("ht-yeji2", ART + "hatch/img/yeji2.jpg", "ITZY - Yeji, II", ""),
             ("ht-yeji3", ART + "hatch/img/yeji3.jpg", "ITZY - Yeji, III", ""),
             ("ht-moonbin", ART + "hatch/img/moonbin.jpg", "Astro - Moonbin", ""),
             ("ht-moonbin2", ART + "hatch/img/moonbin2.jpg", "Astro - Moonbin, II", ""),
             ("ht-eunwoo", ART + "hatch/img/eunwoo.jpg", "Astro - Eunwoo", ""),
             ("ht-bang-chan", ART + "hatch/img/bang chan.jpg", "Stray Kids - Bang Chan", ""),
             ("ht-lee-know", ART + "hatch/img/lee know.jpg", "Stray Kids - Lee Know", ""),
             ("ht-changbin", ART + "hatch/img/changbin.jpg", "Stray Kids - Changbin", ""),
             ("ht-felix", ART + "hatch/img/felix.jpg", "Stray Kids - Felix", ""),
             ("ht-felix2", ART + "hatch/img/felix2.jpg", "Stray Kids - Felix, II", ""),
             ("ht-han-seojun", ART + "hatch/img/han seojun.jpg", "True Beauty - Han Seojun", ""),
             ("ht-cover", ART + "hatch/img/cover.jpg", "Full figure", ""),
         ]),

    dict(slug="still-life", name="Still Life", kind="studio", cover="sl-5", group="Photography",
         tag="Paper and light",
         blurb="Cut-paper flowers, built and then photographed.",
         pieces=[
             ("sl-2", ART + "still-life/img/2.jpg", "Paper flowers on a camera", ""),
             ("sl-1", ART + "still-life/img/1.jpg", "Paper flowers and a cabinet", ""),
             ("sl-3", ART + "still-life/img/3.jpg", "Paper flowers and a figure", ""),
             ("sl-4", ART + "still-life/img/4.jpg", "Cabinet, outdoors", ""),
             ("sl-5", ART + "still-life/img/5.jpg", "Paper flowers on a record player", ""),
         ]),

    dict(slug="football", name="Football", kind="studio", cover="fb-6", group="Photography",
         tag="Sport",
         blurb="Friday nights for the school paper, at a shutter speed that "
               "had to be right the first time.",
         pieces=[
             ("fb-3", ART + "football/img/3.jpg", "Contact, on the line", ""),
             ("fb-1", ART + "football/img/1.jpg", "Open field", ""),
             ("fb-2", ART + "football/img/2.jpg", "Night game", ""),
             ("fb-4", ART + "football/img/4.jpg", "The stiff-arm", ""),
             ("fb-5", ART + "football/img/5.jpg", "At the line", ""),
             ("fb-6", ART + "football/img/6.jpg", "Contested catch", ""),
             ("fb-7", ART + "football/img/7.jpg", "Downfield", ""),
             ("fb-8", ART + "football/img/8.jpg", "The handoff", ""),
             ("fb-9", ART + "football/img/9.jpg", "Block", ""),
             ("fb-10", ART + "football/img/10.jpg", "Tackle", ""),
         ]),

    dict(slug="cheer", name="Cheer", kind="studio", cover="ch-4", group="Photography",
         tag="Sport",
         blurb="Sideline and stunt, where the shot is decided before it "
               "happens.",
         pieces=[
             ("ch-4", ART + "cheer/img/4.jpg", "Stunt, peak height", ""),
             ("ch-1", ART + "cheer/img/1.jpg", "Sideline", ""),
             ("ch-2", ART + "cheer/img/2.jpg", "Toe touch", ""),
             ("ch-3", ART + "cheer/img/3.jpg", "Chant", ""),
             ("ch-5", ART + "cheer/img/5.jpg", "Pom, portrait", ""),
         ]),

    dict(slug="powderpuff", name="Powderpuff", kind="studio", cover="pp-3", group="Photography",
         tag="Sport",
         blurb="Flag football, and the same discipline as the Friday nights.",
         pieces=[
             ("pp-2", ART + "powderpuff/img/2.jpg", "Breakaway", ""),
             ("pp-1", ART + "powderpuff/img/1.jpg", "Flag pull", ""),
             ("pp-3", ART + "powderpuff/img/3.jpg", "The pitch", ""),
             ("pp-4", ART + "powderpuff/img/4.jpg", "Carrying", ""),
             ("pp-5", ART + "powderpuff/img/5.jpg", "Wide", ""),
         ]),

    dict(slug="swim", name="Swim", kind="studio", cover="sw-6", group="Photography",
         tag="Sport",
         blurb="A meet, where everything worth keeping happened inside a fifth "
               "of a second.",
         pieces=[
             ("sw-3", ART + "swim/img/3.jpg", "Butterfly", ""),
             ("sw-1", ART + "swim/img/1.jpg", "Freestyle", ""),
             ("sw-2", ART + "swim/img/2.jpg", "At the wall", ""),
             ("sw-4", ART + "swim/img/4.jpg", "Breathing", ""),
             ("sw-5", ART + "swim/img/5.jpg", "Backstroke", ""),
             ("sw-6", ART + "swim/img/6.jpg", "Down the lane", ""),
         ]),

    dict(slug="nature", name="Nature", kind="studio", cover="nt-3", group="Photography",
         tag="Plants",
         blurb="Plumeria and canopy. Plants photograph well for one reason, "
               "which is that they hold still.",
         pieces=[
             ("nt-1", ART + "nature/img/1.jpg", "Plumeria on stone", ""),
             ("nt-3", ART + "nature/img/3.jpg", "Plumeria, shade side", ""),
             ("nt-5", ART + "nature/img/5.jpg", "Pink plumeria", ""),
             ("nt-2", ART + "nature/img/2.jpg", "Canopy, into the sun", ""),
             ("nt-4", ART + "nature/img/4.jpg", "Leaf against the sky", ""),
         ]),

    dict(slug="fantasy", name="Fantasy", kind="studio", cover="fa-cover", group="Photography",
         tag="Portrait series",
         blurb="A staged series shot on a road and in a forest: confetti, "
               "planets, a lantern, one white dress.",
         pieces=[
             ("fa-4", ART + "fantasy/img/4.jpg", "Confetti", ""),
             ("fa-1", ART + "fantasy/img/1.jpg", "Bubbles", ""),
             ("fa-2", ART + "fantasy/img/2.jpg", "On the road", ""),
             ("fa-3", ART + "fantasy/img/3.jpg", "The box", ""),
             ("fa-5", ART + "fantasy/img/5.jpg", "Umbrella", ""),
             ("fa-6", ART + "fantasy/img/6.jpg", "Lantern", ""),
             ("fa-7", ART + "fantasy/img/7.jpg", "Planets", ""),
             ("fa-cover", ART + "fantasy/img/cover.jpg", "Confetti, close", ""),
         ]),

    dict(slug="flashcards", name="Flashcards", kind="studio", cover="fc-2", group="Photography",
         tag="Card stunt",
         blurb="The card routine, shot from the field.",
         pieces=[
             ("fc-3", ART + "flashcards/img/3.jpg", "Aerial", ""),
             ("fc-1", ART + "flashcards/img/1.jpg", "Formation", ""),
             ("fc-2", ART + "flashcards/img/2.jpg", "Kickline", ""),
             ("fc-4", ART + "flashcards/img/4.jpg", "The line", ""),
             ("fc-5", ART + "flashcards/img/5.jpg", "Flames", ""),
             ("fc-6", ART + "flashcards/img/6.jpg", "Waiting to go", ""),
             ("fc-7", ART + "flashcards/img/7.jpg", "Portrait, with cards", ""),
         ]),

    dict(slug="graphics", name="Graphics", kind="studio", cover="gr-cover", group="Drawing",
         tag="Vector",
         blurb="Flat colour, hard edges, and as few shapes as a likeness "
               "allows.",
         pieces=[
             ("gr-cover", ART + "graphics/img/cover.jpg", "Cover treatment", ""),
             ("gr-bruce", ART + "graphics/img/bruce.jpg", "Bruce Banner", ""),
             ("gr-chan", ART + "graphics/img/chan.jpg", "Stray Kids - Bang Chan", ""),
             ("gr-felix", ART + "graphics/img/felix.jpg", "Stray Kids - Felix", ""),
             ("gr-leeknow", ART + "graphics/img/leeknow.jpg", "Stray Kids - Lee Know", ""),
             ("gr-hwasa", ART + "graphics/img/hwasa.jpg", "Mamamoo - Hwasa", ""),
             ("gr-irene", ART + "graphics/img/irene.jpg", "Red Velvet - Irene", ""),
             ("gr-iu", ART + "graphics/img/iu.jpg", "IU", ""),
             ("gr-jimin", ART + "graphics/img/jimin.jpg", "BTS - Jimin", ""),
             ("gr-suga", ART + "graphics/img/suga.jpg", "BTS - Suga", ""),
             ("gr-v", ART + "graphics/img/v.jpg", "BTS - V", ""),
             ("gr-taeyong", ART + "graphics/img/taeyong.jpg", "NCT - Taeyong", ""),
             ("gr-natasha", ART + "graphics/img/natasha.jpg", "Natasha Romanoff", ""),
             ("gr-shelley", ART + "graphics/img/shelley.jpg", "Shelley Hennig", ""),
             ("gr-tom", ART + "graphics/img/tom.jpg", "Tom Hiddleston", ""),
             ("gr-me", ART + "graphics/img/me.jpg", "Me", ""),
         ]),

    dict(slug="yearbook", name="Yearbook", kind="studio", cover="yb-full3", group="Design",
         tag="Yearbook",
         blurb="Four years of a high school yearbook, which I edited. The cover is "
               "thermal-printed: the black silhouettes warm under your hand and clear "
               "to a collage of students underneath. The only work on this page that "
               "was actually work.",
         pieces=[
             ("yb-cover", ART + "yearbook/img/cover.png", "Cover", ""),
             ("yb-title", ART + "yearbook/img/title.jpg", "Title page", ""),
             ("yb-opening", ART + "yearbook/img/opening.jpg", "Opening spread", ""),
             ("yb-front-ensheet", ART + "yearbook/img/front ensheet.jpg", "Front endsheet", ""),
             ("yb-full", ART + "yearbook/img/full.jpg", "Feature spread", ""),
             ("yb-full2", ART + "yearbook/img/full2.jpg", "Feature spread, II", ""),
             ("yb-full3", ART + "yearbook/img/full3.jpg", "Feature spread, III", ""),
             ("yb-full4", ART + "yearbook/img/full4.jpg", "Feature spread, IV", ""),
             ("yb-full5", ART + "yearbook/img/full5.jpg", "Feature spread, V", ""),
             ("yb-feb", ART + "yearbook/img/feb.jpg", "February spread", ""),
             ("yb-element", ART + "yearbook/img/element.jpg", "Page element", ""),
             ("yb-element2", ART + "yearbook/img/element2.jpg", "Page element, II", ""),
             ("yb-element3", ART + "yearbook/img/element3.jpg", "Page element, III", ""),
             ("yb-closing", ART + "yearbook/img/closing.jpg", "Closing spread", ""),
             ("yb-back-endsheet", ART + "yearbook/img/back endsheet.jpg", "Back endsheet", ""),
         ]),
]
