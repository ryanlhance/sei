#!/usr/bin/env python3
"""Generates data.json for the SEI fit-map page (two roles, tabbed).
Single source of truth: edit this, run `python3 build_data.py`, and data.json
is rewritten. (Or just edit data.json directly — this is a convenience.)
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- Portfolio public URLs (piece -> hance.work case study) ----
PF = {
    "ev-blueprint-global":  "https://www.hance.work/Global-Enterprise-Level-Service-Blueprint-cd937db4cb344b318bae4c6d1e7ca9fa?pvs=25",
    "ev-service-blueprint": "https://www.hance.work/Local-Enterprise-Level-Service-Blueprint-74f9ecfa9f4a4873be1b909a7f5e37d8?pvs=25",
    "ev-bayer-journey":     "https://www.hance.work/Global-Journey-Mapping-Effort-228e643935ea43aab50ee95d8f56305f?pvs=25",
    "ev-eraf":              "https://www.hance.work/Systems-Flow-ERAF-Map-74cfa7e910564777a9883a55f066d4f9?pvs=25",
    "ev-ai-playbook":       "https://www.hance.work/Generative-A-I-Playbook-bb68ca8c80d840e5be083136a0b88f92?pvs=25",
    "ev-playbooks":         "https://www.hance.work/Platform-Design-Playbook-838ea8da681f4577bce28f0ea7e30b67?pvs=25",
}

# ---- Evidence (title + text shown to the reader; shared across both roles) ----
evidence = {
  # --- change management + adoption ---
  "ev-adoption": {"title": "2% to 26% adoption in two months", "text": "Took a Fortune 500's internal AI platform from 2% to 26% adoption in two months by building the playbook and training that got people to actually use it — before large-scale ChatGPT adoption, when 98% of licensed users couldn't operate the tool."},
  "ev-ai-playbook": {"title": "AI playbook shipped in 20+ languages", "text": "Authored Bayer's AI Strategy Playbook and led its global dissemination in 20+ languages to thousands of internal users across business, engineering, design, and HR — training entire sections of the business from Indonesia to Brazil in a single quarter."},
  "ev-franchise": {"title": "Nationwide restructuring, zero layoffs", "text": "Led a nationwide counseling franchise through restructuring across multiple states — ethnographic interviews with corporate and franchisees, comparative org charts, and the Franchise Criteria Canvas that gave corporate a clear standard for franchisee decisions. Locations closed, folded, and opened, and headquarters reorganized without a single layoff."},
  "ev-training-camp": {"title": "67% retention lift from one redesign", "text": "Redesigned a decade-old staff training program at one of the country's largest residential summer camps (1,500 people a summer) using Self-Determination Theory as the leadership framework — driving a 67% year-over-year staff retention increase while leading trainings throughout the season."},

  # --- prototyping + early tech ---
  "ev-agentic-personas": {"title": "Agentic AI before Copilot existed", "text": "Pioneered an agentic persona service at Bayer — AI models of users our design team couldn't otherwise reach, wired into Microsoft Teams before commercial AI integrations existed for the company's stack. The workflow produced high fidelity user representations in under 15 minutes, validated by SMEs above 80% accuracy, and significantly reduced UAT failures across the teams that used them."},
  "ev-bananas": {"title": "Prototyped what the Bananas scaled", "text": "First hire on the Savannah Bananas entertainment team during the alpha run: designed and executed the prototype Fans First experiences the company standardized and scaled to global fame — contributing to a 500% surge in social awareness and the first sold-out season of 250,000 fans."},
  "ev-rd-lab": {"title": "A constantly running R&D lab", "text": "My personal life is a constantly running R&D lab — I've been ramping on a new technology at least once a quarter since high school, and my current operating system pairs agentic AI workflows with a digital brain to extend what I can do. I love unfamiliar domains and emerging tech."},
  "ev-toolstack": {"title": "Fluent across the tool stacks", "text": "I've built project management systems end-to-end in ClickUp, Monday.com, Notion, Aha!, Motion, and Claude, and regularly self-train on unfamiliar enterprise software to the depth of being able to evaluate vendor fit — proven across startups, the entertainment industry, and the Fortune 500 level."},

  # --- product ---
  "ev-site-rebuild": {"title": "35% more opportunities surfaced", "text": "UX Lead for the Farmer experience on Bayer's end-to-end customer site rebuild: refined backlogs and drove product decisions by aligning hundreds of technical stories, research discoveries, and business goals to user needs — a 35% increase in product and service opportunities across the NA and LATAM builds — then led User Acceptance Testing across the North American user base."},
  "ev-eaas": {"title": "Pioneered a new revenue line", "text": "At a university logistics startup, I pioneered an education-as-a-service revenue line and owned it end to end — primary market research with residential life leaders, curriculum design, offer design, and pre-launch partnerships — architecting a B2B2C service structure spanning parents, students, and seven partner universities."},
  "ev-agsage-bizdev": {"title": "Landed clients from day one", "text": "Built my own leadership development practice from scratch — structured the offer, pricing, and go-to-market to land clients from day one, and led the business development that kept it running for three years with consistent five-figure engagements."},
  "ev-cdp": {"title": "Anchored an enterprise vendor selection", "text": "Drove the research and strategy that anchored Bayer's selection of its enterprise Customer Data Platform vendor, then structured the governance team that integrated it — translating between what the business needed, what the technology could do, and what the users would actually adopt."},

  # --- delivery leadership ---
  "ev-delta-pm": {"title": "Eight countries, nine disciplines, one team", "text": "Project Manager on a Delta Air Lines engagement: led a team from eight countries and nine disciplines, owned budget, timeline, and resources, and was the primary contact between client and team — presenting regularly in Delta's corporate rooms while translating business needs to the creative team in the studio."},
  "ev-blueprint-global": {"title": "A 20,000-point global blueprint", "text": "Mapped the Farmer persona inside Bayer's global enterprise service blueprint — 20,000+ data points across five countries and hundreds of teams — connecting tech, personas, and interactions across every customer platform to surface redundancies and gaps."},
  "ev-bayer-journey": {"title": "2,250 journey points across 27 teams", "text": "Facilitated a global journey mapping effort spanning North America, Europe, and Asia-Pacific — 2,250 journey points across 27 teams — that cut environmental toxin risk 70% and raised workplace safety 30% within two quarters."},
  "ev-film-producer": {"title": "Six productions at once, on time, on budget", "text": "Owned film and TV productions end to end as the client's point of contact, delivering on time and on budget while running an average of six concurrent productions, peaking at ten to twelve."},
  "ev-highstakes": {"title": "Million-dollar days were routine", "text": "As a film producer and assistant director, the responsibility of million-dollar days fell entirely on me — the plan, the crew, and the timeline all had to land correctly, every day. That was the normal rhythm of the job for six years."},
  "ev-nexus": {"title": "Decision nexus for 40 productions", "text": "Was the on-set nexus for information, prioritization, and decision-making across 40 productions, coordinating thousands of crew, cast, and vendors live — and de-escalating whatever the day threw at us."},
  "ev-ad-replan": {"title": "Replanning was the day job", "text": "As an assistant director, my job was building the operational plan that made the director's vision possible despite budget, time, and resource constraints — mapping crew, cast, and equipment for hundreds of scenes across 40 productions, then replanning live when the day changed. The day always changed."},
  "ev-budgets": {"title": "Budgets were never someone else's job", "text": "Owned client communication, budgets, timelines, and resource management from film and TV to startups and Fortune 500 engagements — an on-time, on-budget record built in a world where a blown day meant real money."},
  "ev-13yrs": {"title": "13 years of client-facing delivery", "text": "Six years running client work in film and TV, then seven more of client implementation, consulting, and program management across startups, nationwide franchises, Delta Air Lines, and Bayer."},

  # --- business transformation + results ---
  "ev-dryland-scale": {"title": "Built a startup's operating system", "text": "Chief of staff and co-founder who scaled Dryland, a construction-science startup, from one client to a profitable exit — building the operating system as we grew: playbooks, hiring funnel, PM stack, and the org redesign that let the CEO focus on the highest leverage work."},
  "ev-org-redesign": {"title": "Doubled revenue in three months", "text": "Redesigned my startup's organizational structure to detach the CEO from daily hands-on work — that doubled revenue and quadrupled headcount in three months, and the company later exited via a profitable sale."},
  "ev-eraf": {"title": "Kept the employees who were leaving", "text": "Crafted an ERAF map of 100+ interaction points after ethnographic research showed employees ready to quit over \"bad communication\" actually misunderstood the larger business model. Helping siloed teams see their role in the bigger system kept them — the problem was never communication."},
  "ev-playbooks": {"title": "I uncover and write the playbooks", "text": "An operations playbook that cut resource needs 60%, a startup playbook library that lifted efficiency 80% and removed the CEO from lower-level decisions, and a Fortune 500 AI strategy playbook shipped in 20+ languages."},
  "ev-ops-reform": {"title": "A 60% resource reduction", "text": "Reformed the operational systems and org structure at a university logistics startup — a 100,000 square foot warehouse, a 20-truck fleet, and 200+ seasonal staff — then documented the new ways of working into the playbook that propagated across the other campuses. The reform drove a 60% resource reduction."},
  "ev-system-not-symptom": {"title": "I solve the system, not the symptom", "text": "I will spend an entire day on a single problem — solving the system instead of the symptom — because I know it will save days of time in the future."},
  "ev-parallel": {"title": "Bayer 9-to-5, startup 5-to-9", "text": "Built a startup to a profitable exit while working Bayer full time — Bayer was my 9-to-5, the startup was my 5-to-9. Two demanding roles, years of switching between them, and neither one dropped."},

  # --- design thinking + facilitation ---
  "ev-facilitation": {"title": "Hundreds of workshops, 5 to 150 people", "text": "Facilitated hundreds of design thinking workshops from 5 to 150 people, maturing design thinking across a Fortune 500 — and was selected by Miro as the sole Enterprise Advocate for all of Bayer, a company of ~100,000 people."},
  "ev-scad": {"title": "An MBA crossed with service design", "text": "M.A. in Creative Business Leadership from SCAD's De Sole School of Business Innovation — essentially an MBA crossbred with service design, built for intrapreneurship and using design thinking to influence decision making. My B.F.A. is from SCAD too, in the business of film and television."},
  "ev-decision-tools": {"title": "A framework for every situation", "text": "I have a strategic framework or model for every situation — and if I don't, I design one in the moment so teams can communicate and uncover information clearly. The Franchise Criteria Canvas, my startup's playbook library, and the prioritization frameworks my Delta team ran on all started that way."},
  "ev-service-blueprint": {"title": "Blueprints from startup to Fortune 500", "text": "Built service blueprints at every scale: Bayer's 20,000+ point global enterprise blueprint, and the 450-point blueprint of my own startup that became the information architecture for executive decision making."},

  # --- communication + people ---
  "ev-writing": {"title": "20–50 pages a week for a decade", "text": "A decade writing 20 to 50 pages a week — project documentation, strategic recommendations, status reports, decision logs, and client summaries that ship without needing edits."},
  "ev-translator": {"title": "Translator between business, design, and engineering", "text": "Fluent in business, design, and engineering languages: translating business jargon to design requirements, engineering capabilities to business possibilities, and design visions to engineering roadmaps."},
  "ev-exec-alignment": {"title": "Sold Bayer execs on an AI build", "text": "Developed an agentic AI experience at Bayer and sold it internally to senior executives: months of workshops, demos, and one-on-one influencing, navigating the political complexity of enterprise decision making before getting the greenlight to build."},
  "ev-strengths-coach": {"title": "Gallup-certified Strengths Coach", "text": "Gallup-certified Strengths Coach trained in behavior and relationship psychology; taught empathy and emotional intelligence professionally through years of leadership development — reading the room is a trained skill, not a personality trait."},
  "ev-scrumboard": {"title": "Wrote the scrum board nobody had", "text": "Built out and wrote all the stories for a scrum board for a legacy Bayer platform team that had no user stories or change tracking — bringing iterative ways of working to a team that had none."},
  "ev-team-builder": {"title": "Teams that stay: 95% crew retention", "text": "I build teams that stay: roughly 95% crew retention across six years in film, a 67% year-over-year retention lift on a 250-person camp staff, and a startup hiring funnel that delivered 100% season-long retention of the hires who came through it."},
  "ev-hiring": {"title": "Hundreds of first-round interviews", "text": "Built and ran my startup's hiring funnel across three candidate markets — scaling the team from 3 to 15 in a single season and 30–40 hires across seasons, conducting hundreds of first round interviews and designing a paid multi-day field test that drove 100% season-long retention of everyone who completed it."},

  # --- range ---
  "ev-industries": {"title": "Ten industries, hundreds of personas", "text": "Experience across 10+ industries and hundreds of niche personas across unrelated service verticals — film and TV, agriculture, counseling, fitness, hospitality, education, logistics, sports entertainment. The service design and operations skillset transfers to any business domain."},
}
# attach portfolio links
for k, url in PF.items():
    evidence[k]["link"] = url

def ph(pid, text, ev):
    return {"id": pid, "text": text, "evidence": ev}

# =====================================================================
# ROLE 1 — Concept to Delivery Consultant
# =====================================================================
ctd_prose = [
  {"type": "h2", "text": "WHO WE LOOK FOR"},
  {"type": "p", "segments": [
    "An SEI-er is a ",
    ph("p-communicator", "master communicator and active listener who understands how to navigate an audience",
       ["ev-facilitation", "ev-writing", "ev-strengths-coach"]),
    ". Self-aware, almost to a fault, SEI-ers keenly understand how to ",
    ph("p-adjust", "adjust their support and problem solving based on the situation",
       ["ev-strengths-coach", "ev-translator"]),
    ". Following a logical, fact-based approach, SEI-ers possess the superior ability to ",
    ph("p-correlations", "see correlations others may not, ask the right questions and drive solutions",
       ["ev-eraf", "ev-system-not-symptom", "ev-service-blueprint"]),
    "."
  ]},
  {"type": "p", "segments": [
    "As super-connectors, they ",
    ph("p-connector", "connect not only people, but data, trends and experiences",
       ["ev-blueprint-global", "ev-bayer-journey", "ev-translator"]),
    ". Mature, humble, and genuine, SEI-ers frequently go above and beyond for both their clients and their colleagues. SEI-ers are ethical and trustworthy individuals who ",
    ph("p-follow-through", "consistently and repeatedly follow through",
       ["ev-budgets", "ev-film-producer"]),
    ", and hold true to their values in difficult situations. SEI-ers have an ",
    ph("p-curiosity", "insatiable curiosity and love to learn",
       ["ev-rd-lab", "ev-scad"]),
    ". These individuals are commonly ",
    ph("p-tech-savvy", "tech savvy and early adopters",
       ["ev-agentic-personas", "ev-rd-lab", "ev-toolstack"]),
    ". Their ",
    ph("p-infectious", "passion for learning is infectious and excites others",
       ["ev-adoption", "ev-facilitation"]),
    ". As every project is different, an SEI-er must be ",
    ph("p-adaptable", "adaptable and comfortable with unexpected situations",
       ["ev-ad-replan", "ev-nexus", "ev-industries"]),
    ". SEI-ers define ambition differently. They are authentic, low-maintenance individuals who truly enjoy one another- they like to hang out with colleagues outside of work, collaborate and hold one another accountable. SEI-ers enjoy working with genuine, thoughtful folks who want to steer clear of the traditional grind and share the joy of day-to-day life and activities with colleagues, friends, and family."
  ]},

  {"type": "h2", "text": "WHAT WE DO"},
  {"type": "p", "segments": [
    "Our Concept to Delivery consultants work with clients to ",
    ph("p-ideas-to-reality", "turn ideas into reality",
       ["ev-bananas", "ev-agentic-personas", "ev-eaas"]),
    ". No matter the size or complexity, our consultants are skilled at ",
    ph("p-concepts-to-results", "helping clients transform concepts into tangible, impactful results",
       ["ev-dryland-scale", "ev-playbooks", "ev-franchise"]),
    ". We do this by utilizing innovative approaches to design and deliver engaging, value-focused solutions. Our Concept to Delivery approach demands a ",
    ph("p-people-centric", "people-centric mindset",
       ["ev-scad", "ev-bayer-journey"]),
    ", fail-fast mentality, ",
    ph("p-nimble", "nimble decision making",
       ["ev-nexus", "ev-highstakes"]),
    ", steadfast innovation, and engaging ",
    ph("p-cross-functional", "cross-functional collaboration",
       ["ev-delta-pm", "ev-translator"]),
    "."
  ]},
  {"type": "p", "segments": [
    "We work across a ",
    ph("p-industries", "variety of industries and business functions",
       ["ev-industries", "ev-13yrs"]),
    " and provide depth and breadth of experience across numerous strategic capabilities."
  ]},
  {"type": "p", "segments": ["We are actively looking for professionals in the following areas:"]},
  {"type": "li", "segments": [
     ph("p-design-thinking", "Design Thinking",
        ["ev-facilitation", "ev-scad", "ev-decision-tools"])]},
  {"type": "li", "segments": [
     ph("p-rapid-prototyping", "Rapid Prototyping",
        ["ev-agentic-personas", "ev-bananas"])]},
  {"type": "li", "segments": [
     ph("p-product-management", "Product Management",
        ["ev-site-rebuild", "ev-eaas", "ev-delta-pm"])]},
  {"type": "li", "segments": [
     ph("p-solution-delivery", "Solution Delivery",
        ["ev-film-producer", "ev-budgets", "ev-13yrs"])]},
  {"type": "li", "segments": [
     ph("p-change-management", "Change Management",
        ["ev-adoption", "ev-franchise", "ev-training-camp"])]},
  {"type": "p", "segments": ["The ideal candidate’s experience will include elements of the following:"]},
  {"type": "li", "segments": [
    "Providing ",
    ph("p-delivery-leadership", "delivery leadership, and executing on large scale, highly complex initiatives",
       ["ev-blueprint-global", "ev-delta-pm", "ev-film-producer"]),
    " by ",
    ph("p-aligning-stakeholders", "aligning key stakeholders, working across various levels of the organization",
       ["ev-exec-alignment", "ev-translator"]),
    ", and ",
    ph("p-business-results", "driving business results",
       ["ev-org-redesign", "ev-site-rebuild"]),
    ]},
  {"type": "li", "segments": [
    "Leveraging ",
    ph("p-dt-methods", "design thinking methods to facilitate, articulate, and align on problem definition and solution design",
       ["ev-facilitation", "ev-franchise", "ev-decision-tools"]),
    " among business leads, relevant stakeholders, and oftentimes customers."
    ]},
  {"type": "li", "segments": [
    "Developing and adding further detail and fidelity to ",
    ph("p-prototyping", "envisioned solutions through prototyping",
       ["ev-agentic-personas", "ev-bananas"]),
    ", often working with the same stakeholders, by leveraging an ",
    ph("p-agile-feedback", "agile approach towards feedback",
       ["ev-scrumboard", "ev-site-rebuild"]),
    " to deliver quickly while meeting product goals."
    ]},
  {"type": "li", "segments": [
    "Managing the ",
    ph("p-product-lifecycle", "product lifecycle (e.g., vision, roadmap, budget, pricing, development)",
       ["ev-eaas", "ev-site-rebuild", "ev-agsage-bizdev"]),
    ", often by leveraging the collective functions of an enterprise, to deliver solutions that maximize value and minimize time to delivery."
    ]},
  {"type": "li", "segments": [
    "Enabling organizations and its people to ",
    ph("p-adopt-champion", "embrace, adopt, and champion new solutions",
       ["ev-adoption", "ev-ai-playbook", "ev-eraf"]),
    " by leveraging effective ",
    ph("p-change-strategies", "change management strategies and methodologies",
       ["ev-training-camp", "ev-franchise"]),
    ]},
  {"type": "p", "segments": [
    "A career at SEI extends well beyond providing great service and thought leadership to our clients. Everyone takes an active role in building and managing our business, in an environment that runs counter to traditional consulting firms. Our consultants have a “seat at the table” and contribute to growing our business in ways that align to their interests such as growing ",
    ph("p-bizdev", "business development opportunities",
       ["ev-agsage-bizdev"]),
    ", ",
    ph("p-interviews", "conducting interviews to support our hiring process",
       ["ev-hiring"]),
    ", managing internal initiatives that build our brand or ",
    ph("p-trainings", "organizing trainings to share what you know",
       ["ev-ai-playbook", "ev-training-camp"]),
    " with your colleagues. There is no telling what an SEI Consultant will be asked to do on a day-to-day basis – we ",
    ph("p-job-done", "do what it takes to get the job done",
       ["ev-parallel", "ev-nexus"]),
    "."
  ]},

  {"type": "h2", "text": "QUALIFICATIONS"},
  {"type": "h3", "text": "Required"},
  {"type": "li", "segments": ["Alignment to our core values: Excellence, Participation, Integrity, and Collaboration"]},
  {"type": "li", "segments": ["Hungry, Humble, Smart"]},
  {"type": "li", "segments": [
     ph("p-acumen", "Demonstrated business and technology acumen",
        ["ev-cdp", "ev-translator", "ev-scad"])]},
  {"type": "li", "segments": [
     ph("p-comms", "Strong written and verbal communication skills",
        ["ev-writing", "ev-facilitation"])]},
  {"type": "li", "segments": [
     ph("p-real-problems", "Understanding and experience solving real business problems",
        ["ev-eraf", "ev-franchise", "ev-org-redesign"])]},
  {"type": "li", "segments": [
     ph("p-results", "Proven track record of delivering results",
        ["ev-org-redesign", "ev-adoption", "ev-site-rebuild"])]},
  {"type": "li", "segments": [
     ph("p-team", "Experience working with and/or leading a team",
        ["ev-team-builder", "ev-delta-pm", "ev-hiring"])]},
  {"type": "li", "segments": [
     ph("p-across", "Ability to work across industries, roles, functions & technologies",
        ["ev-industries", "ev-toolstack"])]},
  {"type": "li", "segments": ["Authorization for permanent employment in the United States (this position is not eligible for immigration sponsorship)"]},

  {"type": "h3", "text": "Preferred"},
  {"type": "li", "segments": [
     ph("p-degree", "Bachelor’s degree",
        ["ev-scad"])]},
  {"type": "li", "segments": [
     ph("p-years", "8+ years professional experience",
        ["ev-13yrs"])]},
  {"type": "li", "segments": [
     ph("p-offerings", "Experience across our service offerings",
        ["ev-facilitation", "ev-agentic-personas", "ev-eaas", "ev-film-producer", "ev-adoption"])]},

]

# =====================================================================
# ROLE 2 — Strategy and Operations Consultant
# =====================================================================
so_prose = [
  {"type": "h2", "text": "WHO WE LOOK FOR"},
  {"type": "p", "segments": [
    "An SEI-er is a ",
    ph("so-communicator", "master communicator and active listener who understands how to navigate an audience",
       ["ev-facilitation", "ev-writing", "ev-strengths-coach"]),
    ". Self-aware, almost to a fault, SEI-ers keenly understand how to ",
    ph("so-adjust", "adjust their support and problem solving based on the situation",
       ["ev-strengths-coach", "ev-translator"]),
    ". Following a logical, fact-based approach, SEI-ers possess the superior ability to ",
    ph("so-correlations", "see correlations others may not, ask the right questions and drive solutions",
       ["ev-eraf", "ev-system-not-symptom", "ev-service-blueprint"]),
    "."
  ]},
  {"type": "p", "segments": [
    "As super-connectors, they ",
    ph("so-connector", "connect not only people, but data, trends and experiences",
       ["ev-blueprint-global", "ev-bayer-journey", "ev-translator"]),
    ". Mature, humble, and genuine, SEI-ers frequently go above and beyond for both their clients and their colleagues. SEI-ers are ethical and trustworthy individuals who ",
    ph("so-follow-through", "consistently and repeatedly follow through",
       ["ev-budgets", "ev-film-producer"]),
    ", and hold true to their values in difficult situations. SEI-ers have an ",
    ph("so-curiosity", "insatiable curiosity and love to learn",
       ["ev-rd-lab", "ev-scad"]),
    ". These individuals are commonly ",
    ph("so-tech-savvy", "tech savvy and early adopters",
       ["ev-agentic-personas", "ev-rd-lab", "ev-toolstack"]),
    ". Their ",
    ph("so-infectious", "passion for learning is infectious and excites others",
       ["ev-adoption", "ev-facilitation"]),
    ". As every project is different, an SEI-er must be ",
    ph("so-adaptable", "adaptable and comfortable with unexpected situations",
       ["ev-ad-replan", "ev-nexus", "ev-industries"]),
    ". SEI-ers define ambition differently. They are authentic, low-maintenance individuals who truly enjoy one another- they like to hang out with colleagues outside of work, collaborate and hold one another accountable. SEI-ers enjoy working with genuine, thoughtful folks who want to steer clear of the traditional grind and share the joy of day-to-day life and activities with colleagues, friends, and family."
  ]},

  {"type": "h2", "text": "WHAT WE DO"},
  {"type": "p", "segments": [
    "Our Strategy and Operations consultants work with clients at all levels of the organization, ",
    ph("so-all-levels", "from the C-suite to the shop floor",
       ["ev-exec-alignment", "ev-nexus"]),
    ", helping them to ",
    ph("so-strategic-initiatives", "deliver on their most strategic initiatives",
       ["ev-blueprint-global", "ev-delta-pm"]),
    ". We’re known for ",
    ph("so-data-driven", "making realistic, data-driven decisions that deliver value in tangible ways",
       ["ev-service-blueprint", "ev-decision-tools"]),
    " to our clients. Our clients ask for us on projects that require a ",
    ph("so-combination", "superior combination of technical and business capabilities, people and management skills, and a collaborative mindset",
       ["ev-translator", "ev-team-builder", "ev-parallel"]),
    ". We excel in ",
    ph("so-actionable", "understanding complex programs and strategic initiatives and breaking them into actionable pieces",
       ["ev-ad-replan", "ev-playbooks"]),
    "."
  ]},
  {"type": "p", "segments": [
    "We work across a ",
    ph("so-industries", "variety of industries and business functions",
       ["ev-industries", "ev-13yrs"]),
    " and provide depth and breadth of experience across a set of core capabilities:"
  ]},
  {"type": "li", "segments": [
     {"b": "Strategy and Execution – "},
     ph("so-strategy-execution", "Leverage quantitative and qualitative insights to inform strategic alignment, develop roadmaps, and define prioritization",
        ["ev-site-rebuild", "ev-cdp", "ev-decision-tools"])]},
  {"type": "li", "segments": [
     {"b": "Process Improvement - "},
     ph("so-process-improvement", "Work with decision-makers to understand organizational goals, process gaps, and make and implement recommendations",
        ["ev-ops-reform", "ev-bayer-journey"])]},
  {"type": "li", "segments": [
     {"b": "Operational Transformation - "},
     ph("so-op-transformation", "Leverage data-based strategies to define organizational goals, identify performance gaps, advise on closing gaps, predict future demand, and lead transformation initiatives",
        ["ev-org-redesign", "ev-dryland-scale"])]},
  {"type": "li", "segments": [
     {"b": "Organizational Design – "},
     ph("so-org-design", "Ensure effective alignment of skills and responsibilities, spans and layers, governance, and communication across an organization",
        ["ev-franchise", "ev-org-redesign", "ev-eraf"])]},
  {"type": "li", "segments": [
     {"b": "Mergers and Acquisitions – "},
     "work with organizations to identify, plan, and lead post M&A integration activities."]},
  {"type": "p", "segments": [
    "We ",
    ph("so-close-gaps", "close gaps to create unparalleled opportunities for innovation",
       ["ev-site-rebuild", "ev-blueprint-global"]),
    ". We ",
    ph("so-blueprints", "develop and execute strategic blueprints",
       ["ev-service-blueprint", "ev-blueprint-global"]),
    ", ",
    ph("so-transformations", "facilitate, and lead large-scale transformations",
       ["ev-franchise", "ev-bayer-journey"]),
    ", and ",
    ph("so-op-effectiveness", "increase operational effectiveness",
       ["ev-playbooks", "ev-ops-reform"]),
    " with an approach centered on agility and collaboration. Our goal is simple: to position our clients as leaders within their sectors."
  ]},
  {"type": "p", "segments": ["The ideal candidate’s experience may include but is not limited to the following:"]},
  {"type": "li", "segments": [
    "Have experience ",
    ph("so-real-problems-li", "understanding and solving real business problems",
       ["ev-eraf", "ev-franchise"]),
    ]},
  {"type": "li", "segments": [
    "Have experience with ",
    ph("so-c-suite", "presenting business case and strategy to the C-Suite",
       ["ev-exec-alignment", "ev-delta-pm"]),
    ]},
  {"type": "li", "segments": [
    "Have experience in ",
    ph("so-assessments", "conducting assessments in different areas that allow organizations a map of where they are and where they may want to go",
       ["ev-service-blueprint", "ev-bayer-journey", "ev-eraf"]),
    ]},
  {"type": "li", "segments": [
    ph("so-root-causes", "Identifying and addressing root causes of operational and strategic issues in organizational and governance structures",
       ["ev-eraf", "ev-system-not-symptom", "ev-org-redesign"]),
    "."]},
  {"type": "li", "segments": [
    ph("so-process-initiative", "Led a process improvement initiative, facilitating Current State and Future State documentation, performing a Gap Analysis and creating a plan to achieve desired Future State vision",
       ["ev-ops-reform", "ev-franchise", "ev-blueprint-global"]),
    "."]},
  {"type": "li", "segments": [
    "Been a part of standing up a post merger Integration Management Office and worked leading activities related to 2 organizations coming together"]},
  {"type": "p", "segments": [
    "A career at SEI extends well beyond providing great service and thought leadership to our clients. Everyone takes an active role in building and managing our business, in an environment that runs counter to traditional consulting firms. Our consultants have a “seat at the table” and contribute to growing our business in ways that align to their interests such as growing ",
    ph("so-bizdev", "business development opportunities",
       ["ev-agsage-bizdev"]),
    ", ",
    ph("so-interviews", "conducting interviews to support our hiring process",
       ["ev-hiring"]),
    ", managing internal initiatives that build our brand or ",
    ph("so-trainings", "organizing trainings to share what you know",
       ["ev-ai-playbook", "ev-training-camp"]),
    " with your colleagues. There is no telling what an SEI Consultant will be asked to do on a day-to-day basis – we ",
    ph("so-job-done", "do what it takes to get the job done",
       ["ev-parallel", "ev-nexus"]),
    "."
  ]},

  {"type": "h2", "text": "QUALIFICATIONS"},
  {"type": "h3", "text": "Required"},
  {"type": "li", "segments": ["Alignment to our core values: Excellence, Participation, Integrity, and Collaboration"]},
  {"type": "li", "segments": ["Hungry, Humble, Smart"]},
  {"type": "li", "segments": [
     ph("so-acumen", "Demonstrated business and technology acumen",
        ["ev-cdp", "ev-translator", "ev-scad"])]},
  {"type": "li", "segments": [
     ph("so-comms", "Strong written and verbal communication skills",
        ["ev-writing", "ev-facilitation"])]},
  {"type": "li", "segments": [
     ph("so-real-problems", "Understanding and experience solving real business problems",
        ["ev-eraf", "ev-franchise", "ev-org-redesign"])]},
  {"type": "li", "segments": [
     ph("so-results", "Proven track record of delivering results",
        ["ev-org-redesign", "ev-adoption", "ev-site-rebuild"])]},
  {"type": "li", "segments": [
     ph("so-team", "Experience working with and/or leading a team",
        ["ev-team-builder", "ev-delta-pm", "ev-hiring"])]},
  {"type": "li", "segments": [
     ph("so-across", "Ability to work across industries, roles, functions & technologies",
        ["ev-industries", "ev-toolstack"])]},
  {"type": "li", "segments": ["Authorization for permanent employment in the United States (this position is not eligible for immigration sponsorship)"]},

  {"type": "h3", "text": "Preferred"},
  {"type": "li", "segments": [
     ph("so-degree", "Bachelor’s degree",
        ["ev-scad"])]},
  {"type": "li", "segments": [
     ph("so-years", "8+ years professional experience",
        ["ev-13yrs"])]},
  {"type": "li", "segments": [
     ph("so-offerings", "Experience across our service offerings",
        ["ev-decision-tools", "ev-ops-reform", "ev-org-redesign", "ev-service-blueprint"])]},

]

LEDE = "These are selected notes and resume points from Ryan Hance's career experience mapped to SEI's actual job descriptions. Both Boston roles are mapped — use the tabs above to switch between them."

data = {
  "meta": {
    "candidate": "Ryan Hance",
    "portfolio": "https://www.hance.work/",
    "note": "Pure renderer input. Edit copy here (or in build_data.py). Each highlighted phrase carries the evidence ids that back it; evidence is a shared dictionary. Each entry in roles is one tab."
  },
  "roles": [
    {
      "id": "ctd",
      "tab_label": "Concept to Delivery",
      "job": {
        "company": "SEI",
        "role": "Concept to Delivery Consultant",
        "employment": "",
        "location": "Boston, Massachusetts",
        "url": "https://www.sei.com/careers/open-positions/job-position-detail/?gh_jid=4087807005",
        "tab_title": "Ryan Hance · Fit Map",
        "candidate_kicker": "Ryan Hance · Fit Map",
        "candidate_lede": LEDE,
        "candidate_stat": "Hover over any underlined phrase and select it to see Ryan's experience related to the ask.",
      },
      "jd_prose": ctd_prose,
    },
    {
      "id": "so",
      "tab_label": "Strategy and Operations",
      "job": {
        "company": "SEI",
        "role": "Strategy and Operations Consultant",
        "employment": "",
        "location": "Boston, Massachusetts",
        "url": "https://www.sei.com/careers/open-positions/job-position-detail/?gh_jid=4087819005",
        "tab_title": "Ryan Hance · Fit Map",
        "candidate_kicker": "Ryan Hance · Fit Map",
        "candidate_lede": LEDE,
        "candidate_stat": "Hover over any underlined phrase and select it to see Ryan's experience related to the ask.",
      },
      "jd_prose": so_prose,
    },
  ],
  "evidence": evidence,
}

out = os.path.join(HERE, "data.json")
with open(out, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# quick self-check: every referenced evidence id exists; phrase ids unique across roles
ids = set()
phrase_ids = []
for role in data["roles"]:
    for b in role["jd_prose"]:
        for seg in b.get("segments", []):
            if isinstance(seg, dict) and "evidence" in seg:
                ids.update(seg["evidence"])
                phrase_ids.append(seg["id"])
missing = [i for i in ids if i not in evidence]
dupes = sorted({p for p in phrase_ids if phrase_ids.count(p) > 1})
print("Wrote", out)
for role in data["roles"]:
    n = sum(1 for b in role["jd_prose"] for s in b.get("segments", []) if isinstance(s, dict) and "id" in s)
    print(f"  {role['id']}: {n} phrases")
print("evidence items:", len(evidence))
print("missing evidence refs:", missing or "none")
print("duplicate phrase ids:", dupes or "none")
unused = [k for k in evidence if k not in ids]
print("unused evidence:", unused or "none")
