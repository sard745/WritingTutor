from streamlit_option_menu import option_menu

def get_option_menu_config(list_menu):
  return {
    "menu_title": None,
    "options": list_menu,
    "default_index": 0,
    "orientation": "horizontal",
    "styles": {
        "container": {
            "margin": "0!important",
            "padding": "0!important",
            "background-color": "#fafafa",
            "text-align":"center",
        },
        "menu-title": {"font-size": "40px", "font-weight":"bold"},
        "icon": {"color": "fafafa", "font-size": "25px"},
        "nav-link": {
            "font-size": "20px",
            "margin": "0px",
            "--hover-color": "#eee",
    },
    "nav-link-selected": {"background-color": "004a55"},
  },
}

def get_option_menu(list_menu):
  return option_menu(**get_option_menu_config(list_menu))