import plotly.express as px
import pandas as pd


def plot_embeddings(embeddings_2d, emojis, dimensions=(1600, 1200)):
    # Create a DataFrame with your data
    df = pd.DataFrame(
        {"x": embeddings_2d[:, 0], "y": embeddings_2d[:, 1], "emoji": emojis}
    )

    # Create an interactive scatter plot
    fig = px.scatter(
        df, x="x", y="y", text="emoji", width=dimensions[0], height=dimensions[1]
    )

    # Update text properties
    fig.update_traces(textposition="middle center", textfont_size=20)

    # Remove axes and background
    fig.update_layout(
        showlegend=False,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor="white",
    )

    # Show the plot
    fig.show()
    fig.write_html("../emoji_map.html", include_plotlyjs="cdn")
    fig.write_image("screenshots/1000_random.png")
