import pandas as pd

def load_dataframe(path):
    if path.endswith(".csv"):
        return pd.read_csv(path)
    return pd.read_excel(path)


def build_chart_dataset(df, params):
    chart_type = params.get("chart_type")
    x = params.get("parameters", {}).get("x_axis")
    y = params.get("parameters", {}).get("y_axis")

    if chart_type in ("bar", "line"):
        grouped = df.groupby(x)[y].sum().reset_index()
        return {
            "type": chart_type,
            "x": grouped[x].tolist(),
            "y": grouped[y].tolist()
        }

    if chart_type == "pie":
        grouped = df.groupby(x).size().reset_index(name="count")
        return {
            "type": "pie",
            "labels": grouped[x].tolist(),
            "values": grouped["count"].tolist()
        }

    if chart_type == "scatter":
        return {
            "type": "scatter",
            "x": df[x].tolist(),
            "y": df[y].tolist()
        }

    return {"error": "Unsupported chart type"}
