from tracemalloc import start
import streamlit as st
import random
import pendulum
import json
import leafmap.foliumap as leafmap


def generate_polyline(geometry):
    return "-22.931524744840036 -43.186445832252495 -22.931297482830274 -43.185909390449524"


def get_street(geometry):
    return "Rua Umari"


def fill_road_closure(
    geometry,
    starttime,
    endtime,
    alert_type,
    alert_subtype,
    description,
    direction,
):

    return {
        "id": str(random.getrandbits(128))[:14],
        "creationtime": pendulum.now().isoformat(),
        "updatetime": pendulum.now().add(hours=1).isoformat(),
        "description": description,
        "type": alert_type,
        "subtype": alert_subtype,
        "location": {
            "street": get_street(geometry),
            "direction": direction,
            "polyline": generate_polyline(geometry),
        },
        "starttime": starttime,
        "endtime": endtime,
    }


def fill_feed(road_closures):

    return {"incidents": [fill_road_closure(**r) for r in road_closures]}


road_cloasures = [
    dict(
        geometry="",
        starttime=pendulum.now().isoformat(),
        endtime=pendulum.now().isoformat(),
        alert_type="ROAD_CLOSURE",
        alert_subtype="ROAD_CLOSED_HAZARD",
        description="Road closed due to a hazard",
        direction="BOTH_DIRECTIONS",
    )
]

incidents = fill_feed(road_cloasures)

m = leafmap.Map(center=[-23, -43.3], zoom=10.5)
m.add_geojson("data/input/alagamentos.geojson", layer_name="Alagamentos")
m.to_streamlit()

st.json(incidents)

if st.button("Save New Feed"):
    print("saved")
    json.dump(incidents, open("data/incidents.json", "w"))
