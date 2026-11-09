"""Design system shared by all devtheory Streamlit apps (apps/*).

Palette, chart layout and display helpers, so every app looks and behaves the same.
The categorical palette is the validated, colour-blind-safe set used since D-027;
change colours here only after re-running the dataviz palette validator.
"""
import streamlit as st

# Ink and surfaces
INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
AXIS = "#c3c2b7"

# Categorical palette, fixed order (never cycled)
CATEGORICAL = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6"]

# Roles
C_HIGHLIGHT, C_CONTEXT = "#2a78d6", "#c3c2b7"
STATUS = {"good": "#0ca30c", "warning": "#fab219", "critical": "#d03b3b"}

AUTHOR = "Prepared by Paul Wander, Division of Production, Productivity and Management, UN-ECLAC."


def base_layout(fig, title=None, ytitle=None, xtitle=None, height=420, legend=True):
    """Common Plotly layout: quiet axes and grid, horizontal legend above the plot."""
    fig.update_layout(
        title=dict(text=title, font=dict(size=15, color=INK), x=0, xanchor="left") if title else None,
        height=height, margin=dict(l=10, r=10, t=50 if title else 20, b=10),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="system-ui, -apple-system, Segoe UI, sans-serif", size=12, color=INK2),
        hoverlabel=dict(font_size=12), showlegend=legend,
        legend=dict(orientation="h", yanchor="bottom", y=1.0, xanchor="left", x=0, title=None),
        bargap=0.25,
    )
    fig.update_xaxes(title=xtitle, showgrid=False, linecolor=AXIS, ticks="outside",
                     tickcolor=AXIS, zeroline=False)
    fig.update_yaxes(title=ytitle, gridcolor=GRID, gridwidth=1, zeroline=True,
                     zerolinecolor=AXIS, zerolinewidth=1, linecolor="rgba(0,0,0,0)")
    return fig


def show(fig, table=None, caption=None, key=None):
    """Render a chart with an optional caption and a data-table view (every chart has one)."""
    fig.update_traces(cliponaxis=False, selector=dict(type="scatter"))
    fig.update_traces(cliponaxis=False, selector=dict(type="bar"))
    st.plotly_chart(fig, width="stretch", config={"displaylogo": False}, key=key)
    if caption:
        st.caption(caption)
    if table is not None:
        with st.expander("Data table"):
            st.dataframe(table, width="stretch", hide_index=True)


def fmt_k(x):
    return f"{x/1000:,.1f}k"


def credit(sources: str):
    """Standard footer: author line and sources."""
    st.divider()
    st.caption(AUTHOR)
    st.caption(sources)
