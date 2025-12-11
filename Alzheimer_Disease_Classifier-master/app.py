import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

from Utils.components import (
    create_header,
    create_info_banner,
    create_predict_button,
    create_footer,
    create_theme_toggle,
    get_all_feature_cards,
    create_chat_component,
)
from Utils.pages import create_navbar
from callbacks import register_callbacks

# Check for imbalanced-learn
try:
    import imblearn
except ImportError:
    print("WARNING: 'imbalanced-learn' is not installed. Run: pip install imbalanced-learn")

# Brain emoji favicon as base64 SVG
FAVICON = "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🧠</text></svg>"

def create_app():
    """Create and configure the Dash application."""

    # Initialize app with Bootstrap and Font Awesome
    application = dash.Dash(
        __name__,
        external_stylesheets=[
            dbc.themes.BOOTSTRAP,
            "https://use.fontawesome.com/releases/v6.4.2/css/all.css"
        ],
        suppress_callback_exceptions=True,
        title="Neuro ML - Alzheimer's Risk Assessment",
        update_title=None
    )

    # Set custom favicon
    application._favicon = FAVICON

    # Build layout with multi-page support
    application.layout = html.Div([
        # URL component for page routing and theme
        dcc.Location(id='url', refresh=False),
        dcc.Store(id='result-store'),

        # Animated Background
        html.Div(className="bg-animated"),

        # Theme Toggle Button (Fixed Position)
        create_theme_toggle(),

        # Chat Component
        create_chat_component(),

        # Navbar
        create_navbar(),

        # Page Content Container
        html.Div(id="page-content", style={"paddingTop": "80px"})

    ], id="main-container")

    # Register callbacks
    register_callbacks(application)

    return application


# Create app instance
app = create_app()
server = app.server  # For deployment (Gunicorn, etc.)

if __name__ == '__main__':
    app.run(debug=False)