pyinstaller "BFS.py" --onefile
copy /b .\dist\BFS.exe .\AI-Search\Assets\PythonScripts\BFS.exe.bytes
pyinstaller "DFS.py" --onefile
copy /b .\dist\DFS.exe .\AI-Search\Assets\PythonScripts\DFS.exe.bytes
pyinstaller "UCS.py" --onefile
copy /b .\dist\UCS.exe .\AI-Search\Assets\PythonScripts\UCS.exe.bytes
pyinstaller "DepthLimited.py" --onefile
copy /b .\dist\DepthLimited.exe .\AI-Search\Assets\PythonScripts\DepthLimited.exe.bytes
pyinstaller "BestFit.py" --onefile
copy /b .\dist\BestFit.exe .\AI-Search\Assets\PythonScripts\BestFit.exe.bytes
pyinstaller "Astar.py" --onefile
copy /b .\dist\Astar.exe .\AI-Search\Assets\PythonScripts\Astar.exe.bytes
pyinstaller "IterativeDeepening.py" --onefile
copy /b .\dist\IterativeDeepening.exe .\AI-Search\Assets\PythonScripts\IterativeDeepening.exe.bytes

