import dash
from dash import Input, Output, State, ALL, dcc, html
from Utils.chatbot_service import get_chat_response
from Utils.report_generator import generate_report
from config import FEATURE_GROUPS
from dash import html
import dash_bootstrap_components as dbc

def get_readable_data(input_data):
    """
    Converts model-friendly numeric data (0, 1) back to human-readable strings (Male, Female)
    based on the 'options' defined in config.py.
    """
    readable_data = input_data.copy()

    # 1. Build a lookup dictionary from your config
    # Structure will be: {'Gender': {0: 'Male', 1: 'Female'}, 'Smoking': {0: 'No', 1: 'Yes'}}
    value_mappings = {}

    for group in FEATURE_GROUPS.values():
        for feature in group['features']:
            # Only process features that have 'options' (Dropdowns/Radio buttons)
            if 'options' in feature:
                # Create a mini-dictionary for this feature mapping values to labels
                feature_map = {opt['value']: opt['label'] for opt in feature['options']}
                value_mappings[feature['name']] = feature_map

    # 2. Apply mappings to the input data
    for key, val in readable_data.items():
        if key in value_mappings:
            # Try to find the label for this value
            # We handle potential type mismatches (string "0" vs integer 0)
            try:
                # Check for exact match or try converting to int
                mapping = value_mappings[key]
                if val in mapping:
                    readable_data[key] = mapping[val]
                elif int(val) in mapping:
                    readable_data[key] = mapping[int(val)]
            except (ValueError, TypeError):
                # If conversion fails, keep original value
                continue

    return readable_data


