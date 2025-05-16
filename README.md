# myTacc Documentation

## Problem Statement and Solution Overview

In today's fast-paced world, individuals often reflect on what they are grateful for, yet lack structured ways to translate gratitude into tangible, positive actions. This disconnect limits societal impact and individual growth. Simultaneously, organizations aligned with the United Nations Sustainable Development Goals (SDGs) face challenges in engaging individuals meaningfully.

**myTacc** (short for “my T Account”) is a web-based platform that bridges this gap. It allows users to:

- Express gratitude for people, experiences, or privileges. 🙏
- Commit to specific actions that give back to society. 🎯
- Receive real-time feedback via an AI-powered "debt score" (based on how much they’ve benefited) and “XP” (experience points) for their positive contributions. 🤖

Using **Gemini AI** and built on **Django**, myTacc gamifies social good and gratitude, turning personal reflection into collective impact. 💡

---

## Technical Architecture Diagram

Below is an outline of the architecture:

### 📦 Frontend
- Uses React
- Forms for gratitude and action entry
- XP/debt score display module
- “Tacc” dashboard for tasks and debt display

### ⚙️ Backend (Django)
- User authentication & session management
- Views for CRUD operations on gratitude/actions
- Gemini AI integration (via API or internal logic) for scoring

### 🧠 AI Module (Gemini)
- Processes gratitude entries to generate “debt score”
- Evaluates proposed actions and assigns XP
- Adjusts scores based on SDG and its impact on society.

### 🗄️ Database (PostgreSQL)
- Users & their XP Logs
- Gratitude & Action Entries
- All secured

### 🌍 External APIs (Optional for roadmap)
- SDG-aligned charity databases
- Payment/donation gateways

---

## Implementation Details

- **Language & Framework**: Javascript, React, Django
- **AI Integration**: Gemini API (custom logic for NLP scoring)
- **Scoring Logic**:
  - Gratitude statements are scored by AI with a tailored prompt that cleans the user’s statement, then analyses it for benefit.
  - Actions are scored by its impact on society, the effort needed to complete it, and its alignment to the SDGs.
- **XP System**:
  - Users earn XP for actions based on the AI’s evaluation.
  - Debt score decreases as XP gained from actions increases.
  - Feedback with the Tacc dashboard and an XP counter.
- **Data Storage**:
  - All entries of actions & gratuities are time stamped and saved, only to be accessed securely by admins.

---

## SDG Alignment Explanation

myTacc supports the following UN Sustainable Development Goals. Because the platform is highly flexible, users are empowered to log a wide range of meaningful tasks, from micro-actions in daily life to organized volunteering and donations. This flexibility ensures that actions of all scales can contribute meaningfully toward the SDGs.

Users are not restricted to a predefined list of tasks - they can input any custom activity that aligns with their values or circumstances. myTacc’s AI evaluates each action and aligns it with one or more SDGs based on content, impact, and relevance. This makes the platform very adaptable, enabling contributions across diverse causes and communities.

- **🎯 SDG 3: Good Health and Well-being**  
  Donate or volunteer in healthcare-related causes (e.g., health drives, mental health support).  
  Examples: Volunteering at a local clinic, donating to mental health helplines, organizing a wellness event.

- **🎓 SDG 4: Quality Education**  
  Support educational access by tutoring, donating books, or funding learning programs.  
  Examples: Teaching underprivileged students, buying supplies for a school, supporting digital literacy.

- **🏙️ SDG 11: Sustainable Cities and Communities**  
  Take part in urban clean-ups, housing efforts, or donate to community resilience programs.  
  Examples: Participating in recycling campaigns, planting trees, helping in a community shelter.

- **🌱 SDG 13: Climate Action**  
  Donate to climate initiatives or take personal actions like reducing emissions or installing solar panels.  
  Examples: Switching to a bike commute, supporting reforestation, or joining a local sustainability group.

---

## Future Development Roadmap

### 🔜 Short-Term (1–3 months)
- Improve mobile UX/UI
- Recommendation of actions based on your gratitudes
- Add support for payment within the website
- Create public forums Enable media uploads with gratitude/action entries


### 🚀 Mid-Term (3–6 months)
- Collaborations with NGOs to send the users straight to their donation pages 
- Support for multiple languages 
- Improve database system


### 🌍 Long-Term (6+ months)
- Action verification via media/proof
- Global impact leaderboard and map
- Create a public API for third-party app integration (Go-Fund-me use case)

