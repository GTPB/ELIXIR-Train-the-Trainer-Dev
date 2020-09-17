# Episode-Editing Guide

## Table Of Contents

- [Summary](#Summary)
- [Introduction](#Introduction)
- [Editing Instructions and Guidelines](#Editing_Instructions_and_Guidelines)
- [Episode File Structure](#Episode-File-Structure)

## Summary

This is a guide for anyone who wants to edit these episodes. The reason for having such a guide is that, unlike other repositories, the episode files in this folder might undergo some extra automatic transformations after each edit/commit. They are also meant to be used both by GitHub Pages and HackMD, which requires some extra care with the formatting.


## Introduction

Below you will find a careful explanation of how to edit each file. If you want to dig a bit deeper and better understand some of the transformations that the files might undergo, as well as the scripts that execute them, you can check these links:

- [Workflows](../.github/workflows)
- [Lesson-building scripts](../bin/build_lesson)


The links take you to the **.github/workflows** folder and to the  **bin/build_lesson** folder, respectively. Both of them are folders in this repository.

The first folder contains files that are meant to be executed by _GitHub Actions_. You will find there a file named **build_lesson_wf.yml**, which is a yaml file, and recognised by GitHub as a workflow. What this means is that GitHub will execute the code in this file whenever some event is detected. The events that trigger it are defined within the file itself, but you can also find that information in the README.md file in that folder.

The second folder contains the actual script that is run by the aforementioned workflow, as well as a yaml file containing data pertaining to the episode titles and their relative order. It also contains a README.md file with further information.


## Editing Instructions and Guidelines

### Episode File Structure

#### YAML Header

#### Main Body

#### Liquid Comment Section

##### GitHub-Only

##### Slides Content

### Editing

#### Main concerns

#### HackMD

#### Setting up HackMD

##### HackMD account

##### Browser extension

##### Permissions

###### GitHub Permissions

###### HackMD Permissions



##### HackMD Basics

###### Notes

- Episode Notes
- Slides Note

###### Push and Pull

- if you forget to pull

- don't switch





