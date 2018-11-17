import pyttsx

input = raw_input()
engine = pyttsx.init()
output = engine.say(input)
engine.runAndWait()﻿
