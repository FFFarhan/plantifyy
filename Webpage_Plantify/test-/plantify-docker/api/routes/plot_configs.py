PLOT_CONFIGS = {
    "temperature": {
        "endpoint": "all-today",
        "config": lambda df: {
            "y_column": "temperature",
            "y_title": "Temperatur (°C)",
            "y_range": (
                [df["temperature"].min() - 1, df["temperature"].max() + 1]
                if "temperature" in df.columns and not df["temperature"].isna().all()
                else [0, 30]
             ),
            "color": "red",
            "fillcolor": "rgba(255, 0, 0, 0.15)",
            "name": "Temperatur"
        }
    },
    "soil": {
        "endpoint": "all-today",
        "config": lambda df: {
            "y_column": "soil_moisture",
            "y_title": "Bodenfeuchtigkeit (%)",
            "y_range": [0, 100],
            "color": "darkgreen",
            "fillcolor": "rgba(0,128,0,0.2)"
        }
    },
    "air": {
        "endpoint": "all-today",
        "config": lambda df: {
            "y_column": "air_humidity",
            "y_title": "Luftfeuchtigkeit (%)",
            "y_range": [0, 100],
            "color": "blue",
            "fillcolor": "rgba(0, 0, 255, 0.2)"
        }
    },
    "sunlight": {
        "endpoint": "sunlight-30days",
        "config": lambda df: {
            "y_column": "HoS",
            "y_title": "Sonnenstunden",
            "y_range": [0, df["HoS"].max() + 1] if "HoS" in df and not df["HoS"].isnull().all() else [0, 10],
            "color": "orange",
            "fillcolor": "rgba(255, 165, 0, 0.2)",
            "plot_type": "bar",
            "layout_updates": {
                "bargap": 0.2,
                "xaxis": {"tickformat": "%d.%m"
                }
            }
        }
    }
}