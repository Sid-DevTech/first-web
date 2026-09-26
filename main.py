import streamlit as st
from google import genai
from dotenv import load_dotenv
import time
import urllib.parse

load_dotenv()

def progress_bar_ui():
    st.markdown("""
    <style>

    /* ================================
       ANIMATIONS
    ================================= */

    @keyframes floatIcon {
        0%, 100% {
            transform: translateY(0px) rotate(-4deg);
        }
        50% {
            transform: translateY(-8px) rotate(4deg);
        }
    }

    @keyframes glowRing {
        0%, 100% {
            opacity: 0.35;
            transform: scale(0.9);
        }
        50% {
            opacity: 0.8;
            transform: scale(1.3);
        }
    }

    @keyframes shimmerText {
        0% {
            background-position: 0% 50%;
        }
        100% {
            background-position: 200% 50%;
        }
    }

    @keyframes borderGlow {
        0%, 100% {
            box-shadow:
                0 0 10px rgba(0, 198, 255, 0.25),
                inset 0 0 20px rgba(0, 198, 255, 0.05);

            border-color: rgba(0, 198, 255, 0.3);
        }

        50% {
            box-shadow:
                0 0 26px rgba(0, 198, 255, 0.55),
                inset 0 0 30px rgba(0, 198, 255, 0.12);

            border-color: rgba(0, 198, 255, 0.6);
        }
    }

    @keyframes dotBounce {
        0%, 80%, 100% {
            transform: translateY(0);
            opacity: 0.4;
        }

        40% {
            transform: translateY(-5px);
            opacity: 1;
        }
    }

    @keyframes progressShimmer {
        0% {
            background-position: 0% 50%;
        }

        100% {
            background-position: 200% 50%;
        }
    }


    /* ================================
       THINKING BOX
    ================================= */

    .ai-thinking-box {
        display: flex !important;
        align-items: center !important;

        gap: 16px !important;

        background: rgba(15, 23, 42, 0.85) !important;

        border: 1px solid rgba(0, 198, 255, 0.3) !important;
        border-bottom: none !important;

        border-radius: 14px 14px 0 0 !important;

        padding: 18px 22px !important;

        margin-top: 15px !important;
        margin-bottom: 0 !important;

        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;

        animation: borderGlow 2.2s ease-in-out infinite !important;

        box-sizing: border-box !important;
    }


    /* ================================
       ICON
    ================================= */

    .icon-wrap {
        position: relative !important;

        display: flex !important;
        align-items: center !important;
        justify-content: center !important;

        width: 38px !important;
        height: 38px !important;

        flex-shrink: 0 !important;
    }

    .icon-wrap::before {
        content: "" !important;

        position: absolute !important;

        width: 38px !important;
        height: 38px !important;

        border-radius: 50% !important;

        background:
            radial-gradient(
                circle,
                rgba(0, 198, 255, 0.45) 0%,
                rgba(0, 198, 255, 0) 70%
            ) !important;

        animation: glowRing 2s ease-in-out infinite !important;
    }

    .ai-floating-icon {
        position: relative !important;

        font-size: 1.4rem !important;

        display: inline-block !important;

        animation: floatIcon 2.2s ease-in-out infinite !important;
    }


    /* ================================
       TEXT
    ================================= */

    .ai-text-wrap {
        display: flex !important;
        flex-direction: row !important;

        align-items: center !important;

        gap: 10px !important;
    }

    .ai-flicker-text {
        font-size: 1.05rem !important;

        font-weight: 600 !important;

        background:
            linear-gradient(
                90deg,
                #6FE3FF 0%,
                #00C6FF 30%,
                #FFFFFF 60%,
                #00C6FF 100%
            ) !important;

        background-size: 200% auto !important;

        -webkit-background-clip: text !important;
        background-clip: text !important;

        -webkit-text-fill-color: transparent !important;

        animation: shimmerText 2.5s linear infinite !important;
    }


    /* ================================
       THINKING DOTS
    ================================= */

    .thinking-dots {
        display: inline-flex !important;
        gap: 3px !important;
    }

    .thinking-dots span {
        width: 5px !important;
        height: 5px !important;

        border-radius: 50% !important;

        background: #00C6FF !important;

        box-shadow: 0 0 6px #00C6FF !important;

        animation: dotBounce 1.2s ease-in-out infinite !important;
    }

    .thinking-dots span:nth-child(2) {
        animation-delay: 0.15s !important;
    }

    .thinking-dots span:nth-child(3) {
        animation-delay: 0.3s !important;
    }

    """, unsafe_allow_html=True)

    
