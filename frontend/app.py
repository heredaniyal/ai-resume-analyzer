import streamlit as st  # Import Streamlit library - this is what builds our web app

# ---------------------------------------------------------------
# PAGE CONFIGURATION
# This must be the FIRST Streamlit command in the file
# Sets the browser tab title, icon, and layout style
# layout="wide" means the app uses the full width of the screen
# ---------------------------------------------------------------
st.set_page_config(
    page_title="AI Resume Analyzer",  # Text shown on browser tab
    page_icon="📄",                   # Emoji shown on browser tab
    layout="wide"                     # Use full screen width
)

# ---------------------------------------------------------------
# CUSTOM CSS STYLING
# st.markdown() lets us inject raw HTML/CSS into the page
# unsafe_allow_html=True is required to allow HTML tags
# We use this to style things Streamlit can't style by default
# ---------------------------------------------------------------
st.markdown("""
    <style>
        /* Main title styling - large, blue, centered */
        .main-title {
            font-size: 42px;
            font-weight: 700;
            color: #4F8BF9;
            text-align: center;
            margin-bottom: 0px;
        }

        /* Subtitle below the main title - smaller, gray, centered */
        .sub-title {
            font-size: 18px;
            color: #888888;
            text-align: center;
            margin-bottom: 30px;
        }

        /* The big score box shown after upload */
        .score-box {
            background-color: #1E1E2E;
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            border: 2px solid #4F8BF9;
        }

        /* The large score number (e.g. 76) inside score box */
        .score-number {
            font-size: 72px;
            font-weight: 800;
            color: #4F8BF9;
        }

        /* Section headers like "Strengths", "Areas to Improve" */
        .section-header {
            font-size: 20px;
            font-weight: 600;
            color: #4F8BF9;
            margin-top: 20px;
        }
        /* ---------------------------------------------------------------
           UPLOAD BUTTON HACK
           This hides Streamlit's default "200MB per file" text
           and replaces it with our own "10MB" text using CSS
        --------------------------------------------------------------- */

        /* Hide the original "200MB per file • PDF" text */
        [data-testid="stFileUploaderDropzoneInstructions"] div span {
            display: none !important;
        }

        /* Inject our own "10MB" text in its place using ::after */
        [data-testid="stFileUploaderDropzoneInstructions"] div::after {
            content: "10MB per file • PDF";
            font-size: 14px;
            color: #888888;
        }
            

        /* Each feedback tip card shown in results */
        .tip-box {
            background-color: #1E1E2E;
            border-left: 4px solid #4F8BF9;  /* Blue left border accent */
            padding: 12px 16px;
            border-radius: 8px;
            margin-bottom: 10px;
            color: #CCCCCC;
        }
    </style>
""", unsafe_allow_html=True)  # Must be True to allow HTML/CSS injection

# ---------------------------------------------------------------
# SIDEBAR
# Everything inside "with st.sidebar:" appears in the left panel
# This is where we put instructions and app info
# ---------------------------------------------------------------
with st.sidebar:

    # App logo image loaded from a URL
    st.image("https://cdn-icons-png.flaticon.com/512/942/942748.png", width=80)

    st.markdown("## 📄 Resume Analyzer")  # Sidebar heading
    st.markdown("---")                     # Horizontal line divider

    # Step-by-step instructions for the user
    st.markdown("### How it works:")
    st.markdown("1. 📤 Upload your resume PDF")
    st.markdown("2. 🤖 AI reads and analyzes it")
    st.markdown("3. 📊 Get your score out of 100")
    st.markdown("4. 💡 See tips to improve")
    st.markdown("---")

    # List of what the AI checks in the resume
    st.markdown("### What we check:")
    st.markdown("- ✅ Professional Summary")
    st.markdown("- ✅ Work Experience")
    st.markdown("- ✅ Skills Section")
    st.markdown("- ✅ Education")
    st.markdown("- ✅ Formatting & Keywords")
    st.markdown("---")

    # Footer info at the bottom of sidebar
    st.caption("Built for SOFTEC'26 AI Hackathon")
    st.caption("Team: Anwar | Fardeen | Daniyal")

# ---------------------------------------------------------------
# MAIN PAGE - TITLE SECTION
# st.markdown() with HTML lets us use our custom CSS classes
# ---------------------------------------------------------------
st.markdown('<p class="main-title">📄 AI Resume Analyzer</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Upload your resume and get an AI-powered score with actionable feedback</p>', unsafe_allow_html=True)

st.markdown("---")  # Horizontal divider line

# ---------------------------------------------------------------
# FILE UPLOAD SECTION
# st.columns([1,2,1]) splits the page into 3 columns
# The middle column (col2) is twice as wide as the side ones
# This centers the upload button on the page
# ---------------------------------------------------------------
col1, col2, col3 = st.columns([1, 2, 1])  # Create 3 columns, ratio 1:2:1

