# Episode-Editing Guide

<br/>

## Table Of Contents

- [Summary](#Summary)
- [Introduction](#Introduction)
- [Editing Instructions and Guidelines](#Editing-Instructions-and-Guidelines)
  - [Episode File Structure](#Episode-File-Structure)
    - [YAML Header](#YAML-Header)
    - [Website Content](#Website-Content)
    - [Liquid Comment Section](#Liquid-Comment-Section)
      - [GitHub-Only](#GitHub-Only)
      - [Slides Content](#Slides-Content)
  - [Editing](#Editing)
    - [Main concerns](#Main-concerns)
    - [File Creation and Naming](#File-Creation-and-Naming)
    - [HackMD Editing](#HackMD-Editing)
      - [Setting Up HackMD](#Setting-Up-HackMD)
        - [HackMD Account](#HackMD-Account)
        - [Browser Extension](#Browser-Extension)
        - [Permissions](#Permissions)
          - [GitHub Permissions](#GitHub-Permissions)
          - [HackMD Permissions](#HackMD-Permissions)
      - [HackMD Basics](#HackMD-Basics)
        - [Notes](#Notes)
        - [Push and Pull](#Push-and-Pull)
    - [GitHub Editing](#GitHub-Editing)
    - [Editing the YAML Header](#Editing-the-YAML-Header)
  
<br/>

## Summary

This is a guide for anyone who wants to edit these episodes. The reason for having such a guide is that, unlike many simpler repositories, the episode files in this folder might undergo some extra automatic transformations after each edit/commit. They are also meant to be used both by GitHub Pages and HackMD, which requires some extra care with the formatting.

<br/>

## Introduction

Below you will find a careful explanation of how to edit each file. Despite not being strictly necessary, if you want to dig a bit deeper and better understand some of the transformations that the files might undergo, as well as the scripts that execute them, you can check these links:

- [Workflows](../.github/workflows)
- [Lesson-building scripts](../bin/build_lesson)
- [Slides Resources](../slides)


The links take you to the **.github/workflows**, **bin/build_lesson** and **slides** folders, respectively. All of them are folders in this repository.

The first folder contains files that are meant to be executed by _GitHub Actions_. You will find there a file named **build_lesson_wf.yml**, which is a yaml file, and recognised by GitHub as a workflow. What this means is that GitHub will execute the code in this file whenever some event is detected. The events that trigger it are defined within the file itself, but you can also find that information in the README.md file in that folder.

The second folder contains the actual script that is run by the aforementioned workflow, as well as a yaml file containing data pertaining to the episode titles and their relative order. It also contains a README.md file with further information.

The third folder contains not only the markdown file with the final slides content, which is called **slides.md**, but also two other markdown files with information that is automatically added to the first one. It also contains a README.md file with further information.

<br/>

## Editing Instructions and Guidelines

<br/>

### Episode File Structure

Each episode markdown file can be composed of three different sections, two of which can be omitted:

- **YAML Header** (cannot be omitted) 
- **Website Content**
- **Liquid Comment Section**

The **Liquid Comment Section** can, in turn, be composed of two different subsections, both of which can be omitted:

- **GitHub-Only**
- **Slides Content**

<br/>

#### YAML Header

A section of this type should be found at the top of the episode file. It is the only one that cannot be omitted, otherwise the file will not be recognised as an episode. It follows the YAML syntax and looks as depicted below, although the order in which the key-value pairs appear might differ (in the YAML syntax the order of these pairs is not relevant for the correct parsing of the information therein contained).

<br/>

**Example 1**
~~~
---
exercises: 0
keypoints:
- Reflect upon concepts around learning, training and teaching.
- Internalize and learn to mentally structure several ideas and concepts related to
  learning, training and teaching.
outcomes:
- Get a clear understanding of the goals of this session and of the skil the learners
  are expected to acquire.
questions:
- What are the goals and intended learning outcomes of this session?
slides_url: https://hackmd.io/@nyTtT/r1tHvVR4w#/
teaching: 3
title: S1E1-Session description - Training techniques that enhance learner participation
  and engagement

---
~~~

<br/>

As you can see in the example above, there are seven keys (also referred to as fields):

- exercises
- keypoints
- outcomes
- questions
- slides_url
- teaching
- title

<br/>

The information in the YAML header is chiefly responsible for generating the header in the corresponding website and episode (which follows a _Carpentries_ template), as well as the **Key Points** section (which, if it exists, can be found at the bottom of each episode page). **Example: YAML Header** above would generate the following header and **Key Points** section (**Fig: YAML Header** and **Fig: Key Points**):

<br/>

**Fig: YAML Header**
![](editing_figs/YAML_Header.png)

<br/>

**Fig: Key Points**
![](editing_figs/Key_Points.png)

<br/>

In the header, **Slides** (in blue) is a link to whatever URL is assigned to the 'slides_url' field in **Example: YAML Header**.

<br/>

#### Website Content

Below the YAML header, everything you write is what we call the main body of the file. All of the content in that main body, apart from comments, will feature on the website, in the webpage corresponding to the episode. In the next section ([Liquid Comment Section](#Liquid-Comment-Section)) we will show you how to add comments to the main body. These will be written within a tag defined in the Liquid template language, for which reason we might also refer to them as Liquid comments.

<br/>

##### Challenges

Carpentries-style websites can have pre-defined sections for their episodes, which will have a specific look and feel, depending on their purpose. The one that is particularly relevant to us is the **Challenge** section, which looks as depicted below (**Fig: Challenge**):

**Fig: Challenge**
![](editing_figs/Challenge.png)

<br/>

Below you can see the piece of markdown text and liquid tag responsible for generating the section above:

~~~
> ## Challenge: Teaching or training? (3 min + 3 min)
>
> - Based on your experience, what are in your opinion the differences between teaching and training?
> - Identify two main differences
> - Discuss them with your partner
> - Write them in the Gdoc (share them with us)
{: .challenge}
~~~

<br/>

Notice the two aspects needed to create a **Challenge** section:

- **Greater than** symbol (**>**) before every line of text.
- The **{: .challenge}** tag at the end of the piece of text.

#### Liquid Comment Section

##### GitHub-Only

##### Slides Content

### Editing

#### Main Concerns

images
slides

#### File Creation and Naming

add episodes to lesson structure first. why? what happens if you don't?

no duplicate names, avoid symbols like ?, :

name it whatever, but make sure it has an .md at the end

do not add files with no yaml header - might not build the website

de-synching from HackMD if file name changes (whether it is the prefix or the title)
  pulling won't work
  go through github hackmd edit button

#### HackMD Editing

##### Setting Up HackMD

###### HackMD Account

###### Browser Extension

###### Permissions

- GitHub Permissions

- HackMD Permissions



##### HackMD Basics

###### Notes

- Episode Notes
- Slides Note

###### Features

##### HackMD Button

github editor also opens (you will have to exit after, saying yes to not saving changes)

##### Push and Pull

- if you forget to pull

- don't switch

- give it some time

- first time vs every other time

- exiting a note (issue)

if you edit and then push slides file from hackMD to github it won't do anything

#### GitHub Editing

give it some time

actions tab

potential issues if you don't way long enough - warning that file might have been changed
   what to do? - copy-paste
   
if you want the slides to work you still have to go to the TtT file on HackMD and pull

#### Editing the YAML Header

