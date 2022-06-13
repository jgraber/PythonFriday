import pyperclip

# write to the clipboard
pyperclip.copy("a new value for the clipboard")

#read from the clipboard
text = pyperclip.paste()
print(text)
