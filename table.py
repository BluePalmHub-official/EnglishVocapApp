import sqlite3
import os
import sys


def get_db_path():
    """Get database path, works for dev and PyInstaller"""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        application_path = os.path.dirname(sys.executable)
    else:
        # Running as script
        application_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(application_path, 'vocabulary.db')


class VocabDatabase:
    def __init__(self):
        self.db_path = get_db_path()
        self.conn = None
        self.create_tables()
        self.populate_initial_data()  # Auto-populate on initialization

    def connect(self):
        """Create database connection"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Access columns by name
        return self.conn

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

    def create_tables(self):
        """Create all necessary tables"""
        conn = self.connect()
        cursor = conn.cursor()

        # Words table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT NOT NULL,
                pos TEXT NOT NULL,
                definition TEXT NOT NULL,
                list_number INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # User profiles table (for future use)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Quiz history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quiz_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                quiz_type TEXT NOT NULL,
                lists_used TEXT NOT NULL,
                score INTEGER NOT NULL,
                total_questions INTEGER NOT NULL,
                percentage REAL NOT NULL,
                date_taken TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')

        # Quiz details table (individual question results)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quiz_details (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quiz_id INTEGER NOT NULL,
                word_id INTEGER NOT NULL,
                user_answer TEXT,
                is_correct INTEGER NOT NULL,
                FOREIGN KEY (quiz_id) REFERENCES quiz_history(id),
                FOREIGN KEY (word_id) REFERENCES words(id)
            )
        ''')

        conn.commit()
        self.close()

    def populate_initial_data(self):
        """Populate database with all 400 vocabulary words (20 lists)"""
        conn = self.connect()
        cursor = conn.cursor()

        # Check if data already exists
        cursor.execute('SELECT COUNT(*) FROM words')
        if cursor.fetchone()[0] > 0:
            self.close()
            return

        print("Populating database with vocabulary words...")

        # ALL 20 LISTS - 400 WORDS TOTAL
        all_words = [
            # LIST 1
            ("Analogous", "adj.",
             "Similar in some respect, indicates points of similitude often for clarification or emphasis", 1),
            ("Analogue", "n.", "A thing or idea that is the same", 1),
            ("Caitiff", "n.", "Coward", 1),
            ("Darkling", "adv., adj.", "In darkness, or without clarity", 1),
            ("Efficacy", "n.", "The ability to produce the desired result", 1),
            ("Elaborate", "adj.", "Complex detailed; richly decorated", 1),
            ("Fraudulent", "adj.", "Intended to deceive", 1),
            ("Inconsequential", "adj.", "Unimportant or trivial", 1),
            ("Incredulous", "adj.", "Unconvinced or unwilling to believe, often manifest disbelief", 1),
            ("Ironclad", "adj.", "Irrefutable", 1),
            ("Labyrinth", "n.", "Based on mythology, now means a confusing network, or anything very complicated", 1),
            ("Lineaments", "n.",
             "An outline, feature, or contour of a landscape, body or figure and especially of a face — usually used in plural",
             1),
            ("Litigious", "adj.", "Tending towards or wanting to take legal action; may mean quarrelsome", 1),
            ("Nostrum", "n.", "An ineffective or quack remedy", 1),
            ("Plumb", "many",
             "A weight, usually made of lead, attached to a line and used to find the depth of water or to verify a true vertical alignment",
             1),
            ("Ponderous", "adj.", "Heavy looking; lumbering and laborious in movement", 1),
            ("Posthumous", "adj.", "After death", 1),
            ("Resilience", "n.", "Speedy recovery from problems; elastic quality", 1),
            ("Resolute", "adj.", "Characterized by determination", 1),
            ("Smelt", "v.", "To melt ore in order to get metal from it, or produce metal in this way", 1),

            # LIST 2
            ("Anecdote", "n.", "A short personal story", 2),
            ("Anemic", "adj.", "Weak or sickly looking", 2),
            ("Camaraderie", "n.", "A sense of closeness, friendship, unity, and trust within a group", 2),
            ("Dearth", "n.", "A lack or deficiency", 2),
            ("Debacle", "n.", "A failure, disaster or defeat often associated with humiliation", 2),
            ("Eloquent", "adj.", "Verbal expression that is effective and well styled", 2),
            ("Elucidate", "v.", "To explain clearly", 2),
            ("Fray", "v.", "To wear down to threads literally or metaphorically", 2),
            ("Frieze", "n.", "A decorative band on a wall often near the ceiling", 2),
            ("Incubus", "n.", "Anything that causes extreme worry or distress, typically an obsession or nightmare", 2),
            ("Indecorous", "adj.", "Rude, shocking, or socially unacceptable", 2),
            ("Littoral", "adj.",
             "On or near the shore, may specifically refer to the region between the high and low tide marks", 2),
            ("Liturgy", "n.", "The events, activities, form, or order of a public religious ceremony or worship event",
             2),
            ("Obfuscate", "v.", "To make obscure or confusing", 2),
            ("Obliterate", "v.", "To utterly destroy or erase without trace", 2),
            ("Postulate", "v.", "To suggest an argument or theory; to make a claim often based on an assumption", 2),
            ("Pragmatic", "adj.", "Concerned or devoted to practical results more than theories and principles", 2),
            ("Resolve", "v.", "To solidify a decision; to find a solution", 2),
            ("Respite", "n.", "A brief interval of rest or a delay", 2),
            ("Subpoena", "n.",
             "A written legal order requiring the appearance of a person or the submission of evidence", 2),

            # LIST 3
            ("Animosity", "n.", "A feeling or spirit of hostility or resentment", 3),
            ("Annex", "n., v.", "An auxiliary building or an attached document; to take over or to add", 3),
            ("Candid", "adj.", "Honest or direct, without pretense or fabrication", 3),
            ("Candor", "n.", "Freedom from prejudice or malice; unreserved or honest expression", 3),
            ("Debility", "n.", "Weakness, infirmity", 3),
            ("Debunking", "v.", "To expose the sham or falseness of", 3),
            ("Elusive", "adj.", "Tending to evade grasp or pursuit; hard to comprehend or define", 3),
            ("Embezzle", "v.", "To appropriate fraudulently to one's own use", 3),
            ("Frivolous", "adj.", "Lacking in seriousness", 3),
            ("Froward", "adj.", "Habitually disposed to disobedience and opposition", 3),
            ("Indelible", "adj.", "Lasting, unable to be erased or removed", 3),
            ("Indicted", "v.", "To charge with a fault, offense, or crime", 3),
            ("Lobbyist", "n.", "One who works to influence public officials", 3),
            ("Lofty", "adj.", "Elevated in character and spirit; having a haughty overbearing manner", 3),
            ("Obligate", "v.", "To bind legally or morally", 3),
            ("Potable", "adj.", "Suitable for drinking", 3),
            ("Potent", "adj.", "Having or wielding force, authority, or influence", 3),
            ("Rescind", "v.", "To take away; to make void", 3),
            ("Resuscitation", "v.", "To revive from apparent death or from unconsciousness", 3),
            ("Retention", "n.", "The ability to remember", 3),

            # LIST 4
            ("Antagonism", "n.", "Actively expressed hostility or opposition", 4),
            ("Antediluvian", "adj.", "Before the flood; extremely primitive or outmoded", 4),
            ("Callow", "adj.", "Lacking adult sophistication", 4),
            ("Cant", "n.", "A hypocritical or sanctimonious talk", 4),
            ("Cantankerous", "adj.", "Difficult or irritating to deal with", 4),
            ("Decapitate", "v.", "To cut off the head of", 4),
            ("Decimated", "v.", "To reduce drastically", 4),
            ("Embroil", "v.", "To throw into disorder or confusion", 4),
            ("Fugacious", "adj.", "Lasting a short time", 4),
            ("Hapless", "adj.", "Having no luck", 4),
            ("Indigent", "adj.", "Suffering from extreme poverty", 4),
            ("Indigenous", "adj.", "Occurring naturally in a particular environment", 4),
            ("Loll", "v.", "To hang or move in a loose or lazy manner", 4),
            ("Lope", "n.", "An easy gait capable of being maintained", 4),
            ("Paramount", "adj.", "Superior to all others", 4),
            ("Precedent", "adj.", "Prior in time, order, arrangement, or significance", 4),
            ("Precedential", "adj.", "Of, relating to, or constituting a precedent", 4),
            ("Prima donna", "n.", "A principal female singer in an opera; a vain or undisciplined person", 4),
            ("Probity", "n.", "Adherence to the highest principles and ideals", 4),
            ("Retinue", "n.", "A group of retainers or attendants", 4),

            # LIST 5
            ("Anomaly", "n.", "Deviation from the common rule", 5),
            ("Antipathy", "n.", "Settled aversion or dislike", 5),
            ("Canonical", "adj.", "Conforming to a general rule or acceptable procedure", 5),
            ("Capitulate", "v.", "To surrender often after negotiation of terms", 5),
            ("Decalogue", "n.", "The Ten Commandments; a basic set of rules carrying binding authority", 5),
            ("Decorous", "adj.", "Marked by propriety and good taste", 5),
            ("Decorum", "n.", "Propriety and good taste in conduct or appearance", 5),
            ("Emblazon", "v.", "To inscribe on a surface", 5),
            ("Emeritus", "n.", "One retired from professional life but who retains an honorary title", 5),
            ("Emigrate", "v.", "To leave one's country to live elsewhere", 5),
            ("Fungible", "adj.", "Interchangeable, flexible", 5),
            ("Furrier", "n.", "One that makes, repairs, alters, or cleans fur garments", 5),
            ("Inaugurate", "v.", "To observe formally the beginning of", 5),
            ("Indolent", "adj.", "Causing little or no pain; averse to activity, effort, or movement", 5),
            ("Indomitable", "adj.", "Incapable of being subdued", 5),
            ("Loquacious", "adj.", "Full of excessive talk; wordy", 5),
            ("Lugubrious", "adj.", "Mournful or dismal", 5),
            ("Obsession", "n.", "A persistent disturbing preoccupation with an often unreasonable idea or feeling", 5),
            ("Precipitate", "v.",
             "Cause an event or situation typically bad to happen suddenly, unexpectedly, or prematurely", 5),
            ("Revere", "v.", "To show devoted honor to", 5),

            # LIST 6
            ("Anthology", "n.", "A collection of selected literary pieces or works of art or music", 6),
            ("Apathy", "n.", "Lack of feeling or interest", 6),
            ("Aplomb", "n.", "Complete and confident composure or self-assurance", 6),
            ("Capacious", "adj.", "Capable of containing a great deal", 6),
            ("Cardinal", "adj.", "Of greatest importance, fundamental", 6),
            ("Defunct", "adj.", "No longer living, existing, or functioning", 6),
            ("Efface", "v.", "To cause to vanish; to make oneself inconspicuous", 6),
            ("Emergent", "adj.", "Calling for prompt action; newly formed or prominent", 6),
            ("Encomium", "n.", "Glowing and warmly enthusiastic praise", 6),
            ("Fulminate", "v.", "To send forth censures", 6),
            ("Futile", "adj.", "Serving no useful purpose; completely ineffective", 6),
            ("Indolence", "n.", "Inclination to laziness", 6),
            ("Patois", "n.", "A dialect other than the standard or literary dialect", 6),
            ("Obsequious", "adj.", "Marked by or exhibiting a fawning attentiveness", 6),
            ("Obtuse", "adj.", "Lacking sharpness or quickness; difficult to comprehend", 6),
            ("Precipice", "n.", "A hazardous situation or place", 6),
            ("Precocious", "adj.", "Exceptionally early in development or occurrence", 6),
            ("Retraction", "n.", "An act of recanting", 6),
            ("Risible", "adj.", "Arousing or provoking laughter; associated with or related to laughter", 6),
            ("Voluminous", "adj.", "Consisting of great volume or bulk; writing or speaking much at great length", 6),

            # LIST 7
            ("Antiquated", "adj.", "Outmoded or discredited by reason of age", 7),
            ("Apposite", "adj.", "Highly pertinent or appropriate", 7),
            ("Carping", "adj.", "Marked by querulous and often perverse criticism", 7),
            ("Defalcate", "v.", "To engage in embezzlement", 7),
            ("Delusion", "n.", "Something that is falsely believed or propagated", 7),
            ("Enamor", "v.", "To cause to feel a strong or excessive interest or fascination", 7),
            ("Endow", "v.", "To provide with something freely or naturally", 7),
            (
            "Fusillade", "n.", "A number of shots fired simultaneously or in rapid succession; a spirited outburst", 7),
            ("Galleon", "n.", "A ship of the 15th to early 18th centuries used for war or commerce", 7),
            ("Indulgent", "adj.", "Characterized by yielding or giving free reign to", 7),
            ("Luminary", "n.", "A person of prominence or brilliant achievement", 7),
            ("Nomadic", "adj.", "Roaming aimlessly, frequently, or without a fixed pattern of movement", 7),
            ("Nullify", "v.", "To make of no value or consequence", 7),
            ("Obsolescence", "n.", "No longer used or useful", 7),
            ("Precipitous", "adj.", "Very steep, perpendicular, or overhanging in rise or fall", 7),
            ("Preeminent", "adj.", "Having paramount rank, dignity, or importance", 7),
            ("Riddled", "v.", "To spread through; to pierce with many holes", 7),
            ("Rigmarole", "n.", "Confused or meaningless talk; a complex procedure", 7),
            ("Salacious", "adj.", "Lustful or lecherous", 7),
            ("Synergy", "n.", "Increased effectiveness that results when people or businesses work together", 7),

            # LIST 8
            ("Appease", "v.", "To bring to a state of peace or quiet", 8),
            ("Caricature", "n.", "Exaggeration by means of distortion", 8),
            ("Delineate", "v.", "To describe or portray with accuracy or in detail", 8),
            ("Encroach", "v.", "To advance beyond the usual or proper limits", 8),
            ("Endorse", "v.", "To approve openly or recommend", 8),
            ("Gaffe", "n.", "A noticeable mistake", 8),
            ("Gall", "v.", "To irritate or vex", 8),
            ("Inebriation", "n.", "Drunkenness", 8),
            ("Ineffable", "adj.", "Incapable of being expressed", 8),
            ("Lascivious", "adj.", "Lewd, lustful", 8),
            ("Lummox", "n.", "A clumsy person", 8),
            ("Lynch", "v.", "To put to death by mob action without legal sanction", 8),
            ("Maelstrom", "n.", "A powerful often violent whirlpool", 8),
            ("Odious", "adj.", "Arousing or deserving hatred or repugnance", 8),
            ("Ogle", "v.", "To look at especially with greedy or especially interested attention", 8),
            ("Omnivorous", "adj.", "Feeding on both animal and vegetable substances", 8),
            ("Predicament", "n.", "A difficult, perplexing, or trying situation", 8),
            ("Prescience", "n.", "Foreknowledge of events", 8),
            ("Rivulet", "n.", "A small stream", 8),
            ("Subterfuge", "n.", "A deceptive device or stratagem", 8),

            # LIST 9
            ("Apprehensive", "adj.", "Viewing the future with anxiety or alarm", 9),
            ("Approximate", "adj.", "Nearly correct or exact", 9),
            ("Catharsis", "n.", "Purification or purgation", 9),
            ("Demented", "adj.", "Suffering from or exhibiting cognitive dementia", 9),
            ("Enfranchise", "v.", "To admit to political privileges or rights", 9),
            ("Gambit", "n.", "A calculated move", 9),
            ("Gambol", "v.", "Skipping or leaping about in play", 9),
            ("Inept", "adj.", "Lacking in fitness or aptitude", 9),
            ("Inexorable", "adj.", "Not to be persuaded, moved, or stopped", 9),
            ("Inexpedient", "adj.", "Inadvisable; not suited to bring about a desired result", 9),
            ("Machinations", "n.", "A scheming or crafty action intended to accomplish some usually evil end", 9),
            ("Maculated", "adj.", "Marked with spots", 9),
            ("Omnipotent", "adj.", "Having virtually unlimited authority or influence", 9),
            ("Omniscient", "adj.", "Having infinite awareness, understanding, and insight", 9),
            ("Preposterous", "adj.", "Contrary to nature, reason, or common sense", 9),
            ("Prerogative", "n.", "An exclusive or special right, power, or privilege", 9),
            ("Rue", "n., v.", "Regret, sorrow; to feel penitence, remorse, or regret for", 9),
            ("Subversive", "n.", "A systematic attempt to overthrow or undermine a political system", 9),
            ("Teetotaler", "n.", "One who practices or advocates complete abstinence from alcoholic drinks", 9),
            ("Underwrite", "v.", "To assume liability for or guarantee financial support of", 9),

            # LIST 10
            ("Arbitrator", "n.", "One that is given power to decide a dispute", 10),
            ("Arboreal", "adj.", "Of, relating to, or resembling a tree", 10),
            ("Caustic", "adj.", "Capable of destroying by chemical action; marked by incisive sarcasm", 10),
            ("Cavil", "v.", "To raise trivial objection", 10),
            ("Deplete", "v.", "To lessen markedly in quantity, content, power, or value", 10),
            ("Deplore", "v.", "To feel or express grief for", 10),
            ("Ensconce", "v.", "Shelter, conceal; establish or settle", 10),
            ("Garner", "v.", "To acquire by effort", 10),
            ("Genre", "n.", "Kind, sort", 10),
            ("Infer", "v.", "To derive as a conclusion from facts or premises", 10),
            ("Magnate", "n.", "A person of rank, power, influence, or distinction often in a specified area", 10),
            ("Minutia", "n.", "A minor detail", 10),
            ("Opalescence", "n.", "Something that reflects an iridescent light", 10),
            ("Ornate", "adj.", "Elaborately or excessively decorated", 10),
            ("Mensch", "n.", "A person of integrity and honor", 10),
            ("Presumptuous", "adj.", "Overstepping due bounds; taking liberties", 10),
            ("Recrudescence", "n.", "A new outbreak after a period of abatement or inactivity", 10),
            ("Doppelganger", "n.", "A ghostly counterpart to a living person", 10),
            ("Salient", "adj.", "Standing out conspicuously; prominent", 10),
            ("Unfetter", "v.", "To free or liberate", 10),

            # LIST 11
            ("Archipelago", "n.", "A group of islands", 11),
            ("Caulk", "v.", "To stop up and make tight against leakage", 11),
            ("Centurion", "n.", "An officer commanding a subdivision of a Roman legion", 11),
            ("Crass", "adj.", "Guided by or indicative of base or materialistic values", 11),
            ("Demurrage", "n.", "A charge for detaining a ship, freight car, or truck", 11),
            ("Enigmatic", "adj.", "Of, relating to, or resembling something hard to understand or explain", 11),
            ("Envoy", "n.", "A person delegated to represent one government in its dealings with another", 11),
            ("Expatriation", "n.", "The withdrawal of oneself from residence in or allegiance to one's native country",
             11),
            ("Garble", "v.", "To so alter or distort as to create a wrong impression or change the meaning", 11),
            ("Insouciant", "adj.", "Casual; marked by blithe unconcern", 11),
            ("Infamous", "adj.", "Having a reputation of the worst kind; notoriously evil", 11),
            ("Ingratiate", "v.", "To gain favor by deliberate effort", 11),
            ("Magnanimous", "adj.", "Showing or suggesting a lofty and courageous spirit", 11),
            ("Maladroit", "adj.", "Lacking adroitness, inept", 11),
            ("Malady", "n.", "An unwholesome or disordered condition", 11),
            ("Onus", "n.", "A disagreeable necessity", 11),
            ("Orate", "v.", "To speak in an elevated and often pompous manner", 11),
            ("Priggish", "adj.", "An irritating tendency to observe proprieties in a pointed manner", 11),
            ("Priory", "n.", "A religious house", 11),
            ("Salutary", "adj.", "Producing a beneficial effect", 11),

            # LIST 12
            ("Censorious", "adj.", "Marked by or given to judgment involving condemnation", 12),
            ("Depository", "n.", "A place where something is placed for safekeeping", 12),
            ("Enumerate", "v.", "To specify one after another", 12),
            ("Epaulet", "n.", "Something that ornaments or protects the shoulder", 12),
            ("Genteel", "adj.", "Elegant or graceful in manner, appearance, or shape", 12),
            ("Gist", "n.", "The main point or part", 12),
            ("Infirmity", "n.", "Feeble or frail", 12),
            ("Inimitable", "adj.", "Not capable of being imitated", 12),
            ("Inveigle", "v.", "To acquire by ingenuity or flattery", 12),
            ("Irenic", "adj.", "Favoring, conducive to, or operating toward peace, moderation, or conciliation", 12),
            ("Maintain", "v.", "To continue or persevere in; may also mean to affirm", 12),
            ("Malcontent", "n.", "One who bears a grudge from a sense of grievance or thwarted ambition", 12),
            ("Opprobrious", "adj.", "Deserving disgrace; infamous", 12),
            ("Orthodox", "adj.", "Conforming to established doctrine especially in religion", 12),
            ("Pretension", "n.", "An aspiration or intention that may or may not reach fulfillment", 12),
            ("Pristine", "adj.", "Not spoiled, corrupted, or polluted", 12),
            ("Salubrious", "adj.", "Favorable to or promoting health or well-being", 12),
            ("Sporadic", "adj.", "Occurring occasionally, singly, or in irregular or random instances", 12),
            ("Stanch", "v.", "To check or stop the flowing of", 12),
            (
            "Temperate", "adj.", "Marked by an absence or avoidance of extravagance, violence, or extreme partisanship",
            12),

            # LIST 13
            (
            "Arson", "n.", "The willful or malicious burning of property especially with criminal or fraudulent intent",
            13),
            ("Austere", "adj.", "Stern and cold in appearance or manner", 13),
            ("Bard", "n.", "A composer, singer, or declaimer of epic or heroic verse; poet", 13),
            ("Chantey", "n.", "A song sung by sailors in rhythm with their work", 13),
            ("Charlatan", "n.", "One making usually showy pretenses to knowledge or ability", 13),
            ("Circumscribe", "v.", "To define or mark off carefully", 13),
            ("Deferential", "adj.", "Showing or expressing respect", 13),
            ("Depravity", "n.", "The quality or state of being corrupted or evil", 13),
            ("Derelict", "adj.", "Abandoned especially by the owner or occupant", 13),
            ("Egress", "n.", "The action or right of going or coming out", 13),
            ("Epicure", "n.", "One with sensitive and discriminating tastes especially in food or wine", 13),
            ("Glacial", "adj.", "Suggestive of ice (extremely cold) or of the slow movement of glaciers", 13),
            ("Hegemony", "n.", "The social, cultural, ideological, or economic influence exerted by a dominant group",
             13),
            ("Initialize", "v.", "To set to a starting position, value, or configuration", 13),
            ("Knickknack", "n.", "A small trivial, ornamental article", 13),
            ("Malediction", "n.", "Curse, execration", 13),
            ("Ominous", "adj.", "Foreboding or foreshadowing evil", 13),
            ("Ossified", "adj.", "Hardened or conventional and opposed to change", 13),
            ("Probe", "v.", "To search into and explore very thoroughly", 13),
            ("Rancor", "n.", "Bitter deep-seated ill will", 13),

            # LIST 14
            ("Acoustic", "adj.", "Of or relating to the sense of hearing, sound, or the science of sound", 14),
            ("Adroit", "adj.", "Having or showing skill, cleverness, or resourcefulness", 14),
            ("Advise", "v.", "To give a recommendation about what should be done", 14),
            ("Affront", "v.", "To insult especially to the face by behavior or language", 14),
            ("Archaic", "adj.", "Surviving from an earlier period", 14),
            ("Billowing", "v.", "To bulge or swell out", 14),
            ("Caucus", "n.", "A group of people united to promote an agreed-upon cause", 14),
            ("Certitude", "n.", "Certainty of act or event", 14),
            ("Cloture", "n.",
             "The closing or limitation of debate in a legislative body especially by calling for a vote", 14),
            ("Coagulate", "adj.", "Being clotted or congealed", 14),
            ("Connubial", "adj.", "Of or relating to the married state", 14),
            ("Derisive", "adj.", "Expressing or causing ridicule or scorn to show contempt", 14),
            ("Ersatz", "adj.", "Being a usually artificial and inferior substitute or imitation", 14),
            ("Extremity", "n.", "A drastic or desperate act or measure", 14),
            ("Jejune", "adj.", "Devoid of significance or interest", 14),
            ("Mercantile", "adj.", "Relating to merchants or trading", 14),
            ("Nemesis", "n.", "One that inflicts retribution or vengeance; an act or effect of retribution", 14),
            ("Patronize", "v.", "To adopt an air of condescension toward", 14),
            ("Refulgent", "n.", "A radiant or resplendent quality or state", 14),
            ("Sidereal", "adj.", "Of, relating to, or expressed in relation to stars or constellations", 14),

            # LIST 15
            ("Apoplectic", "adj.", "Affected with, inclined to, or showing symptoms of stroke", 15),
            ("Coalesce", "v.", "To unite into a whole or for a common end", 15),
            ("Conducive", "adj.", "Tending to promote or assist", 15),
            ("Defoliate", "v.", "To deprive of leaves especially prematurely", 15),
            ("Extant", "adj.", "Currently or actually existing", 15),
            ("Garrison", "n.", "A military post", 15),
            ("Impartial", "adj.", "Not biased; treating or affecting all equally", 15),
            ("Lumber", "v.", "To move ponderously", 15),
            ("Malevolent", "adj.", "Productive of harm or evil", 15),
            ("Qualitative", "adj.", "Of or relating to quality or kind", 15),
            ("Restive", "adj.", "Stubbornly resisting control", 15),
            ("Sinecure", "n.", "An office or position that requires little or no work and usually provides an income",
             15),
            ("Suffragist", "n.", "One who advocates extension of voting rights especially for women", 15),
            ("Talisman", "n.", "Something producing apparently magical or miraculous effects", 15),
            ("Trivial", "adj.", "Of little worth or importance", 15),
            ("Uproarious", "adj.", "Very noisy and full", 15),
            ("Venerate", "v.", "To regard with reverential respect or with admiring deference", 15),
            ("Vestige", "n.", "A trace, mark, or visible sign left by something vanished or lost", 15),
            ("Vogue", "n.", "Popular or in fashion at a particular time", 15),
            ("Volatile", "adj.", "Dangerous; potentially destructive", 15),

            # LIST 16
            ("Acquiesce", "v.", "To accept, comply, or submit tacitly or passively", 16),
            ("Aqueous", "adj.", "Of, relating to, or resembling water", 16),
            ("Armada", "n.", "A large force or group usually of moving things", 16),
            ("Criterion", "n.", "A standard on which a judgment or decision may be based", 16),
            ("Crux", "n.", "An essential point requiring resolution or resolving an outcome", 16),
            ("Negligence", "n.", "A failure to exercise reasonable care", 16),
            ("Noetic", "adj.", "Of, relating to, or based on the intellect", 16),
            ("Rebarbative", "adj.", "Repellent, irritating", 16),
            ("Sanctimonious", "adj.", "Hypocritically pious or devout", 16),
            ("Sanguinary", "adj.", "Bloodthirsty, murderous", 16),
            ("Spurious", "adj.", "Outwardly similar or corresponding to something without having its genuine qualities",
             16),
            ("Squalid", "adj.", "Marked by filthiness and degradation from neglect or poverty", 16),
            ("Sullied", "v.", "To make soiled or tarnished", 16),
            ("Tenacious", "adj.", "Persistent in seeking something valued or desired", 16),
            ("Untoward", "adj.", "Difficult to guide, manage, or work with", 16),
            ("Unwieldy", "adj.", "Not easily managed, handled, or used", 16),
            ("Vigilant", "adj.", "Alertly watchful especially to avoid danger", 16),
            ("Vignette", "n.", "A short descriptive literary sketch", 16),
            ("Wavelet", "n.", "A little wave; ripple", 16),
            ("Waylay", "v.", "To lie in wait or attack from ambush", 16),

            # LIST 17
            ("Chary", "adj.", "Hesitant and vigilant about dangers and risks", 17),
            ("Chasm", "n.", "A marked division, separation, or difference", 17),
            ("Collusion", "n.", "Secret agreement or cooperation especially for an illegal or deceitful purpose", 17),
            ("Crestfallen", "adj.", "Feeling shame or humiliation; dejected", 17),
            ("Deride", "v.", "To subject to usually bitter or contemptuous ridicule", 17),
            ("Epiphany", "n.", "A revealing scene or moment", 17),
            ("Globular", "adj.", "Having the shape of a globe", 17),
            ("Glower", "v.", "To look or stare with sullen annoyance or anger", 17),
            ("Innocuous", "adj.", "Not likely to give offense or to arouse strong feelings of hostility", 17),
            ("Innovate", "v.", "To make changes or do something in a new way", 17),
            ("Malefactor", "n.", "One who commits an offense against the law", 17),
            ("Nocturnal", "adj.", "Active at night", 17),
            ("Ostentatious", "adj.", "Marked by conspicuous and sometimes pretentious display", 17),
            ("Pandemic", "adj.",
             "Occurring over a wide geographic area and affecting an exceptionally high proportion of the population",
             17),
            ("Sap", "v.", "To weaken or exhaust the energy or vitality of", 17),
            ("Sapient", "adj.", "Possessing or expressing great sagacity", 17),
            ("Statute", "n.", "An act intended as a permanent rule", 17),
            ("Staunch", "adj.", "Steadfast in loyalty or principle", 17),
            ("Tentative", "adj.", "Not fully worked out or developed", 17),
            ("Unwitting", "adj.", "Not knowing or not intended", 17),

            # LIST 18
            ("Articulate", "adj.", "Expressing oneself readily, clearly, or effectively", 18),
            ("Chastises", "v.", "To inflict punishment on or censure severely", 18),
            ("Derision", "n.", "The use of ridicule or scorn to show contempt", 18),
            ("Derive", "v.", "To take, receive, or obtain especially from a specified source", 18),
            ("Epistolary", "adj.", "Of, relating to, or suitable to a letter", 18),
            ("Epitome", "n.", "A typical or ideal example", 18),
            ("Goad", "n.", "Something that urges or stimulates into action", 18),
            ("Hermeneutic", "n.", "A method or principle of interpretation", 18),
            ("Inscrutable", "adj.", "Not readily investigated, interpreted, or understood", 18),
            ("Malign", "v.", "To utter injuriously misleading or false reports about; speak evil of", 18),
            ("Mallet", "n.", "A hammer with a typically barrel-shaped head", 18),
            ("Palatial", "adj.", "Of, relating to, or being a palace", 18),
            ("Palisade", "n.", "A fence of stakes especially for defense", 18),
            ("Performatives", "adj.", "A word that accomplishes an action when it is said", 18),
            ("Procrastinate", "v.", "To put off intentionally and habitually", 18),
            ("Prodigal", "adj.", "Characterized by profuse or wasteful expenditure; lavish", 18),
            ("Sardonic", "adj.", "Disdainfully or skeptically humorous", 18),
            ("Sate", "v.", "To appease by indulging to the full", 18),
            ("Steep", "v.", "To saturate with or subject thoroughly to", 18),
            ("Superannuate", "v.", "To make, declare, or prove obsolete or out-of-date", 18),

            # LIST 19
            ("Archives", "n.", "A repository or collection especially of information", 19),
            ("Artifice", "n.", "An artful stratagem; false or insincere behavior", 19),
            ("Ascertain", "v.", "To find out or learn with certainty", 19),
            ("Crony", "n.", "A close friend especially of long standing", 19),
            ("Derogatory", "adj.", "Detracting from the character or standing of something", 19),
            ("Descry", "v.", "To catch sight of", 19),
            ("Epitomized", "v.", "To serve as the typical or ideal example of", 19),
            ("Equivocate", "v.", "To use uncertain or misleading language intending to deceive", 19),
            ("Gouge", "v.", "To scoop or force out; to subject to extortion", 19),
            ("Insentient", "adj.", "Lacking perception, consciousness, or animation", 19),
            ("Insipid", "adj.", "Lacking in qualities that interest, stimulate, or challenge", 19),
            ("Malleable", "adj.", "Having a capacity for adaptive change", 19),
            ("Manifest", "adj.", "Easily perceived by the senses or understood by the mind", 19),
            ("Palliative", "n.", "Something that moderates the intensity of", 19),
            ("Pallid", "adj.", "Lacking sparkle or liveliness", 19),
            ("Panacea", "n.", "A remedy for all ills or difficulties", 19),
            ("Profane", "v.", "To treat with abuse, irreverence, or contempt", 19),
            ("Recalcitrant", "adj.", "Difficult to manage or operate", 19),
            ("Savant", "n.", "A person of learning, especially in a specialized field", 19),
            ("Supercilious", "adj.", "Coolly and patronizingly haughty", 19),

            # LIST 20
            ("Ascetic", "adj.", "Practicing strict self-denial as a measure of personal and spiritual discipline", 20),
            ("Asperity", "n.", "Roughness of manner or of temper", 20),
            ("Chicanery", "n.", "Deception by artful subterfuge or sophistry", 20),
            ("Chimerical", "adj.", "Fantastically visionary or improbable", 20),
            ("Despicable", "adj.", "So worthless or obnoxious as to rouse moral indignation", 20),
            ("Err", "v.", "To make a mistake or violate an accepted standard of conduct", 20),
            ("Erratic", "adj.", "Characterized by a lack of consistency, regularity, or uniformity", 20),
            ("Gratis", "adv/adj.", "Without charge or recompense; free", 20),
            ("Gratuitous", "adj.", "Not called for by the circumstances", 20),
            ("Instigate", "v.", "To goad or urge forward", 20),
            ("Intelligible", "adj.", "Capable of being understood", 20),
            ("Mannered", "adj.", "Having or displaying a particular way of behaving", 20),
            ("Mantle", "n.",
             "A loose sleeveless garment worn over other clothes; a figurative cloak symbolizing preeminence", 20),
            ("Panegyric", "n.", "A eulogistic oration or writing", 20),
            ("Panoply", "n.", "A magnificent or impressive array", 20),
            ("Profound", "adj.", "Having intellectual depth and insight", 20),
            ("Progeny", "n.", "Descendents; or a body of followers, disciples, or successors", 20),
            ("Ineluctable", "adj.", "Not to be avoided, changed, or resisted", 20),
            ("Savor", "v.", "To season, taste, relish, or enjoy", 20),
            ("Scintillate", "v.", "To emit quick flashes as if throwing off sparks", 20),
        ]

        cursor.executemany('''
            INSERT INTO words (word, pos, definition, list_number)
            VALUES (?, ?, ?, ?)
        ''', all_words)

        conn.commit()
        self.close()
        print(f"✓ Successfully populated database with {len(all_words)} words!")

    def get_lists(self, list_numbers):
        """Get all words from specified list numbers"""
        conn = self.connect()
        cursor = conn.cursor()

        placeholders = ','.join('?' * len(list_numbers))
        query = f'''
            SELECT id, word, pos, definition, list_number
            FROM words
            WHERE list_number IN ({placeholders})
            ORDER BY RANDOM()
        '''

        cursor.execute(query, list_numbers)
        words = cursor.fetchall()
        self.close()

        return [dict(word) for word in words]

    def get_all_list_numbers(self):
        """Get list of all available list numbers"""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('SELECT DISTINCT list_number FROM words ORDER BY list_number')
        lists = [row[0] for row in cursor.fetchall()]
        self.close()

        return lists

    def save_quiz_result(self, quiz_type, lists_used, score, total, correct_words, incorrect_words):
        """Save quiz results to database"""
        conn = self.connect()
        cursor = conn.cursor()

        percentage = (score / total * 100) if total > 0 else 0

        # Insert quiz history
        cursor.execute('''
            INSERT INTO quiz_history (quiz_type, lists_used, score, total_questions, percentage)
            VALUES (?, ?, ?, ?, ?)
        ''', (quiz_type, ','.join(map(str, lists_used)), score, total, percentage))

        quiz_id = cursor.lastrowid

        # Insert correct answers
        for word in correct_words:
            cursor.execute('''
                INSERT INTO quiz_details (quiz_id, word_id, user_answer, is_correct)
                VALUES (?, ?, ?, 1)
            ''', (quiz_id, word['id'], word.get('user_answer', '')))

        # Insert incorrect answers
        for word in incorrect_words:
            cursor.execute('''
                INSERT INTO quiz_details (quiz_id, word_id, user_answer, is_correct)
                VALUES (?, ?, ?, 0)
            ''', (quiz_id, word['id'], word.get('user_answer', '')))

        conn.commit()
        self.close()

        return quiz_id

    def get_quiz_history(self, limit=10):
        """Get recent quiz history"""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, quiz_type, lists_used, score, total_questions, 
                   percentage, date_taken
            FROM quiz_history
            ORDER BY date_taken DESC
            LIMIT ?
        ''', (limit,))

        history = cursor.fetchall()
        self.close()

        return [dict(row) for row in history]

    def get_overall_stats(self):
        """Get overall performance statistics"""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT 
                COUNT(*) as total_quizzes,
                AVG(percentage) as avg_percentage,
                MAX(percentage) as best_score,
                MIN(percentage) as worst_score,
                SUM(score) as total_correct,
                SUM(total_questions) as total_attempted
            FROM quiz_history
        ''')

        stats = dict(cursor.fetchone())
        self.close()

        return stats


# Test the database when running this file directly
if __name__ == "__main__":
    print("Testing VocabDatabase...")
    db = VocabDatabase()

    conn = db.connect()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM words')
    total = cursor.fetchone()[0]

    cursor.execute('SELECT DISTINCT list_number FROM words ORDER BY list_number')
    lists = [row[0] for row in cursor.fetchall()]

    db.close()

    print(f"✓ Total words: {total}")
    print(f"✓ Available lists: {lists}")
    print("✓ Database ready!")