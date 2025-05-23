✅ Task 1 in branch: https://github.com/araza-29/Gen-AI-IBA
✅ Task 2 in branch: https://github.com/araza-29/Gen-AI-IBA/tree/Task2-Agent
✅ Task 3 in branch: https://github.com/araza-29/Gen-AI-IBA/tree/Task3-Agent

# 🧠 EmerGen GenAI Module Challenge – Phase 1: Supabase + Python + Gemini + ElevenLabs #
This repository is our submission for EmerGen's Generative AI Challenge – Phase 1. It showcases a fully working intelligent agent system using Python, Supabase, Gemini, and ElevenLabs.

🚀 Project Overview
This project demonstrates how a smart agent can:

Interact with a Supabase database for CRUD operations

Extract refund amounts from receipt images using Gemini Vision

Summarize customer complaints from audio using ElevenLabs

Retrieve files from Supabase Storage using filenames

All logic and automation are written in Python.

🛠️ Technologies Used
Python – Core programming language

Supabase – Backend database and storage

Gemini – Multimodal AI model for receipt analysis

ElevenLabs – Audio transcription and summarization

PostgREST – Used indirectly via Supabase’s auto-generated APIs

🧱 Supabase Schema
✅ Table: employees

Column	Type	Description
id	UUID	Auto-generated primary key
created_at	Timestamp	Record creation time
name	Text	Employee's name
age	Integer	Employee's age
salary	Numeric	Employee's salary
📥 Data imported from: employees_rows.csv

✅ Table: refund_requests

Column	Type	Description
id	UUID	Auto-generated primary key
created_at	Timestamp	Record creation time
name	Text	Customer name
amount	Numeric	Refund amount (extracted using Gemini Vision)
image_url	Text	Public URL of the uploaded receipt image
audio_url	Text	Public URL of the uploaded customer audio
audio_summary	Text	Transcribed & summarized complaint (via ElevenLabs)
📥 Data imported from: refund_requests_rows.csv

🧾 Supabase Storage
Bucket created: receipts

Uploaded 10 receipt images: refund_req1.png to refund_req10.png

Uploaded 10 audio files: refund_req1.mp3 to refund_req10.mp3

Public URLs used for Gemini and ElevenLabs input

✅ Task 1: AI Agent Functionalities
🧩 1. Database Interaction via Gemini (natural language prompts)
Using Gemini to execute and understand natural language tasks like:

insert a row in employees with the name John Doe, salary 30000

update the new row (You may tell the row id to the agent), make John's age 100

delete the new row (You may tell the row id to the agent)

fetch all employees

fetch all refund requests

fetch employees with age under 40

fetch employees that have salary > 40000 and age > 50

✔️ All above prompts were successfully processed and converted to SQL via Gemini in Python


✅ Task 2: Receipt Image Analysis & Refund Table Update

## 📌 Overview

This project demonstrates an advanced AI agent's capability to
**automatically populate a database** by extracting structured data
(amounts) from **receipt images** using **Gemini Vision** and
integrating it with **Supabase Storage & Database**.

Once the receipt images are uploaded to Supabase, the AI agent autonomously:

- Retrieves public image URLs.

- Uses Gemini Vision to analyze each receipt.

- Extracts the **total amount** from each image.

- Updates the `refund_requests` table accordingly.

This task showcases the seamless fusion of **cloud storage, database
operations**, and **AI-based image understanding** in a fully
automated pipeline.

---

## 🎯 Task Objective

Your AI agent should:

1. ✅ **Take input**: A list of receipt file names (e.g.,
`refund_req1.png`, `refund_req2.png`, ...).

2. 🔗 **Fetch public URLs** for each file from **Supabase Storage**.

3. 🧠 **Analyze images** to detect the **total refund amount** using
**Gemini Vision API**.

4. 📝 **Update the `refund_requests` table** in Supabase with the following:

- `image_url`: The full public URL of the receipt image.

- `amount`: The total refund amount detected in the image.

> 💡 Your agent should perform this entire process **in a single run**, not via repeated manual prompts or updates.

---

## 🧾 Input Data

You are provided with **10 receipt images**.

- 📁 **Google Drive Link**: [Download
Receipts](https://drive.google.com/drive/folders/1Aoyft_0CO1jkiaqM8-PoYwo4AZtx4pKU?usp=sharing)

- 📦 **Upload Location**: Supabase Storage → Bucket name: `receipts`

- 🔐 Make sure the bucket is **set to public** so the URLs can be
accessed by Gemini.

---

## 🛠️ Technologies Used

- ⚙️ **Supabase** – for cloud storage and PostgreSQL database

- 🤖 **Gemini Vision API** – for OCR and image-based amount extraction

- 🐍 **Python** – scripting and automation


---

## 🧩 Key Features

- 🔄 **Dynamic URL Fetching** from Supabase Storage

- 🧠 **AI-Powered Image Analysis** with Gemini

- 🗃️ **Database Automation** via Supabase SDK

- ✅ **Error Handling & Logging** for skipped or failed extractions

---

## 📦 Setup Instructions

1. **Clone this repository** or run the script in Colab.

2. Set up your **Supabase project**:

- Create a `receipts` storage bucket (make it **public**).

- Create a table `refund_requests` with columns:

- `id` (INT, PRIMARY KEY)

- `image_url` (TEXT)

- `amount` (FLOAT)

3. Upload the downloaded receipt images to Supabase.

4. Configure environment variables in the script:

- `SUPABASE_URL`

- `SUPABASE_KEY`

- `GEMINI_API_KEY`

5. Run the agent. It will:

- Extract public URLs

- Analyze the images

- Update the table with extracted data



✅ Task 3:Audio Processing and Summarization Agent

This project is an intelligent audio processing agent designed to download, transcribe, and summarize refund request audio files stored in a Supabase database. It uses cutting-edge APIs like ElevenLabs for transcription, Gemini for summarization, and Supabase for database operations.

⚙️ Features
🎵 Audio Downloading
Downloads audio files from URLs stored in the Supabase refund_requests table.

🗣️ Audio Transcription
Uses ElevenLabs API for speech-to-text transcription
Supports auto language detection and manual input for Urdu, Hindi, or English.

📝 Text Summarization
Summarizes transcribed text using Gemini API
Includes fallback methods if Gemini fails.

Database Interaction
Connects with Supabase to:

Check which refund requests need processing

Update the audio_summary field in the database

Mark processed entries

🛡️ Robust Error Handling
🔍 Ensures smooth execution even if individual steps (e.g., API failures) occur.

🧰 Requirements
🐍 Python 3.7+
📦 Install dependencies via requirements.txt
🔐 Set up environment variables for:

ElevenLabs API Key

Gemini API Key

Supabase Project URL

Supabase Service Role Key

📹 Demo Video
A single comprehensive video demonstrates:

Supabase DB operations (Task 1)

Image URL extraction and refund table update (Task 2)

Audio summarization (Task 3)
[uploaded on drive: https://drive.google.com/drive/folders/1nZ9DQFw-XlPB8NIJo4kcOryNZmwkFrfw?usp=sharing]
