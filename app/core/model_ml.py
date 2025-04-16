from pathlib import Path
import pandas as pd
import bnlearn as bn
import pickle

def define_model_machine_learning():
    # Tentukan path model.pkl relatif terhadap lokasi file ini
    model_path = Path(__file__).resolve().parents[2] / "model" / "model.pkl"

    df = pd.DataFrame({
        "escape": [1],
        "relaxation": [1],
        "play": [1],
        "strengthening_family_bonds": [1],
        "prestige": [0],
        "social_interaction": [1],
        "romance": [0],
        "educational_opportunity": [0],
        "self_fulfillment": [0],
        "wish_fulfillment": [0],
        "infrastruktur_pariwisata": [0],
        "edukasi": [0],
        "alam_sekitar": [1],
        "atraksi_budaya_dan_sejarah": [0],
        "kuliner": [0],
        "makan": [0],
        "belajar": [0],
        "berinteraksi_dengan_satwa": [0],
        "mengambil_foto": [1],
        "berziarah": [0],
        "berkemah": [0],
        "melihat_pemandangan": [1],
        "berbelanja": [0],
        "berenang": [0],
        "berendam": [1],
        "memancing": [0],
        "bermain_wahana": [1]
    })

    try:
        # Load model if exists
        with open(model_path, "rb") as f:
            model = pickle.load(f)
    except FileNotFoundError:
        # If model doesn't exist, create and train new one
        structure = bn.structure_learning.fit(df)
        model = bn.parameter_learning.fit(structure, df)

        # Save the model
        with open(model_path, "wb") as f:
            pickle.dump(model, f)
    except Exception as e:
        raise RuntimeError(f"An error occurred while loading the model: {e}")

    return model
