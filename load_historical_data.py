import duckdb
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, BulkIndexError
import json

#geometry: "Geo Shape"::JSON,
rel = duckdb.sql("""
select
 {
    _index: 'logs-httpjson.sv_vehic_p-historical',
    _op_type: 'create',
    geometry: "Geo Shape"::JSON::STRUCT(type VARCHAR, coordinates FLOAT[]),
    properties: {
        vehicule: vehicule,
        etat: etat,
        statut: statut,
        retard: retard,
        arret: CAST(arret AS BOOLEAN),
        geom_err: geom_err,
        rs_sv_cours_a: rs_sv_cours_a,
        pmr: CAST(pmr AS BOOLEAN),
        cdate: cdate,
        sae: CAST(sae AS BOOLEAN),
        localise: CAST(localise AS BOOLEAN),
        gid: gid,
        rs_sv_ligne_a: rs_sv_ligne_a,
        vitesse: vitesse,
        terminus: terminus,
        sens: sens,
        geom_o: geom_o,
        bloque: CAST(bloque AS BOOLEAN),
        neutralise: CAST(neutralise AS BOOLEAN),
        mdate: mdate,
        rs_sv_arret_p_actu: rs_sv_arret_p_actu,
        rs_sv_arret_p_suiv: rs_sv_arret_p_suiv,
        rs_sv_chem_l: rs_sv_chem_l
        }
    }
 from read_csv('../data/files/**/*.csv.gz',
                union_by_name=true,
                ignore_errors = true,
                delim=';',
                types={'cdate': 'VARCHAR', 'mdate': 'VARCHAR'})
 where mdate is not null
 """)

def gendata(handle):
    while event := handle.fetchone():
        yield event[0]

client = Elasticsearch("https://localhost:9200/", api_key="d3EyU2VwUUIyb01LNmttMmNROU46cmsyNGhSTVBTLXVaMG5Ja2wwajNtZw==", verify_certs=False)

try:
    for res in bulk(client, gendata(rel)):
        print(res)
except BulkIndexError as e:
    print(e.errors)