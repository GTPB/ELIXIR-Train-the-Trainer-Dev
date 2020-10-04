# -----------------------------------------------
# ------------ TABLE OF CONTENTS ----------------
# -----------------------------------------------
# 
# SUMMARY
# PRELIMINARY DEFINITIONS AND OPERATIONS
#   Imports
#   Global Variables
#   Loads
#   Functions
# PROPER SCRIPT




# -------------------------------------
# ------------ SUMMARY ----------------
# -------------------------------------
# This python script is used by the build_lesson_wf.yml workflow to generate the 'slides.md' file (in the 'slides' folder) from
# the set of episodes (.md files) contained in the '_episodes' folder. The 'slides.md' file should then be pulled to and synched
# with a HackMD account so that the slides can be accessed and viewed by anyone with the proper HackMD link.
#
# This script also looks at the title in the yaml header of each episode markdown file and compares it to the titles in the
# 'lesson_structure.yml' file. If it finds a match, it adds that same title to the filename of the correct episode file, plus
# a prefix 'SIEJ-', where I is the session number and J is the episode number (within that session).





# ----------------------------------------------------------------
# ------------ PRELIMINARY DEFINITIONS AND OPERATIONS ------------
# ----------------------------------------------------------------
# We first import some libraries and define some variables and functions that will be useful.


# ---- Imports ----

# The 'os' library allows for the use of several OS related operations, namely listdir(), which we use in this script
# to access the markdown files in the '_episodes' folder.
import os

# The 'yaml' library allows for the use of several yaml related operations, namely load() and dump(), which we use in this script
# to read the 'lesson_structure.yml' file and read/write into the episodes in the '_episodes' folder.
import yaml


# ---- Global Variables ----

# In the 'Liquid' template language (used by GitHub Pages and Jekyll), a comment can be introduced by placing
# it within the {%comment%} and {%endcomment%} tags, respectively, like so:
#
# {%comment%}
# This will be interpreted as a comment by the Liquid template language.
# {%endcomment%}
#
# A 'Liquid' comment and its tags will be shown by a markdown viewer, but they will not be displayed on the website generated
# by Jekyll/GitHub Pages. So, here we are using the 'Liquid' comment to add content that we want people to be
# able to see on the:
#
# 1. GitHub repository (but not on the Carpentries-style website).
# 2. Slides (but not on the Carpentries-style website).

# 'Liquid' tags for a comment (these should not be modified, since they are used by Jekyll
# and GitHub Pages).

# Tag to open a comment section.
liquidCommentTag_beginning = "{%comment%}"

# Tag to close a comment section.
liquidCommentTag_ending = "{%endcomment%}"

# To add content that is solely meant for the slides, we are placing it inside
# the slides tag (within the 'Liquid' comment tags). The slides tag can be changed below.
# Here is an example of how the slides content would be placed, if we choose the slides tag
# to be $$$:
# 
#
# {%comment%}
#
# Some content that will appear neither on the website nor or the slides. 
#
# $$$
# This is content meant only to appear on the slides.
# $$$
# 
# Some more content that will appear neither on the website nor or the slides.
#
# {%endcomment%}

# The slides tag. Change it here if you wish to use another tag for the content of the slides. 
slidesTag = "$$$"

# The tag delimiting a document within a yaml file. It is used in thsi script to detect the
# beginning and ending of a yaml header.
yamlDocumentTag = "---"

# The tag that will be added to unrecognised files in the _episodes folder.
unrecognisedTag = "Unrecognised - "

# Folder where the episodes can be found.
build_lessonFolderPath = "bin/build_lesson/"

# When information is to be dumped into the yaml header of each episode file, we first dump it into
# temporary file called 'temp.yml'. From this file we then extract it and write it into the yaml header
# in the correct episode file. The reason for this is that the Python yaml.dump()
# function seems to have some weird behaviour at times. This way we can better control what we end up writing.
tempFilePath = build_lessonFolderPath + "temp.yml"

# Location of the yaml file containing the structure of the lesson and some options
lesson_structureFilePath = "bin/build_lesson/lesson_structure.yml"

# Folder where the episodes can be found.
episodesFolderPath = "_episodes/"

