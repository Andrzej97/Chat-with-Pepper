# Chat-with-Pepper
Project is being realized as the engineering thesis at AGH UST. Faculty: WIEiT. Field of study: Computer Science.
Authors:
Rafał Pych,
Witold Soczek,
Andrzej Szaflarski.

To run speech_recognition you must install packages: SpeechRecognition, PyAudio.
You can use:
pip install SpeechRecognition
pip install PyAudio

Remember, that PyAudio is not supported for Python3.7. In this project we are using Python3.6.

To run project type:
	python3 main.py

If you want to execute other file directly, first you should add project's root folder (Chat_with_Pepper) to PYTHONPATH i.d. export PYTHONPATH=$PYTHONPATH:root_project_name and remember about dependencies which allow to run program correctly (for example database location). 

To use MongoDB one should install dependencies concerning this software:
	1. sudo apt-get update
	2. sudo apt-get install -y mongodb
	3. To check mongo is running correctly: sudo systemctl status mongodb

This is based upon https://linoxide.com/linux-how-to/install-mongodb-ubuntu/


