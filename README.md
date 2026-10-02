# EasyRead — Dyslexia-Friendly Reading Platform (Backend API)

## 1. Project Overview

EasyRead is a REST API backend for a reading platform designed for people with dyslexia.
It does *not* diagnose anything — it lets each reader choose how they want to read
(custom font size / line spacing, or text-to-speech audio) and recommends stories that
match their reading level.

*Problem it solves:* most reading platforms offer one fixed reading experience. Readers
with dyslexia need adjustable presentation and content that matches their level, and
need a way to track progress and review words they find difficult.

*Intended users:*
- *Readers* — browse and read stories, set reading preferences, track progress, save difficult words.
- *Content Creators* — write stories and submit them for review.
- *Admins* — review, publish, or reject submitted stories.

---

## 2. Main Features

- JWT authentication (register, login, refresh) with role-based access (Reader / Creator / Admin)
- Full CRUD for stories
- Story workflow: Draft → Pending Review → Published / Rejected (with rejection reason)
- Reading preferences per user (font size, line spacing)
- Reading progress tracking (words read, completed)
- Difficult words: save a word and get its meaning
- Recommendation system: suggests stories based on the reader's level and progress
- Story levels: beginner / intermediate / advanced
- Validation, filtering, searching, and ordering on stories

---

## 3. Technologies Used

- Python 3
- Django
- Django REST Framework (DRF)
- PostgreSQL
- JWT (djangorestframework-simplejwt)

---
## 6. How to Run Locally

cd project_settings   
python manage.py runserver


The API will be available at http://127.0.0.1:8000/.

## 7. API Documentation

Full interactive documentation (Apidog): *<>*

*Design notes*
- User extends AbstractUser with a role field (Reader / Creator / Admin).
- Story belongs to an author (User) and has level, status, and rejection_reason.
- Preference is linked to a user (font size, line spacing).
- ReadingProgress links a user and a story (words read, completed) — used by the recommendation logic.
- DifficultWord links a user to a saved word.

*Relationships*
- User 1 — N Story (author)
- User 1 — 1 Preference
- User 1 — N ReadingProgress — N 1 Story
- User 1 — N DifficultWord

*ERD (Lucidchart):* <https://lucid.app/lucidchart/d286d840-97f5-492b-96e9-b95b38fae3ec/edit>