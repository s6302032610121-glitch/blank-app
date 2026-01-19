import streamlit as st
from openai import OpenAI
import pandas as pd
from anastruct import SystemElements
import plotly.graph_objects as go
import numpy as np

# Page config
st.set_page_config(page_title="StructureCAD AI", page_icon="🏗️", layout="wide")

# Custom CSS for a professional look
st.markdown("""
<style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- UI Helper Functions ---
def render_header():
    st.title("🏗️ StructureCAD AI")
    st.markdown("""
    Welcome to **StructureCAD AI**, your intelligent assistant for structural engineering.
    Analyze beams, trusses, and chat with an AI expert.
    """)

def initialize_chat():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am your StructureCAD AI assistant. How can I help you with your structural engineering project today?"}
        ]

# --- Main App ---
render_header()
initialize_chat()

# Sidebar - Configuration
with st.sidebar:
    st.header("Settings")
    openai_api_key = st.text_input("OpenAI API Key", type="password")

    st.divider()
    st.header("Project Configuration")
    unit_system = st.selectbox("Unit System", ["Metric (kN, m, cm)", "Imperial (kip, ft, in)"])

    st.divider()
    st.markdown("### About StructureCAD")
    st.info("StructureCAD is a detailed tool for structural analysis and design, powered by AI.")

    if st.button("Reset All Data"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

# Tabs for different modules
tab_chat, tab_beam, tab_truss, tab_concrete, tab_sections = st.tabs([
    "Chat Assistant",
    "Beam Analysis",
    "Truss Analysis",
    "RC Design",
    "Steel Sections"
])

# --- TAB 1: AI ASSISTANT ---
with tab_chat:
    st.subheader("Structural Engineering Chatbot")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a structural engineering question..."):
        if not openai_api_key:
            st.info("Please add your OpenAI API key in the sidebar to continue.", icon="🗝️")
        else:
            client = OpenAI(api_key=openai_api_key)
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            try:
                # Specialized System Prompt
                messages = [
                    {"role": "system", "content": """You are StructureCAD AI, a highly experienced senior structural engineer.
                    Your expertise covers:
                    - Finite Element Analysis (FEA) and classical structural mechanics.
                    - Design of Reinforced Concrete (RC) structures using ACI 318 and Thai EIT standards.
                    - Steel structure design according to AISC 360 (ASD/LRFD).
                    - Foundation and geotechnical engineering basics.

                    When answering:
                    1. Be precise, professional, and use engineering terminology correctly.
                    2. If the user asks for calculations, explain the formulas used (e.g., rho = As/bd).
                    3. Encourage the use of the 'Beam Analysis' and 'RC Design' tabs available in this application for specific numerical solvers.
                    4. Always prioritize structural safety and recommend consulting a licensed professional for real-world projects."""}
                ] + [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                )

                full_response = response.choices[0].message.content
                with st.chat_message("assistant"):
                    st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Error: {str(e)}")

# --- TAB 2: BEAM ANALYSIS ---
with tab_beam:
    unit_l = "m" if "Metric" in unit_system else "ft"
    unit_f = "kN" if "Metric" in unit_system else "kip"

    st.subheader(f"2D Beam Structural Analysis ({unit_f}, {unit_l})")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### Beam Geometry")
        span = st.number_input(f"Span Length ({unit_l})", min_value=1.0, value=5.0, step=0.5)

        st.divider()
        st.markdown("### Supports")
        support_type = st.selectbox("Support Type", ["Pin", "Roller", "Fixed"])
        support_pos = st.number_input(f"Support Position ({unit_l})", min_value=0.0, max_value=span, value=0.0, step=0.1)

        if st.button("Add Support"):
            if "supports" not in st.session_state: st.session_state.supports = []
            st.session_state.supports.append({"type": support_type, "pos": support_pos})

        if "supports" in st.session_state and st.session_state.supports:
            st.write("Current Supports:")
            for i, s in enumerate(st.session_state.supports):
                st.write(f"{i+1}. {s['type']} at {s['pos']}{unit_l}")
            if st.button("Clear Supports"):
                st.session_state.supports = []
                st.rerun()

        st.divider()
        st.markdown("### Loads")
        load_type = st.selectbox("Load Type", [f"Point Load ({unit_f})", f"UDL ({unit_f}/{unit_l})"])
        load_val = st.number_input("Load Magnitude (Negative for Downward)", value=-10.0, step=1.0)
        l_pos_start = st.number_input(f"Position Start ({unit_l})", min_value=0.0, max_value=span, value=span/2, step=0.1)
        l_pos_end = 0.0
        if "UDL" in load_type:
            l_pos_end = st.number_input(f"Position End ({unit_l})", min_value=l_pos_start, max_value=span, value=span, step=0.1)

        if st.button("Add Load"):
            if "loads" not in st.session_state: st.session_state.loads = []
            st.session_state.loads.append({"type": load_type, "val": load_val, "pos": l_pos_start, "end": l_pos_end})

        if "loads" in st.session_state and st.session_state.loads:
            st.write("Current Loads:")
            for i, l in enumerate(st.session_state.loads):
                if "UDL" in l['type']:
                    st.write(f"{i+1}. {l['type']}: {l['val']} from {l['pos']} to {l['end']}{unit_l}")
                else:
                    st.write(f"{i+1}. {l['type']}: {l['val']} at {l['pos']}{unit_l}")
            if st.button("Clear Loads"):
                st.session_state.loads = []
                st.rerun()

    with col2:
        st.markdown("### Visualization & Results")
        if "supports" in st.session_state and len(st.session_state.supports) >= 2:
            try:
                ss = SystemElements()
                # Create beam elements
                # To accurately place loads and supports, we split the beam at those points
                # and also add intermediate points for smooth UDL visualization.
                points = [0, span]
                for s in st.session_state.supports: points.append(s['pos'])
                for l in st.session_state.loads:
                    points.append(l['pos'])
                    if "UDL" in l['type']: points.append(l['end'])

                # Add intermediate points for smooth curves (especially for UDLs)
                points.extend(np.linspace(0, span, 51).tolist())
                points = sorted(list(set([round(p, 4) for p in points])))

                for i in range(len(points)-1):
                    if points[i+1] > points[i]:
                        ss.add_element(location=[[points[i], 0], [points[i+1], 0]])

                # Add supports
                for s in st.session_state.supports:
                    node_id = ss.find_node_id([s['pos'], 0])
                    if node_id:
                        if s['type'] == "Pin": ss.add_support_hinged(node_id)
                        elif s['type'] == "Roller": ss.add_support_roll(node_id)
                        elif s['type'] == "Fixed": ss.add_support_fixed(node_id)

                # Add loads
                for l in st.session_state.loads:
                    if "Point Load" in l['type']:
                        node_id = ss.find_node_id([l['pos'], 0])
                        if node_id:
                            ss.point_load(node_id, Fy=l['val'])
                    else: # UDL
                        # Find elements that fall under the UDL
                        for el_id in ss.element_map:
                            el = ss.element_map[el_id]
                            # Use a small tolerance for float comparison
                            if el.node_1.x >= (l['pos'] - 1e-4) and el.node_2.x <= (l['end'] + 1e-4):
                                ss.q_load(q=l['val'], element_id=el_id)

                ss.solve()

                # Plotly Plots
                fig_shear = go.Figure()
                fig_moment = go.Figure()

                # Extract results
                x_coords = []
                shear_vals = []
                moment_vals = []

                for el_id in ss.element_map:
                    el = ss.element_map[el_id]
                    res = ss.get_element_results(el_id)
                    x_coords.extend([el.node_1.x, el.node_2.x])
                    # Use Qmin/Qmax and Mmin/Mmax for simple visualization
                    # For more complex beams, anastruct discretizes and we'd need more points
                    shear_vals.extend([res['Qmin'], res['Qmax']])
                    moment_vals.extend([res['Mmin'], res['Mmax']])

                fig_shear.add_trace(go.Scatter(x=x_coords, y=shear_vals, fill='tozeroy', name="Shear (kN)"))
                fig_shear.update_layout(title="Shear Force Diagram (SFD)", xaxis_title="Position (m)", yaxis_title="Shear (kN)")

                fig_moment.add_trace(go.Scatter(x=x_coords, y=moment_vals, fill='tozeroy', name="Moment (kNm)"))
                fig_moment.update_layout(title="Bending Moment Diagram (BMD)", xaxis_title="Position (m)", yaxis_title="Moment (kNm)")

                st.plotly_chart(fig_shear, use_container_width=True)
                st.plotly_chart(fig_moment, use_container_width=True)

                st.success("Analysis Complete!")

                # Export Button
                export_data = []
                for node_id in ss.node_map:
                    res = ss.get_node_results(node_id)
                    export_data.append({
                        "Node": node_id,
                        "X": ss.node_map[node_id].x,
                        "Fx": res['Fx'],
                        "Fy": res['Fy'],
                        "M": res['M']
                    })
                df_export = pd.DataFrame(export_data)
                csv = df_export.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Analysis Report (CSV)", csv, "beam_analysis.csv", "text/csv")

                # Reactions
                st.markdown("#### Support Reactions")
                for node_id in ss.node_map:
                    node = ss.node_map[node_id]
                    if node.Fz: # For 2D beam, Fz might be used or reactions are in ss.get_node_results
                        res = ss.get_node_results(node_id)
                        if any([res['Fx'], res['Fy'], res['M']]):
                            st.write(f"Node {node_id} at {node.x}m: Fx={res['Fx']:.2f}kN, Fy={res['Fy']:.2f}kN, M={res['M']:.2f}kNm")

            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")
        else:
            st.warning("Please add at least 2 supports (e.g., Pin at 0m and Roller at 5m) to perform analysis.")

# --- TAB 3: TRUSS ANALYSIS ---
with tab_truss:
    st.subheader("2D Truss Analysis (Matrix Method)")
    st.markdown("Quickly define nodes and members to calculate axial forces.")

    truss_col1, truss_col2 = st.columns([1, 1])

    with truss_col1:
        st.markdown("#### 1. Define Nodes")
        nx = st.number_input("Node X (m)", value=0.0)
        ny = st.number_input("Node Y (m)", value=0.0)
        if st.button("Add Node"):
            if "t_nodes" not in st.session_state: st.session_state.t_nodes = []
            st.session_state.t_nodes.append([nx, ny])

        if "t_nodes" in st.session_state and st.session_state.t_nodes:
            st.write("Nodes:", pd.DataFrame(st.session_state.t_nodes, columns=["X", "Y"]))

    with truss_col2:
        st.markdown("#### 2. Define Members")
        if "t_nodes" in st.session_state and len(st.session_state.t_nodes) >= 2:
            n1 = st.selectbox("From Node", range(len(st.session_state.t_nodes)))
            n2 = st.selectbox("To Node", range(len(st.session_state.t_nodes)), index=min(1, len(st.session_state.t_nodes)-1))
            if st.button("Add Member"):
                if n1 == n2:
                    st.error("Member must connect two different nodes.")
                else:
                    if "t_members" not in st.session_state: st.session_state.t_members = []
                    st.session_state.t_members.append([n1, n2])

            if "t_members" in st.session_state and st.session_state.t_members:
                st.write("Members:", pd.DataFrame(st.session_state.t_members, columns=["Start Node", "End Node"]))
        else:
            st.info("Add at least 2 nodes to define members.")

    if "t_nodes" in st.session_state and len(st.session_state.t_nodes) >= 2 and "t_members" in st.session_state and len(st.session_state.t_members) >= 1:
        st.divider()
        st.markdown("#### 3. Truss Loads & Supports")
        t_col1, t_col2 = st.columns(2)
        with t_col1:
            t_node_sel = st.selectbox("Select Node ID", range(len(st.session_state.t_nodes)))
            t_sup_type = st.selectbox("Add Support", ["None", "Pin", "Roller"])
            if t_sup_type != "None":
                if st.button("Add Support to Node"):
                    if "t_supports" not in st.session_state: st.session_state.t_supports = []
                    st.session_state.t_supports.append({"node": t_node_sel, "type": t_sup_type})

            if "t_supports" in st.session_state and st.session_state.t_supports:
                st.write("Current Supports:")
                for i, s in enumerate(st.session_state.t_supports):
                    st.write(f"- Node {s['node']}: {s['type']}")
                if st.button("Clear Truss Supports"):
                    st.session_state.t_supports = []
                    st.rerun()

        with t_col2:
            t_fx = st.number_input("Load Fx (kN)", value=0.0, key="t_fx")
            t_fy = st.number_input("Load Fy (kN)", value=-10.0, key="t_fy")
            if st.button("Add Load to Node"):
                if "t_loads" not in st.session_state: st.session_state.t_loads = []
                st.session_state.t_loads.append({"node": t_node_sel, "fx": t_fx, "fy": t_fy})

            if "t_loads" in st.session_state and st.session_state.t_loads:
                st.write("Current Loads:")
                for i, l in enumerate(st.session_state.t_loads):
                    st.write(f"- Node {l['node']}: Fx={l['fx']}, Fy={l['fy']}")
                if st.button("Clear Truss Loads"):
                    st.session_state.t_loads = []
                    st.rerun()

        st.divider()
        if st.button("Solve Truss", type="primary"):
            try:
                ts = SystemElements()
                for mem in st.session_state.t_members:
                    p1 = st.session_state.t_nodes[mem[0]]
                    p2 = st.session_state.t_nodes[mem[1]]
                    ts.add_truss_element(location=[p1, p2])

                # Apply supports
                if "t_supports" in st.session_state:
                    for s in st.session_state.t_supports:
                        pos = st.session_state.t_nodes[s['node']]
                        nid = ts.find_node_id(pos)
                        if nid:
                            if s['type'] == "Pin": ts.add_support_hinged(nid)
                            elif s['type'] == "Roller": ts.add_support_roll(nid)

                # Apply loads
                if "t_loads" in st.session_state:
                    for l in st.session_state.t_loads:
                        pos = st.session_state.t_nodes[l['node']]
                        nid = ts.find_node_id(pos)
                        if nid:
                            ts.point_load(nid, Fx=l['fx'], Fy=l['fy'])

                ts.solve()

                # Helper to map anastruct node to user node index
                def get_user_node_id(an_node):
                    for i, n in enumerate(st.session_state.t_nodes):
                        if abs(n[0] - an_node.x) < 1e-3 and abs(n[1] - an_node.y) < 1e-3:
                            return i
                    return an_node.id

                # Visualization
                fig_truss = go.Figure()
                for el_id in ts.element_map:
                    el = ts.element_map[el_id]
                    res = ts.get_element_results(el_id)
                    force = res['axial']
                    color = "red" if force < -1e-3 else ("blue" if force > 1e-3 else "gray")

                    u1 = get_user_node_id(el.node_1)
                    u2 = get_user_node_id(el.node_2)

                    fig_truss.add_trace(go.Scatter(
                        x=[el.node_1.x, el.node_2.x],
                        y=[el.node_1.y, el.node_2.y],
                        mode='lines+markers+text',
                        line=dict(color=color, width=min(abs(force)/5 + 2, 10)),
                        text=[f"N{u1}", f"N{u2}"],
                        textposition="top center",
                        name=f"Mem {el_id}: {force:.2f} kN"
                    ))
                fig_truss.update_layout(title="Truss Force Analysis (Blue: Tension, Red: Compression)")
                st.plotly_chart(fig_truss, use_container_width=True)

                # Results Table
                truss_results = []
                for el_id in ts.element_map:
                    res = ts.get_element_results(el_id)
                    truss_results.append({"Member": el_id, "Force (kN)": round(res['axial'], 3)})
                st.table(pd.DataFrame(truss_results))

            except Exception as e:
                st.error(f"Truss Analysis failed: {str(e)}")
                st.info("💡 Hint: Ensure the truss is stable (e.g., at least one Pin and one Roller support) and all nodes are connected.")

    if st.button("Reset Truss Data"):
        st.session_state.t_nodes = []
        st.session_state.t_members = []
        st.session_state.t_supports = []
        st.session_state.t_loads = []
        st.rerun()

# --- TAB 4: RC DESIGN ---
with tab_concrete:
    st.subheader("Reinforced Concrete Design")
    rc_sub_tab = st.radio("Component Type", ["Beam Design", "Column Design (Axial)", "One-way Slab"], horizontal=True)

    if rc_sub_tab == "Beam Design":
        st.markdown("### Rectangular Beam Design (ACI/EIT)")
        rc_col1, rc_col2 = st.columns(2)
        with rc_col1:
            fc = st.number_input("f'c (Concrete Strength - ksc)", value=240.0, key="bfc")
            fy = st.number_input("fy (Steel Strength - ksc)", value=4000.0, key="bfy")
            b = st.number_input("b (Width - cm)", value=20.0)
            d = st.number_input("d (Effective Depth - cm)", value=35.0)
            mu = st.number_input("Mu (Factored Moment - kg-m)", value=5000.0)

        with rc_col2:
            if st.button("Calculate Reinforcement"):
                phi = 0.9
                mu_cm = mu * 100
                rn = mu_cm / (phi * b * d**2)
                if rn < (0.85 * fc / 2):
                    rho = (0.85 * fc / fy) * (1 - np.sqrt(1 - (2 * rn) / (0.85 * fc)))
                    as_req = rho * b * d
                    st.metric("Required As", f"{as_req:.2f} cm²")
                    num_db12 = int(np.ceil(as_req / 1.13))
                    num_db16 = int(np.ceil(as_req / 2.01))
                    num_db20 = int(np.ceil(as_req / 3.14))
                    st.write("Suggested Reinforcement:")
                    st.write(f"- {num_db12} x DB12 ({num_db12*1.13:.2f} cm²)")
                    st.write(f"- {num_db16} x DB16 ({num_db16*2.01:.2f} cm²)")
                    st.write(f"- {num_db20} x DB20 ({num_db20*3.14:.2f} cm²)")
                else:
                    st.error("Section failure: Moment is too high for concrete section.")

    elif rc_sub_tab == "Column Design (Axial)":
        st.markdown("### Short Column Axial Capacity (Simplified)")
        cc1, cc2 = st.columns(2)
        with cc1:
            fc = st.number_input("f'c (Concrete Strength - ksc)", value=240.0, key="cfc")
            fy = st.number_input("fy (Steel Strength - ksc)", value=4000.0, key="cfy")
            ag = st.number_input("Gross Area (Ag - cm²)", value=400.0) # 20x20
            ast_percent = st.slider("Steel Percentage (1-6%)", 1.0, 6.0, 1.0)

        with cc2:
            if st.button("Calculate Capacity"):
                ast = (ast_percent/100) * ag
                # Pn = 0.80 * phi * [0.85 * fc * (Ag - Ast) + fy * Ast] (Tied)
                phi = 0.65
                pn = 0.8 * phi * (0.85 * fc * (ag - ast) + fy * ast)
                st.metric("Factored Capacity (øPn)", f"{pn/1000:.2f} Tons")
                st.write(f"Required Steel Area (Ast): {ast:.2f} cm²")

    elif rc_sub_tab == "One-way Slab":
        st.markdown("### One-way Slab Design")
        sc1, sc2 = st.columns(2)
        with sc1:
            t = st.number_input("Thickness (cm)", value=10.0)
            mu_slab = st.number_input("Mu (kg-m/m)", value=1200.0)
        with sc2:
            if st.button("Check Reinforcement"):
                d = t - 2.5 # 2.5cm cover
                # Using basic b=100cm
                phi = 0.9
                fc = 240; fy = 4000
                rn = (mu_slab * 100) / (phi * 100 * d**2)
                rho = (0.85 * fc / fy) * (1 - np.sqrt(1 - (2 * rn) / (0.85 * fc)))
                as_req = rho * 100 * d
                st.write(f"Required As: {as_req:.2f} cm²/m")
                spacing = (1.13 * 100) / as_req # DB12
                st.info(f"Spacing for DB12: @{min(spacing, 3*t, 45):.1f} cm")

# --- TAB 5: STEEL SECTIONS ---
with tab_sections:
    st.subheader("Standard Steel Sections (TIS/JIS)")

    sec_type = st.selectbox("Section Type", ["H-Beam / Wide Flange", "I-Beam", "Channel", "Circular Hollow Section"])

    # Expanded database
    if sec_type == "H-Beam / Wide Flange":
        data = {
            "Section": ["H 100x100x6x8", "H 150x150x7x10", "H 200x200x8x12", "H 250x250x9x14", "H 300x300x10x15", "H 350x350x12x19", "H 400x400x13x21"],
            "Weight (kg/m)": [17.2, 31.5, 49.9, 72.4, 94.0, 137, 172],
            "Area (cm²)": [21.9, 40.1, 63.5, 92.2, 119.8, 173.9, 218.7],
            "Ix (cm⁴)": [383, 1640, 4720, 10800, 20400, 40300, 66600],
            "Iy (cm⁴)": [134, 563, 1600, 3650, 6750, 13600, 22400]
        }
    elif sec_type == "I-Beam":
        data = {
            "Section": ["I 150x75x5.5x9.5", "I 200x100x7x10", "I 250x125x7.5x12.5", "I 300x150x8x13"],
            "Weight (kg/m)": [17.1, 26.0, 38.3, 48.3],
            "Area (cm²)": [21.8, 33.1, 48.8, 61.5],
            "Ix (cm⁴)": [819, 2170, 5180, 9480],
            "Iy (cm⁴)": [57.5, 138, 337, 588]
        }
    elif sec_type == "Channel":
        data = {
            "Section": ["C 75x40x5x7", "C 100x50x5x7.5", "C 150x75x6.5x10", "C 200x80x7.5x11"],
            "Weight (kg/m)": [6.9, 9.4, 18.6, 24.6],
            "Area (cm²)": [8.8, 11.9, 23.7, 31.3],
            "Ix (cm⁴)": [75.3, 188, 861, 1910],
            "Iy (cm⁴)": [12.2, 26.0, 117, 168]
        }
    else: # CHS
        data = {
            "Section": ["CHS 60.5x3.2", "CHS 89.1x3.2", "CHS 114.3x4.5", "CHS 165.2x5.0"],
            "Weight (kg/m)": [4.52, 6.78, 12.2, 19.8],
            "Area (cm²)": [5.76, 8.64, 15.5, 25.2],
            "Ix (cm⁴)": [24.5, 78.4, 236, 804],
            "Iy (cm⁴)": [24.5, 78.4, 236, 804]
        }

    df_sections = pd.DataFrame(data)
    search_query = st.text_input("Search Section (e.g. 200)", "")
    if search_query:
        df_sections = df_sections[df_sections['Section'].str.contains(search_query)]

    st.dataframe(df_sections, use_container_width=True)
    st.info("Section properties based on Thai Industrial Standards (TIS).")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>StructureCAD AI - Professional Structural Engineering Toolkit</p>
    <p><i>Standalone HTML version available in <code>web_version.html</code></i></p>
    <p>© 2025 KMUTNB Student Project x Jules AI</p>
</div>
""", unsafe_allow_html=True)
