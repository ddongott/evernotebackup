#!/usr/bin/python
from datetime import datetime
from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec
from xml.dom import minidom
from xml.dom import Node

def parseEnNote(noteNode):
    
    for notechild in noteNode.childNodes:
        print notechild.nodeValue
    return ''


def parseContent(note):
    print note.content
    htmlcontent = ''
    xmlparse = minidom.parseString(note.content)
    note_nodes = xmlparse.getElementsByTagName('en-note')
    for note_node in note_nodes:
        htmlcontent += parseEnNote(note_node)

    return htmlcontent

dev_token = "S=s1:U=91518:E=156b80aac83:C=14f60597e90:P=1cd:A=en-devtoken:V=2:H=1c7a0bc961458c9a45d45a019ff71439"
client = EvernoteClient(token=dev_token)
userStore = client.get_user_store()
user = userStore.getUser()
print user.username

note_store = client.get_note_store()
# List all of the notebooks in the user's account
notebooks = note_store.listNotebooks()
print "Found ", len(notebooks), " notebooks:"

for notebook in notebooks:
    print notebook.name


nfilter = NoteFilter()
result_spec = NotesMetadataResultSpec(includeTitle=True)
offset = 0
max_notes = 10
result_list = note_store.findNotesMetadata(dev_token, nfilter, offset, max_notes, result_spec)

for notemetadata in result_list.notes:
    #print ("Titolo: " + notemetadata.title + " | GUUID: " + notemetadata.guid)
    note = note_store.getNote(dev_token, notemetadata.guid, True, True, True, True)
    print note.title
    print note.content
    print note.notebookGuid
    timecreated = datetime.fromtimestamp(note.created/1000)
    timeupdated = datetime.fromtimestamp(note.updated/1000)
    
