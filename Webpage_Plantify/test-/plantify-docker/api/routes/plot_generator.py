import pandas as pd
import plotly.graph_objects as go

class PlotGenerator:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def generate(
        self,
        y_column: str,
        y_title: str,
        y_range: list,
        color: str,
        fillcolor: str = None,
        plot_type: str = "line",
        name: str = None,
        x_range: list = None,
        layout_updates: dict = None  # optional z. B. für bargap etc.
    ) -> str:
        if self.df.empty:
            return self._render_empty_figure()
        self.df = self.df.sort_values(by="created")
        self.df = self.df.drop_duplicates(subset="created")
        fig = go.Figure()
        x = self.df["created"]
        y = self.df[y_column]

        if plot_type == "bar":
            fig.add_trace(go.Bar(x=x, y=y, marker_color=color, name=name or y_title))
        else:
            scatter_kwargs = dict(
                x=x,
                y=y,
                mode='lines+markers',
                marker=dict(size=12),
                line=dict(color=color, width=4),
                name=name or y_title,
                hoverinfo='x+y'
            )
            if fillcolor:
                scatter_kwargs["fill"] = "tozeroy"
                scatter_kwargs["fillcolor"] = fillcolor

            fig.add_trace(go.Scatter(**scatter_kwargs))

        if x_range is None:
            x_range = [
                str(x.min().replace(hour=0, minute=0)),
                str(x.max().replace(hour=23, minute=59))
            ]

        layout = self.get_standard_layout(
            x_title="Zeit" if plot_type != "bar" else "Datum",
            y_title=y_title,
            y_range=y_range,
            x_range=x_range
        )

        if layout_updates:
            layout.update(layout_updates)

        fig.update_layout(layout)
        return fig.to_html(include_plotlyjs='cdn', config=dict(displayModeBar=False))

    @staticmethod
    def get_standard_layout(x_title: str, y_title: str, y_range=None, x_range=None) -> dict:
        return dict(
            xaxis=dict(
                title=x_title,
                tickformat="%H:%M",
                automargin=True,
                range=x_range if x_range else ["00:00", "23:59"],
                nticks=6
            ),
            yaxis=dict(
                title=y_title,
                showgrid=True,
                gridcolor="lightgrey",
                gridwidth=1,
                range=y_range
            ),
            plot_bgcolor="white",
            font=dict(family="Arial", size=14),
            margin=dict(l=40, r=20, t=40, b=40),
        )

    def _render_empty_figure(self, title="Keine Daten verfügbar") -> str:
        fig = go.Figure()
        fig.update_layout(
            title=title,
            xaxis=dict(title="Zeit"),
            yaxis=dict(title="Wert"),
            plot_bgcolor="white",
            font=dict(family="Arial", size=14),
            margin=dict(l=40, r=20, t=40, b=40),
        )
        return fig.to_html(include_plotlyjs='cdn', config=dict(displayModeBar=False))