def ai_output():
    for word in output_text.split(" "):
        yield word + " "
        time.sleep(0.02)

def render_badge(text, color="#00C6FF", bg_color="rgba(0, 198, 255, 0.1)"):
    st.markdown(f"""
        <span style="
            background-color: {bg_color};
            color: {color};
            border: 1px solid {color};
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 10px;
        ">
            ● {text}
        </span>
    """, unsafe_allow_html=True)

def update_status(container, icon_emoji, text_message):
    """Renders a glowing status card: pulsing icon halo, shimmering text,
    and a small typing-indicator, inside an st.empty slot."""
    container.markdown(f"""
        <div class="ai-thinking-box">
            <div class="icon-wrap">
                <span class="ai-floating-icon">{icon_emoji}</span>
            </div>
            <div class="ai-text-wrap">
                <span class="thinking-dots"><span></span><span></span><span></span></span>
                <span class="ai-flicker-text">{text_message}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
def sidebar_ui():
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background: 
            /* Linear overlay to ensure white/light text and input labels stay legible */
            linear-gradient(180deg, rgba(15, 23, 42, 0.72) 0%, rgba(10, 15, 29, 0.85) 100%),
            /* Direct Pexels image link */
            url('https://images.pexels.com/photos/15011656/pexels-photo-15011656.jpeg') center/cover no-repeat fixed !important;
        border-right: 1px solid rgba(255, 255, 255, 0.12) !important;
    }

    /* Boost sidebar label contrast */
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] .stMarkdown {
        color: #F8FAFC !important;
        text-shadow: 0 1px 4px rgba(0, 0, 0, 0.8);
    }
    </style>
""", unsafe_allow_html=True)

def brand_logo_name():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');
    
        .sidebar-brand-perfect {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 10px !important;
            width: 100% !important;
            margin-top: -10px !important;
            margin-bottom: 20px !important;
        }
    
        .sidebar-brand-perfect .material-symbols-outlined {
            font-size: 2.4rem !important;      
            color: #FFFFFF !important;
            font-weight: 700 !important;
            display: inline-block !important;
        }
    
        .sidebar-brand-perfect .brand-text-solid {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
            font-size: 2.2rem !important;      
            font-weight: 800 !important;
            color: #FFFFFF !important;
            letter-spacing: -0.5px !important;
            line-height: 1 !important;
        }
        </style>
    """, unsafe_allow_html=True)
    st.markdown("""
            <div class="sidebar-brand-perfect">
                <span class="material-symbols-outlined">flight</span>
                <span class="brand-text-solid">Aero</span>
            </div>
        """, unsafe_allow_html=True)


def mainscreen_ui():
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: 
            /* Subtle dark overlay to keep foreground text legible */
            linear-gradient(180deg, rgba(15, 23, 42, 0.78) 0%, rgba(15, 23, 42, 0.88) 100%),
            /* Direct high-resolution Vernazza, Cinque Terre photo link */
            url('https://images.unsplash.com/photo-1516483638261-f4dbaf036963?auto=format&fit=crop&w=1920&q=80') center/cover no-repeat fixed;
    }
    </style>
""", unsafe_allow_html=True)

