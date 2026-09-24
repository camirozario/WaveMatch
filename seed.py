from app import app, db, SurfSpot


spots = [

    # =========================
    # INICIANTE
    # =========================

    {
        "name": "Perequê-Açu",
        "city": "Ubatuba",
        "state": "SP",
        "latitude": -23.4216,
        "longitude": -45.0623,
        "surf_level": "iniciante",
        "beach_orientation": 75,
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
        "surf_level": "iniciante",
        "beach_orientation": 135,
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
        "surf_level": "iniciante",
        "beach_orientation": 135,
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
        "surf_level": "iniciante",
        "beach_orientation": 120,
        "wave_direction": "left_right",
        "predominant_direction": None,
        "wave_shape": "full",
        "wave_duration": "long",
        "wave_speed": None,
        "break_length": None,
        "current_tendency": None
    },


    # =========================
    # INTERMEDIARIO
    # =========================

    {
        "name": "Praia Grande",
        "city": "Ubatuba",
        "state": "SP",
        "latitude": -23.4727,
        "longitude": -45.0665,
        "surf_level": "intermediario",
        "beach_orientation": 120,
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
        "surf_level": "intermediario",
        "beach_orientation": 135,
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
        "surf_level": "intermediario",
        "beach_orientation": 120,
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
        "surf_level": "intermediario",
        "beach_orientation": 110,
        "wave_direction": "left_right",
        "predominant_direction": "left",
        "wave_shape": "full",
        "wave_duration": "medium",
        "wave_speed": None,
        "break_length": "medium",
        "current_tendency": None
    },


    # =========================
    # AVANCADO
    # =========================

    {
        "name": "Vermelha do Centro",
        "city": "Ubatuba",
        "state": "SP",
        "latitude": -23.4637,
        "longitude": -45.0490,
        "surf_level": "avancado",
        "beach_orientation": 110,
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
        "surf_level": "avancado",
        "beach_orientation": 135,
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
        "surf_level": "avancado",
        "beach_orientation": 135,
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
        "surf_level": "avancado",
        "beach_orientation": 150,
        "wave_direction": "left_right",
        "predominant_direction": None,
        "wave_shape": "tubular",
        "wave_duration": "medium_short",
        "wave_speed": None,
        "break_length": "short",
        "current_tendency": None
    }

]


# =========================
# ADICIONAR / ATUALIZAR SPOTS
# =========================

with app.app_context():

    for spot_data in spots:

        # Verifica se a praia ja existe no banco
        spot_verify_duplicate = db.session.execute(
            db.select(SurfSpot).where(
                SurfSpot.name == spot_data['name']
            )
        ).scalar_one_or_none()

        # Se nao existe, cria um novo SurfSpot
        if spot_verify_duplicate is None:

            spot = SurfSpot(**spot_data)
            db.session.add(spot)

        # Se ja existe, atualiza os dados
        else:

            spot_verify_duplicate.surf_level = spot_data['surf_level']
            spot_verify_duplicate.beach_orientation = spot_data['beach_orientation']

    # Salva todas as alteracoes no banco
    db.session.commit()

    print("Surf spots atualizados com sucesso!")