import streamlit as st
import os
import sys
import importlib.util
import cv2

ejecuta= st.sidebar.radio('¿Elige una funcion?', ['Capturar','Entrenar','Reconocer'])

if ejecuta == 'Capturar':
    #exec('Capturar.py',{})
    file= 'Capturar.py'
if ejecuta == 'Entrenar':
    #exec('Capturar.py',{})
    file= 'entrenar.py'

if ejecuta == 'Reconocer':
    #exec('Capturar.py',{})
    file= 'Reconocer.py'





# Parse command-line arguments.
if len(sys.argv) > 1:
    folder = os.path.abspath(sys.argv[1])
else:
    folder = os.path.abspath(os.getcwd())

# Get filenames for all files in this path, excluding this script.

this_file = os.path.abspath(__file__)
fnames = []

for basename in os.listdir(folder):
    fname = os.path.join(folder, basename)

    if fname.endswith('.py') and fname != this_file:
        fnames.append(fname)

# Make a UI to run different files.

#fname_to_run = st.sidebar.selectbox('Que quieres hacer?', fnames)
fname_to_run =file
# Create module from filepath and put in sys.modules, so Streamlit knows
# to watch it for changes.

fake_module_count = 0

def load_module(filepath):
    global fake_module_count

    modulename = '_dont_care_%s' % fake_module_count
    spec = importlib.util.spec_from_file_location(modulename, filepath)
    module = importlib.util.module_from_spec(spec)
    sys.modules[modulename] = module

    fake_module_count += 1

# Run the selected file.

with open(fname_to_run) as f:
    load_module(fname_to_run)
    filebody = f.read()



exec(filebody, {})