def metric_ui():
    st.markdown("""
    <style>
    /* 1. Ensure the parent container distributes columns evenly */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: wrap !important;
        gap: 16px !important;
        align-items: stretch !important;
    }

    /* 2. Equalize column flex sizing with a smart min-width */
    div[data-testid="column"] {
        flex: 1 1 0px !important;
        min-width: 180px !important;
    }

    /* 3. Metric Card Styling */
    div[data-testid="stMetric"] {
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.85) 0%, rgba(30, 41, 59, 0.75) 100%) !important;
        border: 1px solid rgba(0, 198, 255, 0.3) !important;
        border-radius: 14px !important;
        padding: 16px 20px !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        transition: all 0.3s ease-in-out !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
    }

    /* Hover Glow Effect */
    div[data-testid="stMetric"]:hover {
        border-color: rgba(0, 198, 255, 0.7) !important;
        box-shadow: 0 0 20px rgba(0, 198, 255, 0.25) !important;
        transform: translateY(-2px);
    }

    /* Plain White Label */
    div[data-testid="stMetricLabel"] p {
        color: #FFFFFF !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.8px !important;
        white-space: nowrap !important;
    }

    /* Plain White Value without Ellipses Truncation */
    div[data-testid="stMetricValue"] div {
        font-size: 1.45rem !important;
        font-weight: 800 !important;
        color: #FFFFFF !important;
        background: none !important;
        -webkit-text-fill-color: #FFFFFF !important;
        white-space: nowrap !important;
        overflow: visible !important;
        text-overflow: clip !important;
    }
    </style>
""", unsafe_allow_html=True)
    
def hover_ui():
    st.markdown("""
        <style>
        /* Reset any custom cursor overrides back to standard pointers */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            cursor: default !important;
        }

        button, a, input, select, [role="button"], [data-testid="stMetric"] {
            cursor: pointer !important;
        }
        </style>

        <script>
        (function() {
            try {
                const parentDoc = window.parent.document;
                let spotlight = parentDoc.getElementById('aero-spotlight-layer');

                // 1. Inject global glow layer into parent body if missing
                if (!spotlight) {
                    spotlight = parentDoc.createElement('div');
                    spotlight.id = 'aero-spotlight-layer';
                    spotlight.style.cssText = `
                        position: fixed;
                        top: 0;
                        left: 0;
                        width: 100vw;
                        height: 100vh;
                        pointer-events: none !important;
                        z-index: 999999;
                        mix-blend-mode: screen;
                        transition: background 0.015s linear;
                    `;
                    parentDoc.body.appendChild(spotlight);
                }

                const radius = 300; // Spotlight radius in pixels

                // 2. Remove existing listener before re-attaching (prevents duplication on reruns)
                if (window.parent._aeroMouseTracker) {
                    parentDoc.removeEventListener('mousemove', window.parent._aeroMouseTracker);
                }

                // 3. Define and store global mouse tracker
                window.parent._aeroMouseTracker = function(e) {
                    spotlight.style.background = `radial-gradient(
                        ${radius}px circle at ${e.clientX}px ${e.clientY}px, 
                        rgba(0, 198, 255, 0.28) 0%, 
                        rgba(0, 114, 255, 0.10) 45%, 
                        transparent 100%
                    )`;
                };

                parentDoc.addEventListener('mousemove', window.parent._aeroMouseTracker);
            } catch (err) {
                console.warn("Aero Spotlight: Iframe sandbox restriction fallback active.", err);
            }
        })();
        </script>
    """, unsafe_allow_html=True)
    

# def feedback_message():
#     st.markdown(f"""
#         <!-- Load canvas-confetti library -->
#         <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
        
#         <script>
#             // Fire custom cyan & blue confetti burst on load
#             confetti({{
#                 particleCount: 80,
#                 spread: 70,
#                 origin: {{ y: 0.8 }},
#                 colors: ['#00C6FF', '#0072FF', '#FFFFFF', '#38BDF8']
#             }});
#         </script>

