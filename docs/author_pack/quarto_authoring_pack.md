# Quarto Course Authoring Pack (Word-First Workflow)

## Overview

This document combines:

1. Academic Workflow (how to design a course)
2. Authoring Specification (how to write content in Word)
3. Examples (what it looks like in practice)

This is the complete guide for creating structured courses using the system.

---

# PART 1 — Academic Workflow (Design Thinking)

## Core Model

YAML = structure  
Word = content  
Quarto = output  

> Design first, write second, publish third.

---

## Course Structure

Course  
→ Module  
→ Session  
→ Page  

Each page = one learning intention.

---

## Workflow

### Step 1 — Define Structure (YAML)
- Create modules, sessions, pages
- Assign page types (kinds)

### Step 2 — Write Content (Word)
- Write clearly using headings
- Add directives where needed

### Step 3 — Import
- System converts Word to structured content

### Step 4 — Review
- Check layout, clarity, interactions

---

## Pedagogical Pattern

1. Concept  
2. Example  
3. Practice  
4. Reflection  

---

# PART 2 — Authoring Specification (What to Do in Word)

## Core Principle

> Write clearly in Word. The system handles formatting.

---

## Basic Structure

- Heading 1 → section  
- Heading 2 → subsection  

---

## Directive Syntax

Directive :: value

Use **double colon (::)**

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

Wrong:  
YouTubeEmbed: url  

Correct:  
YouTubeEmbed :: url  

---

# PART 3 — Example Page

## Introduction

This page introduces surveillance.

Callout :: note  
Text :: Surveillance is essential.

---

## Explanation

Surveillance involves monitoring populations.

---

## Self Check

SelfCheck  
Question :: What is surveillance?  
Answer :: Monitoring disease patterns  

---

## Steps

Reveal  
Step 1 :: Identify population  
Step 2 :: Collect data  
Step 3 :: Analyse  

---

## Quiz

Quiz  
Question :: Purpose?  
Option :: Monitor disease  
Option :: Replace diagnosis  
Answer :: Monitor disease  
Explanation :: It tracks trends  

---

## Tabs

Tabs  
Definition :: Continuous monitoring  
Example :: COVID dashboards  

---

## Image

Image :: resources/images/chart.png  
Alt :: Chart  
Caption :: Weekly incidence  
Width :: 80%  

---

## Summary

> Design in YAML, write in Word, publish automatically.

This system transforms simple authored content into structured courses.
