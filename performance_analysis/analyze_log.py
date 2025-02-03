import pandas as pd
from scipy import stats
from datetime import datetime
import numpy as np

def parse_log(log_file: str):
    data = []
    with open(log_file, "r") as f:
        for line in f:
            parts = line.strip().split(" | ")
            if len(parts) < 4:
                continue
            
            message = parts[3]

            if "HELLO" in message or "ADSB" in message:
                msg_parts = message.split(",")
                req_type = msg_parts[0]
                status = msg_parts[1]
                duration = float(msg_parts[2])
                data.append({
                    "type": req_type,
                    "status": status,
                    "duration": duration
                })
    return pd.DataFrame(data)

def generate_report(df: pd.DataFrame):
    if df.empty:
        print("Nenhum dado encontrado.")
        return
    
    df["is_success"] = df["status"].apply(lambda x: x.startswith("2") if isinstance(x, str) else False)
    
    total = len(df)
    success = df["is_success"].sum()
    error = total - success

    mean_duration = df["duration"].mean()
    std_duration = df["duration"].std()
    n = len(df)

    confidence = 0.95
    z_score = stats.norm.ppf((1 + confidence) / 2)
    margin_of_error = z_score * (std_duration / np.sqrt(n))

    confidence_interval = (mean_duration - margin_of_error, mean_duration + margin_of_error)

    return {
        "total_requests": total,
        "success_rate": f"{(success / total) * 100:.2f}%",
        "error_rate": f"{(error / total) * 100:.2f}%",
        "avg_duration": f"{mean_duration:.2f} ms",
        "min_duration": f"{df['duration'].min():.2f} ms",
        "max_duration": f"{df['duration'].max():.2f} ms",
        "std_duration": f"{std_duration:.2f} ms",
        "margin_of_error": f"{margin_of_error:.2f} ms",
        "confidence_interval": f"({confidence_interval[0]:.2f} ms, {confidence_interval[1]:.2f} ms)"
    }

if __name__ == "__main__":
    df = parse_log("collectors_action.log")
    report = generate_report(df)
    
    print("=== Relatório de Requisições HTTP ===")
    for key, value in report.items():
        print(f"{key}: {value}")