def register_callbacks(app):
    """Register all callbacks for the app."""

    # Import here to avoid circular imports
    from Utils.model_handler import model_handler
    from Utils.components import create_result_card, create_error_alert
    from Utils.pages import create_home_page, create_tips_page

    # Import assessment page creator from app module
    def get_assessment_page():
        from Utils.components import (
            create_header, create_info_banner, create_predict_button,
            create_footer, get_all_feature_cards
        )

        return html.Div([
            dbc.Container([
                create_header(),
                create_info_banner(),
                html.Div(get_all_feature_cards()),
                create_predict_button(),
                dbc.Row([
                    dbc.Col([
                        dbc.Spinner(
                            html.Div(id="prediction-output"),
                            color="primary",
                            spinner_style={"width": "3rem", "height": "3rem"}
                        )
                    ], xs=12, md=10, lg=8, className="mx-auto")
                ]),
                create_footer()
            ], fluid=True, style={"maxWidth": "1200px"})
        ], style={"paddingBottom": "3rem"})

    # --- Page Routing Callback ---
    @app.callback(
        Output("page-content", "children"),
        Input("url", "pathname")
    )
    def display_page(pathname):
        """Handle page routing based on URL."""
        if pathname == "/assessment":
            return get_assessment_page()
        elif pathname == "/tips":
            return create_tips_page()
        else:  # Default to home page
            return create_home_page()

    # --- Navbar Toggle for Mobile ---
    @app.callback(
        Output("navbar-collapse", "is_open"),
        Input("navbar-toggler", "n_clicks"),
        State("navbar-collapse", "is_open"),
    )
    def toggle_navbar_collapse(n_clicks, is_open):
        """Toggle navbar collapse on mobile."""
        if n_clicks:
            return not is_open
        return is_open

    # --- Prediction Callback ---
    @app.callback(
        Output("prediction-output", "children"),
        Output("result-store", "data"),
        Input("predict-btn", "n_clicks"),
        State({'type': 'input-field', 'index': ALL}, 'value'),
        State({'type': 'input-field', 'index': ALL}, 'id'),
        prevent_initial_call=True
    )
    def predict_disease(n_clicks, values, ids):
        """Handle prediction when button is clicked."""

        if not n_clicks:
            return dash.no_update, dash.no_update

        if not model_handler.is_loaded():
            return create_error_alert(
                "Model file not found. Please ensure 'alzheimers_model_data.pkl' is in the directory."
            ), None

        try:
            input_data = model_handler.prepare_input(values, ids)
            result = model_handler.predict(input_data)

            return create_result_card(result), result

        except ValueError as e:
            return create_error_alert(str(e)), None
        except Exception as e:
            return create_error_alert(f"Prediction Error: {str(e)}", color="warning"), None

    # Download Report
    @app.callback(
        Output("download-pdf-component", "data"),
        Input("btn-download-pdf", "n_clicks"),
        State('result-store', 'data'),
        State({'type': 'input-field', 'index': ALL}, 'value'),
        State({'type': 'input-field', 'index': ALL}, 'id'),
        prevent_initial_call=True
    )
    def download_report(n_clicks, result, values, ids):
        # 1. Prepare data for the MODEL (keep as numbers)
        input_data = model_handler.prepare_input(values, ids)

        # 2. Prepare data for the PDF REPORT (convert to strings)
        report_data = get_readable_data(input_data)

        # 3. Generate PDF using the readable data
        pdf_bytes = generate_report(report_data, result)

        return dcc.send_bytes(pdf_bytes, filename="neuropredict_report.pdf")

    # Updated Toggle Callback (Handles Visibility)
    @app.callback(
        [Output("chat-canvas", "is_open"),
         Output("chat-btn-wrapper", "style")],
        Input("open-chat", "n_clicks"),
        Input("close-chat-btn", "n_clicks"),
        [State("chat-canvas", "is_open"), State("chat-btn-wrapper", "style")],
    )
    def toggle_chat(n_clicks, close_btn, is_open, current_style):
        if n_clicks or close_btn:
            # If currently open, we are closing it -> Show button
            if is_open:
                current_style['display'] = 'block'
                return False, current_style

            # If currently closed, we are opening it -> Hide button
            else:
                current_style['display'] = 'none'
                return True, current_style

        return is_open, current_style

    # Handle Message Sending (Updated)
    @app.callback(
        [Output("chat-history", "children"), Output("user-msg", "value")],
        [Input("send-msg", "n_clicks"), Input("user-msg", "n_submit")],
        State("user-msg", "value"),
        State("chat-history", "children"),
        State({'type': 'input-field', 'index': ALL}, 'value'),
        State({'type': 'input-field', 'index': ALL}, 'id'),
        prevent_initial_call=True
    )
    def update_chat(n_clicks, n_submit, msg, history, form_values, form_ids):
        # Check if message is empty
        if not msg:
            return dash.no_update, ""

        if history is None:
            history = []

        # 1. Style User Message (Align Right)
        user_bubble = html.Div([
            html.Div(msg, style={
                "backgroundColor": "#e0e7ff", "color": "#333",
                "padding": "10px 15px", "borderRadius": "15px 15px 0 15px",
                "maxWidth": "85%", "alignSelf": "flex-end", "display": "inline-block"
            })
        ], style={"textAlign": "right", "width": "100%"})

        history.append(user_bubble)

        # 2. Get Context
        patient_context = {id_obj['index']: val for val, id_obj in zip(form_values, form_ids) if val}

        # 3. Call Gemini
        ai_text = get_chat_response(msg, patient_context)

        # 4. Style AI Message (Align Left)
        ai_bubble = html.Div([
            html.Div([
                html.I(className="fa-solid fa-robot me-2", style={"color": "var(--primary)"}),
                html.Span(ai_text)
            ], style={
                "backgroundColor": "#f3f4f6", "color": "#1f2937",
                "padding": "10px 15px", "borderRadius": "15px 15px 15px 0",
                "maxWidth": "90%", "display": "inline-block"
            })
        ], style={"textAlign": "left", "width": "100%"})

        history.append(ai_bubble)

        return history, ""

    # Handle Suggestion Chips
    @app.callback(
        Output("user-msg", "value", allow_duplicate=True),
        [Input("sugg-1", "n_clicks"), Input("sugg-2", "n_clicks"), Input("sugg-3", "n_clicks")],
        [State("sugg-1", "children"), State("sugg-2", "children"), State("sugg-3", "children")],
        prevent_initial_call=True
    )
    def populate_suggestion(n1, n2, n3, t1, t2, t3):
        ctx = dash.callback_context
        if not ctx.triggered:
            return dash.no_update

        # Get the text of the clicked badge
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == "sugg-1": return t1
        if button_id == "sugg-2": return t2
        if button_id == "sugg-3": return t3
        return ""

    # Smooth scroll callback for "Learn More" button
    app.clientside_callback(
        """
        function(n_clicks) {
            if (n_clicks) {
                const element = document.getElementById('about-section');
                if (element) {
                    element.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }
            return window.dash_clientside.no_update;
        }
        """,
        Output("scroll-to-about", "data-scroll"),
        Input("scroll-to-about", "n_clicks"),
        prevent_initial_call=True
    )

    # Theme toggle callback
    app.clientside_callback(
        """
        function(n_clicks) {
            // Get current theme
            const html = document.documentElement;
            const currentTheme = html.getAttribute('data-theme');

            // Toggle theme
            if (currentTheme === 'dark') {
                html.setAttribute('data-theme', 'light');
                localStorage.setItem('theme', 'light');
            } else {
                html.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
            }

            return window.dash_clientside.no_update;
        }
        """,
        Output("theme-toggle-btn", "data-theme-clicked"),
        Input("theme-toggle-btn", "n_clicks"),
        prevent_initial_call=True
    )

    # --- Initialize Theme on Page Load ---
    app.clientside_callback(
        """
        function(pathname) {
            // Check localStorage for saved theme preference
            const savedTheme = localStorage.getItem('theme');

            // Check system preference if no saved theme
            if (savedTheme) {
                document.documentElement.setAttribute('data-theme', savedTheme);
            } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                document.documentElement.setAttribute('data-theme', 'dark');
            }

            return window.dash_clientside.no_update;
        }
        """,
        Output("theme-toggle-btn", "data-theme-init"),
        Input("url", "pathname"),
        prevent_initial_call=False
    )