# Folder where the slides can be found.
slidesFolderPath = "slides/"

# Filepath with the information to be added to the yaml header in the 'slides_header.md' file.
slides_headerFilePath = slidesFolderPath + "slides_header.md"

# Filepath with the information to be added to the yaml header in the 'slides_title.md' file.
slides_titleFilePath = slidesFolderPath + "slides_title.md"

# Filepath with the information to be added to the end of each session in the 'slides_end_of_session.md' file.
slides_end_of_sessionFilePath = slidesFolderPath + "slides_end_of_session.md"

# Filepath to the 'slides.md' file.
slidesFilePath = slidesFolderPath + "slides.md"


# ---- Loads ----

# Loading the data in 'lesson_structure.yml' into the variable 'yamlLessonStructure'.
yamlLessonStructure = yaml.safe_load(open(lesson_structureFilePath, "r"))


# ---- Functions ----

# Function used to extract any content within two tags (beginning tag and ending tag).
# If the beginning tag and the ending tag are the same we can call this function by writing
#
# extractContent(text, tag)
#
# instead of
#
# extractContent(text, beginningTag, endingTag)
#
# If one of the tags is not found then the function returns an empty string.
def extractContent(text, beginningTag, endingTag = None):
    if endingTag == None:
        endingTag = beginningTag
        
    beginningTagPosition = text.find(beginningTag)
    if beginningTagPosition != -1:
        content_begins = beginningTagPosition + len(beginningTag)
        content = text[content_begins:]

        endingTagPosition = content.find(endingTag)
        if endingTagPosition != -1:
            content = content[:endingTagPosition]
            content_ends = content_begins + endingTagPosition
            return {"content": content, "content_begins": content_begins, "content_ends": content_ends}
        else:
            return None

    else:
        return None

 
# Function used to replace the string variable 'text' with 'newContent' at the positions specified by
# 'content_begins' and 'content_ends'.
def replaceContent(text, newContent, content_begins, content_ends):
    newText = text[:content_begins] + "\n" + newContent + "\n" + text[content_ends:]
    return newText

# Function used to create a dictionary containing information pertaining to the episodes.
# Here is the information it contains:
#
# - It is a dictionary where the keys are the episode titles.
# - Each value in this dictionary is itself a dictionary, with the following keys:
#   - sessionNumber (number of the session the episode belongs to)
#   - episodeNumber (number of the episode within the session)
#   - globalEpisodeNumber (number of the episode within the whole lesson)
#   - prefix (prefix of the form 'SIEJ-', to be added to the an episode filename, where I is the sessionNumber and J the episodeNumber)
#   - slidesContent (string containing the entire content of the slides in the episode)
#   - slideCount (number of slides in the episode)
#   - firstSlideNumber (number of the first slide of the episode)
def createLessonDict():
    lessonDict = {}
    sessions = yamlLessonStructure["lesson"]
    numberOfSessions = len(sessions)
    episodeCount = 0
    i = 0
    while i < numberOfSessions:
        j = 0
        currentSession = sessions[i]
        numberOfEpisodes = len(currentSession)
        while j < numberOfEpisodes:
            currentEpisodeTitle = currentSession[j]
            episodeCount = episodeCount + 1
            sessionNumber = i + 1
            episodeNumber = j + 1
            episodeInfo = {"sessionNumber": sessionNumber, "episodeNumber": episodeNumber, "globalEpisodeNumber": episodeCount, 
                                                "prefix": "S" + str(sessionNumber) + "E" + str(episodeNumber), "slidesContent": "",
                                                "slideCount": 0, "firstSlideNumber": ""}
            lessonDict[currentEpisodeTitle] = episodeInfo
            j = j + 1
        i = i + 1
     
    return lessonDict

# Function to extract slides information from a string variable called 'text' (the string is usually the whole text from an episode file).
# It only extracts the information from markdown files that have a yaml header with a title that matches the titles in the 'lesson_structure.yml' file.
def extractTextInfoToDict(lessonDict, text):
    episodeHeaderStringInfo = extractContent(text, yamlDocumentTag)
    if episodeHeaderStringInfo != None:
        print("aqui")
        episodeHeaderString = episodeHeaderStringInfo["content"]
    else:
        episodeHeaderString = ""
    yamlEpisodeHeader = yaml.safe_load(episodeHeaderString)
    slidesContent = ""
    matchingTitle = None
    if "title" in yamlEpisodeHeader:
        for episodeTitle in lessonDict:
            if yamlEpisodeHeader["title"].find(episodeTitle) != -1:
                matchingTitle = episodeTitle
    
    if matchingTitle != None:
        # Extracting from the variable 'text' the section that rests inside the 'Liquid' comment.
        liquidCommentContentInfo = extractContent(text, liquidCommentTag_beginning, liquidCommentTag_ending)
        if liquidCommentContentInfo != None:
            liquidCommentContent = liquidCommentContentInfo["content"]
        else:
            liquidCommentContent = ""
            
        # Now, in the content of the 'Liquid' comment, we detect the slide tags and extract the content therein contained.
        slidesContentInfo = extractContent(liquidCommentContent, slidesTag)
        if slidesContentInfo != None:
            slidesContent = slidesContentInfo["content"]
            episodeInfo = lessonDict[matchingTitle]
            episodeInfo["slidesContent"] = slidesContent
                

    return matchingTitle


def preProcessing(lessonDict):
    # Preparing the list of files in the episodes folder, so that we can loop over it.
    fileList = os.listdir(episodesFolderPath)
    for fileName in fileList:
        fileParts = fileName.rsplit(".")
        # Extracting the entire contents of the markdown files (.md) and placing them in the string variable named 'text'.
        if len(fileParts) == 2 and fileParts[1] == "md" and fileParts[0] != "README":
            filePath = episodesFolderPath + fileName
            f = open(filePath, "r")
            text = f.read()
            f.close()
            matchingTitle = extractTextInfoToDict(lessonDict, text)
            newFilePath = filePath
            if matchingTitle != None:
                episodeInfo = lessonDict[matchingTitle]
                newFileName = episodeInfo["prefix"] + " - " + matchingTitle + ".md"
                newFilePath = episodesFolderPath + newFileName
            else:
                if fileName[:len(unrecognisedTag)] != unrecognisedTag:
                    newFilePath = episodesFolderPath + unrecognisedTag + fileName
            
            if not os.path.exists(newFilePath):
                os.rename(episodesFolderPath + fileName, newFilePath)
    
    
def addSlideNumbersToDict(lessonDict):
    slideCount = 0
    for episodeTitle in lessonDict:        
        episodeInfo = lessonDict[episodeTitle]
        if slideCount == 0:
            episodeInfo["firstSlideNumber"] = ""
        else:
            if episodeInfo["slideCount"] == 0:
                episodeInfo["firstSlideNumber"] = lastEpisodeInfo["firstSlideNumber"]
            else:
                episodeInfo["firstSlideNumber"] = str(slideCount)
        
        slideCount = slideCount + episodeInfo["slideCount"]        
        lastEpisodeInfo = episodeInfo
        
    
def updateFileYamlHeader(lessonDict, fileName):
    # Extracting the entire contents of the markdown files (.md) and placing them in the string variable named 'text'.
    f = open(episodesFolderPath + fileName, "r")
    text = f.read()
    f.close()
    
    episodeHeaderStringInfo = extractContent(text, yamlDocumentTag)
    if episodeHeaderStringInfo != None:
        episodeHeaderString = episodeHeaderStringInfo["content"]
    else:
        episodeHeaderString = ""
        
    yamlEpisodeHeader = yaml.safe_load(episodeHeaderString)
    matchingTitle = None      
    if "title" in yamlEpisodeHeader:
        for episodeTitle in lessonDict:
            if yamlEpisodeHeader["title"].find(episodeTitle) != -1:
                matchingTitle = episodeTitle
    
    if matchingTitle != None:
        episodeInfo = lessonDict[matchingTitle]
        yamlEpisodeHeader["title"] = episodeInfo["prefix"] + " - " + matchingTitle
        yamlEpisodeHeader["slides_url"] = yamlLessonStructure["slides_base_url"] + episodeInfo["firstSlideNumber"]
        tempFileWrite = open(tempFilePath, "w")
        yaml.dump(yamlEpisodeHeader, tempFileWrite, default_flow_style=False)
        tempFileWrite.close()
        tempFileRead = open(tempFilePath, "r")
        newYamlEpisodeHeaderString = tempFileRead.read()
        tempFileRead.close()
        newText = replaceContent(text, newYamlEpisodeHeaderString, episodeHeaderStringInfo["content_begins"], episodeHeaderStringInfo["content_ends"])
        updatedFile = open(episodesFolderPath + fileName, "w")
        updatedFile.write(newText)
        updatedFile.close()
   

def updateAllYamlHeaders(lessonDict):
    # Preparing the list of files in the episodes folder, so that we can loop over it.
    fileList = os.listdir(episodesFolderPath)
    for fileName in fileList:
        fileParts = fileName.rsplit(".")
        if len(fileParts) == 2 and fileParts[1] == "md":
            updateFileYamlHeader(lessonDict, fileName)


# Function used to write the content of the slides to a file named 'slides.md' (in a folder also named 'slides').
# We need to access the 'lessonDict' variable to get the slides' content for each episode. Then we can put them all together.
def buildSlidesFile(lessonDict):
    # The content in 'slidesOptionsFile.md' needs to be at the beginning of the 'slides.md' file, so that HackMD can configure
    # the presentation according to these options.
    slides_headerFile = open(slides_headerFilePath, "r")
    slidesContent = slides_headerFile.read()
    slides_headerFile.close()
    slides_end_of_sessionFile = open(slides_end_of_sessionFilePath, "r")
    slides_end_of_sessionContent = slides_end_of_sessionFile.read()
    slides_end_of_sessionFile.close()
    slides_titleFile = open(slides_titleFilePath, "r")
    slidesContent = slides_headerFile.read()
    slidesContent = slidesContent + slides_titleFile.read()
    slides_headerFile.close()
    slides_titleFile.close()
    allEpisodeTitles = list(lessonDict.keys())
    l = len(allEpisodeTitles)
    i = 0
    while i < l:
        currentEpisodeInfo = lessonDict[allEpisodeTitles[i]]
        if i < l - 1:
            nextEpisodeInfo = lessonDict[allEpisodeTitles[i + 1]]
            if currentEpisodeInfo["sessionNumber"] != nextEpisodeInfo["sessionNumber"]:
                currentEpisodeInfo["slidesContent"] = currentEpisodeInfo["slidesContent"] + slides_end_of_sessionContent
        elif i == l - 1:
            currentEpisodeInfo["slidesContent"] = currentEpisodeInfo["slidesContent"] + slides_end_of_sessionContent
        # Counting the number of slides in an episode file is needed in order to assign a number to each slide in a lesson.
        # This will be used below to create the correct hyperlinks on the website to the slides.
        currentEpisodeInfo["slideCount"] = currentEpisodeInfo["slidesContent"].count("---")
        slidesContent =  slidesContent + currentEpisodeInfo["slidesContent"]
        i = i + 1
    slidesFile = open(slidesFilePath, "w")
    slidesFile.write(slidesContent)
    slidesFile.close()

    



# ---------------------------------------
# ------------ PROPER SCRIPT ------------
# ---------------------------------------
# The proper script to be run starts here.


# Firstly, we create the lesson dictionary, which will contain some information about the whole lesson and its episodes.
lessonDict = createLessonDict()

# Next, we need to do some pre-processing.
# Looking into each episode, determine whether or not it has a recognisable title and change the filename accordingly.
# Then, update the lesson dictionary with some information pertaining to the slides.
preProcessing(lessonDict)

# We can finally build the slides file 'slides.md', with the information in the lesson dictionary.
buildSlidesFile(lessonDict)

# This function has to run separately, in a second pass over all the episodes, because we need information that
# was collected in the first pass (carried out in the preprocessing() function).
addSlideNumbersToDict(lessonDict)

# Now, equipped with all the information we need (in the lesson dictionary) we can go back to each of the files and
# update their yaml headers.
updateAllYamlHeaders(lessonDict)

# Before the end of the script we remove the temporary file, since it is no longer needed.
os.remove(tempFilePath)





