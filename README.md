# NFA to DFA converter

This project helps to visualize NFA and converts the NFA with the alphabet given to DFA by making NFA Table and DFA Table.

Check it out [here!](https://mazen-ghaleb.github.io/NFA2DFAconverter/Build/ "Project's Git Page Link")

## Example

![NFA Input image](/media/NFAInput.png)
![Table Output image](/media/TableOutput.png)
![DFA Output image](/media/DFAOutput.png)

## Introduction

This project converts the input NFA to DFA by providing a GUI (Graphical User interface) that accepts the NFA as drawn states and upon pressing the convert button, it converts the NFA to DFA as well as it provides the NFA Table and DFA Table.

## Problem Specification

The user inputs the following:

1. NFA States
2. Transitions between the states
3. The Alphabet

The program converts the input and takes them into consideration while creating the NFA Table then converts it to DFA Table and finally creating the DFA.

## Approach

The program is written in Python and JavaScript and uses as well Unity for graphical user interface (GUI). The design went as to build the application as a web application to enhance the application usability and reusability. The choice of Unity was needed to ease the visualization of the inputs and increase the quality. The inputs can be given easily as states to Unity program as well as the alphabet. Then, Unity converts the input as JSON and sends it to Python to start processing.

Python file destructs the NFA to nodes and edges. Moreover, it converts the node and edges into the NFA Table. The DFA table uses the NFA table and the Alphabet to move between initial state by calculating the union of the states, calculating epsilon closure, and knowing which state to calculate next. The output DFA table is then reconstructed as DFA structure needed by the graphic library used in JavaScript, which is VisJS.

Finally, the Python file then passes the NFA Table , DFA Table, DFA, initial state , alphabet, and final state to the Brython (Library which enables us to use JavaScript with Python) to run the visualization for the web application. The JavaScript script generates the table in html format as well as generate the DFA, where it states the initial state at top left and marks the final state with bold circle.

## How to run

1. Open the deployment website
2. Wait for the Application to load

OR

1. Clone the GitHub repo
2. Have Unity 2020.3.33f1 version downloaded
3. Select the project folder with Unity
4. Change Build Settings to WebGL
5. Build and Run
