import uvicorn
import sys
from app.data.seed_data import seed_data


if __name__ == "__main__":
    
    # python -m  main --seed-data pour remplir la base de données
    if "--seed-data" in sys.argv:
        seed_data()

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

