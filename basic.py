# -----------------  Infectious  ----------------- #

import logging

import rdflib
from SPARQLWrapper import SPARQLWrapper, RDFXML, RDF, TURTLE, XML
from rdflib.graph import Graph, URIRef
from rdflib.plugins.stores.memory import Memory

logging.basicConfig()

sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
construct_query = """
      PREFIX dis: <http://www.semanticweb.org/dorsa/ontologies/diseases.owl#>
      PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
      PREFIX wdt: <http://www.wikidata.org/prop/direct/>
      PREFIX wd: <http://www.wikidata.org/entity/>
      PREFIX wikibase: <http://wikiba.se/ontology#>
      PREFIX bd: <http://www.bigdata.com/rdf#>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      

      CONSTRUCT {
      ?d rdf:type dis:disease .
      ?d dis:caused_by ?cause .
      ?cause rdf:type dis:infectious .
      ?d dis:named_after ?doctor .
      ?doctor rdf:type dis:doctor .
      ?doctor dis:name ?name .
      ?doctor dis:date_of_birth ?birth .
      ?doctor dis:date_of_death ?death .
      ?d dis:affects ?entity .
      ?entity rdf:type dis:biological_entity .
      ?d dis:associated_with ?specialty .
      ?specialty rdf:type dis:medical_specialty .
      ?d dis:has_symptom ?symptom .
      ?symptom rdf:type dis:symptom .
      ?d dis:outbreak_in ?country .
      ?country rdf:type dis:country .
      ?d dis:treated_with ?drug .    
      ?drug rdf:type dis:drug .
      ?d dis:incidence ?number_of_cases .
      ?d dis:death_toll ?number_of_deaths .
      ?d dis:has_risk_factor ?risk_factor .
      ?risk_factor rdf:type dis:risk_factor .
      ?d dis:has_genetic_association ?gene .
      ?gene rdf:type dis:gene .
      ?d dis:confirmed_by ?test .
      ?test rdf:type dis:medical_examination .
      ?gene dis:determined_by ?determination_method .
      ?determination_method rdf:type dis:determination_method .

      ?article rdf:type dis:scientific_article .
      ?article dis:written_on ?d .
      ?article dis:written_by ?author .
      
      ?d dis:name ?dLabel .
      ?cause dis:name ?causeLabel .  
      ?specialty dis:name ?specialtyLabel .
      ?symptom dis:name ?symptomLabel .
      ?drug dis:name ?drugLabel .
      ?gene dis:name ?geneLabel .
      ?determination_method dis:name ?determination_methodLabel .
      ?doctor dis:name ?doctorLabel .
      ?risk_factor dis:name ?risk_factorLabel .
      ?test dis:name ?testLabel .
      ?determination_method dis:name ?determination_methodLabel .
      ?country dis:name ?countryLabel .
      

      }
       WHERE{
       ?d wdt:P31 wd:Q18123741 .
       OPTIONAL {?d wdt:P828 ?cause}
       OPTIONAL {?d wdt:P1478 ?cause}
       OPTIONAL {?d wdt:P1995 ?specialty}
       OPTIONAL {?d wdt:P780 ?symptom}
       OPTIONAL {?d wdt:P2176 ?drug}
       OPTIONAL {?d wdt:P2293 ?gene}
       OPTIONAL {?d wdt:P138 ?doctor}
       OPTIONAL {?d wdt:P1120 ?number_of_deaths}
       OPTIONAL {?d wdt:P1603 ?number_of_cases}
       OPTIONAL {?d wdt:P1479 ?risk_factor}
       OPTIONAL {?d wdt:P923 ?test}
       OPTIONAL {?d wdt:P459 ?determination_method}

       SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } 
       }"""

sparql.setQuery(construct_query)
sparql.setReturnFormat(RDF)

g = Graph(store=Memory(), identifier=URIRef('http://www.semanticweb.org/store/diseases'))
rdflib.plugin.register('sparql', rdflib.query.Processor, 'rdfextras.sparql.processor', 'Processor')
rdflib.plugin.register('sparql', rdflib.query.Result, 'rdfextras.sparql.query', 'SPARQLQueryResult')

g = sparql.query().convert()
g.parse("diseases_rdf.owl", format="xml")
g.serialize("diseases_populated_1.owl", "xml")
