# -------------------------------------
# ------------ SUMMARY ----------------
# -------------------------------------
# This python script is used by the build_lesson_wf.yml workflow to generate the 'slides.md' file (in the 'slides' folder) from
# the set of episodes (.md files) contained in the '_episodes' folder. The 'slides.md' file should then be pulled to and synched
# with a HackMD account so that the slides can be accessed and viewed by anyone with the proper HackMD link.





# ----------------------------------------------------------------
# ------------ PRELIMINARY DEFINITIONS AND OPERATIONS ------------
# ----------------------------------------------------------------
# We first import some libraries and define some variables and functions that will be useful.


# ---- Imports----

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
# The tag delimiting a document within a yaml file.
yamlDocumentTag = "---"
# The tag that will be added to unrecognised files in the _episodes folder.
unrecognisedTag = "Unrecognised-"
# Folder where the episodes can be found.
build_lessonFolderPath = "bin/build_lesson/"
mockFolderPath = build_lessonFolderPath + "mock/"
tempFilePath = build_lessonFolderPath + "temp.yml"
episodesFolderPath = "_episodes/"
# Location of the yaml file containing the structure of the lesson and some options
lesson_structureFilePath = "bin/build_lesson/lesson_structure.yml"
slidesFolderPath = "slides/"
slides_headerFilePath = slidesFolderPath + "slides_header.md"
slides_end_of_sessionFilePath = slidesFolderPath + "slides_end_of_session.md"
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

    
def replaceContent(text, newContent, content_begins, content_ends):
    newText = text[:content_begins] + "\n" + newContent + "\n" + text[content_ends:]
    return newText


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
                                                "prefix": "S" + str(sessionNumber) + "E" + str(episodeNumber), "slidesContent": None,
                                                "slideCount": 0, "firstSlideNumber": ""}
            lessonDict[currentEpisodeTitle] = episodeInfo
            j = j + 1
        i = i + 1
     
    return lessonDict


def extractTextInfoToDict(lessonDict, text):
    episodeHeaderStringInfo = extractContent(text, yamlDocumentTag)
    episodeHeaderString = episodeHeaderStringInfo["content"]
    yamlEpisodeHeader = yaml.safe_load(episodeHeaderString)
    slidesContent = None
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
            
            # Now, in the content of the 'Liquid' comment, we detect the slide tags and extract the content therein contained.
            slidesContentInfo = extractContent(liquidCommentContent, slidesTag)
            if slidesContentInfo != None:
                slidesContent = slidesContentInfo["content"]
                
                # Counting the number of slides in an episode file is needed in order to assign a number to each slide in a lesson.
                # This will be used below to create the correct hyperlinks on the website to the slides.
                slideCount = slidesContent.count("---")
                
                episodeInfo = lessonDict[matchingTitle]
                episodeInfo["slideCount"] = slideCount
                episodeInfo["slidesContent"] = slidesContent

    return matchingTitle


def preProcessing(lessonDict):
    # Preparing the list of files in the episodes folder, so that we can loop over it.
    fileList = os.listdir(episodesFolderPath)
    for fileName in fileList:
        fileParts = fileName.rsplit(".")
        # Extracting the entire contents of the markdown files (.md) and placing them in the string variable named 'text'.
        if len(fileParts) == 2 and fileParts[1] == "md":
            filePath = episodesFolderPath + fileName
            f = open(filePath, "r")
            text = f.read()
            f.close()
            matchingTitle = extractTextInfoToDict(lessonDict, text)
            newFilePath = filePath
            if matchingTitle != None:
                episodeInfo = lessonDict[matchingTitle]
                newFileName = episodeInfo["prefix"] + "-" + matchingTitle + ".md"
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
    episodeHeaderString = episodeHeaderStringInfo["content"]
    yamlEpisodeHeader = yaml.safe_load(episodeHeaderString)
    matchingTitle = None      
    if "title" in yamlEpisodeHeader:
        for episodeTitle in lessonDict:
            if yamlEpisodeHeader["title"].find(episodeTitle) != -1:
                matchingTitle = episodeTitle
    
    if matchingTitle != None:
        episodeInfo = lessonDict[matchingTitle]
        yamlEpisodeHeader["title"] = episodeInfo["prefix"] + "-" + matchingTitle
        yamlEpisodeHeader["slides_url"] = yamlLessonStructure["slides_base_url"] + "/" + episodeInfo["firstSlideNumber"]
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


# Writing the content of the slides to a file named 'slides.md' (in a folder also named 'slides').
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
    allEpisodeTitles = list(lessonDict.keys())
    l = len(allEpisodeTitles)
    i = 0
    while i < l:
        currentEpisodeInfo = lessonDict[allEpisodeTitles[i]]
        if currentEpisodeInfo["slidesContent"] != None:
            slidesContent =  slidesContent + currentEpisodeInfo["slidesContent"]
            if i < l - 1:
                nextEpisodeInfo = lessonDict[allEpisodeTitles[i + 1]]
                if currentEpisodeInfo["sessionNumber"] != nextEpisodeInfo["sessionNumber"]:
                    slidesContent = slidesContent + slides_end_of_sessionContent
            elif i == l - 1:
                slidesContent = slidesContent + slides_end_of_sessionContent
        i = i + 1
    slidesFile = open(slidesFilePath, "w")
    slidesFile.write(slidesContent)
    slidesFile.close()

    



# ---------------------------------------
# ------------ PROPER SCRIPT ------------
# ---------------------------------------
# The proper script to be run starts here.



lessonDict = createLessonDict()
preProcessing(lessonDict)
addSlideNumbersToDict(lessonDict)
updateAllYamlHeaders(lessonDict)
buildSlidesFile(lessonDict)

os.remove(tempFilePath)




