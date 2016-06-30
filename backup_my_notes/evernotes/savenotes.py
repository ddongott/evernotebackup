from datetime import datetime
from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec
from xml.dom import minidom
from xml.dom import Node

MYNOTEBOOK = "First Notebook"
MYNOTETIME = 2016

def writeResource(path, data):
    resfile = open(path,"wb")
    resfile.write(data)
    resfile.close()

def downloadResource(note_store, dev_token, note):
    #print note.content
    xmlparse = minidom.parseString(note.content)
    note_nodes = xmlparse.getElementsByTagName('en-media')
    for note_node in note_nodes:
        if note_node:
            reshash = note_node.getAttribute('hash')
            print reshash
            resource = note_store.getResourceByHash(dev_token, note.guid, reshash, True, False, False);
            writeResource("/tmp/"+str(reshash), resource.data);

def getNoteBookGuid(notebooks):
    for notebook in notebooks:
        print notebook.name
        if notebook.name == MYNOTEBOOK:
            return notebook.guid

    return None

def saveNotesToHtml():
    
dev_token = "S=s1:U=91518:E=156b80aac83:C=14f60597e90:P=1cd:A=en-devtoken:V=2:H=1c7a0bc961458c9a45d45a019ff71439"
client = EvernoteClient(token=dev_token)
userStore = client.get_user_store()
user = userStore.getUser()
print user.username

note_store = client.get_note_store()
# List all of the notebooks in the user's account
notebooks = note_store.listNotebooks()
nbguid = getNoteBookGuid(notebooks)
print "Found notebook guid: " + str(nbguid)

nfilter = NoteFilter(order=None, ascending=None, words=None, notebookGuid=nbguid, tagGuids=None, timeZone=None, inactive=None, emphasized=None)
result_spec = NotesMetadataResultSpec(includeCreated=True)
offset = 0
max_notes = 10
result_list = note_store.findNotesMetadata(dev_token, nfilter, offset, max_notes, result_spec)

div_style = ["background-color:LightGray","background-color:LightGreen","background-color:LightPink","background-color:LightSalmon","background-color:LightSeaGreen"]
div_style_index = 0
htmltxt = "<!DOCTYPE html>\n"
htmltxt += "<html>\n"
htmltxt += "<head>\n"
htmltxt += "<title>Notes from Evernote</title>\n"
htmltxt += "</head>\n"

htmltxt += "<body>\n"
for notemetadata in result_list.notes:
    #print ("Titolo: " + notemetadata.title + " | GUUID: " + notemetadata.guid)
    note_create_time = datetime.fromtimestamp(notemetadata.created/1000)
    print note_create_time.year
    if note_create_time.year == MYNOTETIME:
        htmltxt += "<div style=\"" + div_style[div_style_index] + "\">"
        div_style_index = (div_style_index + 1) % len(div_style)
        note = note_store.getNote(dev_token, notemetadata.guid, True, True, True, True)
        htmltxt += "<h1>"+note.title+"</h1>\n"

        timecreated = datetime.fromtimestamp(note.created/1000)
        htmltxt += "<p>Create time: "+str(timecreated)+"</p>\n"
        timeupdated = datetime.fromtimestamp(note.updated/1000)
        htmltxt += "<p>Update time: "+str(timeupdated)+"</p>\n"
        htmltxt += "<p>"+note.content+"</p>\n"

        if note.resources:
            for resource in note.resources:
                data = note_store.getResourceData(dev_token, resource.guid)
                respath = "/tmp/"+str(resource.guid)+"."+resource.mime.split("/",1)[1]
                writeResource(respath, data);
                imgalt = respath + "Not Found"
                imgstyle = "max-width: 98%; max-height: 98%;"
                htmltxt += "<img src=\""+respath +"\" alt=\""+imgalt+"\"style=\""+imgstyle+"\">"

    
        htmltxt += "</div>\n"
        htmltxt += "<hr>\n"

htmltxt += "</body>\n"
htmltxt += "</html>\n"
f = open("/tmp/evernote.html","wb")
f.write(htmltxt)
f.close()