#         <style>
#         /* Smooth Slide-Up & Glow Entrance Animation */
#         @keyframes slideUpGlow {{
#             0% {{
#                 opacity: 0;
#                 transform: translateY(20px) scale(0.95);
#                 box-shadow: 0 0 0 rgba(0, 198, 255, 0);
#             }}
#             50% {{
#                 box-shadow: 0 8px 30px rgba(0, 198, 255, 0.4);
#             }}
#             100% {{
#                 opacity: 1;
#                 transform: translateY(0) scale(1);
#                 box-shadow: 0 4px 20px rgba(0, 198, 255, 0.2);
#             }}
#         }}

#         .animated-feedback-box {{
#             background: linear-gradient(135deg, rgba(15, 23, 42, 0.85) 0%, rgba(0, 114, 255, 0.15) 100%);
#             border: 1px solid rgba(0, 198, 255, 0.4);
#             border-radius: 14px;
#             padding: 18px 26px;
#             text-align: center;
#             margin-top: 15px;
#             backdrop-filter: blur(10px);
#             animation: slideUpGlow 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
#         }}

#         .animated-feedback-text {{
#             font-size: 1.1rem;
#             font-weight: 600;
#             background: linear-gradient(90deg, #00C6FF, #E0F7FA, #0072FF);
#             -webkit-background-clip: text;
#             background-clip: text;
#             -webkit-text-fill-color: transparent;
#             color: transparent;
#             letter-spacing: 0.2px;
#         }}
#         </style>

#         <div class="animated-feedback-box">
#             <span style="font-size: 1.2rem;">✨</span>
#             <span class="animated-feedback-text">
#                 {user_msg}
#             </span>
#             <span style="font-size: 1.2rem;">✨</span>
#         </div>
#     """, unsafe_allow_html=True) 

