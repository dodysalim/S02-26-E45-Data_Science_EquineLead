from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FILES = {
    "Caballos": "horses_listings_limpio.parquet",
    "Retail": "products_listing_limpio.parquet",
    "Usuarios": "users_info.parquet",
    "SesionesCaballos": "horses_sessions_info.parquet",
    "SesionesRetail": "prods_sessions_info.parquet",
}


def main():
    for table, name in FILES.items():
        source = next(
            (
                p
                for p in [ROOT / "app/data/clean" / name, ROOT / "data/clean" / name]
                if p.exists()
            ),
            None,
        )
        if source is None:
            raise FileNotFoundError(
                f"Falta {name}: descarga datos con DVC antes de exportar."
            )
        target = ROOT / "powerbi/data" / f"{table}.csv"
        cols = pd.read_csv(target, nrows=0).columns.tolist()
        data = pd.read_parquet(source)
        if "job_info" in data:
            data["job_info"] = data.job_info.map(
                lambda x: x.get("title") if isinstance(x, dict) else x
            )
        data[cols].to_csv(target, index=False, encoding="utf-8")
        print(table, len(data))


if __name__ == "__main__":
    main()
