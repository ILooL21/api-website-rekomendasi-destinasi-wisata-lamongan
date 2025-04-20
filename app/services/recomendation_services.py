from sqlalchemy.orm import Session
from app.schemas.recommendation import RecommendationRequest
from app.db.models import User, RekomendasiWisataDetail
import bnlearn as bn
import json

# Load model sekali saat modul diimpor
model = bn.bnlearn.load(filepath="model/model.pkl")

# Mapping label ke nama wisata
LABEL_DESTINASI = {
    11: 'Pantai Joko Mursodo',
    13: 'Pantai Pengkolan Kandang Semangkon',
    12: 'Pantai Kutang',
    15: 'Taman Wisata dan Perkemahan Bumi Moronyamplung',
    3: 'Gunung Mas Mantup',
    2: 'Goa Maharani',
    20: 'Wisata Gunung Pegat',
    17: 'Wisata Air Hangat Mbrumbung',
    14: 'Taman Ekspresi Kendalifornia',
    16: 'Waduk Gondang',
    5: 'Kolam Renang Keraton',
    19: 'Wisata Edukasi Gondang Outbond',
    4: 'INDONESIA ISLAMIC ART MUSEUM',
    18: 'Wisata Bahari Lamongan',
    1: 'G-Park',
    6: 'Makam Sendang Duwur',
    7: 'Makam Sunan Drajat',
    10: 'Masjid Namira',
    9: 'Masjid Ki Bagus Hadikusumo',
    8: 'Makam Syekh Maulana Ishaq'
}

def predict_destination_recommendation(
    db: Session, recommendation_request: RecommendationRequest, current_user: User
):
    try:
        evidence = {
            k: v for k, v in recommendation_request.model_dump().items() if v is not None
        }

        prediction = bn.inference.fit(
            model,
            variables=['Nama Wisata'],
            evidence=evidence,
            verbose=0,
            elimination_order="MinWeight"
        )

        prediction.df['Nama Wisata'] = prediction.df['Nama Wisata'].map(LABEL_DESTINASI)
        prediction.df = prediction.df.sort_values(by='p', ascending=False).head(5)
        result = json.loads(prediction.df.to_json(orient='records'))


        # Ambil rekomendasi yang sudah ada
        existing_recommendations = db.query(RekomendasiWisataDetail).filter(
            RekomendasiWisataDetail.id_rekomendasi == current_user.id_user
        ).all()

        for i, wisata in enumerate(result):
            if i < len(existing_recommendations):
                # Update data yang sudah ada
                existing_recommendations[i].nama_tempat_wisata = wisata['Nama Wisata']
            else:
                # Tambah data baru jika jumlah sebelumnya kurang dari 5
                new_rekomendasi = RekomendasiWisataDetail(
                    id_rekomendasi=current_user.id_user,
                    nama_tempat_wisata=wisata['Nama Wisata'],
                )
                db.add(new_rekomendasi)

        db.commit()
        return result

    except Exception as e:
        raise RuntimeError(f"An error occurred during prediction: {e}")

def get_recommendations_log(db: Session, user_id: int):
    try:
        recommendations = db.query(RekomendasiWisataDetail).filter(
            RekomendasiWisataDetail.id_rekomendasi == user_id
        ).all()

        if not recommendations:
            return []

        result = [
            {
                "id": rec.id,
                "nama_tempat_wisata": rec.nama_tempat_wisata
            }
            for rec in recommendations
        ]

        return result

    except Exception as e:
        raise RuntimeError(f"An error occurred while fetching recommendations: {e}")