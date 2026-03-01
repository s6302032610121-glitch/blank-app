import streamlit as st
import json
import os
import pandas as pd

# Set page config
st.set_page_config(page_title="ระบบจัดการสต็อกสินค้า", page_icon="📦")

# Data file path
DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "inventory.json")

def load_data():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Sidebar navigation
st.sidebar.title("📦 ระบบจัดการสต็อก")
page = st.sidebar.selectbox(
    "เลือกเมนู",
    ["ภาพรวม", "คลังสินค้า", "เพิ่มสินค้าใหม่", "เพิ่ม/ลดสต็อก"]
)

# Load data
inventory = load_data()
df = pd.DataFrame(inventory)

if page == "ภาพรวม":
    st.title("📊 ภาพรวมระบบ")

    if not inventory:
        st.info("👋 ยินดีต้อนรับ! ยังไม่มีข้อมูลสินค้าในระบบ เริ่มต้นโดยการเพิ่มสินค้าใหม่ที่เมนู 'เพิ่มสินค้าใหม่'")
    else:
        total_items = len(inventory)
        total_quantity = sum(item['quantity'] for item in inventory)
        total_value = sum(item['quantity'] * item['price'] for item in inventory)
        low_stock_threshold = 10
        low_stock_items = [item for item in inventory if item['quantity'] < low_stock_threshold]

        col1, col2, col3 = st.columns(3)
        col1.metric("รายการสินค้าทั้งหมด", f"{total_items} รายการ")
        col2.metric("จำนวนสินค้าในคลัง", f"{total_quantity} ชิ้น")
        col3.metric("มูลค่ารวมทั้งหมด", f"฿{total_value:,.2f}")

        if low_stock_items:
            st.error(f"⚠️ มีสินค้าใกล้หมด {len(low_stock_items)} รายการ (ต่ำกว่า {low_stock_threshold} ชิ้น)")
            low_stock_df = pd.DataFrame(low_stock_items)[['name', 'quantity', 'category']]
            st.table(low_stock_df.rename(columns={"name": "ชื่อสินค้า", "quantity": "คงเหลือ", "category": "หมวดหมู่"}))
        else:
            st.success("✅ สินค้าทุกรายการมีจำนวนเพียงพอ")

elif page == "คลังสินค้า":
    st.title("📋 รายการสินค้าในคลัง")

    if not inventory:
        st.warning("ยังไม่มีสินค้าในคลัง กรุณาเพิ่มสินค้าใหม่")
    else:
        # Search bar
        search = st.text_input("🔍 ค้นหาชื่อสินค้า หรือ หมวดหมู่", "")

        # Filter data
        filtered_df = df[
            df['name'].str.contains(search, case=False, na=False) |
            df['category'].str.contains(search, case=False, na=False)
        ]

        # Display data
        display_df = filtered_df.copy()
        display_df.columns = ["ชื่อสินค้า", "หมวดหมู่", "จำนวน", "ราคาต่อหน่วย"]

        st.dataframe(display_df, use_container_width=True, hide_index=True)

        st.write(f"แสดงทั้งหมด {len(filtered_df)} รายการ")

elif page == "เพิ่มสินค้าใหม่":
    st.title("🆕 เพิ่มสินค้าใหม่เข้าสู่ระบบ")

    with st.form("add_product_form", clear_on_submit=True):
        name = st.text_input("ชื่อสินค้า")
        category = st.text_input("หมวดหมู่")
        quantity = st.number_input("จำนวนเริ่มต้น", min_value=0, step=1)
        price = st.number_input("ราคาต่อหน่วย", min_value=0.0, step=0.5)

        submit = st.form_submit_button("บันทึกสินค้า")

        if submit:
            if name and category:
                # Check if product already exists
                if any(item['name'] == name for item in inventory):
                    st.error(f"มีสินค้าชื่อ '{name}' อยู่ในระบบแล้ว")
                else:
                    new_item = {
                        "name": name,
                        "category": category,
                        "quantity": int(quantity),
                        "price": float(price)
                    }
                    inventory.append(new_item)
                    save_data(inventory)
                    st.success(f"เพิ่มสินค้า '{name}' เรียบร้อยแล้ว")
                    st.balloons()
            else:
                st.error("กรุณากรอกชื่อสินค้าและหมวดหมู่")

elif page == "เพิ่ม/ลดสต็อก":
    st.title("🔄 จัดการจำนวนสต็อก (เข้า/ออก)")

    if not inventory:
        st.warning("ยังไม่มีสินค้าในคลัง กรุณาเพิ่มสินค้าใหม่ก่อน")
    else:
        product_names = [item['name'] for item in inventory]
        selected_product = st.selectbox("เลือกสินค้า", product_names)

        # Get current item
        item_index = next(i for i, item in enumerate(inventory) if item['name'] == selected_product)
        item = inventory[item_index]

        st.write(f"จำนวนปัจจุบัน: **{item['quantity']}** {item['category']}")

        col1, col2 = st.columns(2)
        with col1:
            adjustment_type = st.radio("ประเภทการทำรายการ", ["เพิ่มสต็อก (Stock In)", "ลดสต็อก (Stock Out)"])
        with col2:
            amount = st.number_input("จำนวน", min_value=1, step=1)

        if st.button("ยืนยันรายการ"):
            if adjustment_type == "เพิ่มสต็อก (Stock In)":
                inventory[item_index]['quantity'] += int(amount)
                st.toast(f"✅ เพิ่มสต็อก '{selected_product}' จำนวน {amount} เรียบร้อย")
            else:
                if inventory[item_index]['quantity'] >= amount:
                    inventory[item_index]['quantity'] -= int(amount)
                    st.toast(f"✅ ลดสต็อก '{selected_product}' จำนวน {amount} เรียบร้อย")
                else:
                    st.error("❌ จำนวนสินค้าในสต็อกไม่เพียงพอ")
                    st.stop()

            save_data(inventory)
            st.success("บันทึกข้อมูลเรียบร้อย")
            st.rerun()