def pages_ui():
    st.markdown("""
    <style>
    /* Style st.page_link and st.download_button globally */
    div[data-testid="stPageLink"] a, 
    div[data-testid="stDownloadButton"] > button {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.8) 0%, rgba(30, 41, 59, 0.8) 100%) !important;
        border: 1px solid rgba(0, 198, 255, 0.35) !important;
        color: #FFFFFF !important;
        border-radius: 12px !important;
        padding: 10px 18px !important;
        transition: all 0.3s ease-in-out !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
    }

    /* Hover effect with Cyan glow */
    div[data-testid="stPageLink"] a:hover, 
    div[data-testid="stDownloadButton"] > button:hover {
        border-color: #00C6FF !important;
        box-shadow: 0 0 15px rgba(0, 198, 255, 0.4) !important;
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allow_html=True)

if "itinerary_response" not in st.session_state:
    st.session_state.itinerary_response = None

if "locations_data" not in st.session_state:
    st.session_state.locations_data = None

# Progress bar UI
progress_bar_ui()



with st.sidebar:
    sidebar_ui()

    brand_logo_name()

    
    st.divider()
    st.pills("Status", ["🟢 Ready to Explore", "⚡ Gemini Powered"], selection_mode="multi")   
    location = st.text_input("Where are you planning to go? ",placeholder="e.g. Paris, Spain, France")
    days_number = st.slider("Number of days to plan the trip", min_value=1, max_value=30, value=1)
    budget = st.selectbox("What's your budget?", ("Luxury", "Moderate", "Budgeted"))
    trip_plan = st.radio("Who are you planning to go with?", ["Family", "Friends", "Solo", "Partner"])
    plan_btn = st.button("Plan trip", type="primary", use_container_width=True)
    date_time = st.date_input("Schedule your trip")



st.title("Aero Destination Dashboard", icon=":material/flight:")
st.caption("Your Personal Trip Assistant")
st.set_page_config(page_title="Aero Travel", page_icon="✈️", layout="wide")
hover_ui()
mainscreen_ui()
metric_ui()


col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Destination 🗺️", value=location if location else "Not Set", border=True, width="stretch")
with col2:
    st.metric(label="Duration ⏱️", value=f"{days_number} Days", border=True)
with col3:
    st.metric(label="Trip type", value=f"{trip_plan}", border=True)
with col4:
    st.metric(label="Budget 💰", value=f"{budget}", border=True, width="stretch")

col1,col2 = st.columns([1,1],gap="medium")
pages_ui()
with col1:
    view_itinerary = st.page_link(
    "main.py",
    label="View Full Itinerary",
    icon=":material/map:",
    use_container_width=True
)
with col2:
    raw_itinerary= st.session_state.get("itinerary_response")
    itinerary_text= raw_itinerary if raw_itinerary else "No Itinerary Generated yet"
    location_name= st.session_state.get("locations_data") or "trip"
    st.download_button(label="Download Plan",
    data=itinerary_text,
    file_name=f"Aero_Itinerary_{location_name}.txt",
    mime="text/plain",
    icon=":material/file_download:",
    use_container_width=True)
    disabled= (not raw_itinerary)
st.divider()

prompt = f"""
You are an expert, date-conscious travel planner. Plan a detailed {days_number}-day trip to {location} for {trip_plan}.

TRIP CONTEXT & SEASONAL INTELLIGENCE:
- Start Date: {date_time}
- Budget Level: {budget}
- Tailor activities strictly to the typical weather, climate, daylight hours, and local seasonal events in {location} during {date_time}.

Provide your response in EXACTLY three sections as formatted below:

SECTION 1 - ITINERARY:
For each day of the trip, follow this exact structure:

### Day X: [Catchy Day Title] ([Exact Date] - [Day of Week])
* **Morning:** [Detailed morning activity with specific places, entry tips, and best times to visit]
* **Afternoon:** [Detailed afternoon activity, nearby lunch spots, and transit advice]
* **Evening:** [Nightlife, dinner recommendations tailored to a {budget} budget, or relaxed evening walks]
* **💡 Local & Date Tip:** [Date-conscious advice e.g., crowd warnings, advanced booking requirements, or seasonal opening hours]

---

SECTION 2 - LOCATIONS:
Provide a single line containing ONLY key place names separated by commas for mapping.
Example: Zócalo, Palacio de Bellas Artes, Casa Azul Frida Kahlo Museum

SECTION 3 - COSTS:
Provide an itemized cost estimate for this entire {days_number}-day trip in {location} for a {budget} budget.
Return ONLY four lines in this exact format:
Accommodation: $X
Food & Dining: $Y
Activities & Tickets: $Z
Local Transit: $W
"""


if plan_btn:
    if not location:
        st.warning("Please enter a destination in the sidebar.")
    else:
        status_box = st.empty()
        progress_bar = st.progress(0)

        update_status(status_box, "🔍", f"Analyzing preferences for {location}")
        for p in range(0, 36):
            time.sleep(0.3)
            progress_bar.progress(p, text=f"{p}%")

        update_status(status_box, "✈️", f"Mapping top spots across {days_number} days")
        for p in range(36, 71):
            time.sleep(0.3)
            progress_bar.progress(p, text=f"{p}%")

        update_status(status_box, "🗓️", "Building your custom itinerary")
        for p in range(71, 96):
            time.sleep(0.2)
            progress_bar.progress(p, text=f"{p}%")

    
        client = genai.Client()
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        progress_bar.progress(100, text="100%")
        time.sleep(0.2)
        progress_bar.empty()
        status_box.empty()

       
        st.session_state.itinerary_response = response.text
        st.session_state.locations_data = location

   
if st.session_state.itinerary_response:
    output_text = st.session_state.itinerary_response
    saved_location = st.session_state.locations_data

    st.subheader("Route & Daily Itinerary", icon="🗺️")

    with st.container():
        st.caption("Interactive Map View")
        if "SECTION 2 - LOCATIONS:" in output_text:
            raw_locations = output_text.split("SECTION 2 - LOCATIONS:")[1].split("SECTION 3 - COSTS:")[0].strip()
            query = urllib.parse.quote(f"{raw_locations} in {saved_location}")
            map_url = f"https://maps.google.com/maps?q={query}&t=&z=12&ie=UTF8&iwloc=&output=embed"
            st.iframe(map_url, height=400)

    st.success(f"🎉 Awesome! Your custom guide for **{saved_location}** is ready below.")

    st.subheader("Trip Essentials And Tools")
    with st.expander("Recommended Packing Checklist", expanded=False):
        st.checkbox("Universal Power Adapter", key="chk_adapter")
        st.checkbox("Travel Assurance Documents", key="chk_docs")
        st.checkbox("Comfortable Walking Shoes", key="chk_shoes")

    if "SECTION 3 - COSTS:" in output_text:
        cost_text = output_text.split("SECTION 3 - COSTS:")[1].strip()
        costs = {}
        for line in cost_text.split("\n"):
            if ":" in line:
                category, val = line.split(":", 1)
                costs[category.strip()] = val.strip()

        with st.expander("💵 Estimated Cost Breakdown", expanded=False):
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Accommodation", costs.get("Accommodation", "N/A"))
            c2.metric("Food & Dining", costs.get("Food & Dining", "N/A"))
            c3.metric("Activities", costs.get("Activities & Tickets", "N/A"))
            c4.metric("Local Transit", costs.get("Local Transit", "N/A"))        

    with st.expander("💡 Local Safety & Etiquette", expanded=False):
        st.info("Emergency Contact: 112 | Always carry cash for local vendors.") 

   
    if "SECTION 1 - ITINERARY:" in output_text:
        itinerary = output_text.split("SECTION 1 - ITINERARY:")[1].split("SECTION 2 - LOCATIONS:")[0].strip()
        st.markdown(itinerary)
    else:
        st.markdown(output_text)   

   
    st.text("How much did you like Aero?")
    feedback = st.feedback("faces")

    if feedback is not None:
        
        st.balloons()

        
        responses = {
            0: "We're sorry to hear that! We'll keep improving Aero for your next journey.",
            1: "Thanks for the feedback! We're constantly tuning Aero to serve you better.",
            2: "Thanks for checking out Aero! Wishing you a great trip ahead.",
            3: "Awesome! glad Aero helped plan your travel itinerary.",
            4: "Woohoo! Thanks for loving Aero! Safe travels on your upcoming adventure!"
        }
        user_msg = responses.get(feedback, "Thanks for exploring with Aero! Safe travels!")

        st.markdown(f"""
        <!-- Load canvas-confetti library -->
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
        
        <script>
            // Fire custom cyan & blue confetti burst on load
            confetti({{
                particleCount: 80,
                spread: 70,
                origin: {{ y: 0.8 }},
                colors: ['#00C6FF', '#0072FF', '#FFFFFF', '#38BDF8']
            }});
        </script>

        <style>
        /* Smooth Slide-Up & Glow Entrance Animation */
        @keyframes slideUpGlow {{
            0% {{
                opacity: 0;
                transform: translateY(20px) scale(0.95);
                box-shadow: 0 0 0 rgba(0, 198, 255, 0);
            }}
            50% {{
                box-shadow: 0 8px 30px rgba(0, 198, 255, 0.4);
            }}
            100% {{
                opacity: 1;
                transform: translateY(0) scale(1);
                box-shadow: 0 4px 20px rgba(0, 198, 255, 0.2);
            }}
        }}

        .animated-feedback-box {{
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.85) 0%, rgba(0, 114, 255, 0.15) 100%);
            border: 1px solid rgba(0, 198, 255, 0.4);
            border-radius: 14px;
            padding: 18px 26px;
            text-align: center;
            margin-top: 15px;
            backdrop-filter: blur(10px);
            animation: slideUpGlow 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }}

        .animated-feedback-text {{
            font-size: 1.1rem;
            font-weight: 600;
            background: linear-gradient(90deg, #00C6FF, #E0F7FA, #0072FF);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            color: transparent;
            letter-spacing: 0.2px;
        }}
        </style>

        <div class="animated-feedback-box">
            <span style="font-size: 1.2rem;">✨</span>
            <span class="animated-feedback-text">
                {user_msg}
            </span>
            <span style="font-size: 1.2rem;">✨</span>
        </div>
    """, unsafe_allow_html=True)