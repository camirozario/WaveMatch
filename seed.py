from app import app, db, SurfSpot
spots = [

    # =========================
    # BEGINNER
    # =========================

    {
        "name": "Perequê-Açu",
        "city": "Ubatuba",
        "state": "SP",
        "latitude": -23.4216,
        "longitude": -45.0623,
        "surf_level": "beginner",
        "wave_direction": "left_right",
        "predominant_direction": None,
        "wave_shape": "full",
        "wave_duration": "long",
        "wave_speed": "slow",
        "break_length": None,
        "current_tendency": None
    },

    {
        "name": "Fazenda",
        "city": "Ubatuba",
        "state": "SP",
        "latitude": -23.3601,
        "longitude": -44.8563,
        "surf_level": "beginner",
        "wave_direction": "left_right",
        "predominant_direction": None,
        "wave_shape": None,
        "wave_duration": "long",
        "wave_speed": None,
        "break_length": "short",
        "current_tendency": None
    },

    {
        "name": "Ubatumirim",
        "city": "Ubatuba",
        "state": "SP",
        "latitude": -23.3360,
        "longitude": -44.8975,
        "surf_level": "beginner",
        "wave_direction": "left_right",
        "predominant_direction": None,
        "wave_shape": None,
        "wave_duration": "long",
        "wave_speed": None,
        "break_length": "short",
        "current_tendency": None
    },

    {
        "name": "Sapê",
        "city": "Ubatuba",
        "state": "SP",
        "latitude": -23.5277,
        "longitude": -45.2158,
        "surf_level": "beginner",
        "wave_direction": "left_right",
        "predominant_direction": None,
        "wave_shape": "full",
        "wave_duration": "long",
        "wave_speed": None,
        "break_length": None,
        "current_tendency": None
    },


    # =========================
    # INTERMEDIATE
    # =========================

    {
        "name": "Praia Grande",
        "city": "Ubatuba",
        "state": "SP",
        "latitude": -23.4727,
        "longitude": -45.0665,
        "surf_level": "intermediate",
        "wave_direction": "left_right",
        "predominant_direction": None,
        "wave_shape": "full",
        "wave_duration": "long",
        "wave_speed": "slow",
        "break_length": "long",
        "current_tendency": "frequent"
    },

    {
        "name": "Itamambuca",
        "city": "Ubatuba",
        "state": "SP",
        "latitude": -23.4019,
        "longitude": -45.0023,
        "surf_level": "intermediate",
        "wave_direction": "left_right",
        "predominant_direction": None,
        "wave_shape": None,
        "wave_duration": "long",
        "wave_speed": None,
        "break_length": "long",
        "current_tendency": "frequent"
    },

    {
        "name": "Toninhas",
        "city": "Ubatuba",
        "state": "SP",
        "latitude": -23.4873,
        "longitude": -45.0741,
        "surf_level": "intermediate",
        "wave_direction": "left_right",
        "predominant_direction": None,
        "wave_shape": None,
        "wave_duration": "long",
        "wave_speed": None,
        "break_length": "medium",
        "current_tendency": "frequent"
    },

    {
        "name": "Tenório",
        "city": "Ubatuba",
        "state": "SP",
        "latitude": -23.4649,
        "longitude": -45.0562,
        "surf_level": "intermediate",
        "wave_direction": "left_right",
        "predominant_direction": "left",
        "wave_shape": "full",
        "wave_duration": "medium",
        "wave_speed": None,
        "break_length": "medium",
        "current_tendency": None
    },


    # =========================
    # ADVANCED
    # =========================

    {
        "name": "Vermelha do Centro",
        "city": "Ubatuba",
        "state": "SP",
        "latitude": -23.4637,
        "longitude": -45.0490,
        "surf_level": "advanced",
        "wave_direction": "left_right",
        "predominant_direction": "right",
        "wave_shape": "tubular",
        "wave_duration": "medium_short",
        "wave_speed": None,
        "break_length": "short",
        "current_tendency": None
    },

    {
        "name": "Vermelha do Norte",
        "city": "Ubatuba",
        "state": "SP",
        "latitude": -23.4170,
        "longitude": -45.0362,
        "surf_level": "advanced",
        "wave_direction": "left_right",
        "predominant_direction": None,
        "wave_shape": "tubular",
        "wave_duration": "medium_short",
        "wave_speed": None,
        "break_length": "short",
        "current_tendency": None
    },

    {
        "name": "Félix",
        "city": "Ubatuba",
        "state": "SP",
        "latitude": -23.3889,
        "longitude": -44.9708,
        "surf_level": "advanced",
        "wave_direction": "left_right",
        "predominant_direction": "left",
        "wave_shape": "tubular",
        "wave_duration": "short",
        "wave_speed": None,
        "break_length": "short",
        "current_tendency": None
    },

    {
        "name": "Camburi das Pedras",
        "city": "Ubatuba",
        "state": "SP",
        "latitude": -23.3703,
        "longitude": -44.7854,
        "surf_level": "advanced",
        "wave_direction": "left_right",
        "predominant_direction": None,
        "wave_shape": "tubular",
        "wave_duration": "medium_short",
        "wave_speed": None,
        "break_length": "short",
        "current_tendency": None
    }

]

with app.app_context():
    for spot_data in spots:

        spot_verify_duplicate = db.session.execute(
            db.select(SurfSpot).where(SurfSpot.name == spot_data['name'])
            ).scalar_one_or_none() # me devolva UM objeto SurfSpot ou None se não encontrou
                
        if spot_verify_duplicate is None:
            spot = SurfSpot(**spot_data)# atalho para transformar esse dicionário em um objeto da sua classe SurfSpot.
            db.session.add(spot)


    db.session.commit()    