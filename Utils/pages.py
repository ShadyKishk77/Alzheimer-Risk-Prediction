# pages.py - Page layouts and navigation components

from dash import html, dcc
import dash_bootstrap_components as dbc


def create_navbar():
    """Create the navigation bar."""
    return dbc.Navbar(
        dbc.Container([
            # Brand
            dbc.NavbarBrand([
                html.I(className="fa-solid fa-brain me-2"),
                "Neuro ML"
            ], href="/", className="fs-4 fw-bold"),

            # Toggler for mobile
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),

            # Collapsible nav items
            dbc.Collapse(
                dbc.Nav([
                    dbc.NavItem(dbc.NavLink([
                        html.I(className="fa-solid fa-house me-2"),
                        "Home"
                    ], href="/", id="nav-home", className="nav-link-custom")),
                    dbc.NavItem(dbc.NavLink([
                        html.I(className="fa-solid fa-notes-medical me-2"),
                        "Assessment"
                    ], href="/assessment", id="nav-assessment", className="nav-link-custom")),
                    dbc.NavItem(dbc.NavLink([
                        html.I(className="fa-solid fa-heart-pulse me-2"),
                        "Health Tips"
                    ], href="/tips", id="nav-tips", className="nav-link-custom")),
                ], className="ms-auto", navbar=True),
                id="navbar-collapse",
                navbar=True,
            ),
        ], fluid=True),
        color="primary",
        dark=True,
        className="navbar-custom shadow-lg",
        sticky="top",
    )


