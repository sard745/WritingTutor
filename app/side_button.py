import streamlit as st

#　ボタンの初期化(デフォルトは全てのチェックボックスが選択されている)
def init_buttons(all_button, part_button_list):
    if all_button not in st.session_state: 
        st.session_state[all_button] = True
    for part_button in part_button_list:
        if part_button not in st.session_state:
            st.session_state[part_button] = True


def changed_part_button_by_all_button(all_button, part_button_list):
    for part_button in part_button_list:
        if(st.session_state[all_button]):
            #全て選択をTrueにした場合、選択ボタンをすべてTrueにする
            st.session_state[part_button] = st.session_state[all_button]

def changed_all_button_by_part_button(all_button, part_button_list):
    if all(st.session_state[part_button] for part_button in part_button_list):
        # 選択ボタンがすべてTrueの場合、全てをTrueにする
        st.session_state[all_button] = True
    else:
        # 選択ボタンが一部True(False)または全てFalseの場合、全てをFalseにする
        st.session_state[all_button] = False

def create_checkbox_group(all_button, part_button_list, label, page_position):
    init_buttons(all_button, part_button_list)

    page_position.write(label)
    page_position.checkbox(
        all_button, 
        # value=st.session_state[all_button], 
        key=all_button, 
        on_change=lambda: changed_part_button_by_all_button(all_button, part_button_list)
    )

    for part_button in part_button_list:
        page_position.checkbox(part_button, 
            # value=st.session_state[part_button], 
            key=part_button, 
            on_change=lambda: changed_all_button_by_part_button(all_button, part_button_list)
        )