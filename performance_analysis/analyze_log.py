import pandas as pd
from scipy import stats
import numpy as np


def parse_log(log_file: str):
    data = []
    with open(log_file, "r") as f:
        for line in f:
            parts = line.strip().split(" | ")
            if len(parts) < 4:
                continue

            log_entry = parts[3]
            entry_parts = log_entry.split(",")

            if len(entry_parts) >= 3:
                record = {
                    "endpoint": entry_parts[0],
                    "status": entry_parts[1],
                    "duration": float(entry_parts[2])
                }

                if len(entry_parts) > 3:
                    record["error"] = ",".join(entry_parts[3:])

                data.append(record)

    return pd.DataFrame(data)


def generate_report(df: pd.DataFrame, endpoint_filter: str = None):
    if df.empty:
        print("Nenhum dado encontrado.")
        return

    if endpoint_filter:
        df = df[df["endpoint"] == endpoint_filter]

    df["is_success"] = df["status"].apply(
        lambda x: x in ["200", "True"] if isinstance(x, str) else False
    )

    total = len(df)
    success = df["is_success"].sum()
    error = total - success

    duration_stats = {
        "avg": df["duration"].mean(),
        "min": df["duration"].min(),
        "max": df["duration"].max(),
        "std": df["duration"].std()
    }

    n = len(df)
    if n > 1:
        confidence = 0.95
        t_score = stats.t.ppf((1 + confidence) / 2, n - 1)
        margin_of_error = t_score * (duration_stats["std"] / np.sqrt(n))
        ci = (
            duration_stats["avg"] - margin_of_error,
            duration_stats["avg"] + margin_of_error
        )
    else:
        margin_of_error = ci = "N/A"

    return {
        "total_requests": total,
        "success_rate": f"{(success / total) * 100:.2f}%" if total > 0 else "0%",
        "error_rate": f"{(error / total) * 100:.2f}%" if total > 0 else "0%",
        "avg_duration": f"{duration_stats['avg']:.2f} ms" if n > 0 else "N/A",
        "min_duration": f"{duration_stats['min']:.2f} ms" if n > 0 else "N/A",
        "max_duration": f"{duration_stats['max']:.2f} ms" if n > 0 else "N/A",
        "std_duration": f"{duration_stats['std']:.2f} ms" if n > 0 else "N/A",
        "margin_of_error": f"{margin_of_error:.2f} ms" if isinstance(margin_of_error, float) else margin_of_error,
        "confidence_interval": f"({ci[0]:.2f} ms, {ci[1]:.2f} ms)" if isinstance(ci, tuple) else ci
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) not in [2, 3]:
        print("Uso: python3 analyze_logs.py <arquivo_log> [endpoint]")
        print("Exemplos:")
        print("  python3 analyze_logs.py collectors_action.log ADSB")
        print("  python3 analyze_logs.py web_clients_action.log flight_info/")
        sys.exit(1)

    log_file = sys.argv[1]
    endpoint = sys.argv[2] if len(sys.argv) == 3 else None

    df = parse_log(log_file)
    report = generate_report(df, endpoint_filter=endpoint)

    print(f"=== Relatório de Análise - {log_file} ===")
    if endpoint:
        print(f"Filtrado por endpoint: {endpoint}")

    for key, value in report.items():
        print(f"{key.ljust(20)}: {value}")