def create_home_page():
    """Create the home page with engaging visuals."""
    return html.Div([
        # Hero Section
        html.Div([
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.H1([
                                html.Span("Predicting ", className="text-gradient"),
                                html.Span("Alzheimer's Risk", className="text-white"),
                                html.Br(),
                                html.Span("with AI", className="text-gradient")
                            ], className="hero-title"),
                            html.P(
                                "Advanced machine learning technology to assess Alzheimer's disease risk and empower early intervention.",
                                className="hero-subtitle mt-4"
                            ),
                            html.Div([
                                dbc.Button([
                                    html.I(className="fa-solid fa-wand-magic-sparkles me-2"),
                                    "Start Assessment"
                                ], href="/assessment", size="lg", className="hero-btn me-3"),
                                dbc.Button([
                                    html.I(className="fa-solid fa-circle-info me-2"),
                                    "Learn More"
                                ], outline=True, color="light", size="lg", className="hero-btn-outline",
                                    id="scroll-to-about")
                            ], className="mt-4")
                        ], className="hero-content")
                    ], md=6, className="d-flex align-items-center"),
                    dbc.Col([
                        html.Div([
                            html.Div(className="brain-visual-container", children=[
                                html.I(className="fa-solid fa-brain brain-icon-large"),
                                html.Div(className="pulse-ring pulse-ring-1"),
                                html.Div(className="pulse-ring pulse-ring-2"),
                                html.Div(className="pulse-ring pulse-ring-3"),
                            ])
                        ])
                    ], md=6, className="d-flex align-items-center justify-content-center")
                ])
            ], fluid=True)
        ], className="hero-section"),

        # Statistics Section
        html.Div([
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.I(className="fa-solid fa-users stat-icon"),
                            html.H3("50M+", className="stat-number"),
                            html.P("People affected worldwide", className="stat-label")
                        ], className="stat-card")
                    ], md=4),
                    dbc.Col([
                        html.Div([
                            html.I(className="fa-solid fa-chart-line stat-icon"),
                            html.H3("95%", className="stat-number"),
                            html.P("Model accuracy rate", className="stat-label")
                        ], className="stat-card")
                    ], md=4),
                    dbc.Col([
                        html.Div([
                            html.I(className="fa-solid fa-clock stat-icon"),
                            html.H3("<2 min", className="stat-number"),
                            html.P("Quick assessment time", className="stat-label")
                        ], className="stat-card")
                    ], md=4),
                ])
            ])
        ], className="stats-section", id="about-section"),

        # Features Section
        html.Div([
            dbc.Container([
                html.H2("Why Choose Neuro ML?", className="section-title text-center mb-5"),
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.Div([
                                html.I(className="fa-solid fa-robot feature-icon")
                            ], className="feature-icon-wrapper"),
                            html.H4("AI-Powered Analysis", className="feature-title"),
                            html.P(
                                "Utilizes Random Forest machine learning algorithm trained on thousands of clinical cases for accurate risk prediction.",
                                className="feature-description"
                            )
                        ], className="feature-box")
                    ], md=4, className="mb-4"),
                    dbc.Col([
                        html.Div([
                            html.Div([
                                # Changed icon to a brain to represent Alzheimer's/Neurology
                                html.I(className="fa-solid fa-brain feature-icon")
                            ], className="feature-icon-wrapper"),
                            html.H4("Early Detection", className="feature-title"),
                            html.P(
                                "Leverages advanced AI algorithms to identify subtle patterns and biomarkers, aiding in the early diagnosis of Alzheimer's disease.",
                                className="feature-description"
                            )
                        ], className="feature-box")
                    ], md=4, className="mb-4"),
                    dbc.Col([
                        html.Div([
                            html.Div([
                                html.I(className="fa-solid fa-shield-halved feature-icon")
                            ], className="feature-icon-wrapper"),
                            html.H4("Privacy First", className="feature-title"),
                            html.P(
                                "Your data is processed locally and never stored. Complete confidentiality and HIPAA-compliant practices.",
                                className="feature-description"
                            )
                        ], className="feature-box")
                    ], md=4, className="mb-4"),
                    dbc.Col([
                        html.Div([
                            html.Div([
                                html.I(className="fa-solid fa-file-pdf feature-icon")
                            ], className="feature-icon-wrapper"),
                            html.H4("Detailed Reports", className="feature-title"),
                            html.P(
                                "Generate comprehensive PDF reports you can share with healthcare providers for further consultation.",
                                className="feature-description"
                            )
                        ], className="feature-box")
                    ], md=4, className="mb-4"),
                    dbc.Col([
                        html.Div([
                            html.Div([
                                html.I(className="fa-solid fa-comments feature-icon")
                            ], className="feature-icon-wrapper"),
                            html.H4("AI Assistant", className="feature-title"),
                            html.P(
                                "Chat with our Gemini-powered medical assistant to understand your models_results_plots and get health recommendations.",
                                className="feature-description"
                            )
                        ], className="feature-box")
                    ], md=4, className="mb-4"),
                    dbc.Col([
                        html.Div([
                            html.Div([
                                html.I(className="fa-solid fa-mobile-screen feature-icon")
                            ], className="feature-icon-wrapper"),
                            html.H4("Accessible Anywhere", className="feature-title"),
                            html.P(
                                "Fully responsive design works seamlessly on desktop, tablet, and mobile devices for on-the-go access.",
                                className="feature-description"
                            )
                        ], className="feature-box")
                    ], md=4, className="mb-4"),
                ])
            ])
        ], className="features-section"),

        # How It Works Section
        html.Div([
            dbc.Container([
                html.H2("How It Works", className="section-title text-center mb-5"),
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.Div("1", className="step-number"),
                            html.H5("Enter data", className="step-title"),
                            html.P("Fill in demographic, lifestyle, and clinical information",
                                   className="step-description")
                        ], className="step-card")
                    ], md=3),
                    dbc.Col([
                        html.Div([
                            html.Div("2", className="step-number"),
                            html.H5("AI Analysis", className="step-title"),
                            html.P("Our model processes 35+ factors in milliseconds", className="step-description")
                        ], className="step-card")
                    ], md=3),
                    dbc.Col([
                        html.Div([
                            html.Div("3", className="step-number"),
                            html.H5("View Results", className="step-title"),
                            html.P("Get risk probability with detailed explanations", className="step-description")
                        ], className="step-card")
                    ], md=3),
                    dbc.Col([
                        html.Div([
                            html.Div("4", className="step-number"),
                            html.H5("Take Action", className="step-title"),
                            html.P("Download reports and consult healthcare professionals",
                                   className="step-description")
                        ], className="step-card")
                    ], md=3),
                ])
            ])
        ], className="how-it-works-section"),

        # CTA Section
        html.Div([
            dbc.Container([
                html.H2("Ready to Get Started?", className="text-center text-white mb-4"),
                html.P("Early detection can make all the difference. Take the first step today.",
                       className="text-center text-white mb-4", style={"fontSize": "1.2rem", "opacity": "0.9"}),
                html.Div([
                    dbc.Button([
                        html.I(className="fa-solid fa-arrow-right me-2"),
                        "Start Your Assessment"
                    ], href="/assessment", size="lg", color="light", className="cta-button")
                ], className="text-center")
            ])
        ], className="cta-section"),

        # Footer
        html.Div([
            dbc.Container([
                html.P([
                    "© 2025 Neuro ML • Built with ",
                    html.I(className="fa-solid fa-heart", style={"color": "#ef4444"}),
                    " using Machine Learning"
                ], className="text-center mb-0", style={"color": "var(--text-secondary)"})
            ])
        ], className="py-4")
    ])


