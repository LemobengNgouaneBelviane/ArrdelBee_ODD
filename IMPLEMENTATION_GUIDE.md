# 🎯 ODD Alignment System - Implementation Guide

## Overview

This document describes the **project alignment workflow** between the frontend (Next.js) and backend (FastAPI) for the ArrdelBee ODD tracking system.

**Key Requirement:** Projects must exist in BOTH:
1. **Projects Table** (all projects)
2. **Unaligned Projects Table** (projects without ODD) simultaneously upon creation

---

## 📊 Data Model

### 1. Projects Table

```sql
CREATE TABLE projects (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  sector VARCHAR(100),  -- NEW: Santé, Éducation, Eau, Infrastructure, Énergie, Économie, Environnement, Agriculture
  status VARCHAR(50) DEFAULT 'unaligned',  -- NEW: unaligned, pending, aligned
  chapitre VARCHAR(255),
  department VARCHAR(100),
  commune VARCHAR(100),
  budget DECIMAL(15, 2),
  start_date DATE,
  end_date DATE,
  created_at DATETIME DEFAULT NOW(),
  updated_at DATETIME DEFAULT NOW()
);
```

### 2. Unaligned Projects Table (NEW)

```sql
CREATE TABLE unaligned_projects (
  id SERIAL PRIMARY KEY,
  project_id INTEGER UNIQUE NOT NULL,
  created_at DATETIME DEFAULT NOW(),
  FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);
```

### 3. Alignments Table (NEW)

```sql
CREATE TABLE alignments (
  id SERIAL PRIMARY KEY,
  project_id INTEGER NOT NULL,
  selected_odds JSON,  -- Array of ODD numbers: [3, 5] or just [6]
  baseline DECIMAL(10, 2),
  target DECIMAL(10, 2),
  justification TEXT,
  status VARCHAR(50) DEFAULT 'PENDING',  -- VALIDATED, REJECTED, PENDING
  validated_by VARCHAR(100),  -- CTD, ADMIN, FIELD
  created_at DATETIME DEFAULT NOW(),
  updated_at DATETIME DEFAULT NOW(),
  FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);
```

### 4. KPI Results Table (NEW)

```sql
CREATE TABLE kpi_results (
  id SERIAL PRIMARY KEY,
  alignment_id INTEGER NOT NULL,
  odd_id INTEGER,
  calculated_percentage DECIMAL(10, 2),
  variance DECIMAL(10, 2),
  status_alert VARCHAR(50),  -- red, yellow, green
  created_at DATETIME DEFAULT NOW(),
  FOREIGN KEY (alignment_id) REFERENCES alignments(id) ON DELETE CASCADE
);
```

---

## 🔧 API Endpoints to Implement

### 1. Create Project with Dual-List Storage

**Endpoint:** `POST /projets`

**Request Body:**
```json
{
  "title": "Extension du Réseau Électrique Rural",
  "description": "...",
  "sector": "énergie",
  "chapitre": "ENERGIE",
  "department": "Adamaoua",
  "commune": "Ngaoundéré",
  "budget": 210000000,
  "start_date": "2024-01-15",
  "end_date": "2025-06-30"
}
```

**Response:**
```json
{
  "id": 4,
  "title": "Extension du Réseau Électrique Rural",
  "status": "unaligned",
  "sector": "énergie"
}
```

**Logic:**
1. Insert into `projects` table with `status='unaligned'` and captured `sector`
2. Immediately insert into `unaligned_projects` table with same `project_id`
3. Return created project

**Key:** Both table insertions MUST happen atomically

---

### 2. Get Unaligned Projects

**Endpoint:** `GET /projets/non-alignes?limit=200`

**Response:**
```json
{
  "data": [
    {
      "id": 4,
      "title": "Extension du Réseau Électrique Rural",
      "chapitre": "ENERGIE",
      "sector": "énergie",
      "suggested_sdg_codes": []
    }
  ]
}
```

**Logic:**
- Query `unaligned_projects U JOIN projects P ON U.project_id = P.id`
- Filter by `P.status = 'unaligned'`
- Return only unaligned projects with their sector info
- Frontend will use sector to auto-suggest ODD via `suggestODDForSector(sector)`

---

### 3. Validate/Create Alignment

**Endpoint:** `POST /alignements/valider`

**Request Body:**
```json
{
  "project_id": 4,
  "selected_odds": [7],  -- Array of ODD numbers selected by user
  "baseline": 0.15,      -- Current electricity access rate (15%)
  "target": 0.35,        -- Target access rate (35%)
  "justification": "Ce projet contribue directement à l'ODD 7 en augmentant l'accès à l'électricité...",
  "validated_by": "CTD",  -- CTD, ADMIN, FIELD
  "status": "VALIDATED"   -- VALIDATED, REJECTED
}
```

