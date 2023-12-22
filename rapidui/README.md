# Centrality UI - Rapid

Quick and dirty UI for Centrality. Built using some streamlit

## Components

- `flexbox.py` - minimal flexbox for displaying cards
- `header.py` - reusable header component. Also packages up and applies `app.css`
- `pages/` - pages for the app

## Configuration

Passing around a Config to a multi-page streamlit app seems quite difficult. CLI args are only used by the root page,
but we want users to be able to go directly to any page, which leads to the other pages not having a way to get the 
config (if you use `st.session_state`, it will only work if a user enters through the home page so the value can be 
set initially).

Instead we use CentralityConfig's built-in envvar support. But even that is a bit messy since the envvar utilities
exist in Python code, but Python code can't set an environment variable that persists beyond the lifetime of the 
process. `streamlit run` will launch in a new process. So we have to have a Python script that prints out the envvar
name and value (`config_util.py`). Then we have a wrapper shell script that runs `config_util.py`, saves the envvar
and launches streamlit so it has access to the config via envvar.

We don't run `streamlit run` as a Python `subprocess` just for separation of concerns reasons. 