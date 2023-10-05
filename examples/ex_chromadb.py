import chromadb
import chromadb.config
from chromadb.utils import embedding_functions

# Add and load local chatbot module
import os
import sys
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_directory)
import chatbot as cb

# Create the embedding function
openai_api_key = cb.OPENAI_API_KEY
embedding_fn = embedding_functions.OpenAIEmbeddingFunction(model_name="text-embedding-ada-002", api_key=openai_api_key)

# Create a Chroma DB client
chroma_client = chromadb.Client(settings=chromadb.config.Settings(allow_reset=True))
chroma_client.reset()

# Create a collection
chroma_client.create_collection("documents", embedding_function=embedding_fn)
docs_collection = chroma_client.get_collection("documents", embedding_function=embedding_fn)

# Add data
docs = ["Das Food Future Lab Team aus insgesamt 13 Professuren von der Fakultät Agrarwissenschaften und Landschaftsarchitektur.",
        "Prof. Daum ist seit 2007 an der Hochschule Osnabrück. Er leitet das Fachgebiet Pflanzenernährung im Gartenbau und lehrt in agrar- und lebensmittelwissenschaftlichen Studiengängen. Er forscht an Ansätzen zur Verbesserung der Qualität von Obst und Gemüse sowie zur Entwicklung umweltschonender Düngungs- und Anbaustrategien. In aktuellen Forschungsprojekten befasst er sich unter anderem mit der Erzeugung von biofortifiziertem Obst und Gemüse, mit Ansatzpunkten zur Reduktion der Lachgasemission beim Anbau von Gemüse sowie der Entwicklung von holzfaserbasierten Kultursubstraten für den Gartenbau. Vor seiner Tätigkeit an der Hochschule war Herr Daum über 10 Jahre bei Nestlé in der Rohstoffbeschaffung und präventiven Qualitätssicherung für Babynahrung tätig.",
        "Prof. Dr. Werner Dierend leitet das Fachgebiet Obstbau und Obstverwertung Obst ist ein wichtiger Baustein der menschlichen Ernährung. Es enthält viele Inhaltsstoffe, die für die menschliche Gesundheit unverzichtbar sind. Daneben spielt es bei der Versorgung der Menschen mit sauberem Wasser eine zunehmend wichtige Rolle. Die Züchtung neuer Obstsorten, die Produktion von qualitativ hochwertigem Obst, die Verarbeitung und die Erhaltung dieser Qualität in der Nacherntephase sind daher wichtige Herausforderungen der Zukunft. Dabei ist die interdisziplinäre Zusammenarbeit im Bereich der Lebensmittelbranche von großer Wichtigkeit. Food Future Lab biete hierfür eine hoch innovative und geeignete Plattform.",
        "Seit 2011 an der Hochschule Osnabrück. Lehrt im Bereich der Nutztierwissenschaften, hier mit besonderen Fokus auf Erzeugung tierischer Rohstoffe und Produkte, Produktionssysteme und Bestandsmanagement und deren Implikationen auf die gesamte Prozesskette tierischer Lebensmittel. Zusätzlich wissenschaftlicher Mitarbeiter im Fachbereich Tierhaltung und Produkte mit Schwerpunkt Geflügel. Herr Kaufmann ist involviert in Forschungs- und Entwicklungsprojekte in den Themenkomplexen „Tier-Umwelt-Interaktionen“ mit dem Fokus auf der Verbesserung von Tierhaltungssystemen und deren Auswirkungen auf die gesamte Wertschöpfungskette sowie im Bereich „Erwachsenenbildung“, jeweils mit starker Wirtschaftsbeteiligung. Werdegang: Studium und Promotion an der Universität Göttingen, wissenschaftliche Mitarbeiter an der Uni Göttingen in den Fachgebieten Agrartechnik und Produktionssysteme der Nutztiere, Projektmitarbeiter auf Honorarbasis AGRA-TEG GmbH Göttingen und bis heute wissenschaftliche Beratertätigkeit.",
        "Innovationen im Lebensmittelbereich erfolgen im Rahmen des geltenden deutschen und internationalen Lebensmittelrechts oder machen regulatorischen Bedarf sichtbar. Forschungs- und Entwicklungsarbeiten müssen daher von Beginn an auch mit einem Blick auf rechtliche Vorgaben und regulatorische Herausforderungen flankiert werden. Bei den rechtlichen Fragen kann es sich sogar um Schlüsselfragen für ein Projekt handeln, wenn bestimmte Verfahren oder Stoffe amtlicherseits zugelassen werden müssen oder gesetzliche Verbote der Entwicklungsarbeit im Wege stehen.",
        "Mareike Dirks-Hofmeister lehrt seit 2020 an der Hochschule Osnabrück im Studiengang Bioverfahrenstechnik in der Agrar- und Lebensmittelwirtschaft. Die Lehr- und Forschungsschwerpunkte liegen dabei im Bereich der Enzyme, deren biotechnologischen Produktion mithilfe von Mikroorganismen, und deren Verbesserung für die Anwendung.",
        "Prof. Dr. Nicolas Meseth vertritt das Fachgebiet Wirtschaftsinformatik. Seine Schwerpunkte in der Lehre sind die Grundlagen und Trends der Digitalisierung, Daten- und Informationsmanagement, moderne Webanwendungen sowie die Speicherung und Analyse großer und unstrukturierter Daten. In der Forschung fokussiert sich Professor Meseth auf die digitale Unterstützung der Verkaufs- und Distributionsprozesse von Lebensmitteln sowie der Anwendungsmöglichkeiten von KI in diesem Bereich. Das Experimentierfeld ist vornehmlich das Reallalbor Mark & Gesellschaft des Food Future Lab. Vor seiner Tätigkeit als Professor arbeitete er für Deloitte Consulting, eine der weltweit führenden Unternehmensberatungen. Dort war sein Schwerpunkt die Umsetzung von unternehmensweiten Business Intelligence und Analytics-Lösungen für namhafte Kunden in ganz Deutschland.",
        "Prof. Dr. Matthias Kussin, Professur für Medien- und CSR-Kommunikation, forscht mit Methoden der empirischen Sozialforschung an der Bedeutung von öffentlicher Kommunikation, Öffentlichkeitsarbeit sowie interner Kommunikation für den wirtschaftlichen Erfolg in der Agrar- und Lebensmittelbranche. Thematische Schwerpunkte liegen in den Bereichen der Nachhaltigkeits-, Veränderungs- sowie Risiko- und Krisenkommunikation. Er ist Mitglied im Expertengremium des Bundesinformationszentrums Landwirtschaft (BZL) der Bundesanstalt für Landwirtschaft und Ernährung (BLE) sowie Mitglied des Beirats der Landwirtschaft schafft Leben GmbH"
        ]