**Response:**
```json
{
  "id": 1,
  "project_id": 4,
  "status": "VALIDATED",
  "alignment": {
    "selected_odds": [7],
    "baseline": 0.15,
    "target": 0.35,
    "calculated_percentage": 42.86,
    "variance": 0.07,
    "status_alert": "green"
  }
}
```

**Logic:**
1. Create record in `alignments` table
2. **Calculate KPI:**
   ```
   percentage = (baseline ÷ target) × 100
   variance = baseline - target
   variance_percent = (variance ÷ target) × 100
   
   if variance_percent < -20: status_alert = "red"
   elif variance_percent < 0: status_alert = "yellow"
   else: status_alert = "green"
   ```
3. Insert into `kpi_results` table
4. **Update project status:**
   - If `status='VALIDATED'`: Update `projects.status='aligned'`
   - If `status='REJECTED'`: Keep `projects.status='unaligned'`
5. **Update unaligned_projects:**
   - If aligned: Delete from `unaligned_projects`
   - If rejected: Keep record

---

### 4. Get Project Details with Alignment Info

**Endpoint:** `GET /projets/{id}`

**Response:**
```json
{
  "id": 4,
  "title": "Extension du Réseau Électrique Rural",
  "sector": "énergie",
  "status": "aligned",
  "alignment": {
    "id": 1,
    "selected_odds": [7],
    "baseline": 0.15,
    "target": 0.35,
    "justification": "...",
    "kpi": {
      "percentage": 42.86,
      "variance": 0.07,
      "variance_percent": 20,
      "status_alert": "green"
    }
  }
}
```

---

## 🚀 Frontend-Backend Workflow

### User Journey: Project Creation & Alignment

```
1. User fills form: Title, Description, SECTOR (NEW), Location, Budget
   ↓
2. POST /projets → Backend creates in BOTH tables
   ├─ INSERT projects (status='unaligned')
   └─ INSERT unaligned_projects
   ↓
3. Frontend redirects to /projets (shows project with alignment=unaligned)
   ↓
4. User goes to /alignements page
   ↓
5. Frontend: GET /projets/non-alignes → Shows all unaligned projects
   ↓
6. User selects project
   ↓
7. Frontend: AUTO-SUGGEST ODD via sector mapping (NO API CALL)
   suggestODDForSector("énergie") → [7]
   ↓
8. Frontend: User clicks ODD, enters Baseline, Target
   ↓
9. Frontend: Calculate KPI locally:
   KPI = (0.15 ÷ 0.35) × 100 = 42.86%
   Status Alert = GREEN
   ↓
10. User writes justification → Submits
    ↓
11. POST /alignements/valider
    ├─ Backend recalculates KPI
    ├─ Stores in alignments table
    ├─ Updates projects.status → 'aligned'
    └─ Removes from unaligned_projects
    ↓
12. Frontend: Shows success → Redirects to /projets
    ↓
13. Project now appears:
    ├─ In /projets with badge "✅ Aligné"
    ├─ With ODD codes [7] displayed
    ├─ With KPI 42.86% and status "GREEN"
    └─ NOT in /alignements (unaligned filter)
```

---

## 📋 Sector-to-ODD Mapping (From PDF)

This mapping is **already implemented in frontend** at `src/lib/api.ts`:

```typescript
export const SECTOR_TO_ODD_MAPPING = {
  "santé": [3],
  "éducation": [4],
  "eau": [6],
  "infrastructure": [9, 11],
  "énergie": [7],
  "économie": [8, 5],
  "agriculture": [2, 15],
  "environnement": [13, 15],
};
```

**No API call needed for suggestions** — Frontend performs local lookup

---

## 🔐 4-Level Validation Workflow

Currently, the system has basic `validated_by` field. For full compliance with PDF requirements:

### Current Implementation
```json
{
  "validated_by": "CTD",  // CTD | ADMIN | FIELD
  "status": "VALIDATED"   // VALIDATED | REJECTED
}
```

### Future Enhancement (4-Level Gate)
```sql
CREATE TABLE alignment_validations (
  id SERIAL PRIMARY KEY,
  alignment_id INTEGER,
  level INT (1-4),
  validator_role VARCHAR(50),  -- FieldAgent, QC, CTD, ARRDEL
  status VARCHAR(50),  -- APPROVED, REJECTED, PENDING
  comment TEXT,
  created_at DATETIME,
  FOREIGN KEY (alignment_id) REFERENCES alignments(id)
);

Level 1: Field Agent submits with proof
Level 2: Quality Controller verifies completeness
Level 3: CTD Administrator approves locally  
Level 4: ARRDEL Expert certifies & publishes
```

**Current state:** Simplified to single validation. Can enhance after MVP.

---

## 💾 Database Migration Script

```sql
-- Add new columns to projects
ALTER TABLE projects ADD COLUMN sector VARCHAR(100);
ALTER TABLE projects ADD COLUMN status VARCHAR(50) DEFAULT 'unaligned';

-- Create new tables
CREATE TABLE unaligned_projects (
  id SERIAL PRIMARY KEY,
  project_id INTEGER UNIQUE NOT NULL,
  created_at DATETIME DEFAULT NOW(),
  FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

CREATE TABLE alignments (
  id SERIAL PRIMARY KEY,
  project_id INTEGER NOT NULL,
  selected_odds JSON,
  baseline DECIMAL(10, 2),
  target DECIMAL(10, 2),
  justification TEXT,
  status VARCHAR(50) DEFAULT 'PENDING',
  validated_by VARCHAR(100),
  created_at DATETIME DEFAULT NOW(),
  updated_at DATETIME DEFAULT NOW(),
  FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

CREATE TABLE kpi_results (
  id SERIAL PRIMARY KEY,
  alignment_id INTEGER NOT NULL,
  odd_id INTEGER,
  calculated_percentage DECIMAL(10, 2),
  variance DECIMAL(10, 2),
  status_alert VARCHAR(50),
  created_at DATETIME DEFAULT NOW(),
  FOREIGN KEY (alignment_id) REFERENCES alignments(id) ON DELETE CASCADE
);
```

---

## ✅ Testing Checklist

- [ ] POST /projets creates dual entries
- [ ] GET /projets/non-alignes returns only unaligned
- [ ] POST /alignements/valider calculates KPI correctly
- [ ] KPI calculation: (0.15 ÷ 0.35) × 100 = 42.86% ✓
- [ ] Variance calculation: 0.15 - 0.35 = -0.2 = -20% variance
- [ ] Status "red" when variance < -20%
- [ ] Validated projects disappear from unaligned list
- [ ] Frontend shows alignment badge correctly

---

## 🎨 Frontend State Management

The frontend uses React hooks (no Redux/Zustand) to manage:

1. **Selected Project** - From unaligned list
2. **Suggested ODD** - From sector mapping
3. **Selected ODD** - User multi-select
4. **KPI Calculation** - Local calculation (no API)
5. **Form Data** - Baseline, Target, Justification
6. **Submission** - POST to /alignements/valider

**No complex state needed** — Everything is local until final submission.

---

## 📚 Key Files

### Frontend
- **API Functions:** `src/lib/api.ts` (ODD mapping, KPI calc, decision questions)
- **Alignment Page:** `src/app/alignements/page.tsx` (main workflow UI)
- **Projects Page:** `src/app/projets/page.tsx` (displays alignment status)
- **Project Creation:** `src/app/projets/creer/page.tsx` (includes sector field)

### Backend (To Implement)
- `POST /projets` - Dual-list creation
- `GET /projets/non-alignes` - Unaligned filter
- `POST /alignements/valider` - Alignment + KPI storage
- `GET /projets/{id}` - With alignment details

---

## 🔗 Integration Points

1. **Sector Dropdown → Auto-Suggest ODD**
   - Frontend captures sector in creation form
   - Passed to backend in POST /projets
   - Frontend uses sector for local ODD suggestion

2. **KPI Calculation**
   - Frontend calculates locally for instant feedback
   - Backend recalculates on submission for verification
   - Stored in kpi_results table

3. **Alignment State Tracking**
   - Frontend: Badge shows (✅ Aligned | ⏳ Pending | ❌ Not Aligned)
   - Backend: Field `projects.status` drives filtering
   - Frontend: GET /projets/non-alignes filters by status

---

## 🎯 Success Criteria

After implementation:

1. ✅ Create project → Shows in both /projets (unaligned) and /alignements
2. ✅ Select in /alignements → ODD auto-suggests
3. ✅ Enter KPI → Calculates & shows status (red/yellow/green)
4. ✅ Submit → Stores alignment + updates status
5. ✅ Aligned project → Disappears from /alignements unaligned list
6. ✅ User-friendly → Easy to understand, no technical jargon

---

**Questions?** Check `Rapport_Comprehension_sujet_ODD.pdf` for detailed ODD guidance.