with col2:  # Everything below goes into the CENTER column only

    # ---------------------------------------------------------------
    # FILE UPLOADER WIDGET
    # type=["pdf"] means ONLY pdf files are accepted
    # The 10MB limit is set using the Streamlit config below
    # When a file is uploaded, it's stored in "uploaded_file"
    # If no file is uploaded, uploaded_file = None
    # ---------------------------------------------------------------
    uploaded_file = st.file_uploader(
        label="📤 Drop your Resume here (PDF only)",  # Label shown above button
        type=["pdf"],                                  # Only allow PDF files
        help="Make sure your file is in PDF format. Max size: 10MB"  # Tooltip text
    )

    # This caption appears visually right below the upload button
    # It clearly tells the user the 10MB limit
    st.caption("📎 PDF only · Maximum file size: 10MB")

    # ---------------------------------------------------------------
    # CONDITIONAL DISPLAY
    # "if uploaded_file is not None" means: only run this block
    # when the user has actually uploaded a file
    # ---------------------------------------------------------------
    if uploaded_file is not None:

        # Check file size - uploaded_file.size gives size in BYTES
        # 10MB = 10 * 1024 * 1024 = 10,485,760 bytes
        MAX_SIZE_MB = 10                          # Our limit in MB
        MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024  # Convert MB to bytes

        if uploaded_file.size > MAX_SIZE_BYTES:
            # File is too large - show error and stop here
            st.error(f"❌ File too large! Your file is {uploaded_file.size / (1024*1024):.1f}MB. Maximum allowed is {MAX_SIZE_MB}MB.")

        else:
            # File size is fine - proceed to show results
            st.success(f"✅ **{uploaded_file.name}** uploaded successfully!")  # Green success message
            st.markdown("---")  # Divider

            # ---------------------------------------------------------------
            # SCORE DISPLAY SECTION (Placeholder - real score comes from AI)
            # This is just a hardcoded "76" for now
            # Daniyal will replace this with the real AI score later
            # ---------------------------------------------------------------
            st.markdown('<p class="section-header">📊 Your Resume Score</p>', unsafe_allow_html=True)

            # HTML block for the score card with big number
            st.markdown("""
                <div class="score-box">
                    <div class="score-number">76<span style="font-size:32px; color:#888">/100</span></div>
                    <div style="color:#4F8BF9; font-size:20px; margin-top:8px;">Good Resume ⭐</div>
                    <div style="color:#888; font-size:14px; margin-top:6px;">
                        AI analysis will appear here
                    </div>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("---")

            # ---------------------------------------------------------------
            # FEEDBACK COLUMNS
            # Split result area into 2 equal columns: left and right
            # Left = Strengths (what's good)
            # Right = Areas to Improve (what needs fixing)
            # ---------------------------------------------------------------
            left, right = st.columns(2)  # Two equal columns

            with left:
                # GREEN section - things that are good in the resume
                st.markdown('<p class="section-header">✅ Strengths</p>', unsafe_allow_html=True)
                # Each tip-box is one piece of positive feedback
                # Daniyal's AI will fill these dynamically later
                st.markdown('<div class="tip-box">Strong education section detected</div>', unsafe_allow_html=True)
                st.markdown('<div class="tip-box">Good variety of skills listed</div>', unsafe_allow_html=True)
                st.markdown('<div class="tip-box">Consistent formatting throughout</div>', unsafe_allow_html=True)

            with right:
                # ORANGE/RED section - things that need improvement
                st.markdown('<p class="section-header">⚠️ Areas to Improve</p>', unsafe_allow_html=True)
                # Daniyal's AI will fill these dynamically later
                st.markdown('<div class="tip-box">Missing professional summary</div>', unsafe_allow_html=True)
                st.markdown('<div class="tip-box">No measurable achievements found</div>', unsafe_allow_html=True)
                st.markdown('<div class="tip-box">Weak action verbs detected</div>', unsafe_allow_html=True)

            st.markdown("---")

            # Info message reminding team this is still a placeholder UI
            st.info("🤖 This is a UI preview. Real AI analysis coming soon — Daniyal's job!")

    else:
        # ---------------------------------------------------------------
        # EMPTY STATE (shown when no file is uploaded yet)
        # This is what the user sees before they upload anything
        # It's an HTML block styled to look like a dashed drop zone
        # ---------------------------------------------------------------
        st.markdown("###")  # Small spacing gap
        st.markdown("""
            <div style="text-align:center; padding: 60px 20px; border: 2px dashed #4F8BF9;
                        border-radius: 15px; color: #888;">
                <div style="font-size: 60px;">📄</div>
                <div style="font-size: 22px; margin-top: 10px; color: #CCCCCC;">
                    Upload your resume to get started
                </div>
                <div style="font-size: 14px; margin-top: 8px;">
                    Supports PDF format only · Max 10MB
                </div>
            </div>
        """, unsafe_allow_html=True)