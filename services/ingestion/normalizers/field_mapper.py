import hashlib
from datetime import datetime
from services.ingestion.skill_extraction.dict_matcher import extract_skills_from_text


def map_france_travail(raw: dict) -> dict: 
    """Maps raw France Travail API response to unified schema."""

    lieu        = raw.get("lieuTravail", {})
    salaire     = raw.get("salaire", {})
    entreprise  = raw.get("entreprise", {})
    description = raw.get("description", "")

    # Skills — "exigence" S=souhaitée, E=exigée — we keep both label and level
    competences = [
        {
            "libelle": c.get("libelle", ""),
            "exigence": c.get("exigence", "")
        }
        for c in raw.get("competences", [])
    ]

    competences_texte = extract_skills_from_text(description)

    # Soft skills - optional fiels , not always present 
    qualites = [ 
        q.get("libelle", "")
        for q in raw.get("qualitesProfessionnelles", [])
    ]

    #Languages required - also optional 
    langues = [ 
        { 
            "libelle": l.get("libelle", ""), 
            "exigence" : l.get("exigence", "")
        }
        for l in raw.get("langues", [])
    ]

    # Salary — field exists but libelle is NOT guaranteed , sometimes only "commentaire" is present, sometimes nothing
    salaire_brut = salaire.get("libelle") or salaire.get("commentaire") or ""

    #Unique hash ID 
    id_source = raw.get("id", "")
    id_hash   = hashlib.md5(f"france_travail_{id_source}".encode()).hexdigest()

    return {
        #Identification 
        "id_hash":              id_hash,
        "id_source":            id_source,
        "source":               "france_travail",
        "pays":                 "FR",

        # Job
        "titre_brut":           raw.get("intitule", ""),
        "description":          raw.get("description", ""),
        "type_contrat":         raw.get("typeContratLibelle", ""),
        "nature_contrat":       raw.get("natureContrat", ""),
        "niveau_experience":    raw.get("experienceLibelle", ""),
        "qualification":        raw.get("qualificationLibelle", ""),

        # Location
        "ville_brute":          lieu.get("libelle", ""),
        "code_postal":          lieu.get("codePostal", ""),
        "latitude":             lieu.get("latitude"),
        "longitude":            lieu.get("longitude"),

        # Company
        "entreprise":           entreprise.get("nom", ""),
        "secteur_activite":     raw.get("secteurActiviteLibelle", ""),
        "tranche_effectif":     raw.get("trancheEffectifEtab", ""),

        # Salary
        "salaire_brut":         salaire_brut,
        "salaire_min":          None,
        "salaire_max":          None,

        # Skills
        "competences_rome":     competences,
        "competences_brutes":   competences_texte,
        "qualites_pro":         qualites,
        "langues":              langues,

        #ROME reference 
        "code_rome":            raw.get("romeCode", ""),
        "libelle_rome":         raw.get("romeLibelle", ""),
        "appellation_rome":     raw.get("appellationlibelle", ""),

        # Metadata
        "date_publication":     raw.get("dateCreation", ""),
        "date_actualisation":   raw.get("dateActualisation", ""),
        "date_ingestion":       datetime.utcnow().isoformat(),
        "url_offre":            raw.get("origineOffre", {}).get("urlOrigine", ""),
        "nombre_postes":        raw.get("nombrePostes", 1),
        "langue":               "fr",
    }

