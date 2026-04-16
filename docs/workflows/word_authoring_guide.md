# Quarto Course Authoring Guide (Word-Based Workflow)

## Purpose
This guide explains how to write course content in Microsoft Word for use in the Quarto publishing system.

---

## Core Principle
> Write clearly in Word. The system handles formatting.

---

## Basic Structure
- Heading 1 → Section  
- Heading 2 → Subsection  

---

## Directive Syntax
Directive :: value  

Use double colon (::)

---

## Core Features

### Callout
Callout :: note  
Text :: Important idea  

### SelfCheck
SelfCheck  
Question :: What is X?  
Answer :: Explanation  

### Reveal
Reveal  
Step 1 :: First  
Step 2 :: Second  

### Quiz
Quiz  
Question :: Question text  
Option :: A  
Option :: B  
Answer :: A  
Explanation :: Why  

### Tabs
Tabs  
Definition :: Text  
Example :: Text  

---

## Media

### Image
Image :: resources/images/example.png  
Alt :: Description  
Caption :: Caption  
Width :: 80%  

### File
File :: resources/pdf/file.pdf  
Label :: Download  
Display :: embed  

---

## Video

YouTubeEmbed :: https://www.youtube.com/watch?v=VIDEO_ID  

PanoptoEmbed :: https://yourinstitution.panopto.com/...id=VIDEO_ID  

---

## Common Mistake
Wrong: YouTubeEmbed: url  
Correct: YouTubeEmbed :: url  

---

## Summary
> Write clearly using :: directives. The system handles the rest.
