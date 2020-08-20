# -------------------------------------
# ------------ DESCRIPTION ------------
# -------------------------------------
# This python script is meant to generate the slides.md file from the set of episodes (.md files) contained
# in the episodes folder. The slides.md file should then be pulled to and synched with a HackMD account so that the
# slides can be accessed and viewed by anyone with the proper HackMD link.





# ----------------------------------------------------------------
# ------------ PRELIMINARY DEFINITIONS AND OPERATIONS ------------
# ----------------------------------------------------------------
# We first import some libraries and define some variables and functions that will be useful.


# ---- Imports ----

# The 'os' library allows for the use of several OS related operations, namely listdir(), which we use in this script
# to access the markdown files in the '_episodes' folder.
import os


# ---- Variables ----

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
     
    # text.find(string) will return the position where the first occurrence of 'string'
    # begins in the text. It will return -1 if 'string' is not found.
    tagPosition = text.find(beginningTag)
    
    # If tagPosition is -1 then that means beginningTag was not found in the text.
    if tagPosition != -1:
        content_begin = tagPosition + len(beginningTag)
    	content = text[content_begin:]

    	tagPosition = content.find(endingTag)
        if tagPosition != -1:
            content = content[:tagPosition]
            return content
    	else:
    		return ""

    else:
    	return ""





# ---------------------------------------
# ------------ PROPER SCRIPT ------------
# ---------------------------------------
# The proper script to be run starts here.


# Extracting the entire contents of the markdown files (.md) and placing them in a string variable named text.
folderPath = "_episodes/"
fileList = os.listdir(folderPath)
text = ""
slidesContent = ""

for fileName in fileList:
    fileParts = fileName.rsplit(".")
    if len(fileParts) == 2 and fileParts[1] == "md":
        f = open(folderPath + fileName, "r")
        text = f.read()
        f.close()
        
        # Extracting from the variable 'content' the section that rests inside the 'Liquid' comment.
        liquidCommentContent = extractContent(text, liquidCommentTag_beginning, liquidCommentTag_ending)
        
        # Now, in the content of 'Liquid' comment, we detect the slide tags and extract the content therein contained.
        slidesContent = slidesContent + extractContent(liquidCommentContent, slidesTag)
        

# Write the content of the slides to a file named slides.md (in a folder also named slides)
slidesFile = open("slides/slides.md", "w")
slidesFile.write(slidesContent)        
slidesFile.close()
