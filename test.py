import subprocess
def save_score_data():
    subprocess.Popen(["api/python2.7/bin/python", "DeepMoji-main/examples/score_texts_emojis.py"])

save_score_data()