metas = [{ "source" : "FFL Team Website", "url" : "https://www.hs-osnabrueck.de/food-future-lab/team"},
         { "source" : "FFL Team Website", "url" : "https://www.hs-osnabrueck.de/food-future-lab/team"},
         { "source" : "FFL Team Website", "url" : "https://www.hs-osnabrueck.de/food-future-lab/team"},
         { "source" : "FFL Team Website", "url" : "https://www.hs-osnabrueck.de/food-future-lab/team"},
         { "source" : "FFL Team Website", "url" : "https://www.hs-osnabrueck.de/food-future-lab/team"},
         { "source" : "FFL Team Website", "url" : "https://www.hs-osnabrueck.de/food-future-lab/team"},
         { "source" : "FFL Team Website", "url" : "https://www.hs-osnabrueck.de/food-future-lab/team"},
         { "source" : "FFL Team Website", "url" : "https://www.hs-osnabrueck.de/food-future-lab/team"}
         ]

ids = ["ffl", "daum", "dierend", "kaufmann", "grube", "dirks_hofmeister", "meseth", "kussin"]

docs_collection.add(
    documents=docs,
    #embeddings=embeddings,
    metadatas=metas,
    ids=ids
    )

# Query DB
query_prompts = ["Wer kennt sich mit Tieren am besten aus?"]

results = docs_collection.query(
    query_texts=query_prompts,
    n_results=4,
    include=["distances", "documents", "metadatas"]
    ) 

print(results["documents"][0])