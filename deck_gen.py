import os
import genanki
import json

class MyNote(genanki.Note):
  @property
  def guid(self):
    return genanki.guid_for(self.fields[4])


with open('card_front_ex.html', 'r') as f:
    afmt = f.read()
with open('card_back_ex.html', 'r') as f:
    qfmt = f.read()
with open('card_styling.css', 'r') as f:
    my_css = f.read()

my_model = genanki.Model(
    1084725310,
    'Drum Break',
    fields=[
        {'name': 'Whosampled rank'},
        {'name': 'Example 1 Audio'},
        {'name': 'Example 2 Audio'},
        {'name': 'Example 3 Audio'},
        {'name': 'Break Name'},
        {'name': 'Break Nickname'},
        {'name': 'Back Audio'},
        {'name': 'Back Image'},
        {'name': 'Example 1'},
        {'name': 'Example 2'},
        {'name': 'Example 3'},
        {'name': 'Whosampled count'},
        {'name': 'Whosampled URL'},
        {'name': 'Note'},
    ],
    templates=[
        {
            'name': 'Drum Break with Example',
            'qfmt': afmt,
            'afmt': qfmt,
        }
    ],
    css=my_css
)

my_deck = genanki.Deck(
    1829266120,
    'Drum Breaks'
)

my_package = genanki.Package(my_deck)
media_files = []
note_fields = []

for folder_name in os.listdir('breaks'):
    if folder_name.startswith('.'):
        continue
    folder_path = os.path.join('breaks', folder_name)
    fields = ["","","","","","","","","","","","","",""]
    with open(os.path.join(folder_path, 'info.json'), 'r') as f:
        info = json.load(f)
    fields[4] = info['Break Name']
    if 'Break Nickname' in info:
        fields[5] = info['Break Nickname']
    if 'Whosampled count' in info:
        fields[11] = str(info['Whosampled count'])
    if 'Whosampled URL' in info:
        fields[12] = info['Whosampled URL']
    if 'Note' in info:
        fields[13] = info['Note']

    if os.path.exists(os.path.join(folder_path, folder_name + '.wav')):
        fields[6] = '[sound:' + folder_name + '.wav' + ']'
        media_files.append(os.path.join(folder_path, folder_name + '.wav'))
    elif os.path.exists(os.path.join(folder_path, folder_name + '.mp3')):
        fields[6] = '[sound:' + folder_name + '.mp3' + ']'
        media_files.append(os.path.join(folder_path, folder_name + '.mp3'))
    if os.path.exists(os.path.join(folder_path, folder_name + '.jpg')):
        fields[7] = '<img src=\"' + folder_name + '.jpg' + '\">'
        media_files.append(os.path.join(folder_path, folder_name + '.jpg'))
    elif os.path.exists(os.path.join(folder_path, folder_name + '.png')):
        fields[7] = '<img src=\"' + folder_name + '.png' + '\">'
        media_files.append(os.path.join(folder_path, folder_name + '.png'))
    example_count = 0
    for file in os.listdir(folder_path):
        if file.endswith('.mp3') and file != 'break.mp3':
            example_count += 1
            media_files.append(os.path.join(folder_path, file))
            if example_count == 1:
                fields[1] = '[sound:' + file + ']'
                fields[8] = file.replace('.mp3', '')
            elif example_count == 2:
                fields[2] = '[sound:' + file + ']'
                fields[9] = file.replace('.mp3', '')
            elif example_count == 3:
                fields[3] = '[sound:' + file + ']'
                fields[10] = file.replace('.mp3', '')
    note_fields.append(fields)

print (media_files)
my_package.media_files = media_files

note_fields.sort(key=lambda x: int(x[11]) if x[11] else 0, reverse=True)
for i, fields in enumerate(note_fields):
    fields[0] = str(i + 1)
    my_note = genanki.Note(
        model=my_model,
        fields=fields)
    my_deck.add_note(my_note)

def check_fields(note_fields):
    for note in note_fields:
        if len(note) != 14:
                print(f"Incorrect number of fields: {len(note)}")
                return False
        if not all(isinstance(field, str) for field in note):
            print("Not all fields are strings.")
            return False
    return True

my_package.write_to_file('output.apkg')