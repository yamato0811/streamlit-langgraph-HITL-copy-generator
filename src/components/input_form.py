import streamlit as st


def _validate_inputs(product: str) -> bool:
    return bool(product.strip())


def input_form() -> tuple[str, str, str]:
    product_info = st.text_area("商品情報を入力してください")
    submit_button = st.button("Start", type="primary")

    if submit_button:
        if _validate_inputs(product_info):
            st.session_state.is_start = True
        else:
            st.error("商品情報を入力してください")

    if not st.session_state.is_start:
        st.stop()
    return product_info