def create_tips_page():
    """Create the health tips and exercises page."""

    exercises = [
        {
            "icon": "fa-brain",
            "title": "Brain Training Games",
            "description": "Engage in puzzles, crosswords, and memory games daily to keep your mind sharp.",
            "activities": ["Sudoku puzzles", "Chess or card games", "Learning a new language", "Memory matching games"],
            "color": "#6366f1"
        },
        {
            "icon": "fa-dumbbell",
            "title": "Physical Exercise",
            "description": "Regular aerobic exercise increases blood flow to the brain and promotes new neuron growth.",
            "activities": ["30 minutes of brisk walking", "Swimming or water aerobics", "Dancing classes",
                           "Yoga or Tai Chi"],
            "color": "#ec4899"
        },
        {
            "icon": "fa-utensils",
            "title": "Mediterranean Diet",
            "description": "A diet rich in omega-3s, antioxidants, and whole foods supports brain health.",
            "activities": ["Fatty fish 2-3x/week", "Leafy green vegetables", "Berries and nuts",
                           "Olive oil as primary fat"],
            "color": "#10b981"
        },
        {
            "icon": "fa-users",
            "title": "Social Engagement",
            "description": "Maintaining social connections and meaningful relationships protects cognitive function.",
            "activities": ["Join community groups", "Volunteer activities", "Regular family gatherings",
                           "Book clubs or hobby groups"],
            "color": "#f59e0b"
        },
        {
            "icon": "fa-bed",
            "title": "Quality Sleep",
            "description": "7-9 hours of sleep helps clear harmful proteins from the brain.",
            "activities": ["Consistent sleep schedule", "Dark, cool bedroom", "Limit screen time before bed",
                           "Relaxation techniques"],
            "color": "#8b5cf6"
        },
        {
            "icon": "fa-heart-pulse",
            "title": "Cardiovascular Health",
            "description": "What's good for your heart is good for your brain. Manage blood pressure and cholesterol.",
            "activities": ["Regular health check-ups", "Manage diabetes and hypertension", "Quit smoking",
                           "Limit alcohol intake"],
            "color": "#ef4444"
        }
    ]

    return html.Div([
        # Header Section
        html.Div([
            dbc.Container([
                html.H1([
                    html.I(className="fa-solid fa-heart-pulse me-3"),
                    "Brain Health & Lifestyle Tips"
                ], className="tips-page-title text-white text-center"),
                html.P(
                    "Evidence-based strategies to maintain cognitive health and reduce Alzheimer's risk",
                    className="tips-page-subtitle text-white text-center"
                )
            ])
        ], className="app-header mt-4"),

        # Main Content
        dbc.Container([
            # Introduction
            html.Div([
                dbc.Alert([
                    html.I(className="fa-solid fa-lightbulb me-2"),
                    html.Strong("Good News: "),
                    "Research shows that up to 40% of Alzheimer's cases may be preventable through lifestyle modifications. "
                    "The following strategies are backed by scientific evidence to support brain health at any age."
                ], color="info", className="tips-alert")
            ], className="my-4"),

            # Exercise Cards
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Div([
                            html.I(className=f"fa-solid {ex['icon']}",
                                   style={"fontSize": "2.5rem", "color": ex['color']})
                        ], className="tips-card-icon"),
                        html.H4(ex['title'], className="tips-card-title"),
                        html.P(ex['description'], className="tips-card-description"),
                        html.Hr(style={"borderColor": ex['color'], "borderWidth": "2px", "opacity": "0.3"}),
                        html.Div([
                            html.H6("Recommended Activities:", className="mb-3 fw-bold"),
                            html.Ul([
                                html.Li(activity, className="tips-activity-item")
                                for activity in ex['activities']
                            ], className="tips-activity-list")
                        ])
                    ], className="tips-exercise-card")
                ], md=6, lg=4, className="mb-4")
                for ex in exercises
            ]),

            # Daily Routine Section
            html.Div([
                html.H2("Sample Daily Brain-Healthy Routine", className="section-title text-center mt-5 mb-4"),
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.Div([
                                html.I(className="fa-solid fa-sun", style={"color": "#f59e0b", "fontSize": "2rem"}),
                                html.H5("Morning", className="mt-3 mb-3")
                            ]),
                            html.Ul([
                                html.Li("30-minute walk or exercise"),
                                html.Li("Healthy breakfast with berries and nuts"),
                                html.Li("Brain training puzzle (15 min)"),
                            ], className="routine-list")
                        ], className="routine-card")
                    ], md=4),
                    dbc.Col([
                        html.Div([
                            html.Div([
                                html.I(className="fa-solid fa-cloud-sun",
                                       style={"color": "#6366f1", "fontSize": "2rem"}),
                                html.H5("Afternoon", className="mt-3 mb-3")
                            ]),
                            html.Ul([
                                html.Li("Social activity or phone call"),
                                html.Li("Mediterranean-style lunch"),
                                html.Li("Learning activity (language, instrument)"),
                            ], className="routine-list")
                        ], className="routine-card")
                    ], md=4),
                    dbc.Col([
                        html.Div([
                            html.Div([
                                html.I(className="fa-solid fa-moon", style={"color": "#8b5cf6", "fontSize": "2rem"}),
                                html.H5("Evening", className="mt-3 mb-3")
                            ]),
                            html.Ul([
                                html.Li("Light dinner with family"),
                                html.Li("Reading or relaxing hobby"),
                                html.Li("7-9 hours quality sleep"),
                            ], className="routine-list")
                        ], className="routine-card")
                    ], md=4),
                ])
            ], className="routine-section mb-5"),

            # Resources Section
            html.Div([
                html.H2("Helpful Resources", className="section-title text-center mb-4"),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.I(className="fa-solid fa-book-medical mb-3",
                                       style={"fontSize": "2rem", "color": "#6366f1"}),
                                html.H5("Alzheimer's Association", className="card-title"),
                                html.P("Comprehensive information and support", className="card-text"),
                                dbc.Button("Visit Website", color="primary", outline=True,
                                           href="https://www.alz.org", target="_blank", className="btn-sm")
                            ])
                        ], className="resource-card text-center")
                    ], md=4),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.I(className="fa-solid fa-brain mb-3",
                                       style={"fontSize": "2rem", "color": "#ec4899"}),
                                html.H5("NIH Brain Health", className="card-title"),
                                html.P("Research-backed brain health tips", className="card-text"),
                                dbc.Button("Visit Website", color="primary", outline=True,
                                           href="https://www.nia.nih.gov/health", target="_blank", className="btn-sm")
                            ])
                        ], className="resource-card text-center")
                    ], md=4),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.I(className="fa-solid fa-user-doctor mb-3",
                                       style={"fontSize": "2rem", "color": "#10b981"}),
                                html.H5("Find a Specialist", className="card-title"),
                                html.P("Locate neurologists in your area", className="card-text"),
                                dbc.Button("Search", color="primary", outline=True,
                                           href="https://maps.google.com/", target="_blank", className="btn-sm")
                            ])
                        ], className="resource-card text-center")
                    ], md=4),
                ])
            ], className="resources-section mb-5"),

        ], className="py-5"),

        # Footer
        html.Div([
            dbc.Container([
                html.P([
                    "© 2025 Neuro ML • Built with ",
                    html.I(className="fa-solid fa-heart", style={"color": "#ef4444"}),
                    " using Machine Learning"
                ], className="text-center mb-0", style={"color": "var(--text-secondary)"})
            ])
        ], className="py-4")